"""Batch 2026-11-14: antique sweep v1 (protocol v1.5), Europe PMC titles 1800-1969.

Two title queries, run in the laptop browser (period vocabulary, not modern terms):
  A: TITLE:(insanity OR melancholia OR mania OR "dementia praecox" OR lunacy OR hysteria OR obsessional OR
     delusions OR schizophrenia OR psychosis OR alcoholism OR dipsomania OR morphinism OR "opium habit" OR
     inebriety OR neurasthenia OR stupor OR catatonia ...) AND TITLE:(cure OR cured OR recovery OR recovered OR
     "influence of" OR disappearance OR remission OR relieved OR improvement ...) AND PUB_YEAR:[1800 TO 1969]  -> 305
  B: same syndrome block AND TITLE:(fever OR erysipelas OR typhoid OR pneumonia OR influenza OR malaria OR
     intercurrent OR "attack of" OR injury OR fracture OR trephining OR haemorrhage OR operation OR abscess OR
     childbirth OR coma ...) AND PUB_YEAR:[1800 TO 1969]  -> 333
604 distinct, 595 new to the ledger; every title screened. Most have no abstract, so decisions are title-level
and every include is Provisional with the antique-bar flag. Working file: /home/claude/work/raw/ant_new.json.

Result: 12 antique cases, 9 unsure (need the scanned full text, mostly free on PMC).
Run from the repo root:  python3 scripts/batches/b2026_11_14_antique_epmc_v1.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import CASES, U, Ledger, add_records, log_runs  # noqa: E402

RAW = Path("/home/claude/work/raw")
TODAY = "2026-11-14"
new = json.loads((RAW / "ant_new.json").read_text())
LANG = {306: "fre", 224: "fre"}


def cand_of(i):
    x = new[i]
    return dict(pmid=x["pmid"], pmcid=x["pmcid"], doi=x["doi"], title=x["title"], authorString=x["au"] or "Anonymous.",
                journal=x["jn"], year=int(x["yr"]), vol="", issue="", pages="", lang=LANG.get(i, "eng"))


INF, LIFE, TEST = "Injury or illness", "Life event", "Deliberate test (trial)"
OTHER = "Treatment for another condition"
FEVER_ERA = ("emerging", "Intercurrent fever ending insanity was a recurring 19th-century observation and led to "
                         "Wagner-Jauregg's fever therapy (1917); fever in modern psychosis is anecdotal.")
VEST_ERA = ("emerging", "Vestibular stimulation is being re-examined in functional and mood disorders (recalled, not checked).")
A = dict(chronic=None, tr=None, rev="None reported", tier="C", flags=["antique-bar"], caveat="")
R = [
    dict(A, id="anon-1844-pleuropneumonia", src=13, design="Case report", n=1, cats=["Mood"], spec="Acute mania",
         tcat="Fever / infection", tspec="Pleuropneumonia", intent=INF, res="Complete", dl=1, era=FEVER_ERA,
         summary="An acute mania was cured by an attack of pleuropneumonia.", tags=["fever", "pneumonia", "mania", "intercurrent-illness"],
         hist=("Acute mania", "Acute manic episode, possibly delirium", "An early instance of the intercurrent-illness cures that later underpinned fever therapy.")),
    dict(A, id="starr-1845", src=16, design="Case report", n=1, cats=["Psychotic"], spec="Insanity",
         tcat="Systemic illness", tspec="Gangrene and mortification of a limb", intent=INF, res="Complete", dl=1, era=FEVER_ERA,
         summary="A patient's insanity cleared after gangrene of a limb.", tags=["gangrene", "sepsis", "intercurrent-illness", "asylum"],
         hist=("Insanity", "Unspecified psychosis", "Recovery through a life-threatening septic illness, decades before anyone named inflammation.")),
    dict(A, id="perry-1869", src=42, design="Case report", n=1, cats=["Psychotic"], spec="Insanity",
         tcat="Surgery or procedure (outside the brain)", tspec="Extraction of carious teeth", intent=OTHER, res="Complete", dl=1,
         era=("refuted", "The focal-infection theory behind later mass tooth extraction for insanity (Cotton, 1920s) was discredited."),
         summary="Insanity was cured after decayed teeth were removed (reported in two dental journals).",
         caveat="Dental sepsis and pain may have been driving a delirium rather than a primary psychosis.",
         tags=["dental", "tooth-extraction", "focal-infection", "insanity"],
         hist=("Insanity", "Unclear; delirium from dental sepsis is possible", "Fifty years before Henry Cotton pulled teeth to cure psychosis, a dental cure was already in print.")),
    dict(A, id="anon-1890-influenza", src=75, design="Case report", n=1, cats=["Psychotic"], spec="Insanity",
         tcat="Fever / infection", tspec="Influenza (1889-90 pandemic)", intent=INF, res="Complete", dl=1, era=FEVER_ERA,
         summary="Insanity was cured by an attack of influenza during the 1889-90 pandemic.", tags=["influenza", "pandemic", "fever", "insanity"],
         hist=("Insanity", "Unspecified psychosis", "The same pandemic that produced influenzal psychoses also produced reported cures.")),
    dict(A, id="lanphear-1895", src=87, design="Case report", n=1, cats=["Psychotic"], spec="Insanity",
         tcat="Surgery or procedure (outside the brain)", tspec="Removal of an ovarian fibroid", intent=OTHER, res="Complete", dl=1,
         era=("refuted", "Reflex-insanity theory and gynaecological surgery for insanity (Battey's operation) were abandoned."),
         summary="A woman's insanity was cured after removal of a fibroid tumour of the ovary.",
         caveat="Gynaecological surgery was then sometimes done to cure insanity, so the intent needs checking.",
         tags=["gynaecological-surgery", "reflex-insanity", "ovary", "insanity"],
         hist=("Insanity (reflex insanity era)", "Unclear; possibly an affective or psychotic episode", "A window on reflex-insanity thinking, where pelvic organs were blamed for madness.")),
    dict(A, id="mckenzie-1912", src=133, design="Case report", n=1, cats=["Functional neurological"], spec="Hysterical deafness",
         tcat="Brain stimulation", tspec="Caloric vestibular test, done for diagnosis", intent=TEST, res="Complete", dl=1, era=VEST_ERA,
         summary="Hysterical deafness was cured by the caloric vestibular test used to diagnose it.",
         caveat="Suggestion during a dramatic test is the obvious alternative.",
         tags=["caloric-test", "vestibular", "functional-deafness", "hysteria", "diagnostic-test"],
         hist=("Hysterical deafness", "Functional hearing loss (functional neurological disorder)", "A diagnostic test doubling as the cure, the same move made in modern functional neurology.")),
    dict(A, id="cohen-lipton-1950", src=218, design="Case series", n=3, cats=["Psychotic"], spec="Schizophrenic psychoses",
         tcat="Life event", tspec="Death of the patient's mother", intent=LIFE, res="Complete", dl=0,
         summary="Three patients' schizophrenic psychoses remitted after their mothers died.",
         tags=["bereavement", "maternal-death", "schizophrenia", "family"],
         hist=("Schizophrenic psychoses", "Schizophrenia by 1950 American criteria, which were broad", "Read through the period's theory of the schizophrenogenic mother, but the observation stands on its own.")),
    dict(A, id="babinski-voltaic", src=224, design="Case report", n=1, cats=["Mood"], spec="Melancholia",
         tcat="Brain stimulation", tspec="Provoked attack of galvanic (voltaic) vertigo", intent=TEST, res="Complete", dl=1, era=VEST_ERA,
         summary="Melancholia was cured after Babinski provoked an attack of galvanic vertigo.",
         tags=["galvanic-vestibular-stimulation", "vestibular", "melancholia", "babinski"],
         hist=("Mélancolie", "Melancholic depression", "Babinski died in 1932, so this 1950 item reprints or recounts an earlier report (original date not checked).")),
    dict(A, id="thompson-1953", src=273, design="Case series", n=None, cats=["Psychotic"], spec="Psychosis with alcoholism",
         tcat="Medication for another condition", tspec="Conditioned-reflex (aversion) treatment for alcoholism", intent=OTHER,
         res="Partial", dl=0, summary="Psychosis improved after conditioned-reflex aversion treatment given for alcoholism.",
         caveat="Abstinence alone could explain the improvement if the psychosis was alcohol-related.",
         tags=["aversion-therapy", "emetine", "alcoholism", "psychosis"],
         hist=("Psychosis", "Uncertain mix of primary and alcohol-related psychosis", "Nausea-based aversion conditioning, now abandoned, with an unexpected psychiatric side-effect.")),
    dict(A, id="gardes-1954", src=306, design="Case report", n=1, cats=["Psychotic"], spec="Puerperal psychosis",
         tcat="Medication for another condition", tspec="Antituberculous medication", intent=OTHER, res="Complete", dl=2,
         era=("known", "Mood effects of the antituberculous hydrazides (iproniazid, isoniazid) led to the first antidepressants in 1957."),
         summary="A puerperal psychosis was cured during antituberculous treatment (1954, French).",
         tags=["isoniazid", "iproniazid", "tuberculosis", "puerperal-psychosis", "maoi"],
         hist=("Psychose puerpérale", "Postpartum psychosis", "Caught in the same year the antituberculous drugs were showing mood effects in sanatoria.")),
    dict(A, id="petersen-1956", src=334, design="Case report", n=1, cats=["Psychotic"], spec="Psychosis",
         tcat="Acquired brain lesion", tspec="Cerebral air embolism", intent=INF, res="Partial", dl=0,
         summary="A psychosis improved after a cerebral air embolism.", tags=["air-embolism", "brain-injury", "psychosis"],
         hist=("Psychosis", "Unspecified psychosis", "An accidental, diffuse brain insult acting like the shock treatments of its day.")),
    dict(A, id="cotlar-1957", src=357, design="Case report", n=1, cats=["Substance & addictive"], spec="Narcotic addiction",
         tcat="Coma / anaesthesia", tspec="Severe hypoglycaemic shock with coma (possible insulin hypersensitivity)", intent=INF,
         res="Complete", dl=1,
         era=("novel", "Echoes Sakel, whose insulin coma therapy grew from accidental hypoglycaemia during morphine withdrawal; never tested for addiction."),
         summary="Narcotic addiction remitted after a severe hypoglycaemic coma, possibly from insulin hypersensitivity.",
         caveat="Insulin was then used in withdrawal regimens, so the insulin may have been deliberate and only the shock accidental.",
         tags=["insulin", "hypoglycaemia", "coma", "opioid", "addiction"],
         hist=("Narcotic addiction", "Opioid use disorder", "Sakel's original accident, replayed thirty years later and aimed at the addiction this time.")),
]
INC = {13: "anon-1844-pleuropneumonia", 16: "starr-1845", 42: "perry-1869", 41: "perry-1869", 75: "anon-1890-influenza",
       87: "lanphear-1895", 133: "mckenzie-1912", 218: "cohen-lipton-1950", 224: "babinski-voltaic", 273: "thompson-1953",
       306: "gardes-1954", 334: "petersen-1956", 357: "cotlar-1957"}
DEC = dict(INC)
DEC.update({
    15: (U, "1845: insanity cured by a surgical operation; which operation, and for what?"),
    62: (U, "1881 asylum epidemic of erysipelas and enteric fever: did any patients' insanity improve?"),
    71: (U, "1888: influence of typhoid fever upon insanity; check for individual cures"),
    99: (U, "1897: morphine habit cured by bromide poisoning; accidental overdose or a deliberate bromide withdrawal cure?"),
    111: (U, "1902: influence of acute diseases upon insanity; possible context record or case series"),
    202: (U, "1948: early schizophrenia complicated by rheumatic fever; outcome unknown"),
    318: (U, "1955: stupor of more than seven years with recovery; what preceded recovery?"),
    480: (U, "1963 (Russian): effect of brain injury on the course of schizophrenia"),
    524: (U, "1966 (Italian): psychoses during intercurrent viral hepatitis, 200 cases; check for remissions"),
    353: ("E3", "improvement with massive doses of chlorpromazine"), 372: ("E3", "improvement with chlorpromazine"),
    241: ("E3", "prefrontal lobotomy aimed at the psychosis; the hypertension also resolved"),
})

if __name__ == "__main__":
    cand = {str(k["src"]): cand_of(k["src"]) for k in R}
    hist = {k["id"]: k.pop("hist") for k in R}
    add_records(R, cand, collection="antique", found_via="Antique sweep v1 (Europe PMC titles 1800-1969)", today=TODAY)
    d = json.loads(CASES.read_text())
    for r in d["records"]:
        if r["id"] in hist:
            o, m, w = hist[r["id"]]
            r["historical"] = {"original_terms": o, "modern_reading": m, "why_read": w}
            if r["id"] == "perry-1869":
                r["links"]["alternates"] = [{"label": "Dental Register reprint (PMC)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6910379/"}]
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    L = Ledger(TODAY)
    for i, x in enumerate(new):
        L.add("Europe PMC", "EPMC_antique_v1", DEC.get(i), doi=x["doi"], pmid=x["pmid"], pmcid=x["pmcid"], other=x["k"],
              title=x["title"], au=(x["au"] or "").split(" ")[0], yr=x["yr"], jn=x["jn"], lang=LANG.get(i, ""),
              note=f"antique sweep v1, title list {i} (queries {'+'.join('AB'[q] for q in x['q'])}); {TODAY}")
    L.write()
    log_runs([("EPMC_antique_v1", "Europe PMC (browser)", "A: period syndrome terms AND recovery terms in title, 1800-1969", 305, TODAY, ""),
              ("EPMC_antique_v1", "Europe PMC (browser)", "B: period syndrome terms AND trigger terms in title, 1800-1969", 333, TODAY,
               "604 distinct, 595 new, all titles screened; 12 antique cases, 9 unsure")])
