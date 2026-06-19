"""How 'tricky' is each confidence band? = how often Opus overrules v2.
Low agreement -> v2 was unreliable there (tricky). Reuses build_final's resolve+OPUS1/2.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent

# run build_final up to (not incl.) the dataset build -> gives resolve, opus_label(review1+2), ROWS
src = open(HERE / "build_final.py").read().split("records, n_opus")[0]
ns = {"__file__": str(HERE / "build_final.py")}
exec(src, ns)
resolve, ROWS = ns["resolve"], ns["ROWS"]
opus = dict(ns["opus_label"])   # review1 (<0.5) + review2 (0.5-0.7)

OPUS3 = {
 0:{"3":"fullShot","4":"extremeLongShot","13":"longShot","14":"longShot","23":"longShot","35":"fullShot","48":"fullShot","50":"fullShot","60":"longShot","71":"fullShot","80":"mediumShot","99":"detail","101":"mediumShot","103":"mediumCloseUp","105":"mediumShot","110":"longShot","115":"extremeLongShot","122":"extremeLongShot","133":"longShot","140":"fullShot","157":"closeUp","160":"ambiguous","164":"detail","167":"mediumCloseUp","168":"fullShot","169":"ambiguous","170":"detail","183":"longShot","197":"fullShot","199":"fullShot","205":"extremeLongShot","215":"longShot","216":"closeUp","222":"closeUp","228":"longShot"},
 1:{"1":"longShot","2":"longShot","3":"longShot","4":"longShot","5":"mediumShot","6":"longShot","7":"extremeLongShot","8":"longShot","9":"fullShot","10":"closeUp","11":"detail","12":"longShot","13":"longShot","14":"closeUp","15":"extremeLongShot","16":"longShot","17":"longShot","18":"mediumShot","19":"mediumShot","20":"longShot","21":"mediumShot","22":"closeUp","23":"mediumShot","24":"longShot","25":"mediumShot","26":"mediumShot","27":"mediumCloseUp","28":"mediumShot","29":"mediumShot","30":"detail","31":"longShot","32":"mediumCloseUp","33":"mediumShot","34":"fullShot","35":"mediumShot"},
 2:{"1":"closeUp","2":"mediumCloseUp","3":"mediumCloseUp","4":"mediumShot","5":"closeUp","6":"longShot","7":"closeUp","8":"mediumCloseUp","9":"mediumCloseUp","10":"longShot","11":"longShot","12":"mediumCloseUp","13":"fullShot","14":"closeUp","15":"extremeLongShot","16":"mediumShot","17":"detail","18":"mediumShot","19":"extremeLongShot","20":"longShot","21":"mediumShot","22":"mediumShot","23":"ambiguous","24":"mediumShot","25":"longShot","26":"longShot","27":"longShot","28":"mediumShot","29":"mediumCloseUp","30":"mediumShot","31":"fullShot","32":"closeUp","33":"closeUp","34":"longShot","35":"longShot"},
 3:{"1":"longShot","2":"extremeLongShot","3":"longShot","4":"longShot","5":"mediumShot","6":"longShot","7":"mediumShot","8":"longShot","9":"longShot","10":"fullShot","11":"ambiguous","12":"mediumCloseUp","13":"detail","14":"longShot","15":"longShot","16":"longShot","17":"mediumShot","18":"longShot","19":"longShot","20":"longShot","21":"fullShot","22":"closeUp","23":"closeUp","24":"mediumShot","25":"mediumShot","26":"mediumCloseUp","27":"mediumShot","28":"mediumCloseUp","29":"detail","30":"detail","31":"mediumShot","32":"longShot","33":"mediumShot","34":"fullShot","35":"closeUp"},
 4:{"1009":"closeUp","1018":"longShot","1020":"longShot","1021":"extremeLongShot","1022":"longShot","1023":"mediumCloseUp","1043":"longShot","1052":"mediumCloseUp","1059":"mediumShot","1099":"longShot","1100":"longShot","1103":"longShot","1106":"mediumShot","1123":"fullShot","1126":"mediumCloseUp","1133":"longShot","1145":"closeUp","1147":"longShot","1149":"ambiguous","1153":"extremeLongShot","1154":"extremeLongShot","1160":"extremeLongShot","1172":"longShot","1175":"longShot","1177":"mediumShot","1180":"longShot","1184":"mediumCloseUp","1196":"mediumShot","1197":"closeUp","1199":"detail","1205":"longShot","1207":"longShot","1217":"mediumShot","1225":"mediumShot","1226":"mediumShot"},
 5:{"1237":"closeUp","1241":"mediumShot","1242":"longShot","1246":"closeUp","1251":"mediumShot","1261":"longShot","1262":"fullShot","1267":"mediumShot","1280":"detail","1283":"mediumCloseUp","1301":"closeUp","1324":"ambiguous","1328":"longShot","1345":"longShot","1346":"mediumCloseUp","1364":"extremeLongShot","1367":"detail","1374":"extremeLongShot","1377":"longShot","1383":"mediumShot","1385":"longShot","1387":"longShot","1400":"longShot","1406":"longShot","1409":"mediumCloseUp","1418":"ambiguous","1438":"fullShot","1447":"mediumShot","1445":"longShot","1458":"fullShot","1459":"fullShot","1464":"mediumShot","1471":"mediumCloseUp","1484":"mediumCloseUp"},
 6:{"1491":"longShot","1500":"longShot","1504":"longShot","1510":"longShot","1518":"mediumCloseUp","1519":"closeUp","1536":"longShot","1538":"longShot","1543":"ambiguous","1545":"longShot","1546":"mediumShot","1550":"mediumCloseUp","1554":"longShot","1560":"extremeLongShot","1561":"longShot","1574":"closeUp","1587":"longShot","1594":"ambiguous","1595":"detail","1599":"mediumShot","1602":"longShot","1604":"fullShot","1634":"closeUp","1636":"ambiguous","1641":"mediumCloseUp","1645":"mediumCloseUp","1647":"ambiguous","1649":"closeUp","1656":"mediumShot","1668":"extremeLongShot","1675":"closeUp","1686":"mediumCloseUp","1689":"longShot","1690":"longShot","1697":"closeUp"},
 7:{"1710":"closeUp","1720":"mediumCloseUp","1735":"longShot","1739":"extremeLongShot","1745":"mediumCloseUp","1746":"ambiguous","1764":"mediumShot","1778":"mediumShot","1779":"longShot","1800":"longShot","1809":"closeUp","1811":"mediumShot","1813":"mediumCloseUp","1820":"longShot","1825":"fullShot","1832":"fullShot","1848":"mediumShot","1849":"closeUp","1858":"closeUp","1861":"fullShot","1867":"mediumCloseUp","1872":"mediumShot","1875":"mediumCloseUp","1878":"mediumShot","1881":"extremeLongShot","1915":"extremeLongShot","1924":"mediumShot","1929":"closeUp","1937":"extremeLongShot","1942":"detail","1950":"mediumCloseUp","1965":"mediumShot","1984":"longShot","1992":"longShot"}}
opus.update(resolve(OPUS3, "review3"))   # 0.7-0.8

def agree_in(lo, hi):
    m = t = 0
    for i, r in enumerate(ROWS):
        if lo <= r["conf"] < hi and i in opus:
            t += 1; m += (opus[i] == r["shot"])
    return m, t

print("band        Opus==v2   trickiness(=disagree)")
for lo, hi in [(0.0,0.5),(0.5,0.7),(0.7,0.8),(0.8,1.01)]:
    m, t = agree_in(lo, hi)
    if t: print(f"{lo:.1f}-{hi:.1f}    {m}/{t} = {m/t:.0%}      {1-m/t:.0%}")
