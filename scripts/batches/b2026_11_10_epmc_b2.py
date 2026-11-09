"""Batch 2026-11-10 (phase 1b): includes from the rest of the Europe PMC broad set.

The v1.2 broad query (43,112 hits) was reloaded in PUB_YEAR slices, because cursor
paging stops near 21,000. That added 20,669 records (batch 2) and then 1,440 more
(batch 3). Each batch was ranked by title score (scripts/rank_titles.py) and screened
from the top: batch 2 ranks 0-399, batch 3 ranks 0-59.

Abstract-level appraisal only (many of these are letters with no abstract, so it is
often title-level): every record enters as Provisional until its full text is read.
Bibliographic fields come from /home/claude/work/raw/epmc_b2_cand.json (not committed:
it holds abstracts).

Run from the repo root:  python3 scripts/batches/b2026_11_10_epmc_b2.py
"""
import json
from pathlib import Path
from urllib.parse import quote

RAW = Path("/home/claude/work/raw")
cand = json.loads((RAW / "epmc_b2_cand.json").read_text())
# rank 339, fetched separately after the 330-399 extension
cand["339"] = {"pmid": "11135342", "pmcid": "", "doi": "10.1002/1098-108x(200101)29:1<97::aid-eat17>3.0.co;2-2",
               "title": "Anorexia nervosa remission during an episode of encephalitis.", "authors": ["Ho AW", "Birmingham CL"],
               "journal": "Int J Eat Disord", "year": 2001, "vol": "29", "issue": "1", "pages": "97-99", "lang": "eng", "abs": "y"}
PATH = Path("data/cases.json")
d = json.loads(PATH.read_text())
TODAY = "2026-11-10"
LANG = {"eng": None, "swe": "Swedish", "spa": "Spanish", "ger": "German", "dan": "Danish", "und": "Spanish"}


def ckn(doi):
    return "https://go.openathens.net/redirector/ckn.qldhealth.com?url=" + quote("https://doi.org/" + doi, safe="")


R = []
def rec(**k):
    R.append(k)

SEIZ_PSY = ("known", "Seizures relieving psychosis is the principle of convulsive therapy (Meduna, 1934).")
SEIZ_DEP = ("known", "Seizures relieving depression is the principle of convulsive therapy; unexpected here as unplanned seizures.")
STROKE_DEP = ("emerging", "Joins other reports of mood disorders remitting after stroke; lesion-network analyses are recent.")

rec(id="freeman-2001", src="84", design="Case report", n=1, cats=["Trauma & stressor-related"],
    spec="Chronic combat-related PTSD", chronic=True, tr=None,
    tcat="Acquired brain lesion", tspec="Right frontal lobe infarct", intent="Injury or illness", res="Partial", rev="None reported", dl=1,
    summary="A combat veteran's intrusive memories, nightmares and avoidance stopped after a right frontal stroke; the hyperarousal stayed.",
    caveat="History comes partly from family; arousal symptoms persisted, so the PTSD was only partly abolished.",
    tags=["ptsd", "stroke", "frontal", "right-hemisphere", "lesion"], tier="B",
    era=("emerging", "Fits later lesion work: Koenigs 2008 found vmPFC and amygdala damage protected Vietnam veterans from PTSD."))
rec(id="dusoir-2005", src="65", design="Letter", n=1, cats=["Eating"], spec="Anorexia nervosa", chronic=None, tr=None,
    tcat="Acquired brain lesion", tspec="Left thalamic stroke", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Anorexia nervosa remitted after a left thalamic stroke.",
    caveat="Short report; illness duration, measures and follow-up need the full text (free on PMC).",
    tags=["anorexia", "stroke", "thalamus", "left-hemisphere", "lesion"], tier="B",
    era=("emerging", "One of a small set of eating-disorder remissions after brain lesions (see Uher & Treasure 2005)."))
rec(id="ho-2001", src="339", design="Case report", n=1, cats=["Eating"], spec="Anorexia nervosa (weight 37.8 kg)", chronic=None, tr=None,
    tcat="Fever / infection", tspec="Encephalitis with hypoxic brain injury", intent="Injury or illness", res="Temporary",
    rev="Natural off-on", dl=1,
    summary="Anorexic behaviour vanished during encephalitis with hypoxic brain injury and came back once the neurological signs cleared.",
    caveat="Weight gain may partly reflect inpatient care during the illness.",
    tags=["anorexia", "encephalitis", "hypoxia", "reversal"], tier="B",
    era=("emerging", "One of a small set of eating-disorder remissions after brain insults; the return with recovery is the informative part."))
