"""Batch 2026-11-14: APA PsycInfo via CKN (EBSCO), title-restricted query PSY_title_v1 (protocol v1.7).

Query (queries/strings_psycinfo_v1.json): TI(syndrome terms) AND TI(resolution or unexpectedness terms) AND
(TI or AB case-report terms), db=psyh, 1,075 hits on 2026-11-14. Run through the EBSCO advanced-search UI with Brendan
signed in; the result list was read 50 per page from the page itself (no export, no other endpoints).

Extraction fix: the first pass paired some titles with the authors, source and abstract of a neighbouring record
(194 of 1,075). Every page was re-read with a per-record extractor before any decision was written, and candidate
decisions were re-made on the corrected abstracts. Titles were never affected.

Matching: by normalised title against current ledger rows. 256 records were already in the ledger (41 of them library
cases, plus Wilcox 2008 under a variant title); 819 were new or blank and were ranked with the v1.3 classifier.
All 819 titles were screened (no stopping rule needed); abstracts read for every candidate. PsycInfo abstracts also
settled 11 earlier unsure rows (corrections below, written under the original database's row).

Result: 16 new cases + 1 context record (Vender 1990), 2 cases found through earlier unsure rows (Liu 2016, Nguyen 2021,
both included in the 16). Working files: /home/claude/work/raw/psy_v2.json, psy_todo_v2.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_14_psycinfo_v1.py
"""
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, "scripts")
from lib_add import CASES, LEDGER, U, Ledger, add_records, log_runs  # noqa: E402

TODAY = "2026-11-14"
QID = "PSY_title_v1"
SRC = "PsycInfo via CKN (EBSCO)"
RAW = Path("/home/claude/work/raw")
V = json.loads((RAW / "psy_v2.json").read_text())          # [id, title, authors, source, type, abstract]
todo = json.loads((RAW / "psy_todo_v2.json").read_text())  # [id, score, title, authors, source, type, new|blank]
RANK = {x[0]: (i, x[1]) for i, x in enumerate(todo)}
CKN = "https://go.openathens.net/redirector/ckn.qldhealth.com?url="
OTHER = "Treatment for another condition"


def ebsco_url(rid):
    return CKN + quote(f"https://research.ebsco.com/c/lrpoh2/details/{rid}?db=psyh", safe="")


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:80]


def parse_src(src):
    src = re.sub(r"APA PsycInfo$", "", src).strip()
    m = re.search(r",[^,]*?\b(1[6-9]\d\d|20\d\d)\b", src)
    return (src[:m.start()].strip(), m.group(1)) if m else (src, "")


def pm(pmid, doi, title, au, jn, yr, vol, iss, pages, lang="eng", pmcid=""):
    return dict(pmid=pmid, pmcid=pmcid, doi=doi, title=title, authorString=au, journal=jn, year=yr, vol=vol, issue=iss,
                pages=pages, lang=lang)


