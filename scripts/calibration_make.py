"""Build the blinded calibration set (protocol §10: Brendan screens 100 records from step 1.1, blind; target kappa >= 0.7).

Frame: every Europe PMC broad-query record (EPMC_broad_v1_2, step 1.1) with a title/abstract screening decision, taken
at its FIRST decision (the screening call, before any full-text correction).

A simple random 100 would hold about one include (1.3% prevalence), so kappa would be meaningless. The sample is
stratified and enriched; calibration_score.py reports kappa both on the sample as drawn and re-weighted to the frame
(inverse sampling fractions).

  INC   screened in (included at title/abstract)                       25
  UNS   unsure at title/abstract                                       10
  ABX   excluded after reading the abstract (a reason code was given)  25
  TOPX  excluded on title, high in the ranked order (rank < 500)       25
  RNDX  every other exclusion, at random                               15

Writes queries/calibration_v1_sample.json (what the page shows: IDs and citation only, shuffled, no decisions or
strata) and queries/calibration_v1_key.json (Claude's calls, read by the page only after the last record).
Run from the repo root:  python3 scripts/calibration_make.py
"""
import csv
import json
import random
import re
from pathlib import Path

SEED = 20261121
SIZES = {"INC": 25, "UNS": 10, "ABX": 25, "TOPX": 25, "RNDX": 15}


def rank_of(notes):
    m = re.search(r"rerank_v1 rank (\d+)", notes)
    if m:
        return int(m.group(1))
    m = re.match(r"(?:first pass, |year-slice batch \d, )?rank (\d+)", notes)
    return int(m.group(1)) if m else 10**9


def main():
    rows = list(csv.DictReader(Path("ledger/records.csv").open()))
    first = {}
    for r in rows:
        if r["query_id"] == "EPMC_broad_v1_2" and r["screen_stage"] in ("ta", "ab") and r["decision"]:
            first.setdefault(r["other_id"], r)
    frame = {"INC": [], "UNS": [], "ABX": [], "TOPX": [], "RNDX": []}
    for r in first.values():
        if r["decision"] == "included":
            frame["INC"].append(r)
        elif r["decision"] == "unsure":
            frame["UNS"].append(r)
        elif r["reason_code"]:
            frame["ABX"].append(r)
        elif rank_of(r["notes"]) < 500:
            frame["TOPX"].append(r)
        else:
            frame["RNDX"].append(r)
    rng = random.Random(SEED)
    picked = []
    for s, n in SIZES.items():
        pool = sorted(frame[s], key=lambda r: r["record_id"])
        picked += [(s, r) for r in rng.sample(pool, n)]
    rng.shuffle(picked)
    sample, key = [], []
    for i, (s, r) in enumerate(picked):
        src, ext = r["other_id"].split(":", 1)
        sample.append({"i": i, "src": src, "id": ext, "title": r["title"], "au": r["first_author"], "jn": r["journal"],
                       "yr": r["year"], "doi": r["doi"], "pmid": r["pmid"]})
        key.append({"i": i, "record_id": r["record_id"], "stratum": s, "decision": r["decision"], "stage": r["screen_stage"],
                    "reason": r["reason_code"], "library_ids": r["library_ids"], "note": r["notes"]})
    meta = {"set": "calibration_v1", "made": "2026-11-21", "seed": SEED, "frame_query": "EPMC_broad_v1_2",
            "frame_sizes": {s: len(v) for s, v in frame.items()}, "sample_sizes": SIZES}
    Path("queries/calibration_v1_sample.json").write_text(json.dumps({"meta": {"set": meta["set"], "n": len(sample)},
                                                                      "records": sample}, ensure_ascii=False, indent=1) + "\n")
    Path("queries/calibration_v1_key.json").write_text(json.dumps({"meta": meta, "key": key}, ensure_ascii=False, indent=1) + "\n")
    print(meta["frame_sizes"], len(sample))


if __name__ == "__main__":
    main()
