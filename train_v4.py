"""v4: DINOv3-small trained on the 53K scaleup set (v3 labels + Opus corrections
for conf<0.4), validated on human gold. Exports fp32 ONNX (int8 done separately)."""
import io, json, numpy as np, torch, torch.nn as nn
from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
from transformers import AutoModel, AutoImageProcessor
from datasets import load_dataset

HERE = Path(__file__).resolve().parent
SU = HERE / "scaleup"
DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BACKBONE = "facebook/dinov3-vits16-pretrain-lvd1689m"
OLD = ["ambiguous","closeUp","detail","extremeLongShot","fullShot","longShot","mediumCloseUp","mediumShot"]
KEEP = [c for c in OLD if c != "ambiguous"]
O2N = {c: i for i, c in enumerate(KEEP)}

# ---- resolve Opus corrections: review/ (conf<0.3) via build_scaleup, review34/ (0.3-0.4) via out files ----
src = open(SU / "build_scaleup.py").read().split("records, n_opus")[0]
ns = {"__file__": str(SU / "build_scaleup.py")}
exec(src, ns)
opus = dict(ns["opus_label"])
for k in range(40):
    p = SU / "review34" / f"out_{k}.json"
    if not p.exists(): continue
    out = json.load(open(p)); man = [int(l.split("\t")[0]) for l in open(SU / "review34" / f"batch_{k}.txt")]
    gset = set(man)
    if all(int(key) in gset for key in out):
        for key, lab in out.items(): opus[int(key)] = lab
    else:
        for key, lab in out.items(): opus[man[int(key) - 1]] = lab
print("opus corrections:", len(opus))

# ---- training records (drop ambiguous) ----
rows = [json.loads(l) for l in open(SU / "v3_labels.jsonl")]
data = []
for r in rows:
    i = r["i"]; img = SU / "dl" / f"{i}.jpg"
    if not img.exists(): continue
    lab = opus.get(i, r["shot"])
    if lab not in O2N: continue
    data.append((str(img), O2N[lab]))
print("train frames:", len(data))

proc = AutoImageProcessor.from_pretrained(BACKBONE)
NORM = T.Normalize(proc.image_mean, proc.image_std)
train_tf = T.Compose([T.RandomResizedCrop(224, scale=(0.6,1.0)), T.RandomHorizontalFlip(),
                      T.RandAugment(2,7), T.ToTensor(), NORM])
val_tf = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor(), NORM])

class TrainDS(Dataset):
    def __init__(s, d): s.d = d
    def __len__(s): return len(s.d)
    def __getitem__(s, j):
        p, y = s.d[j]; return train_tf(Image.open(p).convert("RGB")), y

# human gold val from HF
gold = load_dataset("szymonrucinski/types-of-film-shots", split="train")
gold = gold.filter(lambda r: r["annotator"] == "human" and OLD[r["label"]] in O2N)
class ValDS(Dataset):
    def __init__(s, g): s.g = g
    def __len__(s): return len(s.g)
    def __getitem__(s, j):
        r = s.g[j]; return val_tf(r["image"].convert("RGB")), O2N[OLD[r["label"]]]
print("human val:", len(gold))

tr = DataLoader(TrainDS(data), batch_size=32, shuffle=True, num_workers=8, drop_last=True)
va = DataLoader(ValDS(gold), batch_size=32, num_workers=4)

class Clf(nn.Module):
    def __init__(s, b, n): super().__init__(); s.backbone = b; s.head = nn.Linear(b.config.hidden_size, n)
    def forward(s, x):
        o = s.backbone(pixel_values=x)
        f = o.pooler_output if getattr(o, "pooler_output", None) is not None else o.last_hidden_state[:, 0]
        return s.head(f)
model = Clf(AutoModel.from_pretrained(BACKBONE), len(KEEP)).to(DEV)

cnt = np.bincount([y for _, y in data], minlength=len(KEEP)).astype(float)
beta = 0.999; w = (1-beta)/(1-np.power(beta, cnt)); w = w/w.sum()*len(KEEP)
crit = nn.CrossEntropyLoss(weight=torch.tensor(w, dtype=torch.float32, device=DEV), label_smoothing=0.05)
opt = torch.optim.AdamW([{"params":[p for n,p in model.named_parameters() if n.startswith("head")],"lr":1e-3},
                         {"params":[p for n,p in model.named_parameters() if not n.startswith("head")],"lr":1e-5}], weight_decay=0.05)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=8)

best, best_sd = 0.0, None
for ep in range(8):
    model.train()
    for x, y in tr:
        x, y = x.to(DEV), y.to(DEV); opt.zero_grad(); crit(model(x), y).backward(); opt.step()
    sched.step()
    model.eval(); cm = np.zeros((len(KEEP), len(KEEP)), int)
    with torch.no_grad():
        for x, y in va:
            p = model(x.to(DEV)).argmax(1).cpu().numpy()
            for t, pr in zip(y.numpy(), p): cm[t, pr] += 1
    acc = cm.trace()/cm.sum(); bal = np.mean(np.diag(cm)/np.clip(cm.sum(1), 1, None))
    print(f"ep {ep+1}  human_acc {acc:.3f}  balanced {bal:.3f}", flush=True)
    if bal > best: best, best_sd = bal, {k: v.cpu().clone() for k, v in model.state_dict().items()}

print(f"best human balanced {best:.3f}")
model.load_state_dict(best_sd); model.eval()
class Wrap(nn.Module):
    def __init__(s, m): super().__init__(); s.m = m
    def forward(s, x): return s.m(x)
import onnx, onnxruntime as ort
from onnxsim import simplify
torch.onnx.export(Wrap(model.cpu()).eval(), (torch.randn(1,3,224,224),), "/tmp/_v4.onnx",
                  input_names=["pixel_values"], output_names=["logits"], opset_version=16, dynamo=False)
simp, ok = simplify(onnx.load("/tmp/_v4.onnx")); assert ok
onnx.save(simp, "dinov3_shot_v4.onnx")
x = torch.randn(1,3,224,224)
with torch.no_grad(): t = Wrap(model)(x).numpy()
o = ort.InferenceSession("dinov3_shot_v4.onnx", providers=["CPUExecutionProvider"]).run(None, {"pixel_values": x.numpy()})[0]
print("onnx diff:", np.abs(t-o).max(), "argmax ok:", t.argmax()==o.argmax())
print("DONE v4")