# Bibliographic fields from PubMed (PMIDs matched by citation on 2026-11-14), else from the PsycInfo record.
cand = {
    "0": pm("39851087", "10.1017/cjn.2025.2", "Transient Resolution of Tics After Left Temporal Lobe Resection for Refractory Epilepsy.",
            "Ripsman DA, Ahmadi Karvigh S, Kiaei S, Fitzpatrick W, Moien-Afshari F", "Can J Neurol Sci", 2025, "", "", "1-3"),
    "3": pm("11593287", "10.1590/s0004-282x2001000500028", "Complete remission of epileptic psychosis after temporal lobectomy: case report.",
            "Marchetti RL, Tavares AG, Gronich G, Fiore LA, Ferraz RB", "Arq Neuropsiquiatr", 2001, "59", "3-B", "802-5"),
    "10": pm("11056831", "", "Sudden remission of obsessive-compulsive disorder by involuntary, massive exposure.",
             "Fontenelle L, Soares ID, Marques C, Rangé B, Mendlowicz MV, Versiani M", "Can J Psychiatry", 2000, "45", "7", "666-7"),
    "20": pm("2366060", "10.1097/00005053-199007000-00008", "Resolution of psychotic depression after right temporoparietal infarction.",
             "Chimowitz MI, Furlan AJ", "J Nerv Ment Dis", 1990, "178", "7", "458-9"),
    "93": pm("1958969", "10.1192/bjp.159.3.446b", "A case of depression responding to spontaneous epilepsy but not ECT.",
             "Silverstone P, Fahy T", "Br J Psychiatry", 1991, "159", "", "446-7"),
    "117": pm("40633788", "10.1016/j.jpainsymman.2025.06.015", "Acute Amnesia Resulting in Complete Relief of Pain, Depression, and Anxiety.",
              "Ohmura J, Sussman CB, Zamani A, Nedeljkovic SS, Lyndon S", "J Pain Symptom Manage", 2025, "70", "4", "e280-e283"),
    "129": pm("18892877", "10.1001/archneurpsyc.1948.02300400082005",
              "Prognostic significance of incidental acute somatic disorders in the course of psychoses; reevaluation of five cases 14 years later.",
              "Gordon A", "Arch Neurol Psychiatry", 1948, "59", "5", "646-52"),
    "153": pm("12490350", "10.1016/s0163-8343(02)00212-8", "Depression improvement with calcium heparin.",
              "Maluquer SS, Arranz B, San L", "Gen Hosp Psychiatry", 2002, "24", "6", "450-1"),
    "160": pm("", "", "Recovery from bulimia nervosa through near-death experience: A case study.",
              "Colli JE, Beck TE", "Journal of Near-Death Studies", 2003, "22", "1", "33-55"),
    "227": pm("16340210", "10.1159/000090109", "Improvement of obsessive-compulsive disorder following left putaminal hemorrhage.",
              "Fujii T, Otsuba Y, Suzuki K, Endo K, Yamadori A", "Eur Neurol", 2005, "54", "3", "166-70"),
    "325": pm("", "", "Lo schizofrenico e la malattia somatica. A proposito di sorprendenti remissioni dei sintomi psicotici.",
              "Vender S, Sommi M, Mazzacane F", "Archivio di Psicologia, Neurologia e Psichiatria", 1990, "51", "2", "247-263", lang="ita"),
    "333": pm("10349592", "10.1002/(sici)1098-108x(199907)26:1<107::aid-eat15>3.0.co;2-u",
              "Complete recovery from intractable bulimia nervosa by the surgical cure of primary hyperparathyroidism.",
              "Ozawa Y, Koyano H, Akama T", "Int J Eat Disord", 1999, "26", "1", "107-10"),
    "387": pm("16476139", "10.1111/j.1440-1614.2006.01774_2.x", "Stevens-Johnson syndrome (SJS) leading to resolution of mania.",
              "Arora M, Praharaj SK", "Aust N Z J Psychiatry", 2006, "40", "2", "193-4"),
    "427": pm("1801768", "10.1176/ajp.148.6.809a", "Catatonia unexpectedly reversed by midazolam.",
              "Delisle JD", "Am J Psychiatry", 1991, "148", "6", "809"),
    "565": pm("23855864", "10.1111/jgs.12332",
              "Recurrent and consistent improvement of cognitive impairment and depression after short time of treatment with enoxaparin.",
              "Feldinger LE", "J Am Geriatr Soc", 2013, "61", "7", "1240-1"),
    "758": pm("30198320", "10.1177/1039856218797441", "Improvement of late life depression after therapeutic enoxaparin: two case reports.",
              "Graham D, Wu QX, Gilligan I, Ismail R, Walker M", "Australas Psychiatry", 2018, "26", "5", "534-536"),
    "liu": pm("26560841", "10.1177/0004867415616697",
              "Refractory depression with catatonic features was remitted with administration of intravenous dopamine and consequent bupropion as maintenance treatment.",
              "Liu YW, Chang C, Chen TY, Chang HA, Kao YC, Tzeng NS", "Aust N Z J Psychiatry", 2016, "50", "6", "599"),
    "nguyen": pm("33217127", "10.1111/bdi.13032", "Schizoaffective disorder: Symptom remission following pneumosepsis.",
                 "Nguyen M, Varapravan S, Sharma V", "Bipolar Disord", 2021, "23", "4", "423-425"),
}
NO_DOI = {"160": "p67toh2p6z", "325": "qhvlzgbxob"}
HEPARIN = ("emerging", "Three separate reports (2002, 2013, 2018) of depression lifting on heparins given for clotting; "
                       "no trial found so far.")

