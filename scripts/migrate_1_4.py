"""One-off migration: schema 1.3 -> 1.4 (2026-11-16).

Schema 1.4 gets the library ready for full-text appraisal (next item 5), the case-page display and the
hypothesis layer. Everything new is additive; no existing field changes meaning.

  appraisal   every record: what the appraisal so far rests on (basis), parsed from the `verified` text.
              The scored parts (unexpectedness T1-T4, attribution items, JBI answers) stay null until a
              full-text read fills them.
  timeline    optional, filled at full-text appraisal: per-patient tracks of events, timed from the exposure.
  lesion      optional, for brain triggers: kind, side, regions, aetiology, imaging, mappability.
  derived     written by scripts/derive.py (latency, durability, scores, the rule tier). Never edited by hand.
  vocabularies for all of the above.

It also creates data/hypotheses.json, the separate layer for our own reading of each case.

Run once from the repo root:  python3 scripts/migrate_1_4.py
"""
import json
import re
from pathlib import Path

PATH = Path("data/cases.json")
HYP = Path("data/hypotheses.json")
d = json.loads(PATH.read_text())
assert d["schema_version"] == "1.3", "already migrated"

V = d["vocabularies"]
V["appraisal_basis"] = {
    "Title": "Judged from the title only",
    "Abstract": "Judged from the abstract (or a database record's abstract)",
    "Full text": "Full text read",
    "Secondary source": "Read through a later paper or review that describes the case",
    "Unrecorded": "Added in the first rounds, before the appraisal basis was recorded",
}
V["unexpectedness_result"] = ["pass", "borderline"]
V["jbi_checklist"] = {"Case report": 8, "Case series": 10}
V["jbi_answer"] = ["Y", "N", "U", "NA"]
V["timeline_event"] = {
    "onset": "Syndrome began",
    "diagnosis": "Diagnosed",
    "treatment_failed": "Treatment tried without lasting benefit",
    "cointervention": "Other change around the time (possible confounder)",
    "exposure_start": "Exposure began (t = 0)",
    "exposure_stop": "Exposure stopped or ended",
    "exposure_restart": "Exposure restarted",
    "first_change": "First improvement",
    "best_response": "Best response",
    "relapse": "Symptoms returned",
    "assessment": "Assessment or observation",
    "follow_up": "Last follow-up",
}
V["time_unit"] = {"minutes": 1 / 1440, "hours": 1 / 24, "days": 1, "weeks": 7, "months": 30.4375, "years": 365.25}
V["time_precision"] = {
    "exact": "As stated, to the unit given",
    "approx": "About this time (the paper says about, several, early, and so on)",
    "at most": "Within this time: an upper bound",
    "at least": "After at least this time: a lower bound",
}
V["clinical_state"] = ["Remitted", "Partial", "Unchanged", "Worse"]
V["sex"] = ["F", "M", "Not stated"]
V["lesion_kind"] = ["Lesion", "Injury", "Resection or ablation", "Stimulation target"]
V["lesion_side"] = ["Left", "Right", "Bilateral", "Midline", "Unstated"]
V["lesion_region"] = [
    "Prefrontal, dorsolateral", "Prefrontal, ventromedial", "Orbitofrontal", "Anterior cingulate", "Frontal, other",
    "Insula", "Temporal, lateral", "Temporal, medial (amygdala, hippocampus)", "Parietal", "Occipital",
    "Caudate", "Putamen", "Ventral striatum (nucleus accumbens)", "Globus pallidus", "Internal capsule", "Thalamus",
    "Subthalamic nucleus", "Hypothalamus", "Bed nucleus of the stria terminalis", "Midbrain", "Pons", "Medulla",
    "Cerebellum", "Corpus callosum", "White matter, other", "Diffuse or multifocal", "Vagus nerve", "Spinal cord",
    "Unstated",
]
V["lesion_aetiology"] = ["Ischaemic stroke", "Haemorrhage", "Hypoxic-ischaemic", "Trauma", "Tumour", "Surgery",
                         "Infection", "Demyelination", "Not applicable", "Other"]
V["imaging"] = ["MRI", "CT", "MRI and CT", "Other", "None reported"]
V["mappable"] = {
    "Coordinates": "Coordinates or a normalised lesion mask are given",
    "Figure": "Images are shown, so the lesion could be traced onto a template",
    "Description only": "Named structures only, no images",
    "No": "No usable localisation",
}
V["latency_band"] = {
    "Under a day": "First change within 24 hours of the exposure",
    "1-13 days": "Within two weeks",
    "2 weeks to 3 months": "Weeks",
    "Over 3 months": "Months or longer",
}
V["durability"] = {
    "Sustained": "Still improved at the last follow-up, with no return",
    "Lost": "Symptoms returned and did not settle again",
    "Lost, then regained": "Symptoms returned, then settled again (often on re-exposure)",
    "Unknown": "No follow-up after the response",
}