rec(id="calache-1991", src="107", design="Case report", n=1, cats=["Mood"], spec="Major depression", chronic=None, tr=None,
    tcat="Physiological stress", tspec="Cardiopulmonary arrest and anoxic encephalopathy after attempted hanging", intent="Injury or illness",
    res="Complete", rev="None reported", dl=0,
    summary="Depression remitted after a hanging attempt caused cardiac arrest and anoxic brain injury, with no lasting neurological deficit.",
    caveat="Psychosocial change after a suicide attempt is a strong alternative explanation; the authors discuss it.",
    tags=["depression", "hypoxia", "suicide-attempt"], tier="C")
rec(id="rubin-1985", src="120", design="Case report", n=1, cats=["Mood", "Psychotic"], spec="Prolonged unipolar psychotic depression, unresponsive to antidepressants",
    chronic=True, tr=True, tcat="Seizures", tspec="Two drug-induced grand mal seizures", intent="Injury or illness",
    res="Partial", rev="None reported", dl=0,
    summary="Treatment-resistant psychotic depression improved rapidly after two grand mal seizures caused by medication.",
    caveat="'Rapid improvement' rather than stated remission; durability needs the full text.",
    tags=["depression", "psychotic-depression", "seizure"], tier="B", era=SEIZ_DEP)
rec(id="spiers-2016", src="14", design="Letter", n=1, cats=["Psychotic"], spec="Organic (secondary) psychosis", chronic=None, tr=None,
    tcat="Seizures", tspec="A spontaneous seizure", intent="Injury or illness", res="Partial", rev="None reported", dl=0,
    summary="An organic psychosis improved after a spontaneous seizure (Australian and New Zealand report).",
    caveat="Letter without an abstract; the underlying cause and its course need the full text.",
    tags=["psychosis", "secondary-psychosis", "seizure", "australia"], tier="C", era=SEIZ_PSY)
rec(id="wilcox-2008", src="52", design="Letter", n=1, cats=["Mood"], spec="Depression", chronic=None, tr=None,
    tcat="Acquired brain lesion", tspec="Stroke", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Depression was 'cured' by a stroke.",
    caveat="One-page letter without an abstract; site, severity and follow-up need the full text.",
    tags=["depression", "stroke", "lesion"], tier="C", era=STROKE_DEP)
rec(id="odeh-1989", src="112", design="Letter", n=1, cats=["Mood"], spec="Depression", chronic=None, tr=None,
    tcat="Acquired brain lesion", tspec="Stroke", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Depression lifted after a stroke.",
    caveat="Two-page report without an abstract; site and follow-up need the full text.",
    tags=["depression", "stroke", "lesion"], tier="C", era=STROKE_DEP)
rec(id="martin-santos-1950", src="280", design="Case report", n=1, cats=["Mood", "Anxiety"], spec="Anxious depression", chronic=None, tr=None,
    tcat="Acquired brain lesion", tspec="A minor stroke", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Anxious depression was cured after a minor stroke (1950, Spanish).",
    caveat="Spanish-language paper without an abstract; details need the full text.",
    tags=["depression", "anxiety", "stroke", "lesion", "spanish"], tier="C", era=STROKE_DEP)
rec(id="behar-1999", src="94", design="Letter", n=1, cats=["Psychotic"], spec="Severe chronic psychosis", chronic=True, tr=None,
    tcat="Coma / anaesthesia", tspec="Coma from septicaemia", intent="Injury or illness", res="Complete", rev="None reported", dl=1,
    summary="Severe chronic psychosis cleared after a coma caused by septicaemia.",
    caveat="Letter without an abstract; fever, sepsis and coma are confounded, and follow-up needs the full text.",
    tags=["psychosis", "sepsis", "coma", "fever"], tier="C",
    era=("emerging", "Joins older reports of psychosis remitting after fever, infection or coma."))
rec(id="galati-2013", src="20", design="Letter", n=1, cats=["Psychotic"], spec="Schizophrenia", chronic=None, tr=None,
    tcat="Acquired brain lesion", tspec="Carbon monoxide poisoning with pallidal lesions", intent="Injury or illness",
    res="Partial", rev="None reported", dl=1,
    summary="Schizophrenia symptoms eased after carbon monoxide poisoning damaged the globus pallidus.",
    caveat="Letter without an abstract; which symptoms improved, and for how long, needs the full text.",
    tags=["schizophrenia", "carbon-monoxide", "globus-pallidus", "lesion"], tier="C")
rec(id="ferrao-2003", src="78", design="Letter", n=1, cats=["Obsessive-compulsive & tic"], spec="Trichotillomania", chronic=None, tr=None,
    tcat="Acquired brain lesion", tspec="Basal ganglia haemorrhage", intent="Injury or illness", res="Temporary", rev="None reported", dl=1,
    summary="Hair-pulling stopped for a while after a basal ganglia haemorrhage.",
    caveat="Letter; the suppression was temporary and its length needs the full text.",
    tags=["trichotillomania", "haemorrhage", "basal-ganglia", "lesion"], tier="C")
