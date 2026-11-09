"""Batch 2026-11-10 (themes, v1.3 fix): the left-sided half of the temporal-lobe sweep.

The first temporal sweep (EPMC_temporal_v1, 577 hits) used right-sided terms only. This run adds the
left/dominant terms and keeps only records the first sweep did not return (275), so the two together
are the symmetric set (852). Screened in full. One new case (Ohara 2004); Yeung 2020 was already in.

Adds: library record, the 'Personality' syndrome category, ledger rows, a search-log row, and the
string to queries/strings_themes_v1.json.  Source export (not committed): /home/claude/work/raw/temporal_left.txt

Run from the repo root:  python3 scripts/batches/b2026_11_10_temporal_left.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

DATE = "2026-11-10"

# ---- library ----
P = Path("data/cases.json")
d = json.loads(P.read_text())
if "Personality" not in d["vocabularies"]["syndrome_category"]:
    d["vocabularies"]["syndrome_category"].append("Personality")
if "ohara-2004" not in {r["id"] for r in d["records"]}:
    d["records"].append({
        "id": "ohara-2004", "record_type": "case", "status": "Provisional", "tier": "C", "collections": ["phase1b"],
        "citation": {"authors": "Ohara K, Nishii R, Nakajima T, Kokai M, Morita Y",
                     "title": "[Alterations of symptoms with borderline personality disorder after fronto-temporal traumatic brain injury. A case study].",
                     "journal": "Seishin Shinkeigaku Zasshi", "year": 2004, "volume": "", "issue": "", "pages": ""},
        "ids": {"doi": "", "pmid": "15179796", "pmcid": ""},
        "links": {"full_text": None, "abstract": "https://pubmed.ncbi.nlm.nih.gov/15179796/", "doi": None, "alternates": [], "ckn": None},
        "access": "Paywalled", "design": "Case report", "n_patients": 1,
        "syndrome": {"categories": ["Personality", "Mood"], "specific": "Borderline personality disorder with recurrent self-mutilation for 10 years",
                     "chronic": True, "treatment_resistant": None},
        "trigger": {"category": "Traumatic brain injury", "specific": "Left fronto-temporal injury (orbital and dorsolateral cortex) from a suicide jump",
                    "intent": "Injury or illness"},
        "outcome": {"resolution": "Complete", "time_to_resolution": None, "follow_up": "5 years", "reversal": "None reported"},
        "downstream": {"level": 0, "note": "", "links": []},
        "summary": "Self-mutilation, emptiness and manipulativeness disappeared after a left fronto-temporal brain injury, with 5 years of follow-up.",
        "caveat": "She was left with aphasia and severe executive and memory deficits, so this may be loss of capacity rather than a targeted effect. Published in Japanese; side from the abstract.",
        "tags": sorted(["borderline", "self-harm", "tbi", "frontal", "temporal-lobe", "left-hemisphere", "lesion", "japanese"]),
        "same_patient_as": None, "found_via": "Europe PMC (temporal-lobe sweep, left-sided terms)", "date_added": DATE,
        "verified": f"{DATE}: abstract-level appraisal; identifiers from Europe PMC",
        "era": {"label": "novel", "note": "", "basis": "from downstream level"}, "flags": []})
d["updated"] = DATE
P.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

# ---- query string ----
Q = Path("queries/strings_themes_v1.json")
q = json.loads(Q.read_text())
q["blocks"]["T_left"] = ('TITLE_ABS:("left temporal" OR "left hemisphere" OR "left hemispheric" OR "dominant temporal" '
                         'OR "dominant hemisphere")')
q["queries"]["EPMC_temporal_left_v1_3"] = {"string": "src AND A2 AND T_left AND B2 AND E NOT T_temporal", "hits": 275,
    "note": "The left-sided complement of EPMC_temporal_v1; together they give the symmetric set (852 on 2026-11-10). "
            "T_temporal has no 'non-dominant' terms, so 'dominant' here slightly favours the left."}
q["known_problems"][0] = ("Fixed 2026-11-10 by EPMC_temporal_left_v1_3. T_temporal's neutral terms (lobectomy, epilepsy surgery, "
                          "temporal lesion) already caught both sides.")
Q.write_text(json.dumps(q, indent=1) + "\n")

# ---- ledger ----
LEDGER = Path("ledger/records.csv")
rows = list(csv.DictReader(LEDGER.open()))
cols = list(rows[0].keys())
nid = max(int(r["record_id"][1:]) for r in rows) + 1
by_pmid = {r["ids"]["pmid"]: r["id"] for r in d["records"] if r["ids"]["pmid"]}
DEC = {192: "ohara-2004",
       1: ("E3",), 2: ("E3", "Placebo responder in a drug trial (post-stroke depression)"),
       74: ("E4", "Ictal anorexia (not anorexia nervosa) ended when left hippocampal seizures were ablated; authors note eating disorders in epilepsy are usually non-dominant"),
       155: ("E3",)}
new = []
for l in Path("/home/claude/work/raw/temporal_left.txt").read_text().splitlines()[1:]:
    rank, src, id_, pmid, pmcid, doi, yr, s, t, jn, au = l.split("|")
    rank = int(rank)
    row = {c: "" for c in cols}
    row.update(record_id=f"R{nid:06d}", source_db="Europe PMC", query_id="EPMC_temporal_left_v1_3", retrieved_date=DATE,
               doi=doi.lower(), pmid=pmid, pmcid=pmcid, other_id=f"{src}:{id_}", title=t[:300], first_author=au, year=yr, journal=jn,
               cluster_id=("pmid:" + pmid) if pmid else (("doi:" + doi.lower()) if doi else f"x:{src}:{id_}"),
               notes=f"rank {rank}, score {s}")
    nid += 1
    dec = DEC.get(rank)
    if isinstance(dec, str):
        row.update(screen_stage="ab", decision="included", library_ids=dec)
    elif isinstance(dec, tuple):
        row.update(screen_stage="ab", decision="excluded", reason_code=dec[0], notes=row["notes"] + ("; " + dec[1] if len(dec) > 1 else ""))
    elif pmid in by_pmid:
        row.update(screen_stage="ta", decision="included", library_ids=by_pmid[pmid])
    else:
        row.update(screen_stage="ta", decision="excluded")
    new.append(row)
with LEDGER.open("a", newline="") as f:
    csv.DictWriter(f, fieldnames=cols).writerows(new)
with Path("ledger/search_log.csv").open("a", newline="") as f:
    csv.writer(f).writerow(["EPMC_temporal_left_v1_3", "Europe PMC (browser)",
                            "src AND A2 AND left/dominant temporal block AND B2 AND case design, NOT the first temporal block", 275, DATE,
                            "all screened; +1 case (Ohara 2004); Yeung 2020 already in library"])
print(len(new), "ledger rows;", Counter(r["decision"] for r in new), [r["library_ids"] for r in new if r["library_ids"]])
