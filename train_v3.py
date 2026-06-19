"""v3: finetune DINOv3-small on the combined human+AI dataset.

Trains on all AI + 80% human; validates on held-out HUMAN-only frames (clean gold).
Drops 'ambiguous' -> 7 classes (matches the Space). Class-balanced CE + RandAugment.
Exports a tract-friendly ONNX for the Space.
"""
import io, numpy as np, torch, torch.nn as nn
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
from transformers import AutoModel, AutoImageProcessor
from datasets import load_dataset

DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BACKBONE = "facebook/dinov3-vits16-pretrain-lvd1689m"
OLD = ["ambiguous","closeUp","detail","extremeLongShot","fullShot","longShot","mediumCloseUp","mediumShot"]
KEEP = [c for c in OLD if c != "ambiguous"]                      # 7
O2N = {OLD.index(c): i for i, c in enumerate(KEEP)}

proc = AutoImageProcessor.from_pretrained(BACKBONE)
MEAN, STD = proc.image_mean, proc.image_std
NORM = T.Normalize(MEAN, STD)
train_tf = T.Compose([T.RandomResizedCrop(224, scale=(0.6,1.0)), T.RandomHorizontalFlip(),
                      T.RandAugment(num_ops=2, magnitude=7), T.ToTensor(), NORM])
val_tf = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor(), NORM])

ds = load_dataset("szymonrucinski/types-of-film-shots", split="train")
amb = OLD.index("ambiguous")
ds = ds.filter(lambda r: r["label"] != amb)                     # drop ambiguous

# stratified 20% of HUMAN rows -> val; everything else -> train
import collections
rng = np.random.default_rng(0)
human_by_cls = collections.defaultdict(list)
for i, r in enumerate(ds):
    if r["annotator"] == "human":
        human_by_cls[r["label"]].append(i)
val_idx = set()
for c, idxs in human_by_cls.items():
    idxs = np.array(idxs); rng.shuffle(idxs)
    val_idx.update(idxs[: max(1, int(0.2*len(idxs)))].tolist())
train_idx = [i for i in range(len(ds)) if i not in val_idx]
print(f"train {len(train_idx)}  val(human) {len(val_idx)}")

class DS(Dataset):
    def __init__(s, base, idx, tf): s.base, s.idx, s.tf = base, list(idx), tf
    def __len__(s): return len(s.idx)
    def __getitem__(s, j):
        r = s.base[s.idx[j]]
        return s.tf(r["image"].convert("RGB")), O2N[r["label"]]

tr = DataLoader(DS(ds, train_idx, train_tf), batch_size=32, shuffle=True, num_workers=4, drop_last=True)
va = DataLoader(DS(ds, val_idx, val_tf), batch_size=32, num_workers=4)

class Classifier(nn.Module):
    def __init__(s, backbone, n):
        super().__init__(); s.backbone = backbone
        s.head = nn.Linear(backbone.config.hidden_size, n)
    def forward(s, x):
        out = s.backbone(pixel_values=x)
        feat = out.pooler_output if getattr(out, "pooler_output", None) is not None else out.last_hidden_state[:, 0]
        return s.head(feat)

model = Classifier(AutoModel.from_pretrained(BACKBONE), len(KEEP)).to(DEV)

# class-balanced weights (effective number) from the TRAIN split
cnt = np.zeros(len(KEEP))
for i in train_idx: cnt[O2N[ds[i]["label"]]] += 1
beta = 0.999; w = (1-beta)/(1-np.power(beta, cnt)); w = w/w.sum()*len(KEEP)
crit = nn.CrossEntropyLoss(weight=torch.tensor(w, dtype=torch.float32, device=DEV), label_smoothing=0.05)
head = [p for n,p in model.named_parameters() if n.startswith("head")]
back = [p for n,p in model.named_parameters() if not n.startswith("head")]
opt = torch.optim.AdamW([{"params":head,"lr":1e-3},{"params":back,"lr":1e-5}], weight_decay=0.05)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=16)

best, best_sd = 0.0, None
for ep in range(16):
    model.train()
    for x,y in tr:
        x,y=x.to(DEV),y.to(DEV); opt.zero_grad(); crit(model(x), y).backward(); opt.step()
    sched.step()
    model.eval(); cm=np.zeros((len(KEEP),len(KEEP)),int)
    with torch.no_grad():
        for x,y in va:
            p=model(x.to(DEV)).argmax(1).cpu().numpy()
            for t,pr in zip(y.numpy(),p): cm[t,pr]+=1
    acc=cm.trace()/cm.sum(); bal=np.mean(np.diag(cm)/np.clip(cm.sum(1),1,None))
    print(f"ep {ep+1:2d}  human_acc {acc:.3f}  balanced {bal:.3f}")
    if bal>best: best,best_sd=bal,{k:v.cpu().clone() for k,v in model.state_dict().items()}

print(f"best human balanced_acc {best:.3f}")
model.load_state_dict(best_sd); model.eval()

class Wrap(nn.Module):
    def __init__(s,m): super().__init__(); s.m=m
    def forward(s,x): return s.m(x)
import onnx, onnxruntime as ort
from onnxsim import simplify
torch.onnx.export(Wrap(model.cpu()).eval(), (torch.randn(1,3,224,224),), "/tmp/_v3.onnx",
                  input_names=["pixel_values"], output_names=["logits"], opset_version=16, dynamo=False)
simp,ok=simplify(onnx.load("/tmp/_v3.onnx")); assert ok
onnx.save(simp, "dinov3_shot.onnx")
x=torch.randn(1,3,224,224)
with torch.no_grad(): t=Wrap(model)(x).numpy()
o=ort.InferenceSession("dinov3_shot.onnx",providers=["CPUExecutionProvider"]).run(None,{"pixel_values":x.numpy()})[0]
print("onnx diff:", np.abs(t-o).max(), "argmax ok:", t.argmax()==o.argmax())
print("classes:", KEEP)
