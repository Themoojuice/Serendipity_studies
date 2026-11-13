"""Batch 2026-11-13: citation route v1 (protocol v1.4), forward and backward citations of every library case.

Europe PMC `/{src}/{id}/citations` and `/references` for the 130 library cases with a PMID or PMCID, run in the
laptop browser: 4,561 links, 3,806 distinct records (48 library records, 133 already excluded, 104 already in the
ledger but unscreened, 3,521 new). Abstracts for all were fetched by ID and scored with
`queries/rerank_model_v1.json` (the v1.3 classifier); the 3,625 new or unscreened records were screened in that
order. Working files (not committed): /home/claude/work/raw/cit_v1.json, cit_ranked.json.

Stopping (protocol section 10): last possibly relevant record at classifier rank 633; ranks 634-933 are 300
consecutive irrelevant; a seeded random 300 of ranks 822-3,624 (seed 20261113,
`queries/stopping_sample_citation_v1_2026_11_13.json`) had 0 includes. Both criteria met. Ranks 934+ outside
the sample stay blank.

Result: 9 cases + 1 context record (Gaznick 2014), 6 unsure.
Run from the repo root:  python3 scripts/batches/b2026_11_13_citation_route_v1.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import U, Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-13"
QID, SRC = "CIT_EPMC_v1", "Europe PMC citations"
allr = json.loads((RAW / "cit_v1.json").read_text())            # [key, title, year, doi, pmid, first author, journal, via]
ranked = json.loads((RAW / "cit_ranked.json").read_text())       # [rank, key, score, pubtype, hasAbs]
SAMPLE = set(json.loads(Path("queries/stopping_sample_citation_v1_2026_11_13.json").read_text())["ranks"])
SCREENED_TO = 933

cand = {
    "9": dict(pmid="23128051", pmcid="", doi="", title="Improvements in anorexia symptoms after deep brain stimulation for intractable obsessive-compulsive disorder.", authorString="McLaughlin NC, Didie ER, Machado AG, Haber SN, Eskandar EN, Greenberg BD.", journal="Biol Psychiatry", year=2013, vol="73", issue="9", pages="e29-31", lang="eng"),
    "10": dict(pmid="8690834", pmcid="", doi="", title="Serotonin, psilocybin, and body dysmorphic disorder: a case report.", authorString="Hanes KR.", journal="J Clin Psychopharmacol", year=1996, vol="16", issue="2", pages="188-189", lang="eng"),
    "33": dict(pmid="34387923", pmcid="PMC9135119", doi="", title="Improvements in obsessive-compulsive disorder and schizophrenia after left putaminal hemorrhage.", authorString="Echizen K, Sakakibara E, Suga M, Kasai K.", journal="Psychiatry Clin Neurosci", year=2021, vol="75", issue="11", pages="354-355", lang="eng"),
    "88": dict(pmid="35263927", pmcid="", doi="", title="Refractory obsessive-compulsive disorder with symptoms regressing after thalamic infarction: A case report.", authorString="Erbay LG, Erbay MF, Kamışlı S, Demirbay S, Ünal S.", journal="Neurol India", year=2022, vol="70", issue="1", pages="399-401", lang="eng"),
    "121": dict(pmid="27351865", pmcid="", doi="", title="Remission of lifelong episodic dyscontrol after bilateral dorsolateral temporal lobe damage.", authorString="Coutinho G, Miele F, Moll J, Mattos P, de Oliveira-Souza R.", journal="Neurocase", year=2016, vol="22", issue="3", pages="339-345", lang="eng"),
    "122": dict(pmid="22291003", pmcid="", doi="", title="Effective treatment of Tourette's syndrome with marijuana.", authorString="Hemming M, Yellowlees PM.", journal="J Psychopharmacol", year=1993, vol="7", issue="4", pages="389-391", lang="eng"),
    "126": dict(pmid="3624208", pmcid="", doi="", title="Delirium and the resolution of depression.", authorString="Borchardt CM, Popkin MK.", journal="J Clin Psychiatry", year=1987, vol="48", issue="9", pages="373-375", lang="eng"),
    "185": dict(pmid="13148864", pmcid="", doi="", title="[Disappearance of grave obsessional phenomena after auto-lobotomy in a severely unbalanced individual].", authorString="Daumezon G, Cor J, Moor L.", journal="Ann Med Psychol (Paris)", year=1954, vol="112", issue="1", pages="93-97", lang="fre"),
    "271": dict(pmid="33867951", pmcid="PMC8046924", doi="", title="Disruption of Cigarette Smoking Addiction After Dorsal Striatum Damage.", authorString="Jing C, Jing C, Zheng L, Hong G, Zheng J, Yu L, Song N, Zhang T, Ma Q, Fang J.", journal="Front Behav Neurosci", year=2021, vol="15", issue="", pages="646337", lang="eng"),
    "633": dict(pmid="24169814", pmcid="PMC3954424", doi="", title="Basal ganglia plus insula damage yields stronger disruption of smoking addiction than basal ganglia damage alone.", authorString="Gaznick N, Tranel D, McNutt A, Bechara A.", journal="Nicotine Tob Res", year=2014, vol="16", issue="4", pages="445-453", lang="eng"),
}
LES = "Injury or illness"
R = [
    dict(id="mclaughlin-2013", src=9, design="Letter", n=1, cats=["Eating"], spec="Anorexia nervosa alongside intractable OCD",
         chronic=None, tr=None, tcat="Brain stimulation", tspec="Deep brain stimulation for intractable OCD",
         intent="Treatment for another condition", res="Partial", rev="None reported", dl=1,
         summary="Anorexia symptoms improved after deep brain stimulation given for intractable OCD.",
         caveat="The OCD improved too, and the eating disorder may have followed it.",
         tags=["dbs", "anorexia-nervosa", "ocd", "comorbidity"], tier="C",
         era=("emerging", "Deep brain stimulation for anorexia itself was being trialled from 2013 (recalled, not checked).")),
    dict(id="hanes-1996", src=10, design="Letter", n=1, cats=["Obsessive-compulsive & tic"], spec="Body dysmorphic disorder",
         chronic=None, tr=None, tcat="Recreational substance", tspec="Psilocybin", intent="Self-administered",
         res="Partial", rev="None reported", dl=1,
         summary="Body dysmorphic disorder improved with psilocybin use.",
         caveat="Self-administered, so expectancy and mood effects are likely.",
         tags=["psilocybin", "psychedelic", "body-dysmorphic-disorder", "serotonin"], tier="C",
         era=("emerging", "Psilocybin for body dysmorphic disorder has since had a small open-label trial (recalled, not checked).")),
    dict(id="echizen-2021", src=33, design="Letter", n=1, cats=["Obsessive-compulsive & tic", "Psychotic"],
         spec="OCD with schizophrenia", chronic=None, tr=None, tcat="Acquired brain lesion",
         tspec="Left putaminal haemorrhage", intent=LES, res="Partial", rev="None reported", dl=0,
         summary="Both OCD and schizophrenia improved after a left putaminal haemorrhage.", caveat="",
         tags=["putamen", "basal-ganglia", "haemorrhage", "ocd", "schizophrenia", "left"], tier="C"),
    dict(id="erbay-2022", src=88, design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="Refractory OCD",
         chronic=True, tr=True, tcat="Acquired brain lesion", tspec="Thalamic infarction", intent=LES,
         res="Partial", rev="None reported", dl=0,
         summary="Treatment-refractory OCD regressed after a thalamic infarct.", caveat="",
         tags=["thalamus", "infarct", "stroke", "ocd", "cstc-loop"], tier="C"),
    dict(id="coutinho-2016", src=121, design="Case report", n=1, cats=["Impulse-control"],
         spec="Lifelong episodic dyscontrol (recurrent aggressive outbursts)", chronic=True, tr=None,
         tcat="Traumatic brain injury", tspec="Bilateral dorsolateral temporal lobe injury", intent=LES,
         res="Complete", rev="None reported", dl=0,
         summary="A 45-year-old woman's lifelong outbursts of aggression stopped for good after a bilateral temporal lobe injury.",
         caveat="Personality change after brain injury can blunt drive in general, not aggression alone.",
         tags=["temporal-lobe", "bilateral", "aggression", "intermittent-explosive", "tbi", "personality-change"], tier="B"),
    dict(id="hemming-1993", src=122, design="Case report", n=1, cats=["Obsessive-compulsive & tic"], spec="Tourette syndrome",
         chronic=True, tr=None, tcat="Recreational substance", tspec="Marijuana", intent="Self-administered",
         res="Partial", rev="None reported", dl=2,
         summary="Tourette symptoms improved with marijuana, after the authors ruled out other treatments as the cause.",
         caveat="Tics wax and wane, and use was probably self-treatment.",
         tags=["cannabis", "marijuana", "thc", "tourette", "tics"], tier="C",
         era=("emerging", "THC was later tested in small randomised trials in Tourette syndrome (Müller-Vahl, early 2000s; recalled, not checked).")),
    dict(id="borchardt-1987", src=126, design="Case series", n=2, cats=["Mood"], spec="Long-standing depressive disorder",
         chronic=True, tr=None, tcat="Systemic illness", tspec="Protracted delirium during a flare of major medical illness",
         intent=LES, res="Complete", rev="None reported", dl=0,
         summary="Two patients' long-standing depression remitted after a protracted delirium during a flare of medical illness.",
         caveat="Recovery from the medical illness itself may have lifted the depression.",
         tags=["delirium", "depression", "medical-illness", "restitution"], tier="B"),
    dict(id="daumezon-1954", src=185, design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
         spec="Severe obsessional illness", chronic=None, tr=None, tcat="Traumatic brain injury",
         tspec="Self-inflicted frontal injury (self-lobotomy)", intent=LES, res="Complete", rev="None reported", dl=1,
         summary="Severe obsessional symptoms disappeared after a man injured his own frontal lobes.", caveat="",
         tags=["self-injury", "frontal-lobe", "lobotomy", "ocd", "historical"], tier="C",
         era=("known", "Prefrontal leucotomy for severe obsessional illness was in use by 1954; the injury reproduced it.")),
    dict(id="jing-2021", src=271, design="Lesion series", n=31, cats=["Substance & addictive"],
         spec="Cigarette smoking addiction", chronic=True, tr=None, tcat="Acquired brain lesion",
         tspec="Acute infarction involving the dorsal striatum (11 smokers, against 20 with infarcts elsewhere)",
         intent=LES, res="Partial", rev="None reported", dl=1,
         summary="Smokers whose infarcts involved the dorsal striatum quit more easily and without relapse than stroke controls.",
         caveat="Recruited by phone after discharge, so recall and survival bias apply.",
         tags=["dorsal-striatum", "caudate", "putamen", "stroke", "smoking", "lesion-series"], tier="B",
         era=("emerging", "Extends the insula finding (Naqvi 2007) to the dorsal striatum; compare Gaznick 2014.")),
    dict(id="gaznick-2014", src=633, record_type="context", design="Lesion series", n=63, cats=["Substance & addictive"],
         spec="Nicotine dependence in smokers with stroke", chronic=True, tr=None, tcat="Acquired brain lesion",
         tspec="Stroke damaging the basal ganglia, with or without the insula", intent=LES, res="Partial",
         rev="None reported", dl=1,
         summary="In 63 smokers followed for a year after stroke, basal ganglia damage, more so with insula involvement, "
                 "led to more and longer-lasting cessation than damage elsewhere.", caveat="",
         tags=["insula", "basal-ganglia", "stroke", "smoking", "prospective"], tier=None),
]

DEC = {
    9: "mclaughlin-2013", 10: "hanes-1996", 33: "echizen-2021", 88: "erbay-2022", 121: "coutinho-2016",
    122: "hemming-1993", 126: "borchardt-1987", 185: "daumezon-1954", 271: "jing-2021", 633: "gaznick-2014",
    0: (U, "no abstract: schizoaffective remission after pneumosepsis; possibly the same patient as Grootendorst-van Mil 2018"),
    1: (U, "no abstract: check whether the amygdala ablation was for epilepsy (as in Bijanki 2020) or aimed at the PTSD"),
    12: (U, "no abstract: temporal lobe epilepsy with obsessive-compulsive symptoms; outcome after treatment unknown"),
    264: (U, "letter, no abstract: coeliac disease with recurrent psychosis; did the gluten-free diet end the psychosis?"),
    292: (U, "letter, no abstract: smoking rose when ventral capsule/ventral striatum stimulation was withdrawn; check indication"),
    521: (U, "letter, no abstract: confirm minocycline was given for another condition (seed paper for minocycline in depression)"),
    15: ("E3", "gluten-free diet tried for the psychosis after antigliadin antibodies were found"),
    20: ("E8", "letter, no abstract: bulimia with temporal lobe epilepsy"),
    30: ("E2", "OCD began after an orbitofrontal contusion"),
    39: ("E2", "OCD began after a left basal ganglia infarct"),
    55: ("E3", "ketogenic diet given in a metabolic psychiatry clinic for the OCD"),
    74: ("E3", "ketamine given for intermittent explosive disorder"),
    82: ("E2", "PTSD began after amygdala-hippocampectomy"),
    111: ("E2", "dissociative flashbacks began after a frontal injury"),
    160: ("E3", "donepezil given for the Capgras delusion"),
    267: ("E4", "compulsions and coprolalia arose with the seizures and ended with tumour resection and seizure control"),
    364: ("E3", "propofol used as a lysis test for catatonia from limbic encephalitis"),
    599: ("E5", "prospective stroke cohort (insula and smoking); context only"),
    716: ("E5", "prospective stroke cohort (insula and smoking); context only"),
    878: ("E5", "prospective stroke cohort (insula and smoking urges); context only"),
}

if __name__ == "__main__":
    add_records(R, cand, collection="phase1c", found_via="Citation route v1 (Europe PMC citations and references)", today=TODAY)
    rank = {k: i for i, k, *_ in ranked}
    L = Ledger(TODAY)
    n = {"screened": 0, "blank": 0}
    for k, title, yr, doi, pmid, au, jn, via in allr:
        links = via.split(";")
        vtxt = f"{len(links)} link(s): " + ", ".join(links[:3]) + (" …" if len(links) > 3 else "")
        i = rank.get(k)
        if i is None:  # already in the library or already decided in the ledger
            dec, screened, rk = None, True, "already decided elsewhere in the ledger or in the library"
        elif i <= SCREENED_TO or i in SAMPLE:
            dec, screened = DEC.get(i), True
            rk = f"classifier rank {i}" + ("; stopping-rule random sample (seed 20261113)" if i in SAMPLE and i > SCREENED_TO else "")
        else:
            dec, screened, rk = None, False, f"classifier rank {i}; not screened (stopping rule met)"
        L.add(SRC, QID, dec, doi=(doi or "").lower(), pmid=pmid or "", other=k, title=title, au=au.split(" ")[0] if au else "",
              yr=yr, jn=jn, lang=cand.get(str(i), {}).get("lang", "") if i is not None else "",
              note=f"citation route v1; {rk}; {vtxt}; {TODAY}", screened=screened)
        n["screened" if screened else "blank"] += 1
    L.write()
    print(n)
    log_runs([(QID, "Europe PMC (browser)", "citations + references of 130 library cases (PMID/PMCID)", 3806, TODAY,
               "3,625 new or unscreened; classifier order; ranks 0-933 + random 300 screened; 9 cases + 1 context, 6 unsure; "
               "stopping rule met")])