R = [
    dict(id="ripsman-2025", src=0, design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
         spec="Severe Tourette syndrome with motor and vocal tics", chronic=True, tr=None, tcat="Neurosurgery",
         tspec="Left (dominant) mesial anterior temporal lobectomy for drug-resistant epilepsy", intent=OTHER, res="Temporary",
         rev="None reported", dl=0,
         summary="Severe motor and vocal tics cleared for a time after a left anterior temporal lobectomy for drug-resistant "
                 "epilepsy. The two earlier reports the authors cite went the other way: tics worsened after right-sided resections.",
         caveat="Tics wax and wane on their own, so a lull after surgery can be coincidence.",
         tags=["tourette", "tics", "temporal-lobectomy", "epilepsy-surgery", "left-temporal"], tier="C"),
    dict(id="marchetti-2001", src=3, design="Case report", n=1, cats=["Psychotic"],
         spec="Chronic, treatment-refractory interictal psychosis of temporal lobe epilepsy (right mesial temporal sclerosis)",
         chronic=True, tr=True, tcat="Neurosurgery", tspec="Right temporal lobectomy for refractory complex partial seizures",
         intent=OTHER, res="Complete", rev="None reported", dl=0,
         summary="A 47-year-old woman whose postictal psychoses had become a chronic, refractory interictal psychosis was "
                 "seizure-free and psychosis-free after a right temporal lobectomy; long-standing personality traits stayed.",
         caveat="The psychosis grew out of the epilepsy, so removing the seizure focus may simply have removed its cause.",
         tags=["epilepsy-surgery", "temporal-lobectomy", "right-temporal", "interictal-psychosis", "mesial-temporal-sclerosis"], tier="C"),
    dict(id="fontenelle-2000", src=10, design="Letter", n=1, cats=["Obsessive-compulsive & tic"],
         spec="Extreme OCD with HIV-contamination fears, avoidance and rituals", chronic=None, tr=None, tcat="Life event",
         tspec="One involuntary, massive exposure to avoided stimuli, following a panic attack with marked depersonalisation",
         intent="Life event", res="Complete", rev="None reported", dl=0,
         era=("known", "Exposure with response prevention was the standard behavioural treatment for OCD by 2000; the surprise "
                       "is complete remission after a single unplanned, involuntary exposure."),
         summary="A 32-year-old taxi driver, terrified of carrying HIV home from his passengers, remitted completely after a "
                 "panic attack with depersonalisation left him unable to go on with his rituals: one massive, involuntary exposure.",
         caveat="A depressive or dissociative shift after the panic attack could have blunted the obsessional drive rather than extinguished it.",
         tags=["ocd", "exposure", "panic-attack", "depersonalisation", "single-session"], tier="C"),
    dict(id="chimowitz-1990", src=20, design="Case report", n=1, cats=["Mood", "Psychotic"],
         spec="Agitated psychotic depression", chronic=None, tr=None, tcat="Acquired brain lesion",
         tspec="Right temporoparietal infarct", intent="Injury or illness", res="Complete", rev="None reported", dl=0,
         summary="An agitated, psychotically depressed 70-year-old man had a right temporoparietal stroke, swung briefly into "
                 "hypomania, then returned to his usual mood from before the depression.",
         caveat="He may already have been responding to antidepressant treatment; the full text should say what he was on.",
         tags=["stroke", "right-hemisphere", "temporoparietal", "psychotic-depression", "hypomania"], tier="C"),
    dict(id="silverstone-1991", src=93, design="Letter", n=1, cats=["Mood"],
         spec="Severe depression in long-standing manic-depressive illness, unresponsive to repeated ECT", chronic=None, tr=True,
         tcat="Seizures", tspec="Spontaneous grand mal seizures (indexing points to drug withdrawal and carbamazepine)",
         intent="Injury or illness", res="Partial", rev="None reported", dl=0,
         era=("known", "Convulsive therapy rests on the antidepressant effect of seizures (1938); the surprise is spontaneous "
                       "seizures working after repeated ECT had not."),
         summary="A severely depressed 67-year-old man with long-standing manic-depressive illness improved after spontaneous "
                 "grand mal seizures, though repeated ECT had done nothing.",
         caveat="If the seizures came from stopping a drug, the drug change could itself explain the mood shift.",
         tags=["seizures", "ect", "spontaneous-seizure", "depression", "carbamazepine"], tier="C"),
    dict(id="ohmura-2025", src=117, design="Letter", n=1, cats=["Mood", "Anxiety"],
         spec="Depression and anxiety for 6.5 years with chronic pain, through many drug combinations and spinal fusion",
         chronic=True, tr=True, tcat="Acquired brain lesion",
         tspec="Acute brain injury leaving her amnesic (headache, confusion, slurred speech, unsteady gait)",
         intent="Injury or illness", res="Complete", rev="None reported", dl=0,
         summary="A 44-year-old woman lost her chronic pain, depression and anxiety all at once after an acute brain injury "
                 "left her amnesic. The authors propose memory as the common thread holding the three in place.",
         caveat="If her opioids or other medicines were stopped or changed in hospital, that alone could shift pain and mood.",
         tags=["amnesia", "memory", "chronic-pain", "depression", "anxiety", "brain-injury", "opioids"], tier="C"),
    dict(id="gordon-1948", src=129, design="Case series", n=5, cats=["Psychotic"],
         spec="Intermittent psychotic attacks (period diagnoses)", chronic=None, tr=None, tcat="Fever / infection",
         tspec="Incidental lobar or bronchopneumonia and other acute somatic illness", intent="Injury or illness",
         res="Complete", rev="None reported", dl=1, flags=["antique-bar"], observed=1934,
         era=("known", "Psychosis easing during intercurrent fever was long recognised and underlay malaria therapy "
                       "(Wagner-Jauregg, 1917); a lasting cure was not expected."),
         hist=("Definite intermittent psychotic symptoms; incidental acute somatic disorders (lobar and bronchopneumonia)",
               "Recurrent psychotic episodes of uncertain diagnosis (periodic psychosis, bipolar or schizoaffective illness)",
               "Fourteen years of follow-up is rare in this literature, and Gordon sets the illness effect beside the new shock therapies."),
         summary="Five patients with recurrent psychotic attacks stopped having them after an incidental pneumonia or other "
                 "acute illness, and were still free of attacks when re-examined 14 years later.",
         caveat="Recurrent psychoses can burn out over 14 years without help, and the abstract gives no diagnoses.",
         tags=["pneumonia", "intercurrent-illness", "fever", "shock-therapy", "long-follow-up"], tier="C"),
    dict(id="maluquer-2002", src=153, design="Letter", n=1, cats=["Mood"],
         spec="Recurrent depression resistant to conventional antidepressants", chronic=None, tr=True,
         tcat="Medication for another condition", tspec="Subcutaneous calcium heparin as thrombosis prophylaxis after hip replacement",
         intent=OTHER, res="Complete", rev="None reported", dl=1, era=HEPARIN,
         summary="A 64-year-old man with recurrent, antidepressant-resistant depression recovered fully in hospital after a hip "
                 "replacement, on unchanged fluoxetine plus prophylactic calcium heparin. The abstract breaks off as heparin is "
                 "stopped two months later; the indexing ('recurrence') hints at relapse.",
         caveat="Relief from a painful hip after major surgery can lift mood on its own.",
         tags=["heparin", "anticoagulant", "thromboprophylaxis", "depression", "vascular-depression"], tier="C"),
    dict(id="colli-2003", src=160, design="Case report", n=1, cats=["Eating"],
         spec="Bulimia nervosa, framed by the authors as complex PTSD after childhood abuse", chronic=None, tr=None,
         tcat="Life event", tspec="Near-death experience during a suicide attempt", intent="Life event", res="Complete",
         rev="None reported", dl=0,
         summary="A woman recovered from bulimia nervosa after a near-death experience during a suicide attempt; the authors, "
                 "who revisited the experience with her under hypnosis, credit what it taught her about choice.",
         caveat="Recovery unfolded alongside psychotherapy and hypnotic regression, which may have done the work.",
         tags=["near-death-experience", "suicide-attempt", "bulimia", "hypnosis", "psychological-trigger"], tier="C"),
    dict(id="fujii-2005", src=227, design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
         spec="OCD since age 43 (15 years)", chronic=True, tr=None, tcat="Acquired brain lesion",
         tspec="Left putaminal haemorrhage (untreated hypertension)", intent="Injury or illness", res="Partial",
         rev="None reported", dl=0,
         summary="A 58-year-old man who had had OCD since 43 improved after a left putaminal haemorrhage.",
         caveat="", tags=["ocd", "basal-ganglia", "putamen", "haemorrhage", "left-hemisphere"], tier="C"),
    dict(id="ozawa-1999", src=333, design="Case report", n=1, cats=["Eating"],
         spec="Bulimia nervosa for over 10 years (binge eating, self-induced vomiting)", chronic=True, tr=True,
         tcat="Surgery or procedure (outside the brain)", tspec="Parathyroidectomy for primary hyperparathyroidism",
         intent=OTHER, res="Complete", rev="None reported", dl=0,
         summary="A 29-year-old Japanese woman's bulimia of more than 10 years stopped completely once surgery cured her "
                 "primary hyperparathyroidism; her depression and anxiety eased too.",
         caveat="Hypercalcaemia causes nausea and vomiting, so part of the bulimic picture may have come from the hyperparathyroidism itself.",
         tags=["hyperparathyroidism", "calcium", "parathyroidectomy", "bulimia", "endocrine"], tier="C"),
    dict(id="arora-2006", src=387, design="Letter", n=1, cats=["Mood"],
         spec="Mania with psychotic features (YMRS 53), worsening again on carbamazepine, olanzapine and lithium after ECT",
         chronic=False, tr=None, tcat="Systemic illness", tspec="Stevens-Johnson syndrome", intent="Injury or illness",
         res="Complete", rev="None reported", dl=0,
         summary="A 23-year-old man's psychotic mania, sliding back after ECT despite carbamazepine, olanzapine and lithium, "
                 "resolved after he developed Stevens-Johnson syndrome.",
         caveat="He had been getting worse on carbamazepine, so stopping it once the reaction appeared is a competing explanation.",
         tags=["stevens-johnson", "mania", "carbamazepine", "intercurrent-illness", "immune"], tier="C"),
    dict(id="delisle-1991", src=427, design="Letter", n=1, cats=["Catatonia", "Psychotic"],
         spec="Catatonia in schizophrenia after stopping maintenance medication", chronic=None, tr=None,
         tcat="Medication for another condition", tspec="Midazolam premedication for an endoscopy", intent=OTHER,
         res="Temporary", rev="On-off rechallenge", dl=4,
         era=("known", "Benzodiazepine reversal of catatonia had been reported from the early 1980s (lorazepam; recalled, not "
                       "checked) and the lorazepam challenge later became standard; in 1991 it was still news to many."),
         summary="A 24-year-old woman with schizophrenia, catatonic after stopping her maintenance medication, came out of it "
                 "briefly when given midazolam before an endoscopy, and again on two later doses. Published replies note that "
                 "ECT was not possible.",
         caveat="", tags=["midazolam", "benzodiazepine", "catatonia", "premedication", "rechallenge"], tier="B"),
    dict(id="feldinger-2013", src=565, design="Letter", n=1, cats=["Mood"],
         spec="New depression with cognitive decline in an 88-year-old", chronic=None, tr=None,
         tcat="Medication for another condition", tspec="Short courses of enoxaparin (indexing lists a fall and hip fracture)",
         intent=OTHER, res="Partial", rev="None reported", dl=1, era=HEPARIN,
         summary="An 88-year-old man with new depression and cognitive decline improved after short courses of enoxaparin; the "
                 "title reports the improvement recurring and consistent, so the full text may show repeated on-off courses.",
         caveat="Delirium after a hip fracture can look like depression with cognitive decline and clear as the patient recovers.",
         tags=["enoxaparin", "heparin", "anticoagulant", "depression", "cognition", "older-adult"], tier="C"),
    dict(id="graham-2018", src=758, design="Case series", n=2, cats=["Mood"], spec="Late-life depression in inpatients",
         chronic=None, tr=None, tcat="Medication for another condition", tspec="Therapeutic enoxaparin for pulmonary embolism",
         intent=OTHER, res="Partial", rev="None reported", dl=1, era=HEPARIN,
         summary="Two older inpatients being treated for depression developed pulmonary emboli; both improved markedly once on "
                 "therapeutic enoxaparin, with nothing else in their depression treatment changed.",
         caveat="Treating a pulmonary embolism relieves breathlessness, hypoxia and fear, any of which weighs on mood.",
         tags=["enoxaparin", "heparin", "pulmonary-embolism", "late-life-depression", "vascular-depression"], tier="C"),
    dict(id="liu-2016", src="liu", design="Letter", n=1, cats=["Mood", "Catatonia"],
         spec="Treatment-refractory depression with catatonic features", chronic=None, tr=True,
         tcat="Medication for another condition", tspec="Intravenous dopamine for septic shock from urosepsis, then bupropion maintenance",
         intent=OTHER, res="Complete", rev="None reported", dl=0,
         summary="An older woman with refractory catatonic depression, septic after urinary retention, came out of it when "
                 "intravenous dopamine was given for septic shock; bupropion then kept her well.",
         caveat="Treating the sepsis and retention removed a medical stressor that can deepen catatonia.",
         tags=["dopamine", "catatonia", "septic-shock", "bupropion", "depression"], tier="C"),
    dict(id="nguyen-2021", src="nguyen", design="Case report", n=1, cats=["Psychotic", "Mood"],
         spec="Schizoaffective disorder, bipolar type", chronic=None, tr=None, tcat="Fever / infection",
         tspec="Presumed pneumosepsis treated with broad-spectrum antibiotics", intent="Injury or illness", res="Complete",
         rev="None reported", dl=1,
         summary="A 56-year-old man with schizoaffective disorder, partway through a switch to clozapine, developed presumed "
                 "pneumosepsis; his symptoms remitted and he stayed well afterwards on a simpler regimen without clozapine.",
         caveat="Infection raises clozapine levels (as in Grootendorst-van Mil 2018), so a brief clozapine surge may have done the work.",
         tags=["sepsis", "pneumonia", "intercurrent-illness", "clozapine", "schizoaffective"], tier="C"),
    dict(id="vender-1990", src=325, record_type="context", design="Review", n=None, cats=["Psychotic"],
         spec="Schizophrenia", chronic=True, tr=None, tcat="Systemic illness", tspec="Intercurrent physical illness",
         intent="Injury or illness", res="Temporary", rev="None reported", dl=1,
         summary="An Italian discussion, with several case histories, of psychotic symptoms in schizophrenia lifting for a "
                 "while during physical illness; an earlier paper from the group behind Vender 1996.",
         caveat="", tags=["intercurrent-illness", "schizophrenia", "pseudo-recovery"], tier=None),
]