def basis(verified):
    v = verified.lower()
    if "full text read" in v:
        return "Full text"
    if "abstract" in v:
        return "Abstract"
    if "title-level" in v:
        return "Title"
    return "Unrecorded"


for r in d["records"]:
    m = re.match(r"^(\d{4}-\d\d-\d\d)", r["verified"])
    b = basis(r["verified"])
    r["appraisal"] = {
        "basis": b,
        "date": m.group(1) if (m and b != "Unrecorded") else None,
        "by": None,
        "unexpectedness": None,
        "attribution": None,
        "jbi": None,
        "note": "",
    }

d["schema_version"] = "1.4"
PATH.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

if not HYP.exists():
    HYP.write_text(json.dumps({
        "layer": "Hypotheses: our reading of what happened in each case",
        "schema_version": "1.0",
        "updated": "2026-11-16",
        "rules": [
            "This file is ours, not the papers'. Facts about a case live in data/cases.json; if hypothesising turns up a factual error, fix the case record there.",
            "Every entry rates all seven boring explanations before proposing a mechanism. A case beats the null only when none is Likely.",
            "Hypotheses are ranked, each with a confidence, the specific variable driving the uncertainty, and an observation that would tell it apart from the next one.",
            "Claude's drafts stay status draft until Brendan has read them.",
        ],
        "vocabularies": {
            "status": {"draft": "Written, not yet discussed", "discussed": "Brendan and Claude have been through it", "settled": "Agreed reading, until new evidence"},
            "written_by": ["Claude", "Brendan", "Both"],
            "null_explanation": {
                "natural_history": "Natural history: spontaneous or episodic remission at this chronicity",
                "regression": "Regression to the mean: the patient presented at a peak",
                "misdiagnosis": "Misdiagnosis or secondary syndrome: the syndrome was driven by the condition being treated, or was something else",
                "cointervention": "Co-intervention: another treatment change, admission, adherence or circumstance at the same time",
                "nonspecific": "Non-specific suppression: sedation, sickness, apathy, cognitive or motor loss reduced all behaviour, not the syndrome itself",
                "expectancy": "Expectancy, placebo or attention: for functional disorders, suggestion may be the mechanism itself, so say so",
                "reporting": "Reporting artefact: selective reporting, single observer, no measure, overclaim",
            },
            "null_rating": ["Unlikely", "Possible", "Likely", "Can't judge"],
            "verdict": {
                "Beats the null": "No boring explanation is Likely; at least one specific feature (reversal, timing, specificity) separates it from chance",
                "Doesn't beat the null": "At least one boring explanation is Likely",
                "Undecided": "The paper doesn't give enough to judge",
            },
            "mechanism_level": ["Pharmacokinetic", "Neurotransmitter", "Cellular", "Systemic", "Circuit", "Psychological", "Non-specific"],
            "mechanism": {
                "Drug level change": "Pharmacokinetic",
                "Dopamine": "Neurotransmitter", "Serotonin": "Neurotransmitter", "Noradrenaline": "Neurotransmitter",
                "Acetylcholine": "Neurotransmitter", "GABA": "Neurotransmitter", "Glutamate": "Neurotransmitter",
                "Opioid": "Neurotransmitter", "Endocannabinoid": "Neurotransmitter", "Histamine": "Neurotransmitter",
                "Neuropeptide (oxytocin, orexin, other)": "Neurotransmitter",
                "Ion channels and excitability": "Cellular", "Intracellular signalling": "Cellular",
                "Neuroplasticity": "Cellular", "Bioenergetics and mitochondria": "Cellular", "Microglia and glia": "Cellular",
                "Inflammation and cytokines": "Systemic", "Fever and heat": "Systemic", "HPA axis and cortisol": "Systemic",
                "Thyroid": "Systemic", "Sex steroids and reproduction": "Systemic",
                "Metabolic state (ketosis, insulin, glucose)": "Systemic", "Gut-brain axis": "Systemic",
                "Respiratory and blood gases": "Systemic", "Sleep and circadian rhythm": "Systemic",
                "Lesion disconnection": "Circuit", "Stimulation of a circuit": "Circuit",
                "Network reset (seizure, coma, anaesthesia)": "Circuit", "Sensory input change": "Circuit",
                "Interoceptive and visceral input": "Circuit",
                "Meaning and life reorganisation": "Psychological", "Extinction and exposure": "Psychological",
                "Suggestion and belief update": "Psychological", "Threat and arousal": "Psychological",
                "Social and environmental change": "Psychological",
                "Global suppression (sedation, apathy, cognitive loss)": "Non-specific", "Sickness behaviour": "Non-specific",
            },
            "confidence": ["Low", "Moderate", "High"],
            "latency_fit": ["Fits", "Doesn't fit", "Can't judge"],
        },
        "entries": [],
    }, ensure_ascii=False, indent=1) + "\n")

from collections import Counter
print("migrated to 1.4; appraisal basis:", dict(Counter(r["appraisal"]["basis"] for r in d["records"])))
