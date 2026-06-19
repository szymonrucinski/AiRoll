"""Label all 2260 empty Firebase frames with our v2 DINOv2 (free/local) + confidence.

Bulk pass of the active-learning plan: v2 labels everything; frames where v2 is
UNSURE (low softmax) get escalated to Opus later. Resumable via v2_labels.jsonl.
Downloads are threaded (the bottleneck); inference is CPU and instant.
"""
import io, json, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np, onnxruntime as ort
from PIL import Image

HERE = Path(__file__).resolve().parent
FRAMES = json.load(open(HERE / "empty_frames.json"))
OUT = HERE / "v2_labels.jsonl"
NEW = ["closeUp", "detail", "extremeLongShot", "fullShot", "longShot", "mediumCloseUp", "mediumShot"]
MEAN = np.array([0.485, 0.456, 0.406], np.float32); STD = np.array([0.229, 0.224, 0.225], np.float32)
sess = ort.InferenceSession(str(HERE.parent / "dinov2_shot_v2.onnx"), providers=["CPUExecutionProvider"])
INAME = sess.get_inputs()[0].name

done = set()
if OUT.exists():
    for l in open(OUT):
        try: done.add(json.loads(l)["key"])
        except Exception: pass

def key(f): return f"{f['movie']}/{f['frame']}"
todo = [f for f in FRAMES if key(f) not in done]
print(f"total {len(FRAMES)}  done {len(done)}  todo {len(todo)}", flush=True)

def fetch(f):
    try: return f, urllib.request.urlopen(f["url"], timeout=25).read()
    except Exception: return f, None

def classify(b):
    im = Image.open(io.BytesIO(b)).convert("RGB"); w, h = im.size; s = 256 / min(w, h)
    im = im.resize((round(w * s), round(h * s)), Image.BICUBIC); W, H = im.size
    l, t = (W - 224) // 2, (H - 224) // 2; im = im.crop((l, t, l + 224, t + 224))
    x = ((np.asarray(im, np.float32) / 255 - MEAN) / STD).transpose(2, 0, 1)[None].astype(np.float32)
    logit = sess.run(None, {INAME: x})[0][0]
    p = np.exp(logit - logit.max()); p /= p.sum(); i = int(p.argmax())
    return NEW[i], float(p[i])

n = 0
with open(OUT, "a") as out, ThreadPoolExecutor(max_workers=16) as ex:
    for f, b in ex.map(fetch, todo):
        if b is None: continue
        try: shot, conf = classify(b)
        except Exception: continue
        out.write(json.dumps({"key": key(f), "movie": f["movie"], "frame": f["frame"],
                              "url": f["url"], "shot": shot, "conf": round(conf, 4)}) + "\n")
        n += 1
        if n % 100 == 0: out.flush(); print(f"labeled {n}/{len(todo)}", flush=True)
print(f"DONE labeled {n}", flush=True)