# Decisions by rank in the classifier-ordered list of 819 (psy_todo_v2.json). Unlisted ranks: title-level exclusion.
SPONT = "no off-target exposure; recovery with ordinary care or the natural course (criterion 3, T4)"
DEC = {0: "ripsman-2025", 3: "marchetti-2001", 10: "fontenelle-2000", 20: "chimowitz-1990", 22: "wilcox-2008",
       93: "silverstone-1991", 117: "ohmura-2025", 129: "gordon-1948", 153: "maluquer-2002", 160: "colli-2003",
       227: "fujii-2005", 325: "vender-1990", 333: "ozawa-1999", 387: "arora-2006", 427: "delisle-1991",
       565: "feldinger-2013", 758: "graham-2018",
       8: ("E4", "depression attributed to tricyclic toxicity, improving once the tricyclics stopped"),
       26: ("E3", "remission of eating disorders in pregnancy was already a recognised pattern by 2009 (the authors say so); fails T2"),
       43: ("E3", "deep brain stimulation aimed at the OCD; benefit persisted after removal"),
       55: ("E4", "psychosis attributed to lamotrigine, remitting on withdrawal"),
       83: ("E3", "penicillin given for presumed PANDAS"),
       111: ("E4", "psychosis remitting after resection of a cerebellar lesion (Lhermitte-Duclos disease)"),
       122: ("E4", "psychosis easing as testosterone replacement was reduced"),
       131: ("E3", "late-onset psychosis remitting with no identified exposure; " + SPONT),
       138: ("E3", "activated charcoal given deliberately to treat the mania (gut-inflammation hypothesis)"),
       145: ("E2", "kleptomania worsened after subarachnoid haemorrhage"),
       197: ("E3", "persuasion by a psychiatrist aimed at the psychosis"),
       218: ("E4", "bipolar symptoms tied to vitamin D deficiency, relieved by supplementation"),
       231: ("E3", "hallucinations changing with the patient's own dose changes of prescribed antipsychotics"),
       233: ("E3", "ascorbic acid given to treat the obsessional neurosis"),
       246: ("E3", "prostaglandin E1 given to treat the depression and delirium"),
       247: ("E2", "hallucinations changed, not resolved, after orchidopexy"),
       296: ("E7", "reply about the included DeLisle 1991 case (ECT was not possible)"),
       303: ("E3", "finasteride given as an experimental treatment for the psychosis"),
       315: ("E1", "diagnostic report: CSF findings in schizophrenia-like encephalitis"),
       359: ("E3", "seven-year depression lifting with the natural course; " + SPONT),
       391: ("E3", "methylphenidate chosen to treat the catatonia"),
       413: ("E2", "anorexia nervosa with spontaneous intracranial hypotension; the headache resolved, not the eating disorder"),
       421: ("E3", "two acute psychoses recovering with ordinary hospital care; " + SPONT),
       435: ("E2", "chlorpromazine worsened agitation in periodic catatonia"),
       463: (U, "single EMDR session followed by remission of treatment-resistant schizophrenia; was EMDR aimed at the psychosis "
               "(the authors reframe it as traumatic dissociation)? PMC full text free"),
       467: (U, "antique (1952): 'criminally insane' patient improved dramatically after playing Gessler in a staging of Wilhelm "
               "Tell; diagnosis, and whether the play was meant as therapy, need the full text"),
       469: ("E4", "depression accompanying undiagnosed Guillain-Barre syndrome"),
       523: ("E4", "negative symptoms improving as obstructive sleep apnoea was treated with CPAP"),
       532: ("E3", "hypnoanalytic theory of anorexia nervosa, treatment aimed at it"),
       570: ("E5", "chart review of rapid responders in mania"),
       611: ("E2", "acromegaly arising in schizophrenia; no remission described"),
       612: ("E7", "comment on the included DeLisle 1991 case"),
       630: ("E1", "therapist's autobiographical account of being shot; no prior syndrome resolving"),
       674: ("E3", "off-label metreleptin given for the anorexia nervosa"),
       687: ("E3", "follow-up of psychoses discharged as recovered in the 1880s; " + SPONT),
       699: ("E3", "nosological essay on melancholia and its recovery"),
       751: ("E3", "ECT aimed at the mania"),
       }
