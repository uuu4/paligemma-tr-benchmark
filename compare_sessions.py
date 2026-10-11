"""Compare the three Colab sessions (v1, v2, v3) of the PaliGemma 2 Turkish OCR benchmark.

Usage:  python compare_sessions.py      (stdlib only; run from the repo root)

Targets and full texts are read from the v3 notebook (cell with `HEDEF = {`), so there is one source of truth.
v1 had 3 prompts (`tr`/`en` there are `tr_tr`/`en_en` here); v2 and v3 have 5. In v3 only repeat 1 is used,
because repeats inside one session are identical.
"""
import csv, difflib, json, re, unicodedata

nb = json.load(open("paligemma2_tr_ocr_v3.ipynb", encoding="utf-8"))
src = next("".join(c["source"]) for c in nb["cells"] if "HEDEF = {" in "".join(c["source"]))
ns = {}
exec(src.split("def tr_lower")[0], ns)
HEDEF, TAM = ns["HEDEF"], ns["TAM_METIN"]

def tr_lower(s): return unicodedata.normalize("NFC", s).replace("İ", "i").replace("I", "ı").lower()
def words(s): return re.findall(r"[^\W_]+", tr_lower(s))
def letters(s): return re.findall(r"[^\W_\d]+", tr_lower(s))
def score(out, target): w = set(words(out)); t = words(target); return 100 * sum(x in w for x in t) / len(t)
def invented(out, full):
    tw = set(letters(full)); res = []
    for w in letters(out):
        if len(w) < 3 or w in tw: continue
        if max(difflib.SequenceMatcher(None, w, x).ratio() for x in tw) >= 0.7: continue
        res.append(w)
    return res

def load(path, rename=None, only_repeat=None):
    rows = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        if only_repeat and r.get("kosu") != str(only_repeat): continue
        p = (rename or {}).get(r["prompt"], r["prompt"])
        rows[(r["foto"], int(r["cozunurluk"]), p)] = r["cikti"]
    return rows

S = {"v1": load("results/sonuclar_v1.csv", {"tr": "tr_tr", "en": "en_en"}),
     "v2": load("results/sonuclar_v2.csv"),
     "v3": load("results/sonuclar_v3.csv", only_repeat=1)}
PROMPTS = ["ocr", "en_en", "tr_en", "tr_tr", "en_tr"]
GROUPS = {"boxes+sign": lambda f: not f.startswith("fis"), "receipts": lambda f: f.startswith("fis"), "all": lambda f: True}

def mean(s, grp, p, res):
    xs = [score(o, HEDEF[f]) for (f, r, q), o in S[s].items() if q == p and r == res and GROUPS[grp](f)]
    return sum(xs) / len(xs) if xs else None
def fmt(a, b): return "   -   " if a is None else f"{a:3.0f}/{b:3.0f}"

print("Average word match (%), 224/448, per session")
print(f"{'group':11} {'prompt':6}   v1       v2       v3")
for g in GROUPS:
    for p in PROMPTS:
        print(f"{g:11} {p:6}", "  ".join(fmt(mean(s, g, p, 224), mean(s, g, p, 448)) for s in S))

print("\nOutputs that differ between sessions (same photo, resolution, prompt)")
for a, b in (("v1", "v2"), ("v1", "v3"), ("v2", "v3")):
    ks = [k for k in S[a] if k in S[b]]
    print(f"{a} vs {b}: {sum(S[a][k] != S[b][k] for k in ks)} / {len(ks)}")

print("\nInvented words (ocr): words not on the photo and not close to any word on it, summed per group, 224/448")
for s in S:
    for g in ("boxes+sign", "receipts"):
        t = {res: sum(len(invented(o, TAM[f])) for (f, r, q), o in S[s].items() if q == "ocr" and r == res and GROUPS[g](f)) for res in (224, 448)}
        print(f"{s} {g:11} {t[224]:3d}/{t[448]:3d}")
