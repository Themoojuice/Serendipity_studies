"""Batch 2026-11-15: antique full-text sweep v1 (protocol v1.7.7).

Europe PMC searches the OCR text of scanned PMC back issues. ANT_FT_v1 (queries/strings_antique_fulltext_v1.json):
recovery phrases ("recovered his reason", "restored to reason", "delusions disappeared", ...) x period syndrome terms,
1800-1950 -> 308 records, 302 new. Most are container sections that a title cannot settle. Five page sets were read
from PMC page images OCR'd locally (Chisholme 1813, Coupland 1898, Kisch 1927, Callam 1941; one 1813 case within):
no case. The rest stay as blank rows to be read later; PMC began challenging repeated article fetches.
Working files: /home/claude/work/raw/ant2_all.json, ant2_match.json; OCR text in /home/claude/work/ocr (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_15_antique_fulltext_v1.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import Ledger, log_runs  # noqa: E402

TODAY = "2026-11-15"
SRC, QID = "Europe PMC", "ANT_FT_v1"
M = json.loads(Path("/home/claude/work/raw/ant2_match.json").read_text())
READ = {
    "PMC2128918": ("E3", "page images read: mercury given for a presumed liver cause of hysterical mania (period standard treatment)"),
    "PMC5253936": ("E4", "page images read: maniacal delirium of pneumonia, clearing as the pneumonia resolved"),
    "PMC2101647": ("E4", "page images read: depression with suicidal threats attributed to sphenoid sinus infection, treated as its cause (focal-infection era)"),
    "PMC2163580": ("E4", "page images read: confusional insanity from the toxaemia of wound infection"),
}

if __name__ == "__main__":
    L = Ledger(TODAY)
    n = {"read": 0, "blank": 0, "already": 0}
    for x in M["all"]:
        key, pmid, pmcid, doi, yr, jn, au, title, pages, vol, iss, kind, blanks, libs, decided = x
        base = dict(doi=doi, pmid=pmid, pmcid=pmcid, other=key, title=title, au=au.rstrip("."), yr=yr, jn=jn, lang="eng")
        if kind == "excluded":
            L.add(SRC, QID, ("", f"decided earlier as {decided}"), **base, note=TODAY)
            n["already"] += 1
        elif pmcid in READ:
            row = L.add(SRC, QID, READ[pmcid], **base, screened=True, note=f"OCR of PMC page images; {TODAY}")
            row["screen_stage"] = "ft"
            n["read"] += 1
        else:
            L.add(SRC, QID, None, **base, screened=False, note=f"antique full-text hit, not yet read; {TODAY}")
            n["blank"] += 1
    L.write()
    print(n)
    log_runs([(QID, SRC, "OCR body-text phrase search of scanned PMC back issues, 1800-1950 (see queries/strings_antique_fulltext_v1.json)",
               308, TODAY, "302 new; 4 read from page images, 0 cases; the rest blank, to be read")])
