"""Download scraped frames + label with v3 (DINOv3) + confidence. Resumable.
Saves images to dl/{i}.jpg (needed for the parquet + Opus review) and writes
v3_labels.jsonl. Threaded downloads (film-grab rate-limits; rerun to fill gaps)."""
import io, json, urllib.request
from urllib.parse import quote, urlsplit, urlunsplit
from concurrent.futures import ThreadPoolExecutor

def enc(u):  # film-grab filenames contain spaces -> percent-encode the path
    s = urlsplit(u)
    return urlunsplit((s.scheme, s.netloc, quote(s.path), s.query, s.fragment))
from pathlib import Path
import numpy as np, onnxruntime as ort
from PIL import Image

HERE = Path(__file__).resolve().parent
FRAMES = [json.loads(l) for l in open(HERE / "frames.jsonl")]
DL = HERE / "dl"; DL.mkdir(exist_ok=True)
OUT = HERE / "v3_labels.jsonl"
KEEP = ["closeUp","detail","extremeLongShot","fullShot","longShot","mediumCloseUp","mediumShot"]
MEAN = np.array([0.485,0.456,0.406],np.float32); STD = np.array([0.229,0.224,0.225],np.float32)
sess = ort.InferenceSession(str(HERE.parent / "dinov3_shot.onnx"), providers=["CPUExecutionProvider"])
INAME = sess.get_inputs()[0].name

done = set()
if OUT.exists():
    for l in open(OUT):
        try: done.add(json.loads(l)["i"])
        except Exception: pass

def classify(b):
    im = Image.open(io.BytesIO(b)).convert("RGB"); w,h = im.size; s = 256/min(w,h)
    im = im.resize((round(w*s),round(h*s)), Image.BICUBIC); W,H = im.size
    l,t = (W-224)//2,(H-224)//2; im = im.crop((l,t,l+224,t+224))
    x = ((np.asarray(im,np.float32)/255-MEAN)/STD).transpose(2,0,1)[None].astype(np.float32)
    lo = sess.run(None,{INAME:x})[0][0]; p = np.exp(lo-lo.max()); p/=p.sum(); i = int(p.argmax())
    return KEEP[i], float(p[i])

def work(idx):
    """Download + classify inside the worker (onnxruntime.run is thread-safe)."""
    i, f = idx
    p = DL / f"{i}.jpg"
    try:
        if p.exists() and p.stat().st_size > 0:
            b = p.read_bytes()
        else:
            b = urllib.request.urlopen(enc(f["url"]), timeout=25).read(); p.write_bytes(b)
        shot, conf = classify(b)
        return {"i": i, "movie": f["movie"], "url": f["url"], "shot": shot, "conf": round(conf, 4)}
    except Exception:
        return None

TARGET = 50000
while len(done) < TARGET:
    todo = [(i, f) for i, f in enumerate(FRAMES) if i not in done]
    if not todo: break
    start = len(done)
    print(f"PASS: have {start} todo {len(todo)}", flush=True)
    with open(OUT, "a") as out, ThreadPoolExecutor(max_workers=16) as ex:
        for rec in ex.map(work, todo):
            if rec is None: continue
            out.write(json.dumps(rec) + "\n"); done.add(rec["i"])
            if len(done) % 1000 == 0:
                out.flush(); print(f"labeled {len(done)}", flush=True)
    if len(done) - start < 150:        # stalled (only dead URLs left)
        print(f"STALL at {len(done)}", flush=True); break
print(f"DONE labeled {len(done)}", flush=True)
