"""Batch 2026-11-14: APA PsycInfo via CKN (EBSCO), broader title/abstract query PSY_tiab_v1 (protocol v1.7.1).

Query (queries/strings_psycinfo_tiab_v1.json): TI(syndrome terms, widened) AND (AB(resolution terms) OR AB(unexpectedness
terms)) AND (TI or AB case terms), db=psyh, 4,765 hits on 2026-11-14. Read from the result list 50 per page with the
per-record extractor (no mis-pairing: 2 identical source+abstract pairs, both genuine duplicate records).

Matching by normalised title against current ledger rows: 325 already found by PSY_title_v1, 357 decided in earlier
rounds (8 library cases, 1 unsure), 4,083 new or blank. The 4,083 were ranked with the v1.3 classifier (scored in the
browser; the Python scorer scripts/rerank_score.py gives identical scores) and every title was screened, abstracts read
for every candidate. Under the section 10 rule the queue would have stopped at rank 3,496 (300 consecutive irrelevant
after rank 3,196); the remaining 587 were screened anyway, so the whole set is covered.

Result: 21 cases + 1 context record (Nahm & Greyson 2009, terminal lucidity), 8 unsure. Includes sat at ranks 4-3,196,
so the classifier ordered this set much less well than the Europe PMC sets it was trained on.
Working files: /home/claude/work/raw/psb_part.json, psb_todo.json, psb_dec.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_14_psycinfo_tiab_v1.py
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, "scripts")
from lib_add import CASES, U, Ledger, add_records, log_runs  # noqa: E402

TODAY = "2026-11-14"
QID = "PSY_tiab_v1"
SRC = "PsycInfo via CKN (EBSCO)"
RAW = Path("/home/claude/work/raw")
ALL = json.loads((RAW / "psb_part.json").read_text())      # [id, title, first author, source, score, has_abstract]
todo = json.loads((RAW / "psb_todo.json").read_text())     # same rows, new or blank only, sorted by score
RANK = {x[0]: i for i, x in enumerate(todo)}
DECS = json.loads((RAW / "psb_dec.json").read_text())     # rank -> "INC id" | "E#|note" | "U|note"
CKN = "https://go.openathens.net/redirector/ckn.qldhealth.com?url="
OTHER = "Treatment for another condition"


def ebsco_url(rid):
    return CKN + quote(f"https://research.ebsco.com/c/lrpoh2/details/{rid}?db=psyh", safe="")


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:80]


def parse_src(src):
    m = re.search(r",[^,]*?\b(1[6-9]\d\d|20\d\d)\b", src)
    return (src[:m.start()].strip(), m.group(1)) if m else (src, "")


def pm(pmid, doi, title, au, jn, yr, vol, iss, pages, pmcid=""):
    return dict(pmid=pmid, pmcid=pmcid, doi=doi, title=title, authorString=au, journal=jn, year=yr, vol=vol, issue=iss,
                pages=pages, lang="eng")


cand = {
    "fontana-2019": pm("30095557", "10.1097/YCT.0000000000000527", "Functional Neurological Symptom Disorder Spontaneously Remits After Electroconvulsive Therapy.",
                       "Fontana RS, Clark FA, Griffeth B", "J ECT", 2019, "35", "2", "e10"),
    "yovell-1994": pm("7931211", "10.1097/00005053-199410000-00017",
                      "Clozapine reverses cocaine craving in a treatment-resistant mentally ill chemical abuser: a case report and a hypothesis.",
                      "Yovell Y, Opler LA", "J Nerv Ment Dis", 1994, "182", "10", "591-2"),
    "taylor-1978": pm("721785", "", "Alpha-methyldopa in schizophrenia.", "Taylor P, Gillman PK, Gaind R", "J Clin Psychiatry", 1978, "39", "11", "815-6"),
    "dukarm-2005": pm("15916509", "10.1089/jwh.2005.14.345",
                      "Bulimia nervosa and attention deficit hyperactivity disorder: a possible role for stimulant medication.",
                      "Dukarm CP", "J Womens Health (Larchmt)", 2005, "14", "4", "345-50"),
    "fujiwara-2025": pm("40909875", "10.1002/pcn5.70201",
                        "From surgical treatment to psychiatric progress in refractory obsessive-compulsive disorder: A case report.",
                        "Fujiwara S, Okamura Y, Wake H, Tanami H, Ishida T, Mizuno M", "PCN Rep", 2025, "4", "3", "e70201", pmcid="PMC12405736"),
    "deon-2012": pm("21940691", "10.1177/0883073811415853",
                    "Pallidal deep-brain stimulation associated with complete remission of self-injurious behaviors in a patient with Lesch-Nyhan syndrome: a case report.",
                    "Deon LL, Kalichman MA, Booth CL, Slavin KV, Gaebler-Spira DJ", "J Child Neurol", 2012, "27", "1", "117-20"),
    "reimer-2009": pm("19223267", "10.1016/j.schres.2009.01.018", "Successful treatment of psychosis with infliximab in a patient with Crohn's disease.",
                      "Reimer J, Fink T, Bläker M, Schäfer I, Otte C", "Schizophr Res", 2009, "109", "1-3", "194-5"),
    "cavenar-1977": pm("894274", "10.1097/00005053-197709000-00009", "Depressive disorders and religious conversions.",
                       "Cavenar JO, Spaulding JG", "J Nerv Ment Dis", 1977, "165", "3", "209-12"),
    "macleod-1990": pm("2086525", "10.2190/M3CW-G06Y-JH4J-0YUN", "Respiratory depression and melancholia.",
                       "Macleod AD", "Int J Psychiatry Med", 1990, "20", "4", "383-91"),
    "yates-1988": pm("", "", "Plastic surgery and the bulimic patient.", "Yates A, Shisslak CM, Allender JR, Wolman W",
                     "International Journal of Eating Disorders", 1988, "7", "4", "557-560"),
    "nagata-2013": pm("23195073", "10.1017/S1041610212002037",
                      "A case in which mirtazapine reduced auditory hallucinations in a patient with Parkinson disease.",
                      "Nagata T, Shinagawa S, Tagai K, Nakayama K", "Int Psychogeriatr", 2013, "25", "7", "1199-201"),
    "yilmaz-2014": pm("24122344", "10.1007/s00787-013-0484-9",
                      "The possible effect of methylphenidate on kleptomania in a school-age girl with attention-deficit/hyperactivity disorder.",
                      "Yılmaz S, Bilgiç A", "Eur Child Adolesc Psychiatry", 2014, "23", "5", "361-3"),
    "puente-1985": pm("", "", "Research participation as therapeutic for schizophrenia: A case study.", "Puente AE",
                      "Psychosocial Rehabilitation Journal", 1985, "8", "4", "95-98"),
    "godschalx-dekker-2014": pm("24504487", "10.1055/s-0034-1367014", "Reduction of parkinsonism and psychosis with mirtazapine: a case report.",
                                "Godschalx-Dekker JA, Siegers HP", "Pharmacopsychiatry", 2014, "47", "3", "81-3"),
    "kastner-2016": pm("", "", "Ketamine and the core symptoms of autism.", "Kastner T, Walsh K, Shulman L, et al.",
                       "International Journal on Disability and Human Development", 2016, "15", "1", "121-123"),
    "morena-1994": pm("8084989", "10.1016/S0033-3182(94)71760-6", "Midazolam and the treatment of catatonia in major depression in an older adult.",
                      "Morena G, Sunderland B, Billig N", "Psychosomatics", 1994, "35", "4", "392-5"),
    "terao-1999": pm("10545010", "10.1080/0004867990475", "Schizophrenia and bladder stones.", "Terao T, Nakamura J, Inatomi H, Eto A",
                     "Aust N Z J Psychiatry", 1999, "33", "5", "769-70"),
    "berner-2008": pm("18681764", "10.4088/jcp.v69n0522a", "A case of sodium oxybate treatment of tardive dyskinesia and bipolar disorder.",
                      "Berner JE", "J Clin Psychiatry", 2008, "69", "5", "862"),
    "maddigan-2004": pm("19030491", "", "Letter to the editor [Mania curing fever?].", "Maddigan B, Young N, Ledrew K",
                        "Can Child Adolesc Psychiatr Rev", 2004, "13", "4", "119", pmcid="PMC2538709"),
    "ward-1975": pm("1176977", "10.1097/00005053-197509000-00009", "Successful lithium treatment of transvestism associated with manic-depression.",
                    "Ward NG", "J Nerv Ment Dis", 1975, "161", "3", "204-6"),
    "koethe-2007": pm("17447179", "10.1055/s-2007-961818", "Cessation of complex visual hallucinations during treatment with mirtazapine.",
                      "Koethe D, Dietl T, Leweke FM, Friess E", "Pharmacopsychiatry", 2007, "40", "2", "82-3"),
    "nahm-2009": pm("20010032", "10.1097/NMD.0b013e3181c22583",
                    "Terminal lucidity in patients with chronic schizophrenia and dementia: a survey of the literature.",
                    "Nahm M, Greyson B", "J Nerv Ment Dis", 2009, "197", "12", "942-4"),
}
NO_ID = {"yates-1988": "54dedabwvz", "puente-1985": "bvnz473cw5", "kastner-2016": "6wjalkratn"}
MIRT = ("emerging", "Three separate reports (2007, 2013, 2014) of hallucinations stopping on mirtazapine given for depression "
                    "or sleep; no trial found so far.")
BENZO = ("known", "Benzodiazepine reversal of catatonia had been reported from the early 1980s (lorazepam; recalled, not "
                  "checked) and the lorazepam challenge later became standard; in 1994 it was not yet routine.")

R = [
    dict(id="fontana-2019", src="fontana-2019", design="Letter", n=1, cats=["Functional neurological"],
         spec="Functional neurological symptom disorder (tremor indexed) for 2 years, with depression with catatonia, GAD and PTSD",
         chronic=True, tr=None, tcat="Brain stimulation", tspec="ECT (indexed with her depression and catatonia)", intent=OTHER,
         res="Complete", rev="None reported", dl=0,
         summary="A 49-year-old woman, admitted three times in two years after a complicated cardiac ablation, had functional "
                 "neurological symptoms alongside depression with catatonia; the functional symptoms remitted after ECT.",
         caveat="Functional symptoms often travel with mood, so lifting the depression may have carried them away.",
         tags=["ect", "functional-neurological-disorder", "tremor", "catatonia"], tier="C"),
    dict(id="yovell-1994", src="yovell-1994", design="Case report", n=1, cats=["Substance & addictive"],
         spec="Cocaine dependence with craving in treatment-resistant schizoaffective disorder", chronic=None, tr=True,
         tcat="Medication for another condition", tspec="Clozapine for treatment-resistant schizoaffective disorder", intent=OTHER,
         res="Complete", rev="None reported", dl=2,
         era=("emerging", "Retrospective and small prospective studies later linked clozapine with less substance use in psychosis "
                          "(2000s; recalled, not checked); no definitive trial."),
         summary="A 37-year-old man with treatment-resistant schizoaffective disorder lost his cocaine craving and stopped using "
                 "once on clozapine, and the change lasted.",
         caveat="Clozapine's blood-monitoring regime brings frequent contact and supervision, which itself discourages use.",
         tags=["clozapine", "cocaine", "dual-diagnosis", "craving", "schizoaffective"], tier="C"),
    dict(id="taylor-1978", src="taylor-1978", design="Case report", n=1, cats=["Psychotic"], spec="Schizophrenia", chronic=None,
         tr=None, tcat="Medication for another condition", tspec="Overdose of alpha-methyldopa (an antihypertensive) in a suicide attempt",
         intent="Self-administered", res="Temporary", rev="Natural off-on", dl=0,
         summary="After an overdose of alpha-methyldopa, a schizophrenic man's psychosis cleared completely, then returned "
                 "suddenly a few weeks later; the authors point to the drug's interference with dopamine.",
         caveat="The overdose and its aftermath (admission, sedation, a suicidal crisis passing) could account for a short lull.",
         tags=["methyldopa", "dopamine", "overdose", "schizophrenia"], tier="C"),
    dict(id="dukarm-2005", src="dukarm-2005", design="Case series", n=6, cats=["Eating"], spec="Bulimia nervosa with comorbid ADHD",
         chronic=None, tr=None, tcat="Medication for another condition", tspec="Dextroamphetamine for comorbid ADHD", intent=OTHER,
         res="Complete", rev="None reported", dl=2,
         era=("emerging", "Stimulants were later trialled in binge-eating disorder (lisdexamfetamine approved for it in the US in "
                          "2015; recalled, not checked); bulimia nervosa itself has no large trial."),
         summary="Six patients with bulimia nervosa and ADHD all stopped bingeing and purging once dextroamphetamine was started "
                 "for their ADHD, and their weight stayed healthy.",
         caveat="Appetite suppression alone could stop the binges without touching the eating disorder's core beliefs.",
         tags=["dextroamphetamine", "stimulant", "adhd", "bulimia", "appetite"], tier="C"),
    dict(id="fujiwara-2025", src="fujiwara-2025", design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
         spec="Severe, long-standing, treatment-resistant OCD (contamination fears, compulsive defecation rituals)", chronic=True,
         tr=True, tcat="Surgery or procedure (outside the brain)",
         tspec="Laparoscopic rectopexy for rectal prolapse and incontinence caused by her compulsions", intent=OTHER, res="Partial",
         rev="None reported", dl=0,
         summary="A woman in her 50s whose defecation rituals had caused rectal prolapse and incontinence cut her cleaning "
                 "compulsions sharply once rectopexy cured the incontinence, and then took up regular psychiatric care.",
         caveat="Curing the incontinence removed the soiling that triggered the cleaning, so the rituals may have lost their trigger rather than the OCD easing.",
         tags=["ocd", "rectal-prolapse", "surgery", "contamination"], tier="C"),
    dict(id="deon-2012", src="deon-2012", design="Case report", n=1, cats=["Neurodevelopmental"],
         spec="Self-injurious behaviour in Lesch-Nyhan syndrome", chronic=True, tr=None, tcat="Brain stimulation",
         tspec="Pallidal deep brain stimulation for hypertonia and dystonia", intent=OTHER, res="Complete", rev="None reported", dl=2,
         era=("known", "Self-injury remitting after pallidal DBS in Lesch-Nyhan syndrome had been reported from the early 2000s "
                       "(recalled, not checked)."),
         summary="A boy with Lesch-Nyhan syndrome, given pallidal deep brain stimulation to ease hypertonia for comfort and "
                 "wheelchair positioning, stopped self-injuring over the following 2.5 years.",
         caveat="Less dystonic pain and fewer restraints may have reduced the triggers for self-injury.",
         tags=["lesch-nyhan", "self-injury", "deep-brain-stimulation", "globus-pallidus", "dystonia"], tier="C"),
    dict(id="reimer-2009", src="reimer-2009", design="Letter", n=1, cats=["Psychotic", "Catatonia"],
         spec="Catatonic psychosis of uncertain cause, starting 7 weeks into steroid treatment for Crohn's disease", chronic=False,
         tr=None, tcat="Medication for another condition", tspec="Infliximab (anti-TNF-alpha) for Crohn's disease", intent=OTHER,
         res="Complete", rev="None reported", dl=1,
         summary="A 23-year-old woman with Crohn's disease, admitted catatonic and psychotic, recovered as infliximab brought her "
                 "Crohn's into remission.",
         caveat="Tapering the steroids as the Crohn's settled is the obvious competing explanation; the authors judge the timing atypical for steroid psychosis.",
         tags=["infliximab", "tnf-alpha", "crohns-disease", "catatonia", "inflammation"], tier="C"),
    dict(id="cavenar-1977", src="cavenar-1977", design="Case series", n=4, cats=["Mood"],
         spec="Depressive illness (resolved in the two of four patients with hysterical personalities)", chronic=None, tr=None,
         tcat="Life event", tspec="Religious conversion", intent="Life event", res="Complete", rev="None reported", dl=0,
         summary="Of four depressed patients who underwent religious conversion, the two with hysterical personalities recovered "
                 "afterwards; the two with obsessional personalities did not, and both died by suicide.",
         caveat="Conversion may mark a recovery already under way rather than cause it.",
         tags=["religious-conversion", "depression", "personality", "psychological-trigger"], tier="C"),
    dict(id="macleod-1990", src="macleod-1990", design="Case report", n=1, cats=["Mood"],
         spec="Major depressive episode of 6 months (melancholia)", chronic=True, tr=None, tcat="Physiological stress",
         tspec="Acute respiratory crisis in asthma needing assisted ventilation", intent="Injury or illness", res="Complete",
         rev="None reported", dl=0,
         summary="A 56-year-old asthmatic woman's 6-month depressive episode resolved after a respiratory crisis that needed "
                 "assisted ventilation; the author proposes the induced delirium as the active ingredient, as in older shock treatments.",
         caveat="Surviving a near-fatal illness changes circumstances and care, which can lift depression without any physiology.",
         tags=["hypoxia", "ventilation", "delirium", "asthma", "physiological-stress"], tier="C"),
    dict(id="yates-1988", src="yates-1988", design="Case series", n=2, cats=["Eating"], spec="Bulimia nervosa in two women aged 19 and 20",
         chronic=None, tr=None, tcat="Surgery or procedure (outside the brain)",
         tspec="Cosmetic surgery they sought to make their bodies more acceptable", intent=OTHER, res="Temporary",
         rev="None reported", dl=0,
         summary="Two young women with bulimia had cosmetic surgery to make their bodies more acceptable to themselves; the "
                 "bulimia remitted markedly afterwards, but only for a while.",
         caveat="Post-operative recovery interrupts binge-purge routines and brings close supervision.",
         tags=["cosmetic-surgery", "bulimia", "body-image"], tier="C"),
    dict(id="nagata-2013", src="nagata-2013", design="Case report", n=1, cats=["Psychotic"],
         spec="Auditory hallucinations in Parkinson's disease, unrelieved by cutting antiparkinsonian drugs or by atypical antipsychotics",
         chronic=None, tr=True, tcat="Medication for another condition", tspec="Mirtazapine for comorbid depression", intent=OTHER,
         res="Complete", rev="None reported", dl=1, era=MIRT,
         summary="A 48-year-old woman with Parkinson's disease whose auditory hallucinations had resisted dose cuts and "
                 "antipsychotics lost them within 4 weeks of mirtazapine started for her depression.",
         caveat="Hallucinations in Parkinson's disease track sleep and mood, both of which mirtazapine improves.",
         tags=["mirtazapine", "parkinsons", "hallucinations", "5ht2a"], tier="C"),
    dict(id="yilmaz-2014", src="yilmaz-2014", design="Letter", n=1, cats=["Impulse-control"],
         spec="Kleptomania (stealing since kindergarten) with ADHD in a 7-year-old", chronic=True, tr=None,
         tcat="Medication for another condition", tspec="Methylphenidate for ADHD", intent=OTHER, res="Complete",
         rev="None reported", dl=0,
         summary="A 7-year-old girl who had stolen since kindergarten stopped completely once methylphenidate was started for her ADHD.",
         caveat="At 7, stealing may be ADHD impulsivity, which methylphenidate treats directly, rather than kleptomania.",
         tags=["methylphenidate", "kleptomania", "adhd", "child"], tier="C"),
    dict(id="puente-1985", src="puente-1985", design="Case report", n=1, cats=["Psychotic"], spec="Schizophrenia", chronic=None,
         tr=None, tcat="Life event", tspec="Helping design and run a study of 200 psychiatric patients' understanding of their illness",
         intent="Life event", res="Complete", rev="None reported", dl=0,
         summary="A 26-year-old man with schizophrenia improved, then remitted, after taking an active part in designing and "
                 "running a study of how 200 psychiatric patients understood their illness, an idea that came from him.",
         caveat="He was presumably on antipsychotics throughout, and remission at 26 is common enough to be coincidence.",
         tags=["research-participation", "schizophrenia", "psychological-trigger", "meaning"], tier="C"),
    dict(id="godschalx-dekker-2014", src="godschalx-dekker-2014", design="Case report", n=1, cats=["Psychotic"],
         spec="Persistent nocturnal visual hallucinations in a parkinsonian disorder despite reduced dopaminergic drugs, quetiapine, clozapine and rivastigmine",
         chronic=None, tr=True, tcat="Medication for another condition", tspec="Mirtazapine prescribed for sleep", intent=OTHER,
         res="Complete", rev="None reported", dl=1, era=MIRT,
         summary="A man's nocturnal visual hallucinations, which had outlasted quetiapine, clozapine and rivastigmine, stopped "
                 "almost at once when mirtazapine was given for sleep, and his parkinsonism eased as well.",
         caveat="Better sleep alone can quiet nocturnal hallucinations in parkinsonian disorders.",
         tags=["mirtazapine", "parkinsons", "hallucinations", "sleep"], tier="C"),
    dict(id="kastner-2016", src="kastner-2016", design="Case report", n=1, cats=["Neurodevelopmental"],
         spec="Autism with severe intellectual disability", chronic=True, tr=None, tcat="Medication for another condition",
         tspec="Ketamine given for another purpose ('adventitious', per the authors)", intent=OTHER, res="Temporary",
         rev="None reported", dl=1,
         summary="A patient with autism and severe intellectual disability showed a dramatic but short-lived remission of core "
                 "autistic features after ketamine given for another purpose; the authors warn against reading too much into it.",
         caveat="Ketamine's dissociative and sedative after-effects can mimic reduced repetitive behaviour for hours.",
         tags=["ketamine", "autism", "nmda", "intellectual-disability"], tier="C"),
    dict(id="morena-1994", src="morena-1994", design="Case report", n=1, cats=["Catatonia", "Mood"],
         spec="Catatonia in major depression in a 74-year-old man", chronic=None, tr=None, tcat="Medication for another condition",
         tspec="Midazolam as sedation for an MRI", intent=OTHER, res="Temporary", rev="None reported", dl=4, era=BENZO,
         summary="A 74-year-old man's catatonia lifted briefly when he was sedated with midazolam for an MRI; in that window he "
                 "described his depression and suicidal thoughts, and lorazepam with nortriptyline then brought a dramatic recovery.",
         caveat="", tags=["midazolam", "benzodiazepine", "catatonia", "older-adult", "mri-sedation"], tier="C"),
    dict(id="terao-1999", src="terao-1999", design="Letter", n=1, cats=["Psychotic"], spec="Treatment-refractory schizophrenia in a 62-year-old man",
         chronic=True, tr=True, tcat="Surgery or procedure (outside the brain)", tspec="Surgical removal of a large bladder stone",
         intent=OTHER, res="Partial", rev="None reported", dl=0,
         summary="A 62-year-old man with refractory schizophrenia, investigated for dysuria, had a large bladder stone removed; "
                 "afterwards his mental state was much improved along with the dysuria.",
         caveat="Pain and urinary symptoms are stressors that can inflame psychosis, so relief may have removed an aggravating factor rather than touched the illness.",
         tags=["bladder-stone", "surgery", "schizophrenia", "pain"], tier="C"),
    dict(id="berner-2008", src="berner-2008", design="Letter", n=1, cats=["Mood"],
         spec="Continuously cycling bipolar disorder (about 4 manic episodes a year), failing lithium, carbamazepine, oxcarbazepine, divalproex and benzodiazepines",
         chronic=True, tr=True, tcat="Medication for another condition", tspec="Sodium oxybate for fibromyalgia", intent=OTHER,
         res="Partial", rev="None reported", dl=0,
         summary="A 51-year-old woman with continuously cycling bipolar disorder, unresponsive to lithium and three "
                 "anticonvulsants, improved profoundly, as did her tardive dyskinesia, once sodium oxybate was prescribed for fibromyalgia.",
         caveat="Olanzapine had been stopped four months earlier, which may itself have changed her course.",
         tags=["sodium-oxybate", "gaba-b", "bipolar", "rapid-cycling", "tardive-dyskinesia", "fibromyalgia"], tier="C"),
    dict(id="maddigan-2004", src="maddigan-2004", design="Letter", n=1, cats=["Mood", "Psychotic"],
         spec="Psychotic mania in a 14-year-old girl (earlier depression on paroxetine), worsening on risperidone, divalproex and temazepam",
         chronic=False, tr=None, tcat="Fever / infection", tspec="Febrile influenza on day 21 of admission", intent="Injury or illness",
         res="Temporary", rev="Natural off-on", dl=1,
         era=("known", "Psychosis lifting during fever was long recognised (Wagner-Jauregg's malaria therapy, 1917); here the lull lasted two days."),
         summary="A 14-year-old girl's mania, worsening through three weeks of medication changes, vanished the day she developed "
                 "influenza with fever and came back two days later.",
         caveat="All medicines were held that same day, so a break from drug effects competes with the fever.",
         tags=["fever", "influenza", "mania", "adolescent", "intercurrent-illness"], tier="C"),
    dict(id="ward-1975", src="ward-1975", design="Case report", n=1, cats=["Paraphilic", "Mood"],
         spec="Transvestism for 2 years in a 24-year-old man with manic-depressive illness", chronic=True, tr=None,
         tcat="Medication for another condition", tspec="Lithium for manic-depressive illness", intent=OTHER, res="Complete",
         rev="None reported", dl=0,
         summary="A 24-year-old manic-depressive man's two years of cross-dressing stopped soon after lithium was started for "
                 "his mood disorder and had not returned a year later.",
         caveat="If the cross-dressing was driven by mood states, as the author suggests, lithium treated its cause rather than the paraphilia.",
         tags=["lithium", "transvestism", "paraphilia", "bipolar"], tier="C"),
    dict(id="koethe-2007", src="koethe-2007", design="Case series", n=2, cats=["Psychotic"],
         spec="Complex visual hallucinations of unknown cause (one woman also with 2 years of treatment-resistant acoustic hallucinations)",
         chronic=True, tr=True, tcat="Medication for another condition", tspec="Mirtazapine for a depressive syndrome", intent=OTHER,
         res="Complete", rev="None reported", dl=1, era=MIRT,
         summary="Two women aged 54 and 78 with unexplained complex visual hallucinations, one with two years of "
                 "treatment-resistant hallucinations, stopped hallucinating once mirtazapine was started for depression.",
         caveat="Hallucinations in older people often track mood and sleep, both of which mirtazapine improves.",
         tags=["mirtazapine", "visual-hallucinations", "older-adult", "depression"], tier="C"),
    dict(id="nahm-2009", src="nahm-2009", record_type="context", design="Review", n=None, cats=["Psychotic"],
         spec="Chronic schizophrenia, dementia and other severe mental disorders", chronic=True, tr=None, tcat="Physiological stress",
         tspec="Approaching death (terminal lucidity)", intent="Injury or illness", res="Temporary", rev="None reported", dl=1,
         summary="A literature survey of 'terminal lucidity', the unexpected return of mental clarity shortly before death: 49 "
                 "retrievable case reports in mental disorders, most recorded before 1849, set beside the febrile remissions of neurosyphilis.",
         caveat="", tags=["terminal-lucidity", "schizophrenia", "dementia", "antique-sources", "fever"], tier=None),
]
RESOLVE = {"zzqybk3w5j": ("E1", "smoking rose when DBS for depression was withdrawn; tobacco dependence had been low before surgery, so no "
                                "existing dependence remitted (PsycInfo abstract)")}


def decision(i):
    v = DECS.get(str(i))
    if v is None:
        return None
    if v.startswith("INC "):
        return v.split()[1]
    code, note = v.split("|", 1)
    return (U, note) if code == "U" else (code, note)


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1e", found_via=f"{SRC} ({QID})", today=TODAY)
    d = json.loads(CASES.read_text())
    ids = {k["id"] for k in R}
    for r in d["records"]:
        if r["id"] in ids:
            r["verified"] = f"{TODAY}: abstract-level appraisal (PsycInfo record)" + ("; identifiers from PubMed" if r["ids"]["pmid"] else "")
            if r["id"] in NO_ID and not r["links"].get("ckn"):
                r["links"]["ckn"] = ebsco_url(NO_ID[r["id"]])
            if r["ids"]["pmcid"] and not r["links"].get("full_text"):
                r["links"]["full_text"] = f"https://pmc.ncbi.nlm.nih.gov/articles/{r['ids']['pmcid']}/"
            r["caveat"] = r["caveat"].strip()
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = [r for r in L.rows if r["record_id"] not in sup]
    by_title = {}
    for r in current:
        by_title.setdefault(norm(r["title"]), []).append(r)
    psy_title = {r["other_id"]: r for r in current if r["query_id"] == "PSY_title_v1"}
    n = {"screened": 0, "already": 0, "corrections": 0}
    for rid, title, au, src, score, _ in ALL:
        jn, yr = parse_src(src)
        base = dict(other=f"psyh:{rid}", title=title, au=au.split(",")[0].strip(), yr=yr, jn=jn)
        matched = by_title.get(norm(title), [])
        if rid in RANK:
            i = RANK[rid]
            dec = decision(i)
            c = cand.get(dec, {}) if isinstance(dec, str) else {}
            row = L.add(SRC, QID, dec, doi=c.get("doi", ""), pmid=c.get("pmid", ""), pmcid=c.get("pmcid", ""), **base,
                        screened=True, note=f"PsycInfo tiab list rank {i}, score {score}; all 4,083 titles screened; {TODAY}")
            n["screened"] += 1
            for old in matched:
                if not old["decision"]:
                    L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=old["record_id"], screened=True,
                          note=f"screened via the PsycInfo record ({QID}); {TODAY}")
                    n["corrections"] += 1
            continue
        n["already"] += 1
        pt = psy_title.get(f"psyh:{rid}")
        decided = [pt] if pt else [r for r in matched if r["decision"]]
        ref = "; ".join(r["record_id"] for r in decided)
        if rid in RESOLVE:
            dec = RESOLVE[rid]
            L.add(SRC, QID, dec, **base, note=f"was unsure as {ref}; settled by the PsycInfo abstract; {TODAY}")
            for old in decided:
                if old["decision"] == "unsure":
                    L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=old["record_id"],
                          note=f"settled with the PsycInfo abstract ({QID}); {TODAY}")
                    n["corrections"] += 1
            continue
        inc = [r for r in decided if r["decision"] == "included"]
        uns = [r for r in decided if r["decision"] == "unsure"]
        if inc:
            L.add(SRC, QID, inc[0]["library_ids"], **base, note=f"library case, also found as {ref}; {TODAY}")
        elif uns:
            L.add(SRC, QID, (U, f"same record as {ref}, still unsure"), **base, note=TODAY)
        else:
            row = L.add(SRC, QID, (decided[0]["reason_code"], f"decided earlier as {ref}"), **base, note=TODAY)
            row["screen_stage"] = decided[0]["screen_stage"]
    L.write()
    print(n)
    log_runs([(QID, SRC, "TI(syndrome, widened) AND (AB resolution OR AB unexpected) AND (TI or AB case terms); see queries/strings_psycinfo_tiab_v1.json",
               4765, TODAY, "4,083 new or blank, all titles screened; 21 cases + 1 context, 8 unsure; 1 earlier unsure row settled")])
