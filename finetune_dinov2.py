"""Finetune DINOv2-small on types-of-film-shots, imbalance-aware, export ONNX.

Fixes the 'detail'-collapse of the old checkpoint:
  * drop the junk `ambiguous` class (8 -> 7) so the head stops dumping uncertainty there
  * class-balanced CrossEntropy (effective-number weights, Cui 2019) — compensates 56..197 imbalance
  * RandAugment + flips — the main defense against 925-image overfit
  * low-LR backbone finetune + higher-LR head
Then export a tract-friendly ONNX (static batch, opset16, onnxsim) for the Space.
"""
import io, numpy as np, pandas as pd, torch, torch.nn as nn
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
from transformers import AutoModelForImageClassification

DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
PARQUET = "https://huggingface.co/datasets/szymonrucinski/types-of-film-shots/resolve/main/data/train-00000-of-00001-35c0da0efe86f2e9.parquet"
# original 8 (alphabetical); index 0 = ambiguous which we drop
ALL = ["ambiguous","closeUp","detail","extremeLongShot","fullShot","longShot","mediumCloseUp","mediumShot"]
KEEP = [c for c in ALL if c != "ambiguous"]               # 7 classes
OLD2NEW = {ALL.index(c): i for i, c in enumerate(KEEP)}   # old label -> new contiguous label
NORM = T.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225])
train_tf = T.Compose([T.RandomResizedCrop(224, scale=(0.6,1.0)), T.RandomHorizontalFlip(),
                      T.RandAugment(num_ops=2, magnitude=7), T.ToTensor(), NORM])
val_tf = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor(), NORM])


class DS(Dataset):
    def __init__(self, df, tf): self.df, self.tf = df.reset_index(drop=True), tf
    def __len__(self): return len(self.df)
    def __getitem__(self, i):
        r = self.df.iloc[i]
        img = Image.open(io.BytesIO(r["image"]["bytes"])).convert("RGB")
        return self.tf(img), int(r["label"])


def main():
    df = pd.read_parquet(PARQUET)
    df = df[df["label"] != ALL.index("ambiguous")].copy()      # drop ambiguous
    df["label"] = df["label"].map(OLD2NEW)                      # remap to 0..6
    rng = np.random.default_rng(0); vidx = []
    for c in df["label"].unique():
        idx = df.index[df["label"] == c].to_numpy().copy(); rng.shuffle(idx)
        vidx += list(idx[: max(1, int(0.15*len(idx)))])
    vm = df.index.isin(vidx)
    tr = DataLoader(DS(df[~vm], train_tf), batch_size=32, shuffle=True, num_workers=4, drop_last=True)
    va = DataLoader(DS(df[vm], val_tf), batch_size=32, num_workers=4)
    print(f"classes={KEEP}\ntrain {(~vm).sum()}  val {vm.sum()}")

    model = AutoModelForImageClassification.from_pretrained(
        "facebook/dinov2-small", num_labels=len(KEEP),
        id2label={i: c for i, c in enumerate(KEEP)},
        label2id={c: i for i, c in enumerate(KEEP)},
        ignore_mismatched_sizes=True).to(DEV)

    # effective-number class weights (Cui 2019): (1-beta)/(1-beta^n)
    n = df[~vm]["label"].value_counts().sort_index().to_numpy().astype(np.float64)
    beta = 0.999
    w = (1-beta)/(1-np.power(beta, n)); w = w/w.sum()*len(KEEP)
    crit = nn.CrossEntropyLoss(weight=torch.tensor(w, dtype=torch.float32, device=DEV), label_smoothing=0.05)
    head = [p for n_,p in model.named_parameters() if "classifier" in n_]
    back = [p for n_,p in model.named_parameters() if "classifier" not in n_]
    opt = torch.optim.AdamW([{"params": head, "lr": 1e-3}, {"params": back, "lr": 1e-5}], weight_decay=0.05)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=16)

    best, best_sd = 0.0, None
    for ep in range(16):
        model.train()
        for x,y in tr:
            x,y = x.to(DEV), y.to(DEV); opt.zero_grad()
            crit(model(pixel_values=x).logits, y).backward(); opt.step()
        sched.step()
        model.eval(); cm = np.zeros((len(KEEP),len(KEEP)), int)
        with torch.no_grad():
            for x,y in va:
                p = model(pixel_values=x.to(DEV)).logits.argmax(1).cpu().numpy()
                for t,pr in zip(y.numpy(), p): cm[t,pr]+=1
        acc = cm.trace()/cm.sum(); bal = np.mean(np.diag(cm)/np.clip(cm.sum(1),1,None))
        print(f"ep {ep+1:2d}  acc {acc:.3f}  balanced_acc {bal:.3f}")
        if bal > best: best, best_sd = bal, {k:v.cpu().clone() for k,v in model.state_dict().items()}

    print(f"best balanced_acc {best:.3f}")
    model.load_state_dict(best_sd); model.eval()

    # ---- export ONNX (static batch, opset16) ----
    class Wrap(nn.Module):
        def __init__(s,m): super().__init__(); s.m=m
        def forward(s,x): return s.m(pixel_values=x).logits
    import onnx, onnxruntime as ort
    from onnxsim import simplify
    torch.onnx.export(Wrap(model.cpu()).eval(), (torch.randn(1,3,224,224),), "/tmp/_v2.onnx",
                      input_names=["pixel_values"], output_names=["logits"], opset_version=16, dynamo=False)
    simp, ok = simplify(onnx.load("/tmp/_v2.onnx")); assert ok
    onnx.save(simp, "dinov2_shot_v2.onnx")
    # sanity: onnx vs torch
    x = torch.randn(1,3,224,224)
    with torch.no_grad(): t = Wrap(model)(x).numpy()
    o = ort.InferenceSession("dinov2_shot_v2.onnx", providers=["CPUExecutionProvider"]).run(None, {"pixel_values": x.numpy()})[0]
    print("onnx max diff:", np.abs(t-o).max(), "argmax ok:", t.argmax()==o.argmax())
    with open("labels_v2.txt","w") as f: f.write("\n".join(KEEP))
    print("wrote dinov2_shot_v2.onnx + labels_v2.txt; classes:", KEEP)


if __name__ == "__main__":
    main()
