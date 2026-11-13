"""Tidy 2026-11-13: fill empty caveats where the abstract or summary shows a specific competing explanation.

Caveats name one concrete alternative explanation for that case, not boilerplate. Records with nothing specific to
add (several lesion cases, context records) are left empty on purpose.
Run from the repo root:  python3 scripts/batches/b2026_11_13_caveats.py
"""
import json
from pathlib import Path

CAV = {
    "mallet-2002": "Dopaminergic doses usually fall after subthalamic surgery, and levodopa can drive compulsive behaviour.",
    "richards-2024": "Retrospective chart review; weight-loss motivation and clinic contact could also cut drinking.",
    "kuhn-2007": "Motivation and closer follow-up after surgery could explain abstinence.",
    "israel-2010": "The depression improved too, so the eating disorder may have followed mood.",
    "moreno-delgado-1997": "Self-reported, uncontrolled use; expectancy effects likely.",
    "kraft-westman-2009": "Weight loss, dropping gluten and a changed routine are inseparable from ketosis.",
    "solyom-1987": "Care and life changes after a suicide attempt may contribute.",
    "leonard-rapoport-1987": "Adolescent self-report; how long relief lasted is unclear.",
    "fontaine-2004": "Surgeons hoped stimulation would also help the OCD, so the benefit was not wholly unexpected.",
    "moussawi-2016": "Cognitive impairment and supervised living after the injury could explain abstinence.",
    "mackillop-2026": "Dense amnesia and dependent living limit access to cocaine.",
    "sosa-gomez-2026": "Pregnancy itself coincided with the seizures and the recovery.",
    "faruqui-2022": "Esketamine also lifted the depression, and less drinking may follow mood.",
    "jewett-2020": "The benefit faded; starting cancer maintenance treatment carries its own expectancy.",
    "downar-2012": "The same course treated the depression, and bulimia may have followed mood.",
    "abdollahifard-2026": "If the paedophilic urges were obsessional, OCD relief would explain their fading.",
    "klok-2025": "In functional disorder, coma offers expectation and a face-saving route to recovery.",
    "pantoni-1997": "Tics often wane by middle age.",
    "kosel-2007": "Relief from disabling tardive dyskinesia may itself have lifted the depression.",
    "sciortino-2021": "The same course treated the depression, and binge eating may have followed mood.",
    "rammouz-2024": "Smoking may have fallen as mood and OCD improved.",
    "barbieri-2005": "The OCD began with the epilepsy, so remission may simply follow seizure control.",
    "meilinger-2026": "Weight-loss counselling and clinic contact came with the drug.",
    "hill-2025": "Weight-loss programme contact came with the drug.",
    "takizawa-2026": "Only one of the three had alcohol use disorder; liver-disease advice to stop drinking came with the drug.",
    "lugo-radillo-2021": "Mushroom use may have been self-treatment rather than incidental.",
}
p = Path("data/cases.json"); d = json.loads(p.read_text()); n = 0
for r in d["records"]:
    if r["id"] in CAV and not (r.get("caveat") or "").strip():
        r["caveat"] = CAV[r["id"]]; n += 1
p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
print("caveats filled:", n)
