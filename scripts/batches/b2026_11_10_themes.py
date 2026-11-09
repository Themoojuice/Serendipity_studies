"""Batch 2026-11-10: theme sweeps (ketogenic / metabolic; right temporal lesions).

Adds context records (downstream trials and confound evidence), upgrades the
downstream level of the ketogenic origin cases, and tags temporal-lesion cases
with laterality where the abstract states it. Figures in summaries are from the
abstracts retrieved on 2026-11-10.
Run from the repo root.
"""
import json
from pathlib import Path
from urllib.parse import quote

PATH = Path("data/cases.json")
d = json.loads(PATH.read_text())
V = d["vocabularies"]
for v in ["Randomised trial", "Open-label trial", "Review"]:
    if v not in V["design"]:
        V["design"].append(v)
if "Deliberate test (trial)" not in V["trigger_intent"]:
    V["trigger_intent"].append("Deliberate test (trial)")
TODAY = "2026-11-10"


def ckn(doi):
    return "https://go.openathens.net/redirector/ckn.qldhealth.com?url=" + quote("https://doi.org/" + doi, safe="")


def ctx(id, au, title, jn, yr, vol, iss, pg, pmid, pmcid, doi, design, n, cats, spec, tcat, tspec, intent, res, dl,
        summary, caveat, tags, era=("emerging", "")):
    return {
        "id": id, "record_type": "context", "status": "Included", "tier": None, "collections": ["themes-2026-11-10"],
        "citation": {"authors": au, "title": title, "journal": jn, "year": yr, "volume": vol, "issue": iss, "pages": pg},
        "ids": {"doi": doi, "pmid": pmid, "pmcid": pmcid},
        "links": {"full_text": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/" if pmcid else None,
                  "abstract": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
                  "doi": f"https://doi.org/{doi}" if doi else None, "alternates": [], "ckn": ckn(doi) if doi else None},
        "access": "Free full text" if pmcid else "Paywalled", "design": design, "n_patients": n,
        "syndrome": {"categories": cats, "specific": spec, "chronic": None, "treatment_resistant": None},
        "trigger": {"category": tcat, "specific": tspec, "intent": intent},
        "outcome": {"resolution": res, "time_to_resolution": None, "follow_up": None, "reversal": "None reported"},
        "downstream": {"level": dl, "note": "", "links": []},
        "summary": summary, "caveat": caveat, "tags": sorted(tags), "same_patient_as": None, "found_via": "Europe PMC",
        "date_added": TODAY, "verified": f"{TODAY}: Europe PMC record matched", "flags": [],
        "era": {"label": era[0], "note": era[1], "basis": "judged"},
    }


