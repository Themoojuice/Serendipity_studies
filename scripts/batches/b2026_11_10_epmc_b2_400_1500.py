"""Batch 2026-11-10 (phase 1c): Europe PMC broad set, year-slice batch 2, ranks 400-1,499.

The ranked IDs were already in the ledger (rows with notes 'year-slice batch 2, rank N'), so no reload was
needed: the 1,100 records were fetched by ID from Europe PMC in Brendan's laptop browser
(`/home/claude/work/raw/b2_400_1500.json`, not committed: it holds abstracts). Title screen of all 1,100,
abstract check of 39. Abstract-level appraisal only: every include enters as Provisional.

Each screened record gets a new ledger row superseding its blank batch-2 row (the ledger is append-only).

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_b2_400_1500.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import U, Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-10"
cand = json.loads((RAW / "epmc_b2c_cand.json").read_text())

R = [
    dict(id="ueki-2004", src=802, design="Case series", n=3, cats=["Mood", "Psychotic"], spec="Delusional (psychotic) depression",
         chronic=None, tr=None, tcat="Physiological stress",
         tspec="Incidental delirium: drug-induced in two, respiratory distress with asphyxia in one", intent="Injury or illness",
         res="Complete", rev="None reported", dl=1,
         summary="Three patients' delusional depression resolved after they recovered from an incidental delirium, caused by "
                 "medication in two and by respiratory distress with asphyxia in the third.",
         caveat="Psychotic depression often remits with treatment; the authors also credit amnesia and supportive care, and "
                "chronicity needs the full text.",
         tags=["depression", "psychotic-depression", "delirium", "hypoxia"], tier="B",
         era=("emerging", "Joins older observations that delirium or unplanned seizures can lift depression (an ECT-like "
                          "effect); never tested.")),
    dict(id="tsolaki-2010", src=856, design="Case report", n=1, cats=["Mood"],
         spec="Depression with anxiety, parkinsonism and cognitive decline, unchanged after 9 months of treatment",
         chronic=True, tr=None, tcat="Physiological stress",
         tspec="Suicide attempt with second-degree burns and respiratory compromise, then intensive care",
         intent="Injury or illness", res="Complete", rev="None reported", dl=1,
         summary="Nine months of treatment-unresponsive depression, with parkinsonism and cognitive decline, remitted after a "
                 "suicide attempt with burns and intensive care; still in remission two years later.",
         caveat="The parkinsonism vanished too, which puts the original diagnosis in question; psychosocial change after a "
                "suicide attempt is an alternative explanation.",
         tags=["depression", "suicide-attempt", "burns", "parkinsonism"], tier="C"),
    dict(id="diamond-2006", src=1242, design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
         spec="Tourette syndrome in a 30-year-old man", chronic=True, tr=None, tcat="Brain stimulation",
         tspec="Vagus nerve stimulator implanted for medication-refractory complex partial epilepsy",
         intent="Treatment for another condition", res="Partial", rev="On-off rechallenge", dl=0,
         summary="A man's tics improved after a vagus nerve stimulator was implanted for epilepsy; a rater blinded to whether "
                 "the stimulator was on or off scored fewer motor and vocal tics with it on.",
         caveat="Tics fluctuate, the on/off comparison is a single pair of videos, and better seizure control may contribute.",
         tags=["tourette", "tics", "vagus-nerve-stimulation", "epilepsy", "reversal"], tier="B"),
]

DEC = {802: "ueki-2004", 856: "tsolaki-2010", 1242: "diamond-2006",
       511: (U, "Trichotillomania improved after topical steroid or antibiotic treatment of pseudofolliculitis: off-target, "
                "but size of change and chronicity need the full text (free on PMC)"),
       537: (U, "Letter, no abstract: was amantadine given for extrapyramidal side effects (off-target) or for the psychosis?"),
       605: (U, "Bulimia cured in 6 patients after biliopancreatic diversion; 4 of 6 had BMI under 35, so the surgery may have "
                "been aimed at the bulimia (T1). Needs full text"),
       779: (U, "Scope: persistent genital arousal disorder is not a DSM-5 diagnosis. Varenicline for smoking abolished lifelong "
                "PGAD with repeated off-on; strong attribution if in scope. For Brendan"),
       899: (U, "Scope: two non-verbal children with epileptic encephalopathy spoke after vagus nerve stimulation; include only "
                "if the full text describes a neurodevelopmental syndrome such as autism"),
       1241: (U, "Scope: persistent sexual arousal syndrome remitted when ECT was given for bipolar depression; possibly part "
                 "of the mood episode. For Brendan, with R-rank 779"),
       1330: (U, "Temporal lobe resection in 6 patients with chronic interictal psychosis: 'relative improvement' in 5 with "
                 "psychiatric care; check the full text for individual remissions"),
       518: ("E5", "Letter on observational data about amantadine and gambling in Parkinson's disease"),
       552: ("E3", "Spironolactone given deliberately for residual bipolar symptoms"),
       600: ("E4", "Dopaminergic-drug gambling resolved once DBS allowed a 74% dose cut"),
       657: ("E1", "Neurological syndrome of the trephined"),
       762: ("E1", "Charles Bonnet hallucinations stopped with total blindness; not a psychiatric syndrome"),
       855: ("E1", "Acute post-accident neuropsychiatric symptoms at day 7, not a chronic syndrome"),
       911: ("E3", "ECT given for the depression"),
       973: ("E5", "Open pilot of faecal transplant for Tourette syndrome"),
       995: ("E3", "Faecal transplant given to treat Tourette syndrome"),
       976: ("E4", "Tics secondary to moyamoya ischaemia resolved after revascularisation"),
       1061: ("E3", "Diet adopted to stabilise mood (also excluded in the keto sweep)"),
       1172: ("E4", "Depression secondary to tinnitus; HAM-D fell 48% when the tinnitus was treated"),
       1187: ("E4", "Dopamine dysregulation syndrome resolved with DBS and dopaminergic dose reduction"),
       1215: ("E3", "Limbic pallidal stimulation aimed at the self-injury"),
       1216: ("E4", "Presumed Bartonella infection treated with antibiotics"),
       1230: ("E4", "Presumed streptococcal autoimmune depression treated with penicillin and tonsillectomy"),
       1276: ("E2", "Psychosis emerged with VNS (forced normalisation)"),
       1289: ("E2", "Cochlear implant feasibility; no psychiatric change reported"),
       1424: ("E3", "Post-traumatic OCD improved on treatment"),
       1466: ("E4", "Infection-triggered anorexia nervosa eased with antibiotics"),
       1474: ("E2", "Negative case series: psychosis unchanged after temporal lobectomy and seizure freedom in all 5"),
       1489: ("E3", "Mania treated with lithium and ECT"),
       1493: ("E4", "Post-TBI agitation eased when a painful hip was treated"),
       1338: ("E3", "Methyldopa added deliberately for psychosis in velocardiofacial syndrome"),
       1251: ("E5", "Open pilot of botulinum toxin for depression"),
       1462: ("E3", "Electroshock given for the depression"),
       1275: ("E3", "Cingulotomy performed for the alcohol dependence"),
       }

if __name__ == "__main__":
    added = add_records(R, cand, collection="phase1c", found_via="Europe PMC (v1.2 broad query, year-sliced reload)",
                        today=TODAY)
    L = Ledger(TODAY)
    old = {}
    for r in L.rows:
        if r["query_id"] == "EPMC_broad_v1_2" and "batch 2" in r["notes"]:
            m = re.search(r"rank (\d+)", r["notes"])
            old[int(m.group(1))] = r["record_id"]
    recs = json.loads((RAW / "b2_400_1500.json").read_text())
    for c in recs:
        rk = c["rank"]
        L.add("Europe PMC", "EPMC_broad_v1_2", DEC.get(rk), doi=c["doi"], pmid=c["pmid"], pmcid=c["pmcid"], other=c["key"],
              title=c["title"], au=c["au"], yr=c["year"], jn=c["journal"], lang=c["lang"],
              note=f"year-slice batch 2, rank {rk}; screened 2026-11-10", supersedes=old[rk])
    L.write()
    log_runs([("EPMC_broad_v1_2", "Europe PMC (browser)", "v1.2 broad, year-slice batch 2, ranks 400-1,499 fetched by ID",
               1100, TODAY, "screened (title, 39 abstracts); +3 provisional cases, 7 unsure; gold rank 1467 already in library")])
