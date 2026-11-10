"""Deeper audit of the library and ledger than validate_cases.py. Reports; changes nothing.

Checks
  ledger   unique record ids; every `supersedes` points at a real row; no row superseded twice (a fork)
  trace    every library record has a current `included` ledger row; every current included row points at a
           real library record
  dupes    the same DOI / PMID / PMCID on two records; near-identical titles
  links    full_text = PMC page iff PMCID (else a non-PMC free link); abstract = PubMed page for the PMID;
           doi / ckn links match the DOI; `access` agrees with full_text
  era      basis "from downstream level" agrees with the level (0 -> novel, >=1 -> emerging)
  text     summary and caveat present, end with a full stop, no doubled spaces; tags lower-case-hyphenated;
           plausible citation year; authors and title present
  copy     (only if /home/claude/work/raw exists) longest run of words shared between a summary or caveat and
           any locally cached abstract for that record; flags runs of 8+ words. The repo is public: summaries
           must be our own words.

Usage:  python3 scripts/audit_library.py            exit code 1 if any hard problem
"""
import csv
import json
import re
import sys
from urllib.parse import parse_qs, quote, urlparse
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

LIB = json.loads(Path("data/cases.json").read_text())
R = LIB["records"]
ROWS = list(csv.DictReader(Path("ledger/records.csv").open()))
hard, soft = [], []


def H(msg):
    hard.append(msg)


def S(msg):
    soft.append(msg)


# ---- ledger --------------------------------------------------------------------------------------------
ids = Counter(r["record_id"] for r in ROWS)
for k, n in ids.items():
    if n > 1:
        H(f"ledger: record_id {k} appears {n}x")
sup = Counter(r["supersedes"] for r in ROWS if r["supersedes"])
for k, n in sup.items():
    if k not in ids:
        H(f"ledger: supersedes unknown row {k}")
    if n > 1:
        H(f"ledger: row {k} superseded {n}x (fork)")
current = [r for r in ROWS if r["record_id"] not in sup]

# ---- trace ---------------------------------------------------------------------------------------------
lib_ids = {r["id"] for r in R}
traced = defaultdict(list)
for r in current:
    if r["decision"] == "included":
        for lid in filter(None, re.split(r"[;, ]+", r["library_ids"])):
            traced[lid].append(r["record_id"])
            if lid not in lib_ids:
                H(f"trace: ledger {r['record_id']} includes unknown library id {lid}")
for rec in R:
    if rec["id"] not in traced:
        H(f"trace: {rec['id']} has no current included ledger row")

# ---- dupes ---------------------------------------------------------------------------------------------
for key in ("doi", "pmid", "pmcid"):
    seen = defaultdict(list)
    for rec in R:
        v = (rec["ids"].get(key) or "").lower()
        if v:
            seen[v].append(rec["id"])
    for v, who in seen.items():
        if len(who) > 1:
            H(f"dupes: {key} {v} on {who}")
norm = lambda t: re.sub(r"[^a-z0-9 ]", "", (t or "").lower()).strip()
titles = [(rec["id"], norm(rec["citation"]["title"])) for rec in R]
for i in range(len(titles)):
    for j in range(i + 1, len(titles)):
        a, b = titles[i][1], titles[j][1]
        if a and b and abs(len(a) - len(b)) < 40 and SequenceMatcher(None, a, b).ratio() > 0.9:
            same = R[i].get("same_patient_as") in (titles[j][0],) or R[j].get("same_patient_as") in (titles[i][0],)
            (S if same else H)(f"dupes: near-identical titles {titles[i][0]} / {titles[j][0]}")