NEW = [
    ctx("pacheco-1965", "Pacheco A, Easterling WS, Pryer MW", "A pilot study of the ketogenic diet in schizophrenia.",
        "Am J Psychiatry", 1965, "121", "", "1110-1111", "14283310", "", "10.1176/ajp.121.11.1110", "Open-label trial", None,
        ["Psychotic"], "Schizophrenia", "Diet", "Ketogenic diet", "Deliberate test (trial)", "Unclear", 3,
        "A 1965 pilot of the ketogenic diet in schizophrenia, largely forgotten until the serendipitous 2009 case revived the idea.",
        "No abstract indexed; the result needs the full text.", ["ketogenic", "schizophrenia", "historical", "trial"]),
    ctx("danan-2022", "Danan A, Westman EC, Saslow LR, Ede G",
        "The Ketogenic Diet for Refractory Mental Illness: A Retrospective Analysis of 31 Inpatients.", "Front Psychiatry", 2022,
        "13", "", "951376", "35873236", "PMC9299263", "10.3389/fpsyt.2022.951376", "Case series", 31, ["Mood", "Psychotic"],
        "Refractory major depression, bipolar disorder and schizoaffective disorder (inpatients)", "Diet",
        "Ketogenic diet (≤20 g carbohydrate a day) added to inpatient care", "Deliberate test (trial)", "Partial", 3,
        "In 28 adherent inpatients with refractory illness, mean HAM-D fell from 25.4 to 7.7 on a strict ketogenic diet, with psychosis and metabolic markers also improving.",
        "Retrospective and uncontrolled, in an intensive inpatient setting.", ["ketogenic", "depression", "schizoaffective", "bipolar", "case-series"]),
    ctx("sethi-2024", "Sethi S, Wakeham D, Ketter T, Hooshmand F, Bjornstad J, Richards B et al.",
        "Ketogenic Diet Intervention on Metabolic and Psychiatric Health in Bipolar and Schizophrenia: A Pilot Trial.",
        "Psychiatry Res", 2024, "335", "", "115866", "38547601", "", "10.1016/j.psychres.2024.115866", "Open-label trial", 23,
        ["Psychotic", "Mood"], "Schizophrenia or bipolar disorder with metabolic abnormalities", "Diet", "Four-month ketogenic diet",
        "Deliberate test (trial)", "Partial", 3,
        "In a 4-month single-arm pilot, BPRS scores fell 32% in schizophrenia, CGI severity improved 31%, and no participant still met metabolic syndrome criteria.",
        "Single-arm and open-label; psychiatric gains were in adherent participants.", ["ketogenic", "schizophrenia", "bipolar", "pilot"]),
    ctx("gao-2026", "Gao M, Kirk M, Knight H, Lash E, Michalopoulou M, Guess N et al.",
        "A Ketogenic Diet for Treatment-Resistant Depression: A Randomized Clinical Trial.", "JAMA Psychiatry", 2026, "83", "4",
        "331-340", "41637092", "PMC12874075", "10.1001/jamapsychiatry.2025.4431", "Randomised trial", 88, ["Mood"],
        "Treatment-resistant depression (PHQ-9 ≥15)", "Diet", "Six-week ketogenic diet vs an active healthy-diet control",
        "Deliberate test (trial)", "Partial", 3,
        "Ketogenic diet beat an active healthy-diet control by 2.2 PHQ-9 points at 6 weeks (P = .05); the 1.9-point gap at 12 weeks was not significant.",
        "Both arms improved markedly (by about 10 and 8 points); diets cannot be blinded.", ["ketogenic", "depression", "rct"]),
    ctx("abram-2026", "Abram SV, Kyner JM, Vu A, Naeem Z, Sethi S, Jacob MS et al.",
        "Metabolic Improvements with a Ketogenic Diet Correlate with Symptom Improvement in Psychosis: A Randomized Controlled Trial.",
        "Schizophr Bull", 2026, "52", "4", "sbag082", "42415343", "", "10.1093/schbul/sbag082", "Randomised trial", 58,
        ["Psychotic", "Mood"], "Schizophrenia-spectrum and bipolar I disorder (outpatients)", "Diet",
        "One-month ketogenic diet vs diet as usual, with a 4-month extension", "Deliberate test (trial)", "Partial", 3,
        "In the first randomised trial in psychosis, metabolic health, cognition and symptoms improved, and depressive improvement tracked ketosis rather than weight loss.",
        "One-month randomised phase; small; the extension was uncontrolled.", ["ketogenic", "schizophrenia", "bipolar", "rct", "mechanism"]),
    ctx("hernandez-poblete-2024", "Hernandez Poblete N, Gay F, Salvo F, Micoulaud-Franchi JA, Bienvenu T, Coelho J",
        "Resective epilepsy surgery and its impact on depression in adults: a systematic review, meta-analysis, and implications for future research.",
        "J Neurol Neurosurg Psychiatry", 2024, "95", "10", "956-965", "38443157", "", "10.1136/jnnp-2023-333073", "Pooled analysis",
        2563, ["Mood"], "Depression in adults with drug-resistant epilepsy", "Neurosurgery", "Resective epilepsy surgery",
        "Treatment for another condition", "Partial", 2,
        "Across 25 studies and 2,563 adults, depression was less common after resective epilepsy surgery (risk ratio 0.70, 95% CI 0.53–0.91), from 6 months onwards.",
        "Key confound for lesion cases after epilepsy surgery: seizure control and medication change, not the resection itself, may drive remission.",
        ["confound", "epilepsy-surgery", "depression", "meta-analysis", "temporal-lobe"], era=("known", "Established by pooled data by 2024.")),
    ctx("pintor-2022", "Pintor L", "Temporal Lobectomy: Does It Worsen or Improve Presurgical Psychiatric Disorders?",
        "Curr Top Behav Neurosci", 2022, "55", "", "307-327", "33959938", "", "10.1007/7854_2021_224", "Review", None,
        ["Mood", "Anxiety", "Psychotic"], "Psychiatric disorders in temporal lobe epilepsy", "Neurosurgery", "Temporal lobectomy",
        "Treatment for another condition", "Partial", 2,
        "After temporal lobectomy, depression and anxiety usually fall by 12 months, yet de novo psychosis appears in 1–14%: the temporal lobe swings psychiatric state both ways.",
        "Narrative review chapter.", ["confound", "epilepsy-surgery", "temporal-lobe", "review"], era=("known", "Bidirectional psychiatric change after temporal lobectomy was well described by the 2010s.")),
    ctx("uher-2005", "Uher R, Treasure J", "Brain lesions and eating disorders.", "J Neurol Neurosurg Psychiatry", 2005, "76", "6",
        "852-857", "15897510", "PMC1739667", "10.1136/jnnp.2004.048819", "Review", 54, ["Eating"],
        "Eating disorders with brain damage (54 published cases)", "Acquired brain lesion", "Focal brain lesions", "Injury or illness",
        "Unclear", 1,
        "In 54 published cases, the characteristic eating-disorder syndromes went with right frontal and temporal lesions, the same territory whose damage has also ended eating disorders.",
        "Mostly lesions that caused rather than cured eating disorders.", ["eating", "lesion", "right-hemisphere", "laterality", "review"]),
]

