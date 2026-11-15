"""Batch 2026-11-15: full-text appraisal of the unsure pile, part 1 (protocol v1.7.4).

53 unsure records (61 current unsure rows). Part 1 settles those whose full text is free: Europe PMC fullTextXML (open
access), psychiatrist.com (Primary Care Companion letters are free) and the PMC author manuscript of Teye-Botchway 2023.
Scanned 19th-century PMC pages are behind a proof-of-work bot check on PMC and a 520 error on Europe PMC's renderer:
left unsure rather than worked around.

Each settled unsure row gets a correction row (same source fields, `supersedes` = the unsure row, screen_stage `ft`).
Result: 1 case (Ray 2016: a single ketamine infusion for neck pain, then sustained remission of refractory panic
disorder, agoraphobia and GAD), 7 excluded.
Run from the repo root:  python3 scripts/batches/b2026_11_15_unsure_fulltext_v1.py
"""
import csv
import json
import sys

sys.path.insert(0, "scripts")
from lib_add import CASES, LEDGER, Ledger, add_records  # noqa: E402

TODAY = "2026-11-15"
OTHER = "Treatment for another condition"

cand = {
    "ray-2016": dict(pmid="27828703", pmcid="", doi="10.4088/pcc.15l01899",
                     title="Sustained Resolution of Panic Disorder, Agoraphobia, and Generalized Anxiety Disorder With a Single Ketamine Infusion: A Case Report.",
                     authorString="Ray SM, Kious BM", journal="Prim Care Companion CNS Disord", year=2016, vol="18", issue="4",
                     pages="15l01899", lang="eng"),
}
R = [
    dict(id="ray-2016", src="ray-2016", design="Case report", n=1, cats=["Anxiety"],
         spec="Treatment-refractory panic disorder, agoraphobia and generalised anxiety disorder (with major depression) in a "
              "34-year-old woman, largely housebound despite escitalopram, lamotrigine and ECT",
         chronic=True, tr=True, tcat="Medication for another condition",
         tspec="A single 0.5 mg/kg ketamine infusion given in the emergency department for neck pain from herniated discs",
         intent=OTHER, res="Complete", rev="None reported", dl=1,
         era=("emerging", "Ketamine's antidepressant effect was established by 2016; its effect on panic and agoraphobia was "
                          "unreported at the time (the authors' search found nothing)."),
         summary="A 34-year-old woman, housebound for years by panic disorder and agoraphobia that escitalopram, lamotrigine and "
                 "ECT had barely touched, was given one ketamine infusion in the emergency department for neck pain; her panic "
                 "attacks stopped, she began going out alone and started a business, and the remission was still holding months later.",
         caveat="Her questionnaire scores were already low before the infusion, so the change was mostly behavioural, and "
                "months of ECT and lamotrigine may have been building towards it.",
         tags=["ketamine", "panic-disorder", "agoraphobia", "generalised-anxiety", "analgesia", "emergency-department"], tier="C"),
]
# unsure record_id(s) -> new decision (library id, or (code, note)); all from full text
SETTLE = {
    ("R000785",): "ray-2016",
    ("R022470",): ("E3", "full text: topiramate and aripiprazole were prescribed to control his tobacco consumption"),
    ("R059916",): ("E3", "full text: duloxetine was started deliberately to test it on the tics"),
    ("R047296",): ("E4", "full text: pulling was kept going by pseudofolliculitis itch, treated as part of trichotillomania care"),
    ("R062731",): ("E2", "full text: weight did not improve after the SMA-syndrome surgery; recovery came with inpatient eating-disorder treatment"),
    ("R059917", "R059918"): ("E3", "full text: tDCS was aimed at the refractory hallucinations; the incidental effect was on clozapine hypersalivation"),
    ("R061787", "R062476"): ("E3", "full text: one EMDR session aimed at newly disclosed incest memories, offered by the treating team "
                                   "with trauma-focused therapy for psychosis in view; complete remission off clozapine for 18 months is "
                                   "striking, but the treatment was psychiatric care directed at his psychopathology"),
    ("R058693",): ("E7", "full text (PMC author manuscript): perspective piece, no new patient data"),
}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1f", found_via="unsure pile, full-text appraisal", today=TODAY)
    d = json.loads(CASES.read_text())
    for r in d["records"]:
        if r["id"] == "ray-2016":
            r["verified"] = f"{TODAY}: full text read (psychiatrist.com, free); identifiers from PubMed"
            r["access"] = "Free full text"
            r["links"]["full_text"] = "https://www.psychiatrist.com/pcc/resolution-of-panic-disorder-with-ketamine/"
            r["outcome"]["time_to_resolution"] = "days"
            r["outcome"]["follow_up"] = "at least 10 weeks, still in remission after a car accident 2 months later"
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
                        note=f"was unsure; settled from the full text; {TODAY}")
            row["screen_stage"] = "ft"
            n += 1
    L.write()
    print("settled rows:", n)
