"""Resolve human-'ambiguous' frames: Opus reclassified 62/66 to concrete shot scales.
Relabel those in the published dataset (source='opus_resolved_amb', annotator='ai');
keep the 4 truly-ambiguous. Re-push to szymonrucinski/types-of-film-shots.
"""
from datasets import load_dataset

# Opus resolution of the 66 human-ambiguous frames, by extraction order k=0..65
B0 = {0:"mediumCloseUp",1:"ambiguous",2:"detail",3:"longShot",4:"mediumShot",5:"longShot",6:"ambiguous",7:"mediumShot",8:"mediumCloseUp",9:"mediumCloseUp",10:"fullShot",11:"ambiguous",12:"fullShot",13:"longShot",14:"longShot",15:"mediumShot",16:"longShot",17:"ambiguous",18:"mediumShot",19:"longShot",20:"fullShot",21:"longShot",22:"mediumCloseUp",23:"fullShot",24:"longShot",25:"mediumShot",26:"fullShot",27:"mediumShot",28:"detail",29:"mediumCloseUp",30:"mediumCloseUp",31:"fullShot",32:"longShot"}
B1_local = {1:"detail",2:"extremeLongShot",3:"longShot",4:"mediumShot",5:"mediumShot",6:"longShot",7:"mediumShot",8:"longShot",9:"longShot",10:"detail",11:"detail",12:"closeUp",13:"longShot",14:"extremeLongShot",15:"detail",16:"detail",17:"mediumCloseUp",18:"fullShot",19:"mediumCloseUp",20:"detail",21:"closeUp",22:"longShot",23:"mediumShot",24:"detail",25:"fullShot",26:"longShot",27:"detail",28:"extremeLongShot",29:"detail",30:"detail",31:"fullShot",32:"mediumShot",33:"mediumShot"}
res = dict(B0)
for k, v in B1_local.items():
    res[32 + k] = v          # batch1 local 1..33 -> global 33..65

ds = load_dataset("szymonrucinski/types-of-film-shots", split="train")
names = ds.features["label"].names
amb_id = names.index("ambiguous")

# dataset indices of human-ambiguous rows, in order (no image load)
meta = ds.select_columns(["annotator", "label"])
amb_positions = [i for i, r in enumerate(meta) if r["annotator"] == "human" and r["label"] == amb_id]
assert len(amb_positions) == len(res), f"{len(amb_positions)} vs {len(res)}"

# map dataset index -> new concrete label id (skip the ones still ambiguous)
idx2new = {amb_positions[k]: names.index(res[k]) for k in res if res[k] != "ambiguous"}
print(f"resolving {len(idx2new)} frames; keeping {len(res)-len(idx2new)} ambiguous")

def fix(r, i):
    if i in idx2new:
        r["label"] = idx2new[i]; r["annotator"] = "ai"; r["source"] = "opus_resolved_amb"
    return r

ds = ds.map(fix, with_indices=True)
from collections import Counter
print("labels now:", {names[k]: v for k, v in sorted(Counter(ds["label"]).items())})
print("annotator:", Counter(ds["annotator"]))
ds.push_to_hub("szymonrucinski/types-of-film-shots", private=False)
print("pushed.")
