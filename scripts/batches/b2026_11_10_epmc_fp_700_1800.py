"""Batch 2026-11-10 (phase 1c): Europe PMC broad set, first-pass queue, ranks 700-1,799.

The first pass (21,000 records, cursor paging) was screened to rank 699 on 2026-11-09. Eight library cases
found by other routes sit between ranks 700 and 1,799, so the queue is not exhausted. The 1,100 records were
fetched by ID from the ledger in Brendan's laptop browser (`/home/claude/work/raw/fp_700_1800.json`, not
committed: it holds abstracts). Title screen of all 1,100, abstract check of 27. All eight known cases in the
range were recognised. Abstract-level appraisal only: every include enters as Provisional.

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_fp_700_1800.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import U, Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-10"
cand = json.loads((RAW / "fp_cand.json").read_text())

DELIRIUM = ("emerging", "Joins older observations that an incidental delirium, like ECT or insulin coma, can precede "
                        "recovery (Malur 2000; Ueki 2004); never tested.")
AMYGDALA = "Fits the right-amygdala account of PTSD and Koenigs 2008 (amygdala and vmPFC lesions protected veterans from PTSD)."

R = [
    dict(id="bijanki-2020", src=822, design="Case series", n=2, cats=["Trauma & stressor-related"],
         spec="Well-documented chronic PTSD, predating late-onset epilepsy", chronic=True, tr=None, tcat="Neurosurgery",
         tspec="Laser ablation of the right (non-dominant) amygdalohippocampal complex for medically refractory temporal lobe epilepsy",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
         summary="Two people with long-standing PTSD had right amygdala laser ablation for epilepsy; both lost most of their "
                 "PTSD symptoms, and in one, startle potentiation and fMRI fear responses fell too.",
         caveat="Seizure control improved at the same time; two patients, one with prospective biomarkers.",
         tags=["ptsd", "amygdala", "temporal", "right-hemisphere", "epilepsy-surgery", "laser-ablation"], tier="B",
         era=("emerging", AMYGDALA + " Xie 2026 replicated it.")),
    dict(id="xie-2026", src=781, design="Case report", n=1, cats=["Trauma & stressor-related"],
         spec="Chronic PTSD with refractory epilepsy", chronic=True, tr=None, tcat="Neurosurgery",
         tspec="SEEG-guided radiofrequency ablation of the right amygdala in a patient with refractory epilepsy",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
         summary="PTSD symptoms and negative interpretation bias fell right after right amygdala ablation in a man with "
                 "epilepsy, while seizure frequency stayed the same; intracranial recordings tracked the change.",
         caveat="A replication of Bijanki 2020 with a prospective design, so the effect was anticipated by the team; n of 1.",
         tags=["ptsd", "amygdala", "temporal", "right-hemisphere", "epilepsy-surgery", "radiofrequency-ablation", "replication"],
         tier="B", era=("emerging", "Replicates Bijanki 2020. " + AMYGDALA)),
    dict(id="gillespie-2019", src=827, design="Case report", n=1, cats=["Psychotic"],
         spec="Long-standing organic delusional disorder (congenital hydrocephalus, cerebral palsy) needing psychiatric admission",
         chronic=True, tr=None, tcat="Fever / infection",
         tspec="Iatrogenic cerebral abscess after an intracranial pressure monitor, treated with 6 weeks of IV meropenem",
         intent="Injury or illness", res="Complete", rev="None reported", dl=1,
         summary="A woman with long-standing delusional disorder developed a brain abscess from a pressure monitor; after six "
                 "weeks of meropenem her delusions and hallucinations went and she now lives independently.",
         caveat="The abscess, the neurosurgery and the antibiotic cannot be separated; follow-up length needs the full text (free on PMC).",
         tags=["delusional-disorder", "psychosis", "cerebral-abscess", "infection", "antibiotic", "meropenem"], tier="B",
         era=("emerging", "Joins older reports of psychosis remitting after brain infection, fever or antibiotics.")),
    dict(id="malur-2000", src=1472, design="Case series", n=5, cats=["Psychotic", "Mood"],
         spec="Exacerbations of chronic major mental illness with psychotic and affective symptoms (inpatients aged 53-69)",
         chronic=True, tr=None, tcat="Physiological stress",
         tspec="Incidental delirium from medication (4) or electrolyte disturbance (1)", intent="Injury or illness",
         res="Temporary", rev="None reported", dl=1,
         summary="In five older inpatients, psychotic and affective symptoms improved or resolved as an incidental delirium "
                 "from drugs or electrolytes cleared; the benefit lasted 1 to 5 months.",
         caveat="Exacerbations often settle in hospital, and medications were washed out during the delirium.",
         tags=["psychosis", "depression", "delirium"], tier="C", era=DELIRIUM),
    dict(id="baek-2022", src=805, design="Case report", n=1, cats=["Psychotic"],
         spec="Schizophrenia for 2 years with residual psychotic symptoms despite adequate treatment", chronic=True, tr=None,
         tcat="Medication for another condition",
         tspec="Donepezil for cognitive impairment from delayed neurological sequelae of carbon monoxide poisoning",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=0,
         summary="Donepezil, given for cognitive damage after carbon monoxide poisoning, also markedly improved a man's "
                 "residual schizophrenic hallucinations.",
         caveat="Carbon monoxide injury to the pallidum may itself ease psychosis (compare Galati 2013), and the delayed "
                "sequelae were recovering; one case.",
         tags=["schizophrenia", "donepezil", "carbon-monoxide", "cholinergic"], tier="C",
         era=("novel", "Cholinesterase inhibitor trials in schizophrenia targeted cognition and were negative; no test in this setting.")),
    dict(id="solmi-2013", src=858, design="Case report", n=1, cats=["Eating"],
         spec="Long-lasting anorexia nervosa in a 26-year-old woman", chronic=True, tr=None,
         tcat="Medication for another condition", tspec="Infliximab for 4 months, then adalimumab, for Crohn's disease",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=0,
         summary="Long-lasting anorexia nervosa improved in weight and psychopathology over the months a woman received "
                 "anti-TNF therapy for Crohn's disease.",
         caveat="She was referred to an eating disorders unit at the same time, and better bowel control alone could aid weight gain.",
         tags=["anorexia", "anti-tnf", "infliximab", "adalimumab", "crohns"], tier="C"),
    dict(id="choo-2024", src=1439, design="Case report", n=1, cats=["Mood"], spec="Bipolar disorder, manic relapse",
         chronic=None, tr=None, tcat="Medication for another condition", tspec="Metformin (indication not given in the title)",
         intent="Treatment for another condition", res="Complete", rev="Natural off-on", dl=1,
         summary="Mania relapsed after metformin was stopped and resolved when it was restarted.",
         caveat="Title-level appraisal (no abstract); concurrent psychiatric treatment and the metformin indication need the full text.",
         tags=["bipolar", "mania", "metformin", "insulin-resistance", "reversal"], tier="C",
         era=("emerging", "Fits proposals linking insulin resistance to treatment-resistant bipolar disorder (Calkin and colleagues).")),
    dict(id="romeo-2025", src=1709, design="Case report", n=1, cats=["Substance & addictive"],
         spec="Cocaine use disorder with obesity in a 54-year-old", chronic=None, tr=None,
         tcat="Medication for another condition", tspec="Semaglutide for obesity, titrated over 12 weeks",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
         summary="Cocaine craving fell markedly over 12 weeks of semaglutide given for obesity.",
         caveat="Craving rather than verified abstinence; short follow-up and a single author.",
         tags=["cocaine", "semaglutide", "glp-1", "craving"], tier="C"),
]

DEC = {822: "bijanki-2020", 781: "xie-2026", 827: "gillespie-2019", 1472: "malur-2000", 805: "baek-2022", 858: "solmi-2013",
       1439: "choo-2024", 1709: "romeo-2025",
       846: (U, "Letter, no abstract: was intravenous dopamine given for hypotension (off-target) or for the depression?"),
       1094: (U, "Letter, no abstract: likely a participant in the authors' metformin trial (then E5); check"),
       709: ("E4", "First-episode psychosis secondary to an arachnoid cyst remitted after its removal"),
       835: ("E3", "Self-directed regimen aimed at the depression"),
       856: ("E4", "Contraceptive-induced depression remitted when stopped"),
       878: ("E2", "Weight gain from BMI 10.9 to 12.9 after a life-threatening illness; not remission"),
       1279: ("E3", "DBS given for Tourette syndrome; benefit persisted after removal"),
       1292: ("E3", "Psychological therapy aimed at the psychotic symptoms"),
       1304: ("E2", "Psychiatric disorders emerging after epilepsy surgery"),
       1378: ("E3", "Snake venom taken to curb drinking; no remission"),
       1424: ("E3", "ECT given for the psychosis and catatonia"),
       1435: ("E4", "Acute haloperidol-induced catatonia improved during dialysis"),
       1584: ("E4", "Tirzepatide-induced anhedonia resolved with dose change"),
       1585: ("E5", "Single-case experimental design testing tirzepatide after CBT for binge eating"),
       1586: ("E2", "Mania emerged during liraglutide-assisted weight loss"),
       1660: ("E3", "Psychiatric treatment aimed at weight gain"),
       1694: ("E3", "Combined oral contraceptive added deliberately for menstrual psychosis"),
       1711: ("E3", "Rituximab given for presumed autoimmune OCD"),
       1743: ("E4", "Impulse control disorders improved after DBS allowed dopaminergic dose reduction"),
       }

if __name__ == "__main__":
    add_records(R, cand, collection="phase1c", found_via="Europe PMC (v1.2 broad query, first pass)", today=TODAY)
    L = Ledger(TODAY)
    old = {}
    for r in L.rows:
        if r["query_id"] == "EPMC_broad_v1_2" and r["notes"].startswith("rank "):
            old[int(re.search(r"rank (\d+)", r["notes"]).group(1))] = r["record_id"]
    for c in json.loads((RAW / "fp_700_1800.json").read_text()):
        rk = c["rank"]
        L.add("Europe PMC", "EPMC_broad_v1_2", DEC.get(rk), doi=c["doi"], pmid=c["pmid"], pmcid=c["pmcid"], other=c["key"],
              title=c["title"], au=c["au"], yr=c["year"], jn=c["journal"], lang=c["lang"],
              note=f"first pass, rank {rk}; screened 2026-11-10", supersedes=old[rk])
    L.write()
    log_runs([("EPMC_broad_v1_2", "Europe PMC (browser)", "v1.2 broad, first-pass queue, ranks 700-1,799 fetched by ID",
               1100, TODAY, "screened (title, 27 abstracts); +8 provisional cases, 2 unsure; all 8 known cases in range recognised")])
