"""Batch 2026-11-14: Embase title-restricted set (EMB_title_v1_2), remaining ranks, re-ranked with the v1.3 classifier.

The original query was reconstructed and rerun through the Embase UI via CKN (search #5, 1,402 hits on 2026-11-14 vs
1,375 on 2026-11-09):
  A(syndrome, from EMB_broad_v1_2):ti AND (B(resolution):ti OR U(unexpected):ti) AND E(case block) AND
  [embase]/lim NOT [medline]/lim AND [humans]/lim
Records were read from the results endpoint (paced), scored in the browser with queries/rerank_model_v1.json, and
matched to the ledger by Embase ID: 1,044 still blank + 27 added since = 1,071 to screen, in classifier order.

Stopping (protocol section 10): last possibly relevant at rank 414; ranks 415-714 are 300 consecutive irrelevant; a
seeded random 300 of ranks 497-1,070 (seed 20261114, queries/stopping_sample_embase_title_2026_11_14.json) had 0
includes. Both criteria met; ranks 715+ outside the sample stay blank.

Result: 5 cases + 1 context record (Vender 1996), 9 unsure rows (7 records). Working file: /home/claude/work/raw/emb_todo.json.
Run from the repo root:  python3 scripts/batches/b2026_11_14_embase_title_rerank.py
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, "scripts")
from lib_add import CASES, U, Ledger, add_records, log_runs  # noqa: E402

TODAY = "2026-11-14"
todo = json.loads(Path("/home/claude/work/raw/emb_todo.json").read_text())   # [id, score, yr, pt, doi, hasAbs, title, new|blank, old_record_id]
SAMPLE = set(json.loads(Path("queries/stopping_sample_embase_title_2026_11_14.json").read_text())["ranks"])
SCREENED_TO = 714
CKN = "https://go.openathens.net/redirector/ckn.qldhealth.com?url="


def emb_url(eid):
    return CKN + quote(f"https://www.embase.com/records?subaction=viewrecord&id={eid}", safe="")


cand = {
    "0": dict(pmid="", pmcid="", doi="10.1097/jcp.0b013e31827c2f2f", title="Body dysmorphic disorder incidentally treated with bupropion: A case report", authorString="Canan F., Sinani G., Aydinoglu U.", journal="J Clin Psychopharmacol", year=2012, vol="", issue="", pages="", lang="eng"),
    "6": dict(pmid="", pmcid="", doi="10.4088/pcc.v10n0312d", title="Improvement in depressive symptoms with felbamate: A case report", authorString="Sharma A., Drake J., Qasimyar M., Tucker S.", journal="Prim Care Companion J Clin Psychiatry", year=2008, vol="10", issue="3", pages="252", lang="eng"),
    "24": dict(pmid="", pmcid="", doi="", title="Prebiotic lactosucrose may improve not only constipation but also psychotic symptoms of schizophrenia", authorString="Ido Y., Nagamine T., Okamura T., Tasaki M., Fukuo K.", journal="International Medical Journal", year=2017, vol="24", issue="3", pages="305-306", lang="eng"),
    "53": dict(pmid="", pmcid="", doi="10.1016/j.eurpsy.2017.01.1059", title="About a case suicide attempt as a trigger of remission in obsessive and compulsive disorder", authorString="Gota Garces J.M., Garcia Lopez R., Porras Segovia A., Munoz Negro J.E., Garcia Jimenez J., Gutierrez Rojas L.", journal="Eur Psychiatry", year=2017, vol="41", issue="", pages="S641", lang="eng"),
    "61": dict(pmid="", pmcid="", doi="10.1002/mds.28268", title="Spontaneous smoking cessation in a parkinsonian patient treated with apomorphine pump", authorString="Auffret M., Geny C., Lees A., Verin M.", journal="Mov Disord", year=2020, vol="35", issue="Suppl 1", pages="S437-S438", lang="eng"),
    "86": dict(pmid="", pmcid="", doi="", title="Pseudo-recovery in schizophrenic patients with intercurrent physical disorders", authorString="Vender S., Civitarese G., Loconte M.", journal="New Trends in Experimental and Clinical Psychiatry", year=1996, vol="12", issue="1", pages="31-37", lang="eng"),
}
EMB_ID = {"24": "L616850333", "86": "L26157003"}
OTHER = "Treatment for another condition"
R = [
    dict(id="canan-2012", src=0, design="Letter", n=1, cats=["Obsessive-compulsive & tic"], spec="Body dysmorphic disorder",
         chronic=None, tr=None, tcat="Medication for another condition", tspec="Bupropion", intent=OTHER, res="Partial",
         rev="None reported", dl=0, summary="Body dysmorphic disorder improved incidentally on bupropion.", caveat="",
         tags=["bupropion", "body-dysmorphic-disorder", "noradrenaline-dopamine"], tier="C"),
    dict(id="sharma-2008", src=6, design="Letter", n=1, cats=["Mood"], spec="Depression", chronic=None, tr=None,
         tcat="Medication for another condition", tspec="Felbamate (antiepileptic)", intent=OTHER, res="Partial",
         rev="None reported", dl=0, summary="Depressive symptoms improved on felbamate, an antiepileptic.",
         caveat="Better seizure control can lift mood on its own.", tags=["felbamate", "antiepileptic", "nmda", "depression"], tier="C"),
    dict(id="ido-2017", src=24, design="Letter", n=1, cats=["Psychotic"], spec="Schizophrenia", chronic=True, tr=None,
         tcat="Diet", tspec="Prebiotic lactosucrose for constipation", intent=OTHER, res="Partial", rev="None reported", dl=1,
         era=("emerging", "Gut-microbiome interventions in schizophrenia are being trialled; results so far are mixed (recalled, not checked)."),
         summary="Psychotic symptoms of schizophrenia improved with a prebiotic given for constipation.",
         caveat="Relief of severe constipation, common on clozapine, can ease agitation and distress.",
         tags=["prebiotic", "microbiome", "constipation", "schizophrenia", "gut-brain"], tier="C"),
    dict(id="gota-garces-2017", src=53, design="Conference abstract", n=1, cats=["Obsessive-compulsive & tic"],
         spec="Late-onset, severe, treatment-refractory OCD", chronic=True, tr=True, tcat="Life event",
         tspec="Failed suicide attempt", intent="Life event", res="Complete", rev="None reported", dl=0,
         summary="A 73-year-old woman's severe, refractory late-onset OCD remitted suddenly after a failed suicide attempt.",
         caveat="Any physical injury or hypoxia from the attempt needs the full text, as does the length of remission.",
         tags=["ocd", "late-onset", "suicide-attempt", "older-adult"], tier="C"),
    dict(id="auffret-2020", src=61, design="Conference abstract", n=1, cats=["Substance & addictive"],
         spec="Nicotine dependence (about 20 a day for over 30 years, earlier failed quits)", chronic=True, tr=None,
         tcat="Medication for another condition", tspec="Continuous subcutaneous apomorphine infusion for Parkinson's disease",
         intent=OTHER, res="Complete", rev="None reported", dl=0,
         summary="A woman with Parkinson's disease and long-standing nicotine dependence stopped smoking without difficulty "
                 "after starting an apomorphine pump.",
         caveat="Parkinson's disease itself is linked to lower reward from smoking.",
         tags=["apomorphine", "dopamine-agonist", "parkinsons", "smoking", "nicotine"], tier="C"),
    dict(id="vender-1996", src=86, record_type="context", design="Review", n=None, cats=["Psychotic"],
         spec="Chronic schizophrenia", chronic=True, tr=None, tcat="Systemic illness", tspec="Intercurrent physical illness",
         intent="Injury or illness", res="Partial", rev="None reported", dl=1,
         summary="An essay on the transient remission of chronic schizophrenia during intercurrent physical illness, "
                 "described as well known and analysed in psychodynamic terms.",
         caveat="", tags=["intercurrent-illness", "schizophrenia", "pseudo-recovery", "fever"], tier=None),
]
DEC = {0: "canan-2012", 6: "sharma-2008", 24: "ido-2017", 53: "gota-garces-2017", 61: "auffret-2020", 86: "vender-1996",
       2: "tsolaki-2010", 4: "baek-2022",
       7: (U, "letter, no abstract: was duloxetine given for depression or pain, or aimed at the tics?"),
       8: (U, "letter, no abstract: which drug stopped the clozapine hypersalivation? If amisulpride, it is an antipsychotic (E3)"),
       9: (U, "duplicate of the clozapine hypersalivation letter"),
       14: (U, "letter, no abstract: what was midazolam given for?"),
       22: (U, "no abstract: physical illness inducing psychosis remission (compare Vender 1996)"),
       196: (U, "depression remitted with episodic sweating in Shapiro syndrome: which treatment, and for what?"),
       431: (U, "duplicate of the Shapiro syndrome report"),
       322: (U, "conference abstract of Abe 2016: gabapentin improved Parkinson's visual hallucinations and pain; started for pain or aimed at both?"),
       414: (U, "Abe 2016: gabapentin improved Parkinson's visual hallucinations and pain; started for pain or aimed at both?"),
       1: ("E1", "depression gave way to Ganser syndrome; one syndrome replacing another, no external trigger"),
       3: ("E5", "commentary on a deep brain stimulation case"),
       54: ("E1", "adolescent stopped drinking after frightening alcohol-related experiences; no use disorder"),
       75: ("E3", "mirtazapine given for depression in the same patient"),
       87: ("E3", "adjunct serotonergic medication aimed at the psychosis"),
       138: ("E3", "dexamphetamine given for the postpartum depression"),
       139: ("E3", "ECT given for the methamphetamine psychosis"),
       146: ("E2", "patient-reported easing of voices with Datura; remission came with clozapine"),
       151: ("E2", "duplicate of the Datura abstract"),
       161: ("E3", "remission over years of antipsychotic treatment"),
       171: ("E3", "anorexia nervosa treated directly"), 177: ("E3", "sandplay therapy for the tics"),
       184: ("E3", "sublingual influenza 'neutralizing doses' given for schizophrenia (clinical ecology)"),
       220: ("E3", "entacapone started to reduce cocaine craving"), 261: ("E3", "fluoxetine for the OCD"),
       263: ("E3", "penicillin prophylaxis for presumed PANDAS"), 438: ("E3", "conservative treatment aimed at the functional deformity"),
       447: ("E4", "depression framed as caused by chronic pain, relieved by spinal cord stimulation"),
       517: ("E3", "coercive treatment of the manic episode")}

if __name__ == "__main__":
    add_records(R, cand, collection="phase1d", found_via="Embase via CKN (EMB_title_v1_2, re-ranked v1.3)", today=TODAY)
    d = json.loads(CASES.read_text())
    lib_titles = {re.sub(r"[^a-z0-9]", "", r["citation"]["title"].lower())[:80]: r["id"] for r in d["records"]}
    for r in d["records"]:
        for src, eid in EMB_ID.items():
            if r["id"] == next(k["id"] for k in R if str(k["src"]) == src) and not r["links"].get("ckn"):
                r["links"]["ckn"] = emb_url(eid)
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    L = Ledger(TODAY)
    n = {"screened": 0, "blank_new": 0}
    for i, (eid, s, yr, pt, doi, has_abs, title, kind, old) in enumerate(todo):
        screened = i <= SCREENED_TO or i in SAMPLE
        if not screened and kind == "blank":
            continue  # stays blank under its original row
        dec = DEC.get(i)
        if dec is None and screened:
            dec = lib_titles.get(re.sub(r"[^a-z0-9]", "", title.lower())[:80])
        what = "stopping-rule random sample (seed 20261114)" if (i in SAMPLE and i > SCREENED_TO) else ("re-ranked order" if screened else "not screened (stopping rule met)")
        L.add("Embase via CKN", "EMB_title_v1_2", dec, doi=doi, other=eid, title=title, yr=yr,
              note=f"rerank_v1 rank {i}, score {s}; {what}; {'added since 2026-11-09' if kind == 'new' else 'was blank'}; {TODAY}",
              supersedes=old if kind == "blank" else "", screened=screened)
        n["screened" if screened else "blank_new"] += 1
    L.write()
    print(n)
    log_runs([("EMB_title_v1_2", "Embase via CKN",
               "rerun as search #5: A:ti AND (B:ti OR U:ti) AND E AND Embase-only, humans; 1,071 unscreened ranked with v1.3 classifier",
               1402, TODAY, "ranks 0-714 + random 300 screened; 5 cases + 1 context, 7 unsure records; stopping rule met")])
