"""Batch 2026-11-10 (phase 1c, evening): Europe PMC broad set, stopping-rule checks (protocol section 10).

Samples drawn with seed 20261110 (`queries/stopping_samples_2026_11_10.json`) from the current ledger:
  - first pass: random 300 from the unscreened remainder, ranks 4,000-20,999 (16,999 records)
  - batch 2: ranks 1,500-1,799 in order (300 consecutive), then random 300 from ranks 1,800+ (18,868)
  - batch 3: ranks 60-359 in order (300 consecutive), then random 300 from ranks 360+ (1,080)
Records fetched by ID in the laptop browser (`/home/claude/work/raw/stop.json`, not committed); titles screened,
abstracts checked for 2.

Result:
  - first pass: consecutive criterion met earlier (1,328 since rank 2,671); random sample 1/300 -> FAILS.
    The include (rank 9,842, Makris 2021) scored low because the ranking lexicon lacks unresponsiveness,
    resignation syndrome and functional coma terms.
  - batch 2: 332 consecutive irrelevant since rank 1,467, random sample 0/300 -> both criteria met.
  - batch 3: 300 consecutive (no relevant record anywhere in the queue), random sample 0/300 -> met.
  - Pooled across the two big remainders (1/600 of 35,867), the point estimate is about 60 relevant records left
    (95% interval roughly 2-330): the deep tail is sparse but not empty.

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_stopping.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-10"
recs = json.loads((RAW / "stop.json").read_text())
cand = {"9842": next(dict(r, abs="y") for r in recs if r["grp"] == "fp_sample" and r["rank"] == 9842)}

R = [
    dict(id="makris-2021", src=9842, design="Case report", n=1, cats=["Catatonia", "Functional neurological", "Trauma & stressor-related"],
         spec="Six months of unresponsiveness after witnessing a traumatic event in a refugee child (resignation syndrome, "
              "functional coma or catatonia)", chronic=True, tr=None, tcat="Surgery or procedure (outside the brain)",
         tspec="Neurosurgical release of a tethered spinal cord found during the medical work-up", intent="Treatment for another condition",
         res="Partial", rev="None reported", dl=0,
         summary="A refugee child who had been unresponsive for six months after a traumatic event began responding shortly "
                 "after surgery for a tethered spinal cord.",
         caveat="Resignation syndrome usually lifts slowly with safety and care, which she was also receiving; the authors "
                "leave the cause open; one case.",
         tags=["resignation-syndrome", "functional-coma", "catatonia", "refugee", "child", "tethered-cord", "spinal-surgery"],
         tier="C"),
]

DEC = {("fp_sample", 9842): "makris-2021",
       ("fp_sample", 4120): ("E3", "ECT and lorazepam given for the catatonia"),
       ("b2_consec", 1675): ("E3", "Haemodialysis given to treat schizophrenia (follow-up of Wagemaker and Cade 1977, in library)"),
       ("b2_consec", 1672): ("E3", "Peritoneal dialysis given to treat schizophrenia"),
       ("b2_consec", 1671): ("E5", "Pilot study of haemodialysis for schizophrenia"),
       ("b2_consec", 1677): ("E5", "Double-blind trial of dialysis for schizophrenia")}
PREFIX = {"fp": "rank ", "b2": "year-slice batch 2", "b3": "year-slice batch 3"}
LABEL = {"fp": "first pass", "b2": "year-slice batch 2", "b3": "year-slice batch 3"}

if __name__ == "__main__":
    add_records(R, cand, collection="phase1c", found_via="Europe PMC (v1.2 broad query, stopping-rule random sample)", today=TODAY)
    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    old = {}
    for r in L.rows:
        if r["query_id"] != "EPMC_broad_v1_2" or r["record_id"] in sup or r["decision"]:
            continue
        for q, p in PREFIX.items():
            if r["notes"].startswith(p):
                old[(q, int(re.search(r"rank (\d+)", r["notes"]).group(1)))] = r["record_id"]
    for c in recs:
        q, kind = c["grp"].split("_")
        rk = c["rank"]
        what = "stopping-rule random sample" if kind == "sample" else "stopping-rule consecutive run"
        L.add("Europe PMC", "EPMC_broad_v1_2", DEC.get((c["grp"], rk)), doi=c["doi"], pmid=c["pmid"], pmcid=c["pmcid"],
              other=c["key"], title=c["title"], au=c["au"], yr=c["year"], jn=c["journal"], lang=c["lang"],
              note=f"{LABEL[q]}, rank {rk}; {what} (seed 20261110); screened 2026-11-10", supersedes=old[(q, rk)])
    L.write()
    log_runs([
        ("EPMC_broad_v1_2", "Europe PMC (browser)", "first pass: random 300 of ranks 4,000-20,999 (seed 20261110)", 300, TODAY,
         "stopping check: 1 include (rank 9,842, Makris 2021) -> queue not stopped"),
        ("EPMC_broad_v1_2", "Europe PMC (browser)", "batch 2: ranks 1,500-1,799 + random 300 of ranks 1,800+ (seed 20261110)", 600, TODAY,
         "stopping check: 0 includes; 332 consecutive irrelevant since 1,467 -> both criteria met"),
        ("EPMC_broad_v1_2", "Europe PMC (browser)", "batch 3: ranks 60-359 + random 300 of ranks 360+ (seed 20261110)", 600, TODAY,
         "stopping check: 0 includes -> both criteria met"),
    ])