# Records already in the ledger whose PsycInfo abstract settles an earlier unsure decision (PsycInfo id -> decision).
RESOLVE = {
    "zmok4gm75v": "liu-2016",
    "5uizgsu4d5": "nguyen-2021",
    "ovtdqhmvtv": ("E4", "substance-induced (peyote) psychosis clearing once sleep was restored (PsycInfo abstract)"),
    "d22l5d37dv": ("E4", "psychosis improving as hypoestrogenaemia was treated with oestrogen and progesterone (PsycInfo abstract)"),
    "euza7pf23b": ("E3", "amantadine added to antipsychotics for the schizophrenia, after the authors' memantine trial (PsycInfo abstract)"),
    "afnzyfatgj": ("E3", "metformin started to reverse insulin resistance as a treatment for the bipolar depression (PsycInfo abstract)"),
    "oik3gczb3b": ("E3", "ketamine-assisted psychotherapy given for the bulimia nervosa (PsycInfo abstract)"),
    "ciqkpuyxev": ("E3", "off-label esketamine with psychotherapy aimed at the OCD and depression (PsycInfo abstract)"),
}
# Two records missed by the first title-matching pass, screened now.
EXTRA = {"ut6nqaasgf": ("E3", "post-stroke depression remitting on placebo in a drug trial; placebo responders are excluded (section 1)"),
         "2odcyefu4r": ("E2", "unexpected adverse reaction to olanzapine with lorazepam")}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    for k in R:
        k["cand_key"] = str(k["src"])
    hist = {k["id"]: (k.pop("hist"), k.pop("observed")) for k in R if "hist" in k}
    add_records(R, cand, collection="phase1e", found_via=f"{SRC} ({QID})", today=TODAY)
    d = json.loads(CASES.read_text())
    by_id = {r["id"]: r for r in d["records"]}
    for k in R:
        r = by_id[k["id"]]
        r["verified"] = f"{TODAY}: abstract-level appraisal (PsycInfo record); identifiers from PubMed" if cand[k["cand_key"]]["pmid"] \
            else f"{TODAY}: abstract-level appraisal (PsycInfo record)"
        if k["cand_key"] in NO_DOI and not r["links"].get("ckn"):
            r["links"]["ckn"] = ebsco_url(NO_DOI[k["cand_key"]])
        if k["id"] in hist:
            (o, m, w), yr = hist[k["id"]]
            r["historical"] = {"original_terms": o, "modern_reading": m, "why_read": w}
            r["observed_year"] = yr
        if any(ch in r["ids"]["doi"] for ch in "<>"):
            r["links"]["doi"] = "https://doi.org/" + quote(r["ids"]["doi"], safe="/()-.;:_")
        r["caveat"] = r["caveat"].strip()
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = [r for r in L.rows if r["record_id"] not in sup]
    by_title = {}
    for r in current:
        by_title.setdefault(norm(r["title"]), []).append(r)
    lib_doi = {k["id"]: (cand[k["cand_key"]]["doi"], cand[k["cand_key"]]["pmid"]) for k in R}
    n = {"new_or_blank": 0, "already": 0, "corrections": 0}
    for rid, title, authors, src, typ, _abs in V:
        jn, yr = parse_src(src)
        au = authors.split(",")[0].strip()
        base = dict(other=f"psyh:{rid}", title=title, au=au, yr=yr, jn=jn)
        matched = by_title.get(norm(title), [])
        if rid in RANK:
            i, s = RANK[rid]
            dec = DEC.get(i)
            doi, pmid = lib_doi.get(dec, ("", "")) if isinstance(dec, str) else ("", "")
            row = L.add(SRC, QID, dec, doi=doi, pmid=pmid, **base, screened=True,
                        note=f"PsycInfo list rank {i}, score {s}; all 819 titles screened; {TODAY}")
            if dec is None:
                row["screen_stage"] = "ta"
            n["new_or_blank"] += 1
            for old in matched:  # blank rows from stopped queues, screened now via the same record
                if not old["decision"]:
                    L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=old["record_id"], screened=True,
                          note=f"screened via the PsycInfo record ({QID}); {TODAY}")
                    n["corrections"] += 1
            continue
        if rid in EXTRA:
            L.add(SRC, QID, EXTRA[rid], **base, note=f"missed by the first title match, screened {TODAY}")
            n["new_or_blank"] += 1
            continue
        decided = [r for r in matched if r["decision"]]
        inc = [r for r in decided if r["decision"] == "included"]
        uns = [r for r in decided if r["decision"] == "unsure"]
        ref = "; ".join(r["record_id"] for r in decided)
        if rid in RESOLVE:
            dec = RESOLVE[rid]
            doi, pmid = lib_doi.get(dec, ("", "")) if isinstance(dec, str) else ("", "")
            L.add(SRC, QID, dec, doi=doi, pmid=pmid, **base, note=f"was unsure as {ref}; settled by the PsycInfo abstract; {TODAY}")
            for old in uns:
                f = copy_fields(old)
                if isinstance(dec, str):
                    f.update(doi=f["doi"] or doi, pmid=f["pmid"] or pmid)
                L.add(old["source_db"], old["query_id"], dec, **f, supersedes=old["record_id"],
                      note=f"settled with the PsycInfo abstract ({QID}); {TODAY}")
                n["corrections"] += 1
        elif inc:
            L.add(SRC, QID, inc[0]["library_ids"], **base, note=f"library case, also found as {ref}; {TODAY}")
        elif uns:
            L.add(SRC, QID, (U, f"same record as {ref}, still unsure after the PsycInfo abstract"), **base, note=TODAY)
        else:
            row = L.add(SRC, QID, (decided[0]["reason_code"], f"decided earlier as {ref}"), **base, note=TODAY)
            row["screen_stage"] = decided[0]["screen_stage"]
        n["already"] += 1
    # Embase unsure rows settled by the Turkish-language PsycInfo record of the same case (title names amitriptyline).
    shapiro = "amitriptyline, an antidepressant, given; depression and sweating attacks remitted together (PsycInfo title, rank 263)"
    for old in [r for r in current if r["record_id"] in ("R060105", "R060340")]:
        L.add(old["source_db"], old["query_id"], ("E3", shapiro), **copy_fields(old), supersedes=old["record_id"],
              note=f"settled with the PsycInfo record ({QID}); {TODAY}")
        n["corrections"] += 1
    L.write()
    print(n)
    log_runs([(QID, SRC, "TI(syndrome) AND TI(resolution or unexpected) AND (TI or AB case terms); see queries/strings_psycinfo_v1.json",
               1075, TODAY, "819 new or blank, all titles screened; 16 cases + 1 context; 9 earlier unsure rows settled")])