ids = {r["id"] for r in d["records"]}
added = 0
for r in NEW:
    if r["id"] not in ids:
        d["records"].append(r)
        added += 1

KETO_LINKS = [{"label": "Danan 2022 (31 inpatients)", "doi": "10.3389/fpsyt.2022.951376"},
              {"label": "Sethi 2024 (pilot)", "doi": "10.1016/j.psychres.2024.115866"},
              {"label": "Gao 2026 (RCT, depression)", "doi": "10.1001/jamapsychiatry.2025.4431"},
              {"label": "Abram 2026 (RCT, psychosis)", "doi": "10.1093/schbul/sbag082"}]
right_temporal = {"kanner-1993", "shreedhara-2018", "levine-2003", "tsang-2023", "hosseini-2012"}
epilepsy_surgery = {"kanner-1993", "shreedhara-2018", "sun-2023", "guarnieri-2005"}
for r in d["records"]:
    if r["id"] in ("kraft-westman-2009", "palmer-2017", "palmer-2019"):
        r["downstream"] = {"level": 3, "links": KETO_LINKS,
                           "note": "Ketogenic diet trials followed: open-label (Danan 2022, Sethi 2024) and randomised (Gao 2026, Abram 2026). A 1965 pilot (Pacheco) predates it."}
        r["era"] = {"label": "emerging", "basis": "judged",
                    "note": "Randomised evidence so far is modest in depression (Gao 2026) and suggestive in psychosis (Abram 2026)."}
    if r["id"] in right_temporal:
        r["tags"] = sorted(set(r["tags"]) | {"right-temporal"})
    if r["id"] in epilepsy_surgery:
        r["tags"] = sorted(set(r["tags"]) | {"epilepsy-surgery-confound"})
        if "seizure control" not in r["caveat"].lower():
            r["caveat"] = (r["caveat"] + " Depression and anxiety fall after epilepsy surgery on average (Hernandez Poblete 2024), so seizure control is a live alternative.").strip()

d["updated"] = TODAY
PATH.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
print("added", added, "context records; total", len(d["records"]))