# ---- links ---------------------------------------------------------------------------------------------
for rec in R:
    rid, L, I = rec["id"], rec["links"], rec["ids"]
    if I.get("pmcid"):
        want = f"https://pmc.ncbi.nlm.nih.gov/articles/{I['pmcid']}/"
        if L.get("full_text") != want:
            S(f"links: {rid} has PMCID but full_text is {L.get('full_text')}")
    elif L.get("full_text") and "pmc.ncbi" in L["full_text"]:
        H(f"links: {rid} full_text points at PMC but no PMCID")
    if I.get("pmid") and L.get("abstract") != f"https://pubmed.ncbi.nlm.nih.gov/{I['pmid']}/":
        H(f"links: {rid} abstract link does not match PMID")
    if not I.get("pmid") and L.get("abstract"):
        S(f"links: {rid} has an abstract link but no PMID ({L['abstract']})")
    if I.get("doi"):
        if L.get("doi") not in (f"https://doi.org/{I['doi']}", "https://doi.org/" + quote(I["doi"], safe="/()';:")):
            H(f"links: {rid} doi link does not match DOI")
        if not L.get("ckn"):
            S(f"links: {rid} has a DOI but no CKN link")
        elif parse_qs(urlparse(L["ckn"]).query).get("url", [""])[0] != f"https://doi.org/{I['doi']}":
            H(f"links: {rid} CKN link does not carry the DOI")
        if re.search(r"[<>\"\s]", L.get("doi") or ""):
            S(f"links: {rid} doi link has characters that need percent-encoding")
    elif L.get("doi"):
        H(f"links: {rid} doi link without a DOI")
    acc = rec.get("access")
    if L.get("full_text") and acc != "Free full text":
        S(f"links: {rid} has full_text but access is {acc!r}")
    if not L.get("full_text") and acc == "Free full text":
        H(f"links: {rid} says Free full text but has no full_text link")

# ---- era -----------------------------------------------------------------------------------------------
for rec in R:
    e, lvl = rec["era"], rec["downstream"]["level"]
    if e.get("basis") == "from downstream level":
        want = "novel" if int(lvl) == 0 else "emerging"
        if e["label"] != want and e["label"] not in ("known", "refuted"):
            S(f"era: {rec['id']} label {e['label']} but downstream level {lvl} implies {want}")

# ---- text ----------------------------------------------------------------------------------------------
TAG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
for rec in R:
    rid = rec["id"]
    for f in ("summary", "caveat"):
        t = (rec.get(f) or "").strip()
        if not t:
            (H if f == "summary" else S)(f"text: {rid} empty {f}")
            continue
        if not t.endswith((".", "?", ")")):
            S(f"text: {rid} {f} lacks a full stop")
        if "  " in t:
            S(f"text: {rid} {f} has doubled spaces")
    for tg in rec.get("tags", []):
        if not TAG.match(tg):
            S(f"text: {rid} tag {tg!r} not lower-case-hyphenated")
    c = rec["citation"]
    if not c.get("title") or not c.get("authors"):
        H(f"text: {rid} citation missing title or authors")
    if not (1800 <= int(c.get("year") or 0) <= 2027):
        H(f"text: {rid} implausible year {c.get('year')}")
    if rec["record_type"] == "case" and not rec.get("tier"):
        H(f"text: {rid} case without tier")

# ---- copy ----------------------------------------------------------------------------------------------
raw = Path("/home/claude/work/raw")
copy_checked = 0
if raw.exists():
    ab = {}
    for f in raw.glob("*.json"):
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if x.get("abs") and (x.get("pmid") or x.get("doi")):
                    for k in (x.get("pmid"), (x.get("doi") or "").lower()):
                        if k:
                            ab[k] = x["abs"]
                stack.extend(v for v in x.values() if isinstance(v, (dict, list)))
            elif isinstance(x, list):
                stack.extend(v for v in x if isinstance(v, (dict, list)))
    words = lambda t: re.findall(r"[a-z0-9']+", t.lower())
    for rec in R:
        a = ab.get(rec["ids"].get("pmid")) or ab.get(rec["ids"].get("doi"))
        if not a:
            continue
        copy_checked += 1
        aw = words(a)
        grams = {tuple(aw[i:i + 8]) for i in range(len(aw) - 7)}
        for f in ("summary", "caveat"):
            sw = words(rec.get(f) or "")
            hits = [i for i in range(len(sw) - 7) if tuple(sw[i:i + 8]) in grams]
            if hits:
                H(f"copy: {rec['id']} {f} shares an 8-word run with its abstract: '{' '.join(sw[hits[0]:hits[0] + 8])}'")

# ---- report --------------------------------------------------------------------------------------------
st = Counter(r["status"] for r in R)
un = [r for r in current if r["decision"] == "unsure"]
print(f"library {len(R)} records ({st['Provisional']} Provisional, {st['Included']} Included); ledger {len(ROWS)} rows, "
      f"{len(current)} current, {len(un)} unsure; copy-checked {copy_checked} summaries against cached abstracts")
for title, items in (("HARD", hard), ("soft", soft)):
    if items:
        print(f"\n{title} ({len(items)})")
        print("\n".join("  " + m for m in items))
if not hard:
    print("\nno hard problems")
sys.exit(1 if hard else 0)
