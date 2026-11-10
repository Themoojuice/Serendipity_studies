"""Batch 2026-11-10 (phase 1c, evening): Europe PMC broad set, first-pass queue, ranks 2,900-3,999.

Queue read in the browser straight from the committed ledger (current rows with a blank decision), records
fetched by ID (`/home/claude/work/raw/fp3.json`, not committed). Title screen of all 1,100 (almost entirely
score-4 cohort studies), abstract check of 6. No includes: with the last relevant record at rank 2,671, ranks
2,672-3,999 give 1,328 consecutive irrelevant records, meeting the first half of the stopping rule.

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_fp_2900_4000.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import Ledger, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-10"
DEC = {2902: ("E4", "Delusions in hypopituitarism resolved with growth hormone replacement"),
       3970: ("E2", "Pregabalin augmented response in an acute early-onset episode; not resolution of a chronic syndrome"),
       3453: ("E2", "Brain abscess after self-trephination; psychosis managed with antipsychotics, no remission reported"),
       3171: ("E3", "Psychotic depression improved with medication changes and ECT")}

if __name__ == "__main__":
    L = Ledger(TODAY)
    old = {int(re.search(r"rank (\d+)", r["notes"]).group(1)): r["record_id"] for r in L.rows
           if r["query_id"] == "EPMC_broad_v1_2" and r["notes"].startswith("rank ")}
    for c in json.loads((RAW / "fp3.json").read_text()):
        rk = c["rank"]
        L.add("Europe PMC", "EPMC_broad_v1_2", DEC.get(rk), doi=c["doi"], pmid=c["pmid"], pmcid=c["pmcid"], other=c["key"],
              title=c["title"], au=c["au"], yr=c["year"], jn=c["journal"], lang=c["lang"],
              note=f"first pass, rank {rk}; screened 2026-11-10", supersedes=old[rk])
    L.write()
    log_runs([("EPMC_broad_v1_2", "Europe PMC (browser)", "v1.2 broad, first-pass queue, ranks 2,900-3,999 fetched by ID",
               1100, TODAY, "screened (title, 6 abstracts); no includes; 1,328 consecutive irrelevant since rank 2,671")])
