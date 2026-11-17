"""Write docs/fulltext_queue.md: every case not yet fully coded, grouped by how its full text can be reached.
Run from the repo root after a coding batch:  python3 scripts/make_fulltext_queue.py
"""
import json
from pathlib import Path

d = json.loads(Path("data/cases.json").read_text())
H = {e["case_id"] for e in json.loads(Path("data/hypotheses.json").read_text())["entries"]}
cases = [r for r in d["records"] if r["record_type"] == "case"]
todo = [r for r in cases if r["id"] not in H]

# Free copies that exist but sit behind a bot check or sign-up in the app's browser (2026-11-17); one click in a normal browser
EASY = {
    "klok-2025": "Edinburgh repository PDF (Cloudflare check in the app's browser)",
    "mira-2024": "HAL copy: hal.science/hal-04741916 (bot check in the app's browser)",
    "kalenderoglu-2011": "Türkiye Klinikleri PDF (Cloudflare check)",
    "de-filippis-2026": "Preprints.org (bot check)",
    "sair-2018": "Open access at Psychiatry and Clinical Psychopharmacology (site refused the app's browser)",
    "tsang-2023": "Open access at East Asian Archives of Psychiatry (site refused the app's browser)",
    "berner-2008": "Free PDF at psychiatrist.com after a free account",
    "richards-2024": "Free PDF at psychiatrist.com after a free account",
    "dusoir-2005": "PMC scanned PDF (proof-of-work check in the app's browser)",
    "wagner-jauregg-1883": "PMC page scans, 17 pages (long; left for a dedicated read)",
    "nagata-2013": "Cambridge abstract only; letter",
}
ROUTES = [
    ("CKN, Ovid / Lippincott (works once signed in)", ("10.1097/",)),
    ("CKN, Springer (works once signed in)", ("10.1007/",)),
    ("Download the PDF yourself (Elsevier: Cloudflare in the app's browser)", ("10.1016/",)),
    ("Download the PDF yourself (Wiley)", ("10.1002/", "10.1111/", "10.1046/")),
    ("Download the PDF yourself (SAGE / Mary Ann Liebert)", ("10.1177/", "10.1089/")),
    ("Download the PDF yourself (Taylor & Francis / Informa)", ("10.1080/", "10.3109/")),
    ("Psychiatry Online (tick the terms box)", ("10.1176/",)),
    ("Physicians Postgraduate Press (psychiatrist.com)", ("10.4088/",)),
    ("Thieme / Karger / AMA / AAN / BMJ / JNS / other", ("10.1055/", "10.1159/", "10.1001/", "10.1212/", "10.1136/", "10.3171/", "10.1161/", "10.1053/", "10.1227/", "10.2190/", "10.1192/", "10.1017/")),
]

def line(r):
    c = r["citation"]
    au = (c.get("authors") or [c.get("first_author", "")])[0] if isinstance(c.get("authors"), list) else c.get("first_author", "")
    doi = r["ids"].get("doi")
    links = []
    if r["links"].get("ckn"): links.append(f"[CKN]({r['links']['ckn']})")
    if doi: links.append(f"[DOI](https://doi.org/{doi})")
    if r["links"].get("abstract"): links.append(f"[PubMed]({r['links']['abstract']})")
    return f"- **{r['id']}** · tier {r['tier']} · {c['title']} ({c.get('journal', '')} {c.get('year', '')}) · " + " · ".join(links)

out = ["# Full texts still needed", "",
       f"{len(todo)} of {len(cases)} cases aren't fully coded yet because their full text couldn't be reached from this session "
       "(written by `scripts/make_fulltext_queue.py`). Each needs a read and a coding batch (`protocol/SCHEMA.md` §7). "
       "Easy wins first: free copies that only a bot check stood in front of.", ""]
done = set()
easy = [r for r in todo if r["id"] in EASY]
if easy:
    out += [f"## Easy wins: free, one click in a normal browser ({len(easy)})", ""]
    out += [line(r) + f" · *{EASY[r['id']]}*" for r in sorted(easy, key=lambda r: r["tier"])] + [""]
    done |= {r["id"] for r in easy}
for title, prefixes in ROUTES:
    rs = [r for r in todo if r["id"] not in done and (r["ids"].get("doi") or "").lower().startswith(prefixes)]
    if not rs: continue
    out += [f"## {title} ({len(rs)})", ""] + [line(r) for r in sorted(rs, key=lambda r: (r["tier"], r["id"]))] + [""]
    done |= {r["id"] for r in rs}
rest = [r for r in todo if r["id"] not in done]
nodoi = [r for r in rest if not r["ids"].get("doi")]
other = [r for r in rest if r["ids"].get("doi")]
if other:
    out += [f"## Other publishers ({len(other)})", ""] + [line(r) for r in sorted(other, key=lambda r: (r["tier"], r["id"]))] + [""]
if nodoi:
    out += [f"## No DOI: older or non-indexed papers, library or interlibrary loan ({len(nodoi)})", ""] + [line(r) for r in sorted(nodoi, key=lambda r: (r["tier"], r["id"]))] + [""]
Path("docs/fulltext_queue.md").write_text("\n".join(out) + "\n")
print(f"{len(todo)} cases listed")
