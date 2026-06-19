"""Merge v2 (high-conf) + Opus (low-conf review) labels -> push HF silver dataset.

Active-learning result: v2 labels everything; the 315 conf<0.5 frames were re-judged
by Opus. Final label = Opus where reviewed, else v2. Published as a SEPARATE 'silver'
dataset (not the gold types-of-film-shots) with provenance columns.
"""
import json
from pathlib import Path
import datasets

HERE = Path(__file__).resolve().parent
ROWS = [json.loads(l) for l in open(HERE / "v2_labels.jsonl")]   # index = line number
CLASSES = ["ambiguous", "closeUp", "detail", "extremeLongShot",
           "fullShot", "longShot", "mediumCloseUp", "mediumShot"]   # 8, gold order

# Opus subagent outputs. Batches 0,2,3 returned LOCAL 1..35 indices -> remap by manifest order.
OPUS = {
 0:{"1":"longShot","2":"longShot","3":"fullShot","4":"longShot","5":"longShot","6":"ambiguous","7":"longShot","8":"longShot","9":"longShot","10":"longShot","11":"longShot","12":"longShot","13":"longShot","14":"mediumShot","15":"ambiguous","16":"ambiguous","17":"closeUp","18":"ambiguous","19":"mediumShot","20":"mediumShot","21":"mediumShot","22":"mediumCloseUp","23":"ambiguous","24":"detail","25":"longShot","26":"fullShot","27":"longShot","28":"fullShot","29":"mediumShot","30":"longShot","31":"mediumShot","32":"ambiguous","33":"mediumShot","34":"mediumShot","35":"fullShot"},
 1:{"240":"longShot","258":"mediumShot","262":"mediumShot","263":"detail","273":"fullShot","280":"longShot","292":"fullShot","312":"mediumCloseUp","322":"ambiguous","327":"mediumCloseUp","330":"closeUp","337":"longShot","342":"ambiguous","348":"longShot","355":"longShot","366":"detail","367":"mediumShot","368":"detail","369":"mediumCloseUp","377":"longShot","382":"detail","386":"longShot","389":"closeUp","405":"mediumCloseUp","416":"mediumShot","428":"mediumShot","434":"ambiguous","436":"ambiguous","437":"mediumShot","440":"fullShot","442":"mediumShot","453":"longShot","471":"mediumCloseUp","473":"ambiguous"},
 2:{"1":"extremeLongShot","2":"longShot","3":"mediumCloseUp","4":"detail","5":"mediumShot","6":"longShot","7":"detail","8":"ambiguous","9":"longShot","10":"fullShot","11":"fullShot","12":"closeUp","13":"ambiguous","14":"ambiguous","15":"mediumShot","16":"ambiguous","17":"ambiguous","18":"fullShot","19":"mediumShot","20":"ambiguous","21":"longShot","22":"ambiguous","23":"closeUp","24":"mediumCloseUp","25":"mediumCloseUp","26":"closeUp","27":"fullShot","28":"fullShot","29":"longShot","30":"ambiguous","31":"mediumShot","32":"longShot","33":"extremeLongShot","34":"mediumShot","35":"mediumShot"},
 3:{"1":"mediumShot","2":"extremeLongShot","3":"longShot","4":"longShot","5":"longShot","6":"longShot","7":"longShot","8":"longShot","9":"mediumShot","10":"mediumShot","11":"detail","12":"fullShot","13":"mediumShot","14":"mediumCloseUp","15":"fullShot","16":"extremeLongShot","17":"mediumShot","18":"fullShot","19":"fullShot","20":"mediumCloseUp","21":"fullShot","22":"mediumShot","23":"ambiguous","24":"longShot","25":"longShot","26":"mediumShot","27":"longShot","28":"fullShot","29":"longShot","30":"closeUp","31":"extremeLongShot","32":"mediumShot","33":"mediumShot","34":"closeUp","35":"mediumShot"},
 4:{"933":"detail","936":"longShot","938":"mediumShot","956":"longShot","982":"mediumCloseUp","993":"longShot","1004":"extremeLongShot","1010":"detail","1015":"mediumCloseUp","1017":"ambiguous","1027":"closeUp","1032":"mediumCloseUp","1046":"mediumCloseUp","1049":"longShot","1055":"mediumShot","1065":"longShot","1076":"closeUp","1078":"fullShot","1085":"longShot","1089":"mediumShot","1091":"longShot","1096":"longShot","1097":"mediumShot","1104":"detail","1107":"longShot","1111":"longShot","1114":"extremeLongShot","1115":"longShot","1117":"mediumCloseUp","1124":"longShot","1132":"fullShot","1134":"longShot","1142":"mediumShot","1152":"longShot"},
 5:{"1158":"longShot","1162":"mediumShot","1163":"longShot","1166":"fullShot","1174":"extremeLongShot","1178":"closeUp","1179":"mediumShot","1204":"ambiguous","1212":"mediumShot","1219":"mediumShot","1236":"detail","1239":"mediumShot","1252":"closeUp","1254":"fullShot","1265":"closeUp","1266":"longShot","1290":"longShot","1303":"fullShot","1306":"longShot","1309":"longShot","1314":"longShot","1315":"ambiguous","1318":"longShot","1320":"fullShot","1329":"fullShot","1343":"longShot","1348":"longShot","1361":"detail","1368":"mediumCloseUp","1388":"mediumShot","1390":"longShot","1394":"mediumShot","1397":"fullShot","1399":"longShot","1398":"longShot"},
 6:{"1401":"longShot","1402":"longShot","1408":"mediumShot","1411":"closeUp","1414":"ambiguous","1421":"mediumCloseUp","1424":"closeUp","1431":"mediumShot","1436":"longShot","1444":"mediumCloseUp","1457":"closeUp","1460":"mediumCloseUp","1470":"mediumCloseUp","1473":"mediumCloseUp","1481":"longShot","1486":"mediumShot","1490":"longShot","1494":"longShot","1506":"extremeLongShot","1508":"longShot","1516":"longShot","1517":"mediumCloseUp","1526":"mediumCloseUp","1534":"longShot","1537":"ambiguous","1539":"mediumShot","1555":"detail","1569":"mediumCloseUp","1573":"detail","1577":"ambiguous","1581":"longShot","1585":"longShot","1597":"extremeLongShot","1598":"extremeLongShot","1600":"longShot"},
 7:{"1606":"longShot","1622":"longShot","1643":"mediumCloseUp","1646":"longShot","1653":"fullShot","1663":"mediumShot","1670":"longShot","1672":"mediumShot","1684":"longShot","1685":"detail","1693":"detail","1700":"longShot","1713":"mediumCloseUp","1716":"mediumShot","1719":"mediumCloseUp","1721":"mediumShot","1722":"closeUp","1724":"fullShot","1734":"closeUp","1736":"fullShot","1747":"longShot","1748":"mediumShot","1752":"mediumCloseUp","1754":"mediumShot","1762":"longShot","1763":"detail","1774":"longShot","1776":"fullShot","1789":"mediumShot","1793":"longShot","1812":"fullShot","1816":"longShot","1817":"fullShot","1826":"mediumShot"},
 8:{"1828":"mediumShot","1839":"detail","1841":"longShot","1843":"longShot","1846":"longShot","1847":"mediumCloseUp","1852":"fullShot","1862":"fullShot","1869":"mediumShot","1871":"fullShot","1879":"longShot","1880":"longShot","1882":"longShot","1885":"extremeLongShot","1893":"longShot","1901":"fullShot","1903":"closeUp","1921":"detail","1926":"ambiguous","1928":"closeUp","1932":"longShot","1939":"mediumShot","1940":"mediumCloseUp","1945":"longShot","1947":"detail","1951":"longShot","1957":"mediumShot","1958":"ambiguous","1959":"longShot","1961":"longShot","1964":"detail","1971":"extremeLongShot","1974":"fullShot","1975":"mediumShot","1977":"longShot"}}

