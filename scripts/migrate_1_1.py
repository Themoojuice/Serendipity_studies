"""One-off migration: schema 1.0 -> 1.1.

Adds the `era` field: where each finding stands now, so discoveries that were
unexpected when reported but are established since stay in the library,
labelled as such.

Run once from the repo root:  python3 scripts/migrate_1_1.py
"""
import json
from pathlib import Path

PATH = Path("data/cases.json")
d = json.loads(PATH.read_text())
assert d["schema_version"] == "1.0", "already migrated"

d["vocabularies"]["era"] = {
    "novel": "Still unexplained: nothing comparable established since",
    "emerging": "Emerging: similar cases, pooled data or trials, not yet settled",
    "known": "Known now: unexpected when reported, established since",
    "refuted": "Refuted: failed under controlled testing",
}

# Judged labels. Everything else defaults from downstream.level and is marked as such.
JUDGED = {
    "wagner-jauregg-1883": ("known", "Fever therapy for general paresis won the 1927 Nobel Prize; the observation is now psychiatric history."),
    "mallet-2002": ("known", "Subthalamic stimulation for OCD went on to a randomised trial (Mallet, NEJM 2008)."),
    "fontaine-2004": ("known", "Replicated Mallet 2002; the randomised STOC trial followed."),
    "naqvi-2007": ("known", "Addiction remission after insula and related lesions has since been pooled into one circuit (Joutsa, Nat Med 2022)."),
    "hefzy-2011": ("known", "Reported after the insula-smoking link was published (Naqvi 2007): a replication of an effect already known."),
    "wagemaker-cade-1977": ("refuted", "Remissions on dialysis did not survive sham-controlled testing (1980)."),
}

for r in d["records"]:
    if r["id"] in JUDGED:
        label, note = JUDGED[r["id"]]
        r["era"] = {"label": label, "note": note, "basis": "judged"}
    else:
        lvl = r["downstream"]["level"]
        r["era"] = {"label": "emerging" if lvl >= 1 else "novel", "note": "", "basis": "from downstream level"}

d["schema_version"] = "1.1"
d["unit_of_record"] = "One published study (a paper). n_patients counts patients within it; same_patient_as links papers describing the same patient."
PATH.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
from collections import Counter
print("migrated:", Counter(r["era"]["label"] for r in d["records"]))
