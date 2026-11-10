"""Batch 2026-11-10 (phase 1c, night): Europe PMC broad set, re-ranked order ranks 1,000-1,999, plus the
protocol section 10 stopping check on the re-ranked order (v1.3).

Titles from the browser's scored tail (`window.SC`), abstracts for 9 candidates fetched by ID; metadata from a
Europe PMC lite fetch (`/home/claude/work/raw/rr2_batch.json`, not committed).

Stopping check on `queries/rerank_v1_order.csv`:
  - consecutive: last possibly relevant record at new rank 1,622 (Grootendorst-van Mil 2018); ranks 1,623-1,922
    are 300 consecutive irrelevant -> met. Screening continued to 1,999 (nothing further).
  - random: 300 of new ranks 1,600-35,269 (seed 20261111, `queries/stopping_sample_rerank_v1_2026_11_10.json`),
    0 includes -> met.
Both criteria met: the Europe PMC broad first-pass and batch-2 tails are stopped.

Result: +2 cases (Yousefzadeh-Fard 2013, Grootendorst-van Mil 2018).

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_rerank_1000_2000_stop.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-10"
B = json.loads((RAW / "rr2_batch.json").read_text())
rr, lite = B["rr"], B["lite"]          # rr: [new_rank, queue, old_rank, key, score, hasAbs]
cand = {"1435": B["c1435"], "1622": B["c1622"]}
SAMPLE = set(json.loads(Path("queries/stopping_sample_rerank_v1_2026_11_10.json").read_text())["new_ranks"])

R = [
    dict(id="yousefzadeh-fard-2013", src=1435, design="Lesion series", n=None, cats=["Substance & addictive"],
         spec="Opium addiction", chronic=True, tr=None, tcat="Acquired brain lesion",
         tspec="Ischaemic stroke, grouped by site (insula, basal ganglia, other)", intent="Injury or illness",
         res="Partial", rev="None reported", dl=1,
         summary="Among opium-addicted stroke patients in Tehran, 75% of those with insular ischaemia changed how much or "
                 "how they used, and 37.5% stopped, significantly more than with strokes elsewhere.",
         caveat="Questionnaire recall at 1, 3 and 6 months; group sizes and relapse need the full text (free on PMC); "
                "younger patients changed more, which may confound site.",
         tags=["insula", "stroke", "opium", "opioid", "addiction", "lesion-series", "iran"], tier="B",
         era=("emerging", "Extends the insula finding for smoking (Naqvi 2007, in library) to opium; not independently "
                          "replicated for opioids.")),
    dict(id="grootendorst-van-mil-2018", src=1622, design="Case report", n=1, cats=["Psychotic", "Mood"],
         spec="Treatment-resistant schizoaffective disorder, unresponsive to clozapine and ECT", chronic=True, tr=True,
         tcat="Fever / infection", tspec="Pneumonia, with an unintended rise to supratherapeutic clozapine levels",
         intent="Injury or illness", res="Partial", rev="None reported", dl=0,
         summary="Psychosis that had not responded to clozapine or ECT fell markedly and stayed down after pneumonia "
                 "pushed clozapine levels above the usual range.",
         caveat="The authors credit the higher clozapine level; infection and inflammation are the alternative "
                "(compare Zuschlag 2016).",
         tags=["clozapine", "pneumonia", "infection", "schizoaffective", "treatment-resistant", "drug-levels"], tier="C"),
]

DEC = {
    1435: "yousefzadeh-fard-2013", 1622: "grootendorst-van-mil-2018",
    1240: ("E1", "neurological recovery after COVID-19 in dementia and brain injury; no primary psychiatric syndrome"),
    1574: ("E5", "cohort of 97 patients after spinal cord stimulation"),
    1666: ("E2", "chronic interictal psychosis after epilepsy surgery: mixed course, no remission reported"),
    1671: ("E3", "lifestyle programme aimed at the psychiatric symptoms"),
    1965: ("E1", "OCD of one month's duration after streptococcal infection; not chronic"),
    6100: ("E1", "dementia and parkinsonism improved on donepezil"),
}
LABEL = {"fp": "first pass", "b2": "year-slice batch 2"}
PREFIX = {"fp": "rank ", "b2": "year-slice batch 2"}


def first_author(s):
    return (s or "").split(",")[0].strip().rsplit(" ", 1)[0]


if __name__ == "__main__":
    add_records(R, cand, collection="phase1c", found_via="Europe PMC (v1.2 broad query, re-ranked tail v1)", today=TODAY)
    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    old = {}
    for r in L.rows:
        if r["query_id"] != "EPMC_broad_v1_2" or r["record_id"] in sup or r["decision"]:
            continue
        for q, p in PREFIX.items():
            if r["notes"].startswith(p):
                old[(q, int(re.search(r"rank (\d+)", r["notes"]).group(1)))] = r["record_id"]
    n = 0
    for nr, q, rk, key, s, has_abs in rr:
        m = lite[key]
        c = cand.get(str(nr), {})
        what = "stopping-rule random sample (seed 20261111)" if nr in SAMPLE else "re-ranked order"
        L.add("Europe PMC", "EPMC_broad_v1_2", DEC.get(nr), doi=(m["doi"] or "").lower(), pmid=m["pmid"],
              pmcid=m["pmcid"], other=key, title=m["title"], au=first_author(m["au"]), yr=m["yr"], jn=m["jn"],
              lang=c.get("lang", ""),
              note=f"{LABEL[q]}, rank {rk}; rerank_v1 rank {nr}, score {s}; {what}; screened {TODAY}",
              supersedes=old[(q, rk)])
        n += 1
    L.write()
    print("ledger rows:", n)
    log_runs([
        ("EPMC_broad_v1_2", "Europe PMC (browser)", "rerank_v1: new ranks 1,000-1,999", 1000, TODAY,
         "2 includes (ranks 1,435 and 1,622); 300 consecutive irrelevant at 1,623-1,922"),
        ("EPMC_broad_v1_2", "Europe PMC (browser)", "rerank_v1: random 300 of new ranks 1,600-35,269 (seed 20261111)",
         300, TODAY, "stopping check: 0 includes -> both criteria met; first-pass and batch-2 tails stopped"),
    ])
