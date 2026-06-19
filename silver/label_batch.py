"""Silver-label the 2260 unlabeled Firebase frames via codex (gpt-5.4-mini vision).

Resumable: appends to labels.jsonl; rerun skips frames already done. Batches 6
frames per codex call to amortise the CLI's per-call overhead. Failed downloads /
codex errors are skipped (frame stays undone -> retried on the next run).

NOTE: produces a SILVER set (machine labels). Do NOT merge into the gold dataset
without confidence/agreement filtering + a human spot-check.
"""
import json, os, subprocess, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRAMES = json.load(open(HERE / "empty_frames.json"))
IMGS = HERE / "imgs"; IMGS.mkdir(exist_ok=True)
OUT = HERE / "labels.jsonl"
SCHEMA = HERE / "schema_batch.json"
BATCH = 6
ENUM = "extremeLongShot,longShot,fullShot,mediumShot,mediumCloseUp,closeUp,detail,ambiguous"
PROMPT = (
    "{n} film frames are attached, numbered 1 to {n} in attachment order. "
    "Classify each frame's SHOT SCALE into one of: " + ENUM + ". "
    "Return a results array of length {n}; index is the 1-based frame number. "
    "Definitions: extremeLongShot=subject tiny in vast environment; longShot=full body "
    "with lots of environment; fullShot=full body head-to-toe filling frame; mediumShot=waist up; "
    "mediumCloseUp=chest/shoulders up; closeUp=head/face fills frame; detail=extreme close-up "
    "of an object/part; ambiguous=genuinely unclear."
)

done = set()
if OUT.exists():
    for line in open(OUT):
        try: done.add(json.loads(line)["key"])
        except Exception: pass

def key(f): return f"{f['movie']}/{f['frame']}"
def dl(f, i):
    p = IMGS / f"f{i}.jpg"
    if p.exists() and p.stat().st_size > 0: return p
    try:
        urllib.request.urlretrieve(f["url"], p); return p if p.stat().st_size > 0 else None
    except Exception: return None

todo = [(i, f) for i, f in enumerate(FRAMES) if key(f) not in done]
print(f"total {len(FRAMES)}  done {len(done)}  todo {len(todo)}", flush=True)

for b in range(0, len(todo), BATCH):
    chunk = todo[b:b + BATCH]
    imgs, valid = [], []
    for i, f in chunk:
        p = dl(f, i)
        if p: imgs += ["-i", str(p)]; valid.append(f)
    if not valid: continue
    tmp = HERE / "_tmp.json"
    cmd = (["codex", "exec", *imgs, "-m", "gpt-5.4-mini", "-s", "read-only",
            "-c", "model_reasoning_effort=low", "--output-schema", str(SCHEMA),
            "-o", str(tmp), PROMPT.format(n=len(valid))])
    try:
        subprocess.run(cmd, timeout=300, capture_output=True)
        res = json.load(open(tmp))["results"]
    except Exception as e:
        print(f"batch {b//BATCH} FAILED: {type(e).__name__}", flush=True); continue
    with open(OUT, "a") as out:
        for f, r in zip(valid, res):           # zip by order; index field is a cross-check
            out.write(json.dumps({"key": key(f), "movie": f["movie"], "frame": f["frame"],
                                  "url": f["url"], "shot": r["shot"],
                                  "confidence": r.get("confidence", 0)}) + "\n")
    print(f"batch {b//BATCH+1}/{(len(todo)+BATCH-1)//BATCH}  +{len(valid)}  "
          f"total_done {len(done)+b+len(valid)}", flush=True)
print("DONE", flush=True)
