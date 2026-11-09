"""Batch 2026-11-09 (phase 1, first pass): includes from Embase via CKN
(strategy 1 and title-ranked broad set) and Europe PMC (ranked broad set, top 700).

Abstract-based appraisal only: every record enters as Provisional until its
full text is read at step 1.9. Bibliographic fields come from the exported
records in /home/claude/work/raw (not committed: they contain abstracts).

Run from the repo root:  python3 scripts/batches/b2026_11_09_phase1a.py
"""
import json
import re
from pathlib import Path
from urllib.parse import quote

RAW = Path("/home/claude/work/raw")
emb = json.loads((RAW / "emb_includes.json").read_text())
ep = json.loads((RAW / "epmc_includes.json").read_text())
cand, meta = ep["cand"], ep["meta"]
PATH = Path("data/cases.json")
d = json.loads(PATH.read_text())
V = d["vocabularies"]
TODAY = "2026-11-09"

# ---- vocabulary additions (schema 1.2) ----
def add_vocab(key, vals):
    for v in vals:
        if v not in V[key]:
            V[key].append(v)
add_vocab("syndrome_category", ["Trauma & stressor-related", "Neurodevelopmental", "Catatonia"])
add_vocab("trigger_category", ["Surgery or procedure (outside the brain)", "Systemic illness", "Life event",
                               "Hormonal / reproductive", "Physiological stress"])
add_vocab("trigger_intent", ["Medication error", "Life event"])
add_vocab("design", ["Conference abstract", "Preprint"])
V["tier"]["C"] = "Logged: qualifies, but weak, abstract-only or flagged"


def ckn(doi):
    return "https://go.openathens.net/redirector/ckn.qldhealth.com?url=" + quote("https://doi.org/" + doi, safe="")


def norm_au(a):
    # "Hosseini S.H." -> "Hosseini SH"
    return re.sub(r"\.", "", a).strip()


def bib_from(key):
    """Return citation + ids from the exported records."""
    if key.startswith("ep"):
        c = cand[key[2:]]
        au = ", ".join(c["authors"][:6]) + (" et al." if len(c["authors"]) > 6 else "")
        return dict(authors=au, title=c["title"], journal=c["journal"], year=int(c["year"]), volume=c["vol"],
                    issue=c["issue"], pages=c["pages"]), dict(doi=c["doi"], pmid=c["pmid"], pmcid=c["pmcid"]), None
    if key.startswith("meta:"):
        m = meta[key[5:]]
        return dict(authors=m["au"], title=None, journal=m["jn"], year=int(m["yr"]), volume=m["vol"], issue=m["iss"],
                    pages=m["pg"]), dict(doi=m["doi"], pmid=m["pmid"], pmcid=m["pmcid"]), None
    r = emb[key]
    return dict(authors=norm_au(r["au"]) + " et al.", title=r["t"], journal=r["jn"], year=int(r["yr"]), volume="",
                issue="", pages=""), dict(doi=r["doi"], pmid="", pmcid=""), r


# id, source key (+ optional meta key for better ids), design, n, syndrome cats, specific, chronic, TR,
# trigger cat, specific, intent, resolution, reversal, downstream level, summary, caveat, tags, tier, era (label, note), extra
R = []
def rec(**k):
    R.append(k)

# ---------------- Embase (strategy 1 + title-ranked set) ----------------
rec(id="hosseini-2026", src="emb0", m="hosseini-2026", design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
    spec="Postpartum-onset OCD, relapsed after clomipramine was stopped", chronic=True, tr=None,
    tcat="Medication for another condition", tspec="Clomiphene (a fertility drug) dispensed in error instead of clomipramine",
    intent="Medication error", res="Partial", rev="None reported", dl=0,
    summary="Relapsed OCD improved after a pharmacy error supplied clomiphene, a fertility drug, in place of clomipramine.",
    caveat="Improvement rather than remission, in a patient with a history of good treatment response.",
    tags=["ocd", "medication-error", "hormonal", "serendipity"], tier="B", via="Embase (CKN)")
