"""Scrape film-grab frame URLs for the picked diverse movies (HTTP, no Selenium).
movie page -> bwg gallery_id -> admin-ajax bwg_frontend_data -> .bwg-a frame hrefs.
Resumable: appends to frames.jsonl; skips movies already scraped."""
import json, re, urllib.request, urllib.parse, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

HERE = Path(__file__).resolve().parent
MOVIES = [l.strip() for l in open(HERE / "movies.txt") if l.strip()]
OUT = HERE / "frames.jsonl"
UA = {"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}

done = set()
if OUT.exists():
    for l in open(OUT):
        try: done.add(json.loads(l)["movie"])
        except Exception: pass

def slug(p): return p.rstrip("/").split("/")[-1]

def scrape(perma):
    s = slug(perma)
    if s in done: return None
    try:
        h = urllib.request.urlopen(urllib.request.Request("https://film-grab.com" + perma, headers=UA), timeout=30).read().decode("utf-8", "ignore")
        m = re.search(r"bwg_container_(\d+)", h) or re.search(r"gallery_id[\"'=: ]+(\d+)", h)
        if not m: return (s, [])
        gid = m.group(1)
        d = urllib.parse.urlencode({"action": "bwg_frontend_data", "gallery_id": gid, "image_id": "0", "shortcode_id": gid}).encode()
        r = urllib.request.urlopen(urllib.request.Request("https://film-grab.com/wp-admin/admin-ajax.php", data=d, headers=UA), timeout=30).read().decode("utf-8", "ignore")
        urls = re.findall(r'class="bwg-a[^"]*"[^>]*href="(https://film-grab\.com/wp-content/uploads/photo-gallery/[^"]+?)"', r)
        return (s, sorted(set(u.replace("\\/", "/") for u in urls)))
    except Exception:
        return (s, None)   # None = failed (retry next run)

todo = [p for p in MOVIES if slug(p) not in done]
print(f"movies {len(MOVIES)} done {len(done)} todo {len(todo)}", flush=True)
n_mov = n_fr = 0
with open(OUT, "a") as out, ThreadPoolExecutor(max_workers=5) as ex:
    for res in ex.map(scrape, todo):
        if res is None: continue
        s, urls = res
        if urls is None: continue          # failed, don't mark done
        for u in urls: out.write(json.dumps({"movie": s, "url": u}) + "\n")
        n_mov += 1; n_fr += len(urls)
        if n_mov % 25 == 0: out.flush(); print(f"{n_mov} movies, {n_fr} frames", flush=True)
print(f"DONE {n_mov} movies, {n_fr} frames", flush=True)
