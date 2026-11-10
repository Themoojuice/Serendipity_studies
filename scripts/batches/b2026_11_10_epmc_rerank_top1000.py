"""Batch 2026-11-10 (phase 1c, night): Europe PMC broad set, top 1,000 of the re-ranked tail (protocol v1.3).

The unscreened tail of the first-pass and batch-2 queues (35,270 records) was scored with the classifier in
`queries/rerank_model_v1.json` and sorted (`queries/rerank_v1_order.csv`). Titles of the top 1,000 were screened;
abstracts of 43 candidates were fetched by ID in the laptop browser (`/home/claude/work/raw/rr_cand_abs.json`,
not committed). Bibliographic fields for the other rows come from a Europe PMC lite fetch (`rr_lite.json`).

Held-out library cases in this order: Kraft & Westman 2009 at 1 (was 6,182), Solyom 1987 at 354 (was 7,808);
both already decided, so no new rows. O'Hara 2004 (rank 0) was in the library but blank here; now matched.

Result: 6 new cases, 5 unsure, 37 excluded at abstract level, the rest excluded at title level.
Two records excluded earlier in the temporal theme sweep (EPMC_temporal_v1) are corrected to included,
and one in the left-temporal sweep to unsure.

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_rerank_top1000.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import U, Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-10"
top = json.loads((RAW / "rr_top1000.json").read_text())       # [new_rank, queue, old_rank, key, score, hasAbs, pt, title]
lite = json.loads((RAW / "rr_lite.json").read_text())         # key -> pmid, pmcid, doi, title, au, jn, yr
core = {r["nr"]: r for r in json.loads((RAW / "rr_cand_abs.json").read_text())}
cand = {str(n): r for n, r in core.items()}

EPI_NOTE = ("Psychiatric gains after epilepsy surgery are reported but inconsistent, and seizure control is a "
            "confound (see Pintor 2022).")

R = [
    dict(id="zuschlag-2016", src=78, design="Case report", n=1, cats=["Psychotic"],
         spec="Schizoaffective disorder with severe psychotic symptoms", chronic=True, tr=None,
         tcat="Fever / infection", tspec="Bacteraemia with high fever", intent="Injury or illness",
         res="Complete", rev="None reported", dl=1,
         summary="A woman with schizoaffective disorder and severe psychosis had a striking remission of psychotic "
                 "symptoms after a bacteraemia with high fever.",
         caveat="Duration of remission and concurrent medication changes need the full text; the report is framed as "
                "a revival of pyrotherapy.",
         tags=["fever", "pyrotherapy", "bacteraemia", "schizoaffective", "psychosis"], tier="B",
         era=("emerging", "Fever-linked remission of psychosis has a long anecdotal history (Wagner-Jauregg, in "
                          "library) but no modern controlled test.")),
    dict(id="silva-2021", src=210, design="Conference abstract", n=1, cats=["Personality", "Mood"],
         spec="Borderline personality disorder with a depressive episode, self-injury ideation and repeated acting out",
         chronic=True, tr=None, tcat="Immune reset", tspec="Intravenous immunoglobulin for a myasthenia gravis flare",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=0,
         summary="After intravenous immunoglobulin for myasthenia, a woman with borderline personality disorder had "
                 "full remission of a depressive episode, stopped acting out and had less self-injury ideation.",
         caveat="Conference abstract; follow-up one month; other medicines unchanged but the myasthenia flare itself "
                "may have been depressogenic.",
         tags=["ivig", "immunoglobulin", "myasthenia", "borderline-personality", "self-injury", "depression"], tier="C"),
    dict(id="stevens-1990", src=294, design="Case series", n=14, cats=["Personality", "Impulse-control"],
         spec="Incapacitating paranoid personality disorder (one patient) and explosive rage attacks (another), with "
              "temporal lobe epilepsy", chronic=True, tr=None,
         tcat="Neurosurgery", tspec="Temporal lobectomy for intractable seizures", intent="Treatment for another condition",
         res="Partial", rev="None reported", dl=1,
         summary="In a 20-30-year follow-up of 14 temporal lobectomies, one patient with incapacitating paranoid "
                 "personality disorder and one with explosive rage both improved markedly; others developed psychosis.",
         caveat="Two relevant patients in a series where six got worse or newly psychotic; side of surgery per "
                "patient needs the full text.",
         tags=["temporal-lobectomy", "epilepsy-surgery", "paranoid-personality", "rage", "long-follow-up"], tier="C",
         era=("emerging", EPI_NOTE)),
    dict(id="rizzo-2008", src=392, design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
         spec="Tourette syndrome in an 8-year-old boy", chronic=True, tr=None,
         tcat="Medication for another condition", tspec="Ondansetron for chemotherapy-induced nausea (acute lymphoblastic leukaemia)",
         intent="Treatment for another condition", res="Partial", rev="Natural off-on", dl=1,
         summary="A boy with Tourette syndrome given ondansetron for chemotherapy nausea had his tics settle too; "
                 "they came back when the dose was cut.",
         caveat="Child with leukaemia and chemotherapy, so many moving parts; tics wax and wane naturally.",
         tags=["ondansetron", "5ht3", "tourette", "tics", "child", "leukaemia", "chemotherapy"], tier="B",
         era=("emerging", "A small randomised trial of ondansetron added to haloperidol in Tourette syndrome "
                          "(Toren 2005, recalled, not checked) was positive; not adopted.")),
    dict(id="serratrice-2002", src=398, design="Case report", n=1, cats=["Psychotic", "Mood"],
         spec="Psychosis with hallucinations, depression, anorexia and withdrawal in a 41-year-old woman with Down syndrome",
         chronic=None, tr=None, tcat="Diet", tspec="Gluten-free diet for silent coeliac disease (anti-gliadin antibodies, no villous atrophy)",
         intent="Treatment for another condition", res="Complete", rev="None reported", dl=1,
         summary="A woman with Down syndrome and new psychosis and depression improved strikingly and lastingly after "
                 "12 months on a gluten-free diet for silent coeliac disease.",
         caveat="Arguably a secondary psychosis, as with De Santis 1997; duration before the diet unclear; slow "
                "response over a year.",
         tags=["coeliac", "gluten-free-diet", "down-syndrome", "psychosis", "depression"], tier="C",
         era=("emerging", "Gluten-linked psychosis remains contested; see De Santis 1997 and Jansson 1984 in library.")),
    dict(id="juiz-fernandez-2022", src=557, design="Case report", n=1, cats=["Anxiety", "Mood"],
         spec="Anxiety-depressive syndrome and phobias with drug-resistant right mesial temporal epilepsy",
         chronic=True, tr=None, tcat="Neurosurgery", tspec="Right anteromedial temporal lobectomy for epilepsy",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
         summary="A woman's phobias and anxious depression improved along with her seizures after a right "
                 "anteromedial temporal lobectomy.",
         caveat="Interictal versus seizure-bound symptoms not separable from the abstract; extent of improvement unstated.",
         tags=["temporal-lobectomy", "epilepsy-surgery", "right-temporal", "amygdala", "phobia", "anxiety"], tier="C",
         era=("emerging", EPI_NOTE)),
]

DEC = {
    0: None,  # O'Hara 2004, matched by DOI/PMID
    78: "zuschlag-2016", 210: "silva-2021", 294: "stevens-1990", 392: "rizzo-2008", 398: "serratrice-2002",
    557: "juiz-fernandez-2022",
    49: (U, "letter, no abstract: was sleep induced to treat the persisting peyote psychosis?"),
    439: (U, "scope: persistent stuttering (DSM-5 childhood-onset fluency disorder); stopped on baclofen for alcohol "
             "dependence with on-off rechallenge"),
    551: (U, "letter: was metformin started for the polycystic ovary syndrome or for the menstrual psychosis?"),
    686: (U, "bilateral amygdalotomy for seizures; outcome of long-standing depression not in abstract"),
    884: (U, "chronic pain with opioid dependence lifted after sudden amnesia (seizures in one): physiological "
             "dependence or use disorder?"),
    55: ("E1", "persistent genital arousal disorder is out of scope (protocol v1.2.2)"),
    71: ("E3", "single-blind haemodialysis versus sham given to treat schizophrenia"),
    109: ("E3", "cognitive-coping therapy given for the OCD"),
    136: ("E3", "selegiline given for the depression"),
    234: ("E3", "vagus nerve stimulation and ECT given for the depression"),
    334: ("E2", "mood elevation then depression began on aromatase inhibitors"),
    357: ("E3", "gluten-free diet tried for an acute psychosis after usual treatment failed"),
    365: ("E3", "acamprosate given for the alcohol dependence; skin reaction on drinking"),
    379: ("E4", "psychic symptoms were part of the seizures and eased with seizure control"),
    423: ("E3", "ACTH and prednisone given for the tics on an immune hypothesis"),
    472: ("E4", "panic disorder brought on by triphasic oral contraceptives resolved on stopping them"),
    502: ("E5", "review, no new case"),
    504: ("E3", "olanzapine started alongside the gluten-free diet"),
    510: ("E1", "serendipity in functional neurosurgery for movement disorders; psychiatric syndromes not the outcome"),
    525: ("E1", "histamine intolerance misdiagnosed as anorexia nervosa"),
    562: ("E3", "focused ultrasound aimed at the depression"),
    589: ("E3", "cabergoline added for the depression"),
    599: ("E4", "six months of depression with symptomatic coeliac disease, framed by the authors as secondary"),
    605: ("E3", "mirtazapine given for compulsive masturbation in autism"),
    654: ("E3", "celecoxib added for the tics on an inflammation hypothesis"),
    666: ("E1", "ovarian cysts and cholestasis"),
    678: ("E2", "psychosis worsened on amantadine for neuroleptic malignant syndrome"),
    723: ("E2", "no surgery; partial response to antipsychotics"),
    763: ("E3", "nabiximols given for the tics"),
    785: ("E3", "vortioxetine given for the depression"),
    813: ("E3", "elimination diet trialled for the treatment-resistant depression"),
    868: ("E4", "psychiatric syndrome of CNS relapsing polychondritis resolved with tocilizumab"),
    899: ("E1", "weight loss only; no psychiatric outcome"),
    926: ("E2", "eating-disorder outcome not reported; coeliac disease as a differential"),
    968: ("E3", "phenelzine given for the depression"),
    970: ("E4", "upper airway resistance syndrome treated as the presumed cause; depression had already remitted with ECT"),
    979: ("E2", "psychosis emerged before facial pain surgery"),
}
LABEL = {"fp": "first pass", "b2": "year-slice batch 2"}
PREFIX = {"fp": "rank ", "b2": "year-slice batch 2"}
# Earlier theme-sweep rows corrected here: record_id -> (decision, note)
CORRECT = {"R046028": ("juiz-fernandez-2022", "EPMC_temporal_v1", 557),
           "R046360": ("stevens-1990", "EPMC_temporal_v1", 294),
           "R047109": ((U, "outcome of depression not in abstract"), "EPMC_temporal_left_v1_3", 686)}


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
    for nr, q, rk, key, s, has_abs, pt, title in top:
        if (q, rk) not in old:
            continue  # held-out cases already decided
        m = lite[key]
        c = core.get(nr, {})
        L.add("Europe PMC", "EPMC_broad_v1_2", DEC.get(nr), doi=(m["doi"] or "").lower(), pmid=m["pmid"],
              pmcid=m["pmcid"], other=key, title=m["title"] or title, au=first_author(m["au"]), yr=m["yr"],
              jn=m["jn"], lang=c.get("lang", ""),
              note=f"{LABEL[q]}, rank {rk}; rerank_v1 rank {nr}, score {s}; screened {TODAY}", supersedes=old[(q, rk)])
        n += 1
    byid = {r["record_id"]: r for r in L.rows}
    for rid, (dec, qid, nr) in CORRECT.items():
        o = byid[rid]
        L.add(o["source_db"], qid, dec, doi=o["doi"], pmid=o["pmid"], pmcid=o["pmcid"], other=o["other_id"],
              title=o["title"], au=o["first_author"], yr=o["year"], jn=o["journal"], lang=o["language"],
              note=f"correction: abstract read via rerank_v1 rank {nr} on {TODAY}", supersedes=rid)
    L.write()
    print("ledger rows:", n + len(CORRECT))
    log_runs([
        ("EPMC_broad_v1_2", "Europe PMC (browser)",
         "rerank_v1: top 1,000 of 35,270 unscreened (first pass + batch 2), classifier queries/rerank_model_v1.json",
         1000, TODAY, "6 includes, 5 unsure; held-out Kraft & Westman 2009 at 1, Solyom 1987 at 354"),
    ])