rec(id="takano-2002", src="5", design="Letter", n=1, cats=["Psychotic"], spec="Schizophrenia", chronic=None, tr=None,
    tcat="Surgery or procedure (outside the brain)", tspec="Stellate ganglion block", intent="Treatment for another condition",
    res="Partial", rev="None reported", dl=0,
    summary="A stellate ganglion block given by anaesthetists had an unexpected beneficial effect on schizophrenia.",
    caveat="Letter without an abstract; the indication for the block and the size of the effect need the full text.",
    tags=["schizophrenia", "stellate-ganglion-block", "sympathetic"], tier="C",
    era=("novel", "Stellate ganglion block later entered trials for PTSD, not for psychosis."))
rec(id="wahed-1934", src="281", design="Case report", n=1, cats=["Psychotic"], spec="Schizophrenia", chronic=None, tr=None,
    tcat="Fever / infection", tspec="Superimposed benign tertian malaria, treated with atebrin (mepacrine)", intent="Injury or illness",
    res="Complete", rev="None reported", dl=0,
    summary="Schizophrenia was reported cured after the patient caught malaria and was treated with atebrin (1934, India).",
    caveat="Diagnostic standards of 1934; fever, the antimalarial and natural remission cannot be separated.",
    tags=["schizophrenia", "malaria", "fever", "historical"], tier="C",
    era=("novel", "Malarial fever therapy, established for general paresis (Wagner-Jauregg, 1917), was tried in schizophrenia and abandoned."))
rec(id="hoirisch-clapauch-2013", src="303", design="Case series", n=5, cats=["Psychotic", "Mood"],
    spec="Psychotic illness, including chronic schizophrenia and long-term depression", chronic=True, tr=None,
    tcat="Medication for another condition", tspec="Long-term warfarin for thrombosis, in patients with thrombophilias", intent="Treatment for another condition",
    res="Complete", rev="None reported", dl=0,
    summary="Five psychotic patients on long-term warfarin for blood clots remitted and stayed off psychotropics for 2 to 11 years.",
    caveat="Hypothesis paper in Medical Hypotheses by the authors of the plasminogen-activator theory; selection and diagnoses need checking.",
    tags=["psychosis", "warfarin", "anticoagulation", "thrombophilia"], tier="C", flags=["venue", "overclaim"])

existing = {r["id"] for r in d["records"]}
lib_pmids = {r["ids"].get("pmid") for r in d["records"]}
added = 0
for k in R:
    c = cand[k["src"]]
    if k["id"] in existing or c["pmid"] in lib_pmids:
        print("skip (already in library):", k["id"])
        continue
    au = ", ".join(c["authors"][:6]) + (" et al." if len(c["authors"]) > 6 else "")
    cit = dict(authors=au, title=c["title"], journal=c["journal"], year=int(c["year"]), volume=c["vol"], issue=c["issue"], pages=c["pages"])
    doi, pmid, pmcid = (c["doi"] or "").lower(), c["pmid"], c["pmcid"]
    links = {"full_text": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/" if pmcid else None,
             "abstract": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
             "doi": f"https://doi.org/{doi}" if doi else None, "alternates": [], "ckn": ckn(doi) if doi else None}
    era = k.get("era") or (("emerging" if k["dl"] >= 1 else "novel"), "")
    lang = LANG.get(c.get("lang"), None)
    d["records"].append({
        "id": k["id"], "record_type": "case", "status": "Provisional", "tier": k["tier"], "collections": ["phase1b"],
        "citation": cit, "ids": {"doi": doi, "pmid": pmid, "pmcid": pmcid}, "links": links,
        "access": "Free full text" if pmcid else "Paywalled",
        "design": k["design"], "n_patients": k["n"],
        "syndrome": {"categories": k["cats"], "specific": k["spec"], "chronic": k["chronic"], "treatment_resistant": k["tr"]},
        "trigger": {"category": k["tcat"], "specific": k["tspec"], "intent": k["intent"]},
        "outcome": {"resolution": k["res"], "time_to_resolution": None, "follow_up": None, "reversal": k["rev"]},
        "downstream": {"level": k["dl"], "note": "", "links": []},
        "summary": k["summary"], "caveat": k["caveat"] + (f" Published in {lang}." if lang and lang.lower() not in k["caveat"].lower() else ""),
        "tags": sorted(set(k["tags"])), "same_patient_as": None,
        "found_via": "Europe PMC (v1.2 broad query, year-sliced reload)", "date_added": TODAY,
        "verified": f"{TODAY}: {'abstract' if c.get('abs') else 'title'}-level appraisal; identifiers from Europe PMC",
        "era": {"label": era[0], "note": era[1], "basis": "judged" if k.get("era") else "from downstream level"},
        "flags": k.get("flags", []),
    })
    added += 1

d["updated"] = TODAY
PATH.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
print(f"added {added}; total {len(d['records'])}")
