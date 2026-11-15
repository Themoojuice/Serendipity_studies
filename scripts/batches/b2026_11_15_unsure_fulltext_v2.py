"""Batch 2026-11-15: full-text appraisal of the unsure pile, part 2 (protocol v1.7.4), through CKN.

With Brendan signed in to CKN, Springer and Ovid (Lippincott journals) load; Elsevier, SAGE (and Liebert, now on SAGE),
Taylor & Francis and Wiley stop at a Cloudflare bot check, and Psychiatry Online asks for terms acceptance. None of
those were worked around: their records stay unsure. Ovid showed abstract pages; the published abstract settled Abe and
Coffey, the Springer full text settled Andreou.

Result: 2 cases (Andreou 2008: metformin for polycystic ovary syndrome, menstrual psychosis largely gone once cycles
became regular; Abe 2016: gabapentin for pain ended Parkinson's visual hallucinations), 1 excluded (Coffey 2013, E4).
Run from the repo root:  python3 scripts/batches/b2026_11_15_unsure_fulltext_v2.py
"""
import csv
import json
import sys

sys.path.insert(0, "scripts")
from lib_add import CASES, LEDGER, Ledger, add_records  # noqa: E402

TODAY = "2026-11-15"
OTHER = "Treatment for another condition"
cand = {
    "andreou-2008": dict(pmid="18827957", pmcid="", doi="10.1007/s00737-008-0032-7",
                         title="Metformine for psychosis associated with the menstrual cycle in a patient with polycystic ovary syndrome.",
                         authorString="Andreou C, Syngelakis M, Karavatos A", journal="Arch Womens Ment Health", year=2008,
                         vol="11", issue="5-6", pages="387-8", lang="eng"),
    "abe-2016": dict(pmid="26757314", pmcid="", doi="10.1097/wnf.0000000000000122",
                     title="A Case of Parkinson Disease With Both Visual Hallucination and Pain Improved by Gabapentin.",
                     authorString="Abe K, Chiba Y, Katsuse O, Hirayasu Y", journal="Clin Neuropharmacol", year=2016, vol="39",
                     issue="1", pages="55-6", lang="eng"),
}
R = [
    dict(id="andreou-2008", src="andreou-2008", design="Case report", n=1, cats=["Psychotic"],
         spec="Menstrual psychosis: manic and psychotic episodes in the days before each period since menarche, only partly "
              "helped by antipsychotics and mood stabilisers, in a young woman with polycystic ovary syndrome",
         chronic=True, tr=True, tcat="Medication for another condition",
         tspec="Metformin 850 mg/day for polycystic ovary syndrome, given because her menstrual dysfunction persisted",
         intent=OTHER, res="Partial", rev="None reported", dl=0,
         summary="A young woman whose manic and psychotic episodes had arrived with her periods since adolescence, barely "
                 "touched by antipsychotics and mood stabilisers, was started on metformin for polycystic ovary syndrome; once "
                 "her cycles became regular, the episodes all but stopped for the following year.",
         caveat="If anovulatory oestrogen swings were driving the episodes, restoring ovulation treated their cause rather than the psychosis.",
         tags=["metformin", "polycystic-ovary-syndrome", "menstrual-psychosis", "oestrogen", "ovulation"], tier="C"),
    dict(id="abe-2016", src="abe-2016", design="Case report", n=1, cats=["Psychotic"],
         spec="Visual hallucinations of insects, felt as painfully invading his body, in an 81-year-old man with advanced "
              "Parkinson's disease, persisting despite standard measures", chronic=None, tr=True,
         tcat="Medication for another condition", tspec="Gabapentin given to ease his pain", intent=OTHER, res="Complete",
         rev="None reported", dl=0,
         summary="An 81-year-old man with advanced Parkinson's disease saw insects that he felt burrowing into him; standard "
                 "measures had failed, and gabapentin given for the pain ended both the pain and the hallucinations.",
         caveat="The pain was part of the hallucinatory experience, so relieving it may have removed what kept the insects coming.",
         tags=["gabapentin", "parkinsons", "visual-hallucinations", "pain", "tactile-hallucinations"], tier="C"),
]
SETTLE = {
    ("R053636",): "andreou-2008",
    ("R060231", "R060323", "R061336", "R064367"): "abe-2016",
    ("R023590",): ("E4", "published abstract (Ovid): self-injury caused by frontal lobe seizures, resolving when phenytoin controlled them"),
}
VIA = {"andreou-2008": "full text read through CKN (Springer)", "abe-2016": "published abstract read through CKN (Ovid)"}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1f", found_via="unsure pile, full-text appraisal", today=TODAY)
    d = json.loads(CASES.read_text())
    for r in d["records"]:
        if r["id"] in VIA:
            r["verified"] = f"{TODAY}: {VIA[r['id']]}; identifiers from PubMed"
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    rows = list(csv.DictReader(LEDGER.open()))
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    by_id = {r["record_id"]: r for r in rows}
    L = Ledger(TODAY)
    n = 0
    for ids, dec in SETTLE.items():
        for rid in ids:
            old = by_id[rid]
            assert old["decision"] == "unsure" and rid not in sup, rid
            row = L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=rid,
                        note=f"was unsure; settled through CKN; {TODAY}")
            row["screen_stage"] = "ft"
            n += 1
    L.write()
    print("settled rows:", n)
