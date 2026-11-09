"""Batch 2026-11-10 (phase 1c): Europe PMC broad set, first-pass queue, ranks 1,800-2,899.

Same method as ranks 700-1,799 (see b2026_11_10_epmc_fp_700_1800.py): 1,100 records fetched by ID in the
laptop browser (`/home/claude/work/raw/fp2.json`, not committed). Title screen of all 1,100, abstract check of
20. All four library cases in the range (Hefzy 2011, Barbieri 2005, Fontaine 2004, Mallet 2002) were recognised.

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_fp_1800_2900.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import U, Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-10"
cand = json.loads((RAW / "fp2_cand.json").read_text())
EPI = ("emerging", "Psychiatric gains after epilepsy surgery are reported but inconsistent: Reutens 1997 found chronic "
                   "interictal psychosis unchanged, and seizure control is a confound (see Pintor 2022).")

R = [
    dict(id="basheikh-2017", src=2361, design="Case report", n=1,
         cats=["Trauma & stressor-related", "Mood", "Functional neurological"],
         spec="PTSD and depression with psychogenic non-epileptic seizures, alongside drug-resistant epilepsy", chronic=None,
         tr=None, tcat="Neurosurgery", tspec="Right anterior temporal resection for right mesial temporal sclerosis",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
         summary="After a right anterior temporal resection for epilepsy, a man's non-epileptic seizures stopped along with "
                 "his epileptic ones, and his PTSD and depression improved enough to cut his psychotropics.",
         caveat="Seizure freedom itself relieves distress; 'remarkable improvement' needs measures from the full text (free on PMC).",
         tags=["ptsd", "depression", "pnes", "temporal", "right-hemisphere", "epilepsy-surgery"], tier="C", era=EPI),
    dict(id="shahani-2019", src=2288, design="Case report", n=1, cats=["Psychotic", "Mood"],
         spec="Psychosis, depression and irritability needing antipsychotics, with refractory temporal lobe epilepsy",
         chronic=True, tr=None, tcat="Neurosurgery", tspec="Anterior temporal lobectomy and amygdalohippocampectomy for epilepsy",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
         summary="A woman's psychosis, depression and irritability improved along with her seizures after anterior temporal "
                 "lobectomy and amygdalohippocampectomy.",
         caveat="Psychosis of epilepsy may simply follow seizure control; side of surgery and measures need the full text (free on PMC).",
         tags=["psychosis", "depression", "temporal", "epilepsy-surgery", "amygdala"], tier="C", era=EPI),
    dict(id="hamdani-2013", src=2542, design="Case report", n=1, cats=["Mood"],
         spec="Severe manic episode of bipolar disorder, unresolved by standard treatment", chronic=None, tr=True,
         tcat="Medication for another condition", tspec="Two anthelmintics for Wuchereria bancrofti filariasis, found through eosinophilia",
         intent="Treatment for another condition", res="Complete", rev="None reported", dl=0,
         summary="A treatment-resistant manic episode resolved after anthelmintic treatment for filariasis found by chance "
                 "through eosinophilia; psychotropics were unchanged.",
         caveat="The infection may have been driving the episode (then E4); one case from a group researching infection in bipolar disorder.",
         tags=["bipolar", "mania", "filariasis", "anthelmintic", "infection", "immune"], tier="C"),
]

DEC = {2361: "basheikh-2017", 2288: "shahani-2019", 2542: "hamdani-2013",
       2072: (U, "Bulimia nervosa with COVID-related smell and taste loss: abstract does not say whether bingeing changed"),
       1837: ("E1", "Neurological outcome after prolonged CPR"),
       1921: ("E2", "Parkinsonism improved after DBS; schizophrenia not reported to change"),
       2244: ("E2", "Schizophrenia already in remission before bariatric surgery"),
       2306: ("E4", "Zolpidem-induced sleep-related eating stopped with zolpidem"),
       2381: ("E3", "Levetiracetam given for epileptiform discharges presumed to drive the psychosis"),
       2455: ("E3", "ECT given for withdrawal delirium and craving"),
       2473: ("E4", "Tacrolimus-associated anorexia nervosa resolved on switching to cyclosporine"),
       2487: ("E4", "Dopamine agonist-induced delusional jealousy resolved on withdrawal"),
       2509: ("E2", "Renal transplant feasibility; psychosis continued"),
       2527: ("E2", "Negative case: schizophrenia persisted after 8 months of gluten-free diet with coeliac remission"),
       2535: ("E3", "Deliberate NAc DBS series following the Kuhn 2007 accidental observation (in library)"),
       2593: ("E3", "Weight restored by eating disorder treatment"),
       2606: ("E3", "Minocycline given for methamphetamine psychosis"),
       2649: ("E2", "Imaging case; no psychiatric change"),
       2656: ("E4", "Dopamine dysregulation syndrome abolished with DBS and dopaminergic reduction"),
       2754: ("E4", "Rituximab for a presumed lupus-related neuropsychiatric process"),
       }

if __name__ == "__main__":
    add_records(R, cand, collection="phase1c", found_via="Europe PMC (v1.2 broad query, first pass)", today=TODAY)
    L = Ledger(TODAY)
    old = {int(re.search(r"rank (\d+)", r["notes"]).group(1)): r["record_id"] for r in L.rows
           if r["query_id"] == "EPMC_broad_v1_2" and r["notes"].startswith("rank ")}
    for c in json.loads((RAW / "fp2.json").read_text()):
        rk = c["rank"]
        L.add("Europe PMC", "EPMC_broad_v1_2", DEC.get(rk), doi=c["doi"], pmid=c["pmid"], pmcid=c["pmcid"], other=c["key"],
              title=c["title"], au=c["au"], yr=c["year"], jn=c["journal"], lang=c["lang"],
              note=f"first pass, rank {rk}; screened 2026-11-10", supersedes=old[rk])
    L.write()
    log_runs([("EPMC_broad_v1_2", "Europe PMC (browser)", "v1.2 broad, first-pass queue, ranks 1,800-2,899 fetched by ID",
               1100, TODAY, "screened (title, 20 abstracts); +3 provisional cases, 1 unsure; all 4 known cases in range recognised")])