# resolve Opus labels to GLOBAL row index, remapping the local-indexed batches by manifest order
opus_label = {}
for k, d in OPUS.items():
    manifest = [int(l.split("\t")[0]) for l in open(HERE / f"review/batch_{k}.txt")]
    gset = set(manifest)
    if all(int(key) in gset for key in d):                 # already global indices
        for key, lab in d.items(): opus_label[int(key)] = lab
    else:                                                  # local 1..N -> manifest position
        for key, lab in d.items(): opus_label[manifest[int(key) - 1]] = lab

records, n_opus = [], 0
for i, r in enumerate(ROWS):
    img = HERE / "dl" / f"{i}.jpg"
    if not img.exists() or img.stat().st_size == 0: continue
    if i in opus_label:
        lab, src, n_opus = opus_label[i], "opus_review", n_opus + 1
    else:
        lab, src = r["shot"], "v2_highconf"
    if lab not in CLASSES: continue
    records.append({"image": str(img), "label": lab, "source": src,
                    "confidence": r["conf"], "movie": r["movie"], "frame": r["frame"]})

print(f"records {len(records)}  (opus-reviewed {n_opus}, v2 {len(records)-n_opus})")
ds = datasets.Dataset.from_list(records)
ds = ds.cast_column("image", datasets.Image())
ds = ds.cast_column("label", datasets.ClassLabel(names=CLASSES))
ds.push_to_hub("szymonrucinski/types-of-film-shots-silver", private=False)
print("pushed -> szymonrucinski/types-of-film-shots-silver")