rec(id="bedell-2025", src="meta:bedell-2025", title="A Severe Case of Pica Resolved With GLP-1 Agonist Therapy",
    authors="Bedell BR et al.", design="Conference abstract", n=1, cats=["Eating"], spec="Severe pica", chronic=None, tr=None,
    tcat="Medication for another condition", tspec="GLP-1 receptor agonist for obesity", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=1,
    summary="Severe pica disappeared after a GLP-1 receptor agonist was started for weight loss.",
    caveat="Conference abstract; duration of pica and follow-up not given.", tags=["glp-1", "pica", "eating", "conference-abstract"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="richards-2022", src=None, title="Case Series: Successful Treatment of Moderate to Severe Binge Eating with GLP-1 Agonist Semaglutide",
    authors="Richards J et al.", journal="Obesity", year=2022, doi="10.1002/oby.23626", design="Conference abstract", n=5,
    cats=["Eating"], spec="Moderate to severe binge eating disorder (Binge Eating Scale)", chronic=None, tr=None,
    tcat="Medication for another condition", tspec="Semaglutide given for obesity, per clinic protocol", intent="Treatment for another condition",
    res="Partial", rev="None reported", dl=1,
    summary="Five obesity-clinic patients' binge eating scores fell after semaglutide was started for weight.",
    caveat="Retrospective chart review in an obesity clinic, abstract only.", tags=["glp-1", "binge-eating", "case-series", "conference-abstract"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="fernandes-2020", src="emb119", design="Conference abstract", n=1, cats=["Eating"], spec="Anorexia nervosa", chronic=None, tr=None,
    tcat="Acquired brain lesion", tspec="Infective endocarditis with cerebral embolism", intent="Injury or illness",
    res="Complete", rev="None reported", dl=0,
    summary="Anorexia nervosa went into remission after infective endocarditis sent emboli to the brain.",
    caveat="Conference abstract; lesion sites and follow-up need the poster or full text.", tags=["anorexia", "lesion", "embolism", "conference-abstract"],
    tier="C", via="Embase (CKN)")
rec(id="mathew-2019", src="emb_mathew", m="mathew-2019", design="Conference abstract", n=1, cats=["Substance & addictive"],
    spec="Nicotine dependence, 1–2 packs a day for about 30 years", chronic=True, tr=None,
    tcat="Medication for another condition", tspec="Erenumab for migraine; its nausea was made worse by smoking", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=0,
    summary="A lifelong heavy smoker stopped after erenumab, a migraine drug, caused nausea that smoking made worse.",
    caveat="An aversive side effect rather than a change in craving; abstract only.", tags=["smoking", "migraine", "aversion", "conference-abstract"],
    tier="C", via="Embase (CKN)")
rec(id="kim-2016", src="emb201", m="kim-2016", design="Case report", n=1, cats=["Mood"], spec="Treatment-resistant depression", chronic=True, tr=True,
    tcat="Seizures", tspec="A seizure during a course of rTMS", intent="Injury or illness", res="Complete", rev="None reported", dl=0,
    summary="Treatment-resistant depression remitted after an accidental seizure during repetitive transcranial magnetic stimulation.",
    caveat="The rTMS course itself may have contributed.", tags=["depression", "seizure", "rtms", "adverse-event"],
    tier="B", era=("known", "Seizures relieving depression is the principle of convulsive therapy (1930s); unexpected here as a single accidental seizure."),
    via="Embase (CKN)")
rec(id="canan-2013", src="meta:canan-2011", title="Body dysmorphic disorder incidentally treated with bupropion",
    design="Letter", n=1, cats=["Obsessive-compulsive & tic"], spec="Body dysmorphic disorder (preoccupation with his face)", chronic=None, tr=None,
    tcat="Medication for another condition", tspec="Bupropion SR for smoking cessation", intent="Treatment for another condition",
    res="Partial", rev="None reported", dl=1,
    summary="A man taking bupropion to quit smoking found his body dysmorphic preoccupation had faded by week 8.",
    caveat="No standardised measure in the abstract; bupropion has antidepressant effects. First reported as a 2011 conference abstract.",
    tags=["bdd", "bupropion", "smoking"], tier="B", era=("emerging", ""), via="Embase (CKN)")
rec(id="pardo-gonzalez-2023", src="emb68", m="pardo-gonzalez-2023", design="Conference abstract", n=1, cats=["Mood"],
    spec="Chronic mania in bipolar disorder with intellectual disability and epilepsy", chronic=True, tr=None,
    tcat="Systemic illness", tspec="Stevens–Johnson syndrome 14 days after starting cariprazine", intent="Injury or illness",
    res="Partial", rev="None reported", dl=0,
    summary="Chronic mania improved after an episode of Stevens–Johnson syndrome.",
    caveat="Medication changes forced by the reaction confound attribution; abstract only.", tags=["mania", "sjs", "systemic-illness", "conference-abstract"],
    tier="C", via="Embase (CKN)")
rec(id="felizardo-2023", src="emb69", m="felizardo-2023", design="Conference abstract", n=1, cats=["Psychotic"],
    spec="Persistent delusional disorder", chronic=True, tr=None, tcat="Seizures", tspec="Clozapine-induced epileptic seizures",
    intent="Injury or illness", res="Complete", rev="None reported", dl=0,
    summary="Persistent delusional disorder remitted after clozapine provoked epileptic seizures.",
    caveat="Clozapine itself may have been effective; abstract only.", tags=["delusional-disorder", "clozapine", "seizure", "conference-abstract"],
    tier="C", era=("known", "Seizures relieving psychosis is the principle of convulsive therapy (Meduna, 1934)."), via="Embase (CKN)")
rec(id="gerken-2022", src="emb80", design="Conference abstract", n=1, cats=["Obsessive-compulsive & tic"],
    spec="Severe contamination OCD since age 19", chronic=True, tr=None, tcat="Acquired brain lesion", tspec="Ischaemic stroke in the basal ganglia",
    intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Ten years of severe contamination OCD remitted after an ischaemic stroke in the basal ganglia.",
    caveat="Conference abstract; lesion detail and follow-up need the full text.", tags=["ocd", "stroke", "basal-ganglia", "conference-abstract"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="durbin-2022", src="emb85", m="durbin-2022", design="Conference abstract", n=1, cats=["Obsessive-compulsive & tic"],
    spec="Gilles de la Tourette syndrome since age 7", chronic=True, tr=None, tcat="Physiological stress",
    tspec="Heat-induced dehydration (follow-up of the Brasic patient)", intent="Self-administered", res="Complete", rev="None reported", dl=0,
    summary="Follow-up of the man whose Tourette syndrome remitted after hot-tub dehydration: still doing well years later.",
    caveat="Same patient as Brasic 2018; abstract only.", tags=["tourette", "dehydration", "heat", "follow-up", "conference-abstract"],
    tier="C", same="brasic-2018", via="Embase (CKN)")
rec(id="aminzade-2021", src="emb94", m="aminzade-2021", design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
    spec="OCD component of refractory Tourette syndrome", chronic=True, tr=True, tcat="Brain stimulation",
    tspec="Anteromedial globus pallidus internus DBS for tics", intent="Treatment for another condition", res="Complete", rev="None reported", dl=1,
    summary="DBS aimed at tics left them unchanged but almost completely resolved the patient's OCD.",
    caveat="OCD is part of the Tourette spectrum, so the target was adjacent rather than unrelated.", tags=["ocd", "tourette", "dbs", "gpi"],
    tier="B", era=("emerging", ""), via="Embase (CKN)")
rec(id="huhne-2021", src="emb96", m="huhne-2021", design="Case report", n=1, cats=["Anxiety"], spec="Social anxiety disorder", chronic=True, tr=None,
    tcat="Life event", tspec="A traumatic event (posttraumatic growth)", intent="Life event", res="Complete", rev="None reported", dl=0,
    summary="Long-standing social anxiety disorder remitted after a traumatic event, framed as posttraumatic growth.",
    caveat="Psychological mechanism; measures need checking in the full text.", tags=["social-anxiety", "trauma", "posttraumatic-growth"],
    tier="B", via="Embase (CKN)")
rec(id="vendrell-serres-2021", src="emb110", m="vendrell-serres-2021", design="Case report", n=1, cats=["Functional neurological"],
    spec="Functional neurological disorder with treatment-resistant depression", chronic=True, tr=True, tcat="Medication for another condition",
    tspec="Esketamine nasal spray for treatment-resistant depression", intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
    summary="Functional neurological symptoms improved when esketamine was given for comorbid treatment-resistant depression.",
    caveat="Mood improved at the same time, so the effect may run through depression.", tags=["fnd", "esketamine", "comorbid"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="van-den-hoven-2021", src="emb111", design="Case report", n=1, cats=["Catatonia"],
    spec="Catatonia in recurrent depressive disorder after a stroke, partly lorazepam-responsive", chronic=None, tr=True,
    tcat="Coma / anaesthesia", tspec="Propofol infusion given for an unrelated reason", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=1,
    summary="Catatonia that lorazepam only partly relieved resolved abruptly during a propofol infusion given for something else.",
    caveat="Catatonia was weeks old, not chronic.", tags=["catatonia", "propofol", "anaesthesia", "gaba"],
    tier="B", era=("emerging", ""), via="Embase (CKN)")
rec(id="collyer-2020", src="emb115", design="Case series", n=3, cats=["Mood"], spec="Depression with irritable bowel syndrome", chronic=None, tr=None,
    tcat="Surgery or procedure (outside the brain)", tspec="Faecal microbiota transplantation for irritable bowel syndrome",
    intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
    summary="Mood improved in three people given faecal microbiota transplants for irritable bowel syndrome.",
    caveat="Retrospective record review; outcome measures heterogeneous.", tags=["depression", "fmt", "microbiome", "case-series"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="achamrah-2020", src="emb125", m="achamrah-2020", design="Case report", n=1, cats=["Eating"], spec="Bulimia nervosa for 15 years",
    chronic=True, tr=None, tcat="Surgery or procedure (outside the brain)", tspec="Total gastrectomy for gastric necrosis after a binge",
    intent="Injury or illness", res="Partial", rev="None reported", dl=0,
    summary="Fifteen years of bulimia nervosa eased markedly after an emergency total gastrectomy.",
    caveat="Bingeing becomes physically limited after gastrectomy, so behaviour change is not clean evidence of remission.",
    tags=["bulimia", "gastrectomy", "surgery"], tier="B", via="Embase (CKN)")
rec(id="jarvinen-2019", src="emb155", m="jarvinen-2019", design="Case report", n=1, cats=["Eating", "Neurodevelopmental"],
    spec="Severe obsessive food craving and binge eating in autism", chronic=True, tr=True, tcat="Medication for another condition",
    tspec="Liraglutide (a GLP-1 agonist)", intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
    summary="Obsessive food craving and binge eating in a man with autism eased on liraglutide.",
    caveat="Indication needs checking; weight management was a stated aim.", tags=["autism", "glp-1", "binge-eating"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="shreedhara-2018", src="emb162", m="shreedhara-2018", design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
    spec="OCD with refractory temporal lobe epilepsy", chronic=True, tr=None, tcat="Neurosurgery",
    tspec="Right anterior temporal lobectomy with amygdalohippocampectomy for epilepsy", intent="Treatment for another condition",
    res="Partial", rev="None reported", dl=1,
    summary="OCD improved after a right temporal lobectomy done to stop epileptic seizures.",
    caveat="Seizure control and medication changes after surgery could contribute.", tags=["ocd", "epilepsy-surgery", "temporal-lobe"],
    tier="B", era=("emerging", "Follows Kanner 1993 and Guarnieri 2005."), via="Embase (CKN)")
rec(id="sair-2018", src="emb167", design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="Obsessive-compulsive disorder",
    chronic=None, tr=None, tcat="Acquired brain lesion", tspec="Temporoparietal haemorrhage", intent="Injury or illness",
    res="Complete", rev="None reported", dl=1,
    summary="Obsessive-compulsive symptoms remitted after a temporoparietal haemorrhage.",
    caveat="Chronicity and measures need the full text.", tags=["ocd", "haemorrhage", "lesion"], tier="B", era=("emerging", ""), via="Embase (CKN)")
rec(id="sumner-2017", src="emb187", design="Conference abstract", n=1, cats=["Psychotic"], spec="Chronic schizophrenia", chronic=True, tr=None,
    tcat="Acquired brain lesion", tspec="Bilateral thalamic infarcts (artery of Percheron occlusion)", intent="Injury or illness",
    res="Partial", rev="None reported", dl=0,
    summary="A man with chronic schizophrenia needed far less antipsychotic after bilateral thalamic strokes.",
    caveat="Dose requirement is an indirect measure, and he was severely amnestic after the stroke.", tags=["schizophrenia", "thalamus", "stroke", "conference-abstract"],
    tier="C", via="Embase (CKN)")
rec(id="ali-2015", src="emb211", m="ali-2015", design="Letter", n=1, cats=["Mood"], spec="Depression with Parkinson's disease", chronic=None, tr=None,
    tcat="Brain stimulation", tspec="Globus pallidus internus DBS for Parkinson's disease (no motor benefit)", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=1,
    summary="Pallidal DBS for Parkinson's disease failed to help her movement but relieved her depression.",
    caveat="Letter; depression severity and duration need checking.", tags=["depression", "parkinsons", "dbs", "gpi"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="coffey-2014", src="emb214", design="Conference abstract", n=1, cats=["Neurodevelopmental"], spec="Childhood-onset ADHD",
    chronic=True, tr=None, tcat="Brain stimulation", tspec="Bifrontal ECT for adolescent major depression", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=0,
    summary="A teenager's childhood ADHD resolved after a course of ECT given for depression.",
    caveat="Abstract only; depressive symptoms can mimic and amplify ADHD.", tags=["adhd", "ect", "adolescent", "conference-abstract"],
    tier="C", via="Embase (CKN)")
rec(id="brieler-2014", src="emb223", m="brieler-2014", design="Letter", n=1, cats=["Psychotic"], spec="Schizophrenia", chronic=True, tr=None,
    tcat="Traumatic brain injury", tspec="Traumatic brain injury", intent="Injury or illness", res="Partial", rev="None reported", dl=0,
    summary="Positive symptoms of schizophrenia resolved after a traumatic brain injury.",
    caveat="Letter; injury site and follow-up need the full text.", tags=["schizophrenia", "tbi"], tier="B", via="Embase (CKN)")
rec(id="nakama-2013", src="emb226", design="Case report", n=1, cats=["Trauma & stressor-related"], spec="PTSD with treatment-resistant depression",
    chronic=True, tr=True, tcat="Brain stimulation", tspec="Left dorsolateral prefrontal rTMS for treatment-resistant depression",
    intent="Treatment for another condition", res="Complete", rev="None reported", dl=1,
    summary="Comorbid PTSD remitted alongside depression during rTMS given for the depression.",
    caveat="Comorbid improvement; PTSD may have tracked mood.", tags=["ptsd", "rtms", "comorbid"], tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="zakrzewski-2013", src="emb237", design="Conference abstract", n=12, cats=["Impulse-control"], spec="Compulsive shopping after traumatic brain injury",
    chronic=True, tr=None, tcat="Medication for another condition", tspec="Dextromethorphan/quinidine for pseudobulbar affect",
    intent="Treatment for another condition", res="Partial", rev="None reported", dl=0,
    summary="Compulsive shopping after brain injury eased in patients given dextromethorphan/quinidine for pathological crying and laughing.",
    caveat="Retrospective series of 12; how many shopped compulsively is unclear from the abstract.", tags=["compulsive-buying", "tbi", "dextromethorphan", "conference-abstract"],
    tier="C", via="Embase (CKN)")
rec(id="bagnati-2013", src="emb238", design="Conference abstract", n=1, cats=["Substance & addictive"], spec="Nicotine addiction", chronic=True, tr=None,
    tcat="Acquired brain lesion", tspec="Strategic acute brain ischaemia in reward-circuit pathways (MRI and DTI)", intent="Injury or illness",
    res="Complete", rev="None reported", dl=1,
    summary="Nicotine addiction stopped abruptly after a small stroke in reward-circuit pathways, along with new apathy.",
    caveat="Abstract only; apathy may explain the loss of drive to smoke.", tags=["smoking", "stroke", "reward-circuit", "conference-abstract"],
    tier="C", era=("known", "Replicates the lesion-induced addiction remission shown by Naqvi 2007 and pooled by Joutsa 2022."), via="Embase (CKN)")
rec(id="sandeep-2013", src="emb241", design="Conference abstract", n=1, cats=["Eating"], spec="Anorexia nervosa for 4 years in an adolescent",
    chronic=True, tr=None, tcat="Life event", tspec="A spiritual experience", intent="Life event", res="Complete", rev="None reported", dl=0,
    summary="An adolescent's four-year anorexia nervosa remitted after a spiritual experience.",
    caveat="Abstract only; no follow-up or measures reported.", tags=["anorexia", "spiritual", "conference-abstract"], tier="C", via="Embase (CKN)")
rec(id="boudjani-2012", src="emb247", design="Conference abstract", n=1, cats=["Substance & addictive"], spec="Cocaine addiction", chronic=True, tr=None,
    tcat="Acquired brain lesion", tspec="Dorsolateral striatal stroke (presented with hemiparesis)", intent="Injury or illness",
    res="Complete", rev="None reported", dl=1,
    summary="Cocaine addiction was relieved after a stroke in the dorsolateral striatum.",
    caveat="Abstract only; follow-up length unknown.", tags=["cocaine", "stroke", "striatum", "conference-abstract"], tier="C",
    era=("known", "Fits the lesion-addiction literature after Naqvi 2007."), via="Embase (CKN)")
rec(id="hosseini-2012", src="emb257", m="hosseini-2012", design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="Severe OCD",
    chronic=True, tr=None, tcat="Traumatic brain injury", tspec="Right temporo-parieto-frontal lesion after head trauma", intent="Injury or illness",
    res="Complete", rev="None reported", dl=1,
    summary="Severe OCD disappeared after head trauma damaged the right temporal, parietal and frontal lobes.",
    caveat="Measures and follow-up need the full text.", tags=["ocd", "tbi", "lesion"], tier="B", era=("emerging", ""), via="Embase (CKN)")
rec(id="kalenderoglu-2011", src="emb270", design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="Treatment-refractory OCD",
    chronic=True, tr=True, tcat="Recreational substance", tspec="Heroin use", intent="Self-administered", res="Complete", rev="None reported", dl=1,
    summary="Treatment-refractory OCD went into remission when the patient began using heroin.",
    caveat="Ongoing opioid use; follow-up and measures need the full text.", tags=["ocd", "heroin", "opioid"], tier="B",
    era=("emerging", "Opioid effects on OCD had been reported with tramadol and morphine."), via="Embase (CKN)")
rec(id="vartian-2004", src="emb283", design="Case report", n=1, cats=["Substance & addictive"], spec="Nicotine dependence in schizophrenia",
    chronic=True, tr=None, tcat="Medication for another condition", tspec="Ziprasidone for schizophrenia", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=0,
    summary="A man with schizophrenia stopped smoking nine days after starting ziprasidone and was still abstinent two years later.",
    caveat="Single observation; smokers do quit spontaneously.", tags=["smoking", "schizophrenia", "antipsychotic"], tier="C", via="Embase (CKN)")
rec(id="stuve-2003", src="emb287", design="Case report", n=1, cats=["Psychotic"], spec="Difficult-to-treat paranoid schizophrenia with epilepsy",
    chronic=True, tr=True, tcat="Medication for another condition", tspec="Lamotrigine for epilepsy: remission on it, relapse when stopped",
    intent="Treatment for another condition", res="Complete", rev="Natural off-on", dl=1,
    summary="Paranoid schizophrenia remitted while the patient took lamotrigine for epilepsy and relapsed when it was stopped.",
    caveat="Dutch-language paper with an English abstract; timing evidence only.", tags=["schizophrenia", "lamotrigine", "glutamate", "reversal"],
    tier="B", era=("emerging", ""), via="Embase (CKN)")
rec(id="curran-1995", src="emb297", design="Case report", n=1, cats=["Anxiety"], spec="Severe long-standing panic disorder", chronic=True, tr=None,
    tcat="Hormonal / reproductive", tspec="Pregnancy (relapse after delivery)", intent="Life event", res="Complete", rev="Natural off-on", dl=1,
    summary="Severe long-standing panic disorder fully remitted during pregnancy and relapsed after delivery.",
    caveat="Pregnancy-related remission of panic is recognised, so the surprise is modest.", tags=["panic", "pregnancy", "hormonal", "reversal"],
    tier="C", era=("emerging", ""), via="Embase (CKN)")
rec(id="kanner-1993", src="emb300", design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="OCD with intractable complex partial seizures",
    chronic=True, tr=None, tcat="Neurosurgery", tspec="Right anterior temporal lobectomy for epilepsy", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=1,
    summary="OCD remitted after a right temporal lobectomy performed for intractable seizures.",
    caveat="Seizure control itself may have helped.", tags=["ocd", "epilepsy-surgery", "temporal-lobe"], tier="B",
    era=("emerging", "Later replicated by Guarnieri 2005 and Shreedhara 2018."), via="Embase (CKN)")

# ---------------- Europe PMC (ranked broad set) ----------------
def epr(**k):
    k["via"] = "Europe PMC"
    rec(**k)
epr(id="zhang-2024", src="ep3", design="Case report", n=1, cats=["Mood"], spec="Depression on antidepressants", chronic=True, tr=None,
    tcat="Surgery or procedure (outside the brain)", tspec="Laparotomy for abdominal cocoon with intestinal necrosis (no greater omentum)",
    intent="Injury or illness", res="Partial", rev="None reported", dl=0,
    summary="Depression improved and antidepressants were stopped after surgery for an abdominal cocoon.",
    caveat="Improvement was self-reported at 3 months.", tags=["depression", "abdominal-surgery", "gut-brain"], tier="B")
epr(id="liu-2026", src="ep12", design="Letter", n=1, cats=["Psychotic"], spec="Treatment-refractory schizoaffective disorder", chronic=True, tr=True,
    tcat="Surgery or procedure (outside the brain)", tspec="Haemodialysis (indication to be checked in the full text)", intent="Treatment for another condition",
    res="Partial", rev="None reported", dl=0,
    summary="Treatment-refractory psychosis eased markedly once haemodialysis began.",
    caveat="Letter without an abstract; why dialysis was started is unverified.", tags=["schizoaffective", "dialysis"], tier="C",
    era=("novel", "Dialysis as a treatment for schizophrenia was tested and refuted around 1980 (see Wagemaker & Cade 1977)."))
epr(id="lipov-2024", src="ep13", design="Preprint", n=1, cats=["Eating"], spec="Bulimia nervosa with PTSD", chronic=None, tr=None,
    tcat="Surgery or procedure (outside the brain)", tspec="Cervical sympathetic block for PTSD", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=0,
    summary="Bulimia symptoms disappeared after a cervical sympathetic block given for PTSD.",
    caveat="Preprint by a proponent of the block for PTSD; bulimia was partly framed as trauma-driven.", tags=["bulimia", "ptsd", "sympathetic-block", "preprint"],
    tier="C", flags=["preprint", "coi-trigger"])
epr(id="gong-2024", src="ep55", design="Letter", n=1, cats=["Eating"], spec="Binge eating disorder", chronic=None, tr=None,
    tcat="Medication for another condition", tspec="Semaglutide for obesity and type 1 diabetes", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=1,
    summary="Binge eating disorder symptoms resolved after semaglutide was started for obesity and type 1 diabetes.",
    caveat="Letter without an abstract; duration and measures need the full text.", tags=["binge-eating", "glp-1", "semaglutide"], tier="C",
    era=("emerging", ""))
epr(id="tsang-2023", src="ep66", design="Case report", n=1, cats=["Psychotic"], spec="Clozapine-resistant schizoaffective disorder with persistent auditory hallucinations",
    chronic=True, tr=True, tcat="Acquired brain lesion", tspec="Right superior temporal haemorrhagic stroke (ruptured AVM) and excision",
    intent="Injury or illness", res="Partial", rev="None reported", dl=1,
    summary="Auditory hallucinations that resisted clozapine and maintenance ECT stopped after a right temporal haemorrhage.",
    caveat="Symptom-level change; other features of the illness not reported.", tags=["hallucinations", "stroke", "temporal-lobe", "schizoaffective"],
    tier="B", era=("emerging", ""))
epr(id="sun-2023", src="ep75", design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="Tourette syndrome with temporal lobe epilepsy",
    chronic=True, tr=None, tcat="Neurosurgery", tspec="Temporal lobe epilepsy surgery", intent="Treatment for another condition",
    res="Partial", rev="None reported", dl=0,
    summary="Tourette syndrome improved after surgery for intractable temporal lobe epilepsy.",
    caveat="Antiepileptic changes after surgery could contribute.", tags=["tourette", "epilepsy-surgery"], tier="B")
epr(id="moccia-2022", src="ep81", design="Case report", n=1, cats=["Functional neurological"], spec="Functional movement disorder with treatment-resistant depression",
    chronic=True, tr=None, tcat="Medication for another condition", tspec="Weekly intranasal esketamine for treatment-resistant depression",
    intent="Treatment for another condition", res="Complete", rev="None reported", dl=1,
    summary="Functional movement symptoms remitted during esketamine treatment for depression.",
    caveat="Comorbid improvement; mood may mediate.", tags=["fnd", "esketamine", "comorbid"], tier="C", era=("emerging", ""))
epr(id="bright-2018", src="ep148", design="Case report", n=1, cats=["Mood"], spec="Depression with ankylosing spondylitis and chronic fatigue",
    chronic=True, tr=None, tcat="Surgery or procedure (outside the brain)", tspec="Autologous adipose stromal vascular fraction injection for osteoarthritis",
    intent="Treatment for another condition", res="Partial", rev="None reported", dl=0,
    summary="Depression lifted alongside ankylosing spondylitis and fatigue after stem-cell-fraction injections for osteoarthritis.",
    caveat="Authors are associated with a commercial cell-therapy provider; self-report outcomes.", tags=["depression", "stem-cells", "inflammation"],
    tier="C", flags=["coi-trigger"])
epr(id="funayama-2016", src="ep170", design="Case report", n=1, cats=["Mood"], spec="Treatment-resistant major depression for 14 years", chronic=True, tr=True,
    tcat="Acquired brain lesion", tspec="Subarachnoid haemorrhage damaging the orbitofrontal cortex and subgenual cingulate", intent="Injury or illness",
    res="Complete", rev="None reported", dl=1,
    summary="Fourteen years of treatment-resistant depression disappeared after a haemorrhage damaged the orbitofrontal and subgenual cingulate cortex.",
    caveat="Mild personality change accompanied the recovery.", tags=["depression", "haemorrhage", "subgenual-cingulate", "orbitofrontal"],
    tier="B", era=("emerging", "The subgenual cingulate is the target of DBS for depression (Mayberg 2005)."))
epr(id="jawaid-2016", src="ep173", design="Case report", n=1, cats=["Psychotic"], spec="Treatment-resistant schizophrenia", chronic=True, tr=True,
    tcat="Seizures", tspec="Clozapine-induced seizure", intent="Injury or illness", res="Complete", rev="None reported", dl=0,
    summary="Treatment-resistant schizophrenia remitted only after clozapine caused a seizure.",
    caveat="Clozapine response can be delayed.", tags=["schizophrenia", "clozapine", "seizure"], tier="B",
    era=("known", "Seizures relieving psychosis is the principle of convulsive therapy (Meduna, 1934)."))
epr(id="donoghue-2015", src="ep175", design="Case report", n=1, cats=["Trauma & stressor-related"], spec="PTSD with severe aggression and emotional dysregulation in a child",
    chronic=True, tr=True, tcat="Coma / anaesthesia", tspec="Procedural ketamine sedation", intent="Treatment for another condition",
    res="Temporary", rev="None reported", dl=1,
    summary="A child's refractory PTSD-related aggression remitted for 8–13 days after ketamine given for procedural sedation.",
    caveat="Effect was temporary; repeated observations strengthen it.", tags=["ptsd", "ketamine", "child", "anaesthesia"], tier="B",
    era=("emerging", "Ketamine's antidepressant effect in adults was known by 2015; the paediatric PTSD effect was not."))
epr(id="lauritsen-2015", src="ep178", design="Case report", n=1, cats=["Mood"], spec="Treatment-resistant depression for 3 years (many drug trials)", chronic=True, tr=True,
    tcat="Acquired brain lesion", tspec="Subarachnoid haemorrhage", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Three years of treatment-resistant depression resolved abruptly after a subarachnoid haemorrhage.",
    caveat="Danish-language paper with an English abstract.", tags=["depression", "haemorrhage"], tier="B", era=("emerging", ""))
epr(id="setsaas-2014", src="ep189", design="Case report", n=1, cats=["Mood"], spec="Treatment-resistant bipolar mania", chronic=None, tr=True,
    tcat="Fever / infection", tspec="Recurrent cycles of chills and fever", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Treatment-resistant mania appeared to resolve as a result of recurrent fevers.",
    caveat="Mania is episodic, so spontaneous resolution is a real alternative.", tags=["mania", "fever", "immune"], tier="B",
    era=("emerging", "Echoes fever therapy (Wagner-Jauregg)."))
epr(id="rosenblat-2013", src="ep193", design="Case report", n=1, cats=["Mood"], spec="Major depression refractory to medication and 15 ECT treatments",
    chronic=True, tr=True, tcat="Seizures", tspec="Accidental hypoglycaemic seizure (type 1 diabetes)", intent="Injury or illness",
    res="Complete", rev="None reported", dl=0,
    summary="Depression that 15 ECT treatments barely touched resolved completely after one accidental hypoglycaemic seizure.",
    caveat="Delayed ECT response cannot be excluded.", tags=["depression", "hypoglycaemia", "seizure", "ect-refractory"], tier="B",
    era=("known", "Seizure as antidepressant is the ECT principle; striking here because ECT had failed."))
epr(id="harrison-2013", src="ep197", design="Case report", n=1, cats=["Substance & addictive"], spec="Cannabis and nicotine use", chronic=True, tr=None,
    tcat="Medication for another condition", tspec="Broad-spectrum micronutrients taken for psychiatric symptoms such as ADHD",
    intent="Treatment for another condition", res="Partial", rev="On-off rechallenge", dl=0,
    summary="Cannabis and nicotine use fell on micronutrients taken for other psychiatric symptoms, rose when stopped and fell again when restarted.",
    caveat="The micronutrient formula is a commercial product promoted by this research group.", tags=["cannabis", "smoking", "micronutrients", "reversal"],
    tier="C", flags=["coi-trigger"])
epr(id="muskens-2012", src="ep200", design="Case report", n=1, cats=["Substance & addictive"], spec="Alcohol and nicotine addiction", chronic=True, tr=None,
    tcat="Acquired brain lesion", tspec="Dorsal striatal stroke", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Alcohol and nicotine addiction stopped after a stroke in the dorsal striatum, with abstinence at follow-up.",
    caveat="Single case; follow-up length needs the full text.", tags=["alcohol", "smoking", "stroke", "striatum"], tier="B",
    era=("known", "Fits the lesion-addiction literature after Naqvi 2007, pooled by Joutsa 2022."))
epr(id="mantione-2010", src="ep210", design="Case report", n=1, cats=["Substance & addictive"], spec="Nicotine dependence (with obesity and refractory OCD)",
    chronic=True, tr=None, tcat="Brain stimulation", tspec="Nucleus accumbens DBS for refractory OCD", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=2,
    summary="A woman given accumbens DBS for OCD quit smoking and lost weight without trying.",
    caveat="Smoking cessation was a side observation.", tags=["smoking", "dbs", "nucleus-accumbens", "ocd"], tier="B",
    era=("emerging", "Accumbens DBS for addiction has since reached pilot studies."))
epr(id="etches-2009", src="ep219", design="Case report", n=1, cats=["Mood", "Anxiety"], spec="Treatment-resistant bipolar II and panic disorder for 25 years",
    chronic=True, tr=True, tcat="Acquired brain lesion", tspec="Subarachnoid haemorrhage with vasospasm stroke", intent="Injury or illness",
    res="Complete", rev="None reported", dl=1,
    summary="Twenty-five years of treatment-resistant bipolar II and panic disorder resolved after a subarachnoid haemorrhage and stroke.",
    caveat="Stroke site and follow-up need the full text.", tags=["bipolar", "panic", "haemorrhage", "stroke"], tier="B", era=("emerging", ""))
epr(id="guarnieri-2005", src="ep232", design="Case series", n=2, cats=["Obsessive-compulsive & tic"], spec="OCD symptoms with intractable epilepsy",
    chronic=True, tr=None, tcat="Neurosurgery", tspec="Epilepsy surgery including unilateral anterior cingulate ablation", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=1,
    summary="Two men's obsessive-compulsive symptoms remitted after epilepsy surgery that ablated the anterior cingulate.",
    caveat="Seizure control may contribute.", tags=["ocd", "epilepsy-surgery", "cingulate"], tier="B", era=("emerging", "Anterior cingulotomy is a psychosurgical target for OCD."))
epr(id="thomas-2003", src="ep235", design="Letter", n=1, cats=["Mood", "Obsessive-compulsive & tic"], spec="Major depression with OCD",
    chronic=None, tr=None, tcat="Brain stimulation", tspec="A single unilateral ECT for depression", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=0,
    summary="Both major depression and OCD remitted after a single unilateral ECT treatment.",
    caveat="Letter without an abstract; a single ECT is an unusual dose.", tags=["ocd", "depression", "ect"], tier="C")
epr(id="levine-2003", src="ep236", design="Case series", n=2, cats=["Eating"], spec="Bulimia nervosa; anorexia nervosa", chronic=True, tr=None,
    tcat="Acquired brain lesion", tspec="Right temporal lesions (epileptogenic focus; head-injury encephalomalacia)", intent="Injury or illness",
    res="Complete", rev="None reported", dl=1,
    summary="Two women's eating disorders, one bulimia and one anorexia, resolved after right temporal brain lesions.",
    caveat="Mood also improved, which may mediate.", tags=["bulimia", "anorexia", "temporal-lobe", "lesion"], tier="B", era=("emerging", ""))
epr(id="de-filippis-2026", src="ep239", design="Preprint", n=2, cats=["Substance & addictive"], spec="Long-standing weekly intranasal cocaine use", chronic=True, tr=None,
    tcat="Medication for another condition", tspec="Tirzepatide for obesity", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=1,
    summary="Two people with obesity reported less cocaine craving and sustained abstinence on tirzepatide.",
    caveat="Preprint; not yet peer reviewed.", tags=["cocaine", "glp-1", "tirzepatide", "preprint"], tier="C", era=("emerging", ""), flags=["preprint"])
epr(id="viglione-2025", src="ep350", design="Case report", n=1, cats=["Catatonia"], spec="Catatonia", chronic=None, tr=None,
    tcat="Coma / anaesthesia", tspec="Propofol anaesthesia", intent="Treatment for another condition", res="Complete", rev="None reported", dl=1,
    summary="Catatonia resolved after propofol anaesthesia (Australian report).",
    caveat="Duration and prior treatment need the full text.", tags=["catatonia", "propofol", "anaesthesia", "australia"], tier="B", era=("emerging", ""))
epr(id="mira-2024", src="ep374", design="Letter", n=1, cats=["Substance & addictive"], spec="Cocaine use and dopamine dysregulation in Parkinson's disease",
    chronic=None, tr=None, tcat="Brain stimulation", tspec="Subthalamic nucleus DBS for Parkinson's disease", intent="Treatment for another condition",
    res="Partial", rev="None reported", dl=1,
    summary="Cocaine and dopamine-medication misuse improved after subthalamic DBS for Parkinson's disease.",
    caveat="Dopaminergic medication was likely reduced after DBS, which explains part of it.", tags=["cocaine", "parkinsons", "dbs", "stn"], tier="C",
    era=("emerging", ""))
epr(id="brasic-2018", src="ep658", design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="Gilles de la Tourette syndrome since age 7 (YGTSS 55)",
    chronic=True, tr=None, tcat="Physiological stress", tspec="Heat-induced dehydration: 3–4 hours in a 39–40°C hot tub", intent="Self-administered",
    res="Partial", rev="None reported", dl=0,
    summary="Tourette syndrome eased for two years (YGTSS 55 to 13) after hours in a very hot tub left him dehydrated.",
    caveat="First reported as a 2011 conference abstract; later follow-up in Durbin 2022.", tags=["tourette", "dehydration", "heat"], tier="B")

# ---------------- build records ----------------
existing = {r["id"] for r in d["records"]}
added = 0
for k in R:
    if k["id"] in existing:
        continue
    if k.get("src"):
        cit, ids, raw = bib_from(k["src"])
    else:
        cit, ids, raw = dict(authors="", title=None, journal="", year=0, volume="", issue="", pages=""), dict(doi="", pmid="", pmcid=""), None
    if k.get("m"):  # better identifiers and bibliographic detail from Europe PMC
        mc, mi, _ = bib_from("meta:" + k["m"])
        for f in ("authors", "journal", "volume", "issue", "pages"):
            if mc[f]:
                cit[f] = mc[f]
        for f in ("pmid", "pmcid"):
            ids[f] = mi[f] or ids[f]
        ids["doi"] = ids["doi"] or mi["doi"]
    for f in ("title", "authors", "journal", "year"):
        if k.get(f):
            cit[f] = k[f]
    if k.get("doi"):
        ids["doi"] = k["doi"]
    ids["doi"] = (ids["doi"] or "").lower()
    pmcid, pmid, doi = ids["pmcid"], ids["pmid"], ids["doi"]
    links = {"full_text": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/" if pmcid else None,
             "abstract": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
             "doi": f"https://doi.org/{doi}" if doi else None, "alternates": [],
             "ckn": ckn(doi) if doi else (raw or {}).get("ckn") or None}
    if raw and raw.get("id"):
        links["alternates"].append({"label": "Embase record (CKN login)", "url": f"https://www.embase.com/records?subaction=viewrecord&id={raw['id']}"})
    if not pmid and not pmcid and ids.get("pmcid") is None:
        pass
    era = k.get("era") or (("emerging" if k["dl"] >= 1 else "novel"), "")
    rec_out = {
        "id": k["id"], "record_type": "case", "status": "Provisional", "tier": k["tier"], "collections": ["phase1a"],
        "citation": cit, "ids": ids, "links": links,
        "access": "Free full text" if pmcid else "Paywalled",
        "design": k["design"], "n_patients": k["n"],
        "syndrome": {"categories": k["cats"], "specific": k["spec"], "chronic": k["chronic"], "treatment_resistant": k["tr"]},
        "trigger": {"category": k["tcat"], "specific": k["tspec"], "intent": k["intent"]},
        "outcome": {"resolution": k["res"], "time_to_resolution": None, "follow_up": None, "reversal": k["rev"]},
        "downstream": {"level": k["dl"], "note": "", "links": []},
        "summary": k["summary"], "caveat": k["caveat"], "tags": sorted(set(k["tags"])),
        "same_patient_as": k.get("same"), "found_via": k["via"], "date_added": TODAY,
        "verified": f"{TODAY}: abstract-level appraisal; identifiers from {'Europe PMC' if (pmid or pmcid) else 'Embase'}",
        "era": {"label": era[0], "note": era[1], "basis": "judged" if k.get("era") else "from downstream level"},
        "flags": k.get("flags", []),
    }
    d["records"].append(rec_out)
    added += 1

# CKN access link for every record with a DOI (locks in institutional access)
for r in d["records"]:
    r["links"].setdefault("ckn", None)
    if r["ids"]["doi"] and not r["links"]["ckn"]:
        r["links"]["ckn"] = ckn(r["ids"]["doi"])
    r.setdefault("flags", [])

d["schema_version"] = "1.2"
d["updated"] = TODAY
PATH.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
print(f"added {added}; total {len(d['records'])}")
