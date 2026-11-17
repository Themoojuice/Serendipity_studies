"""Decisions after full-text appraisal (2026-11-17), delegated by Brendan ("go with your gut on all the calls").

Exclusions (record removed from the library, hypothesis entry dropped, ledger correction rows appended):
  gupta-2026     E3  a days-old relapse already easing on olanzapine and valproate started three days before;
                     the authors themselves credit treatment and natural course (criterion 3, T4)
  maddigan-2004  E1  a four-week first manic episode with two short trials: not chronic or treatment-resistant (criterion 1)
  viglione-2025  E1  catatonia about a day old and untreated: not chronic or treatment-resistant (criterion 1);
                     propofol relieving catatonia is also close to expected GABAergic pharmacology

Promotions: every fully coded Provisional case that passed full-text appraisal becomes Included (tier = rule tier).
"""
import csv
import json
from pathlib import Path

TODAY = "2026-11-17"
CASES, HYP, LEDGER = Path("data/cases.json"), Path("data/hypotheses.json"), Path("ledger/records.csv")
EXCL = {
    "gupta-2026": ("E3", "full-text appraisal 2026-11-17: days-old relapse already easing on olanzapine and valproate begun 3 days before the seizures; treatment response and natural course explain it (authors agree)"),
    "maddigan-2004": ("E1", "full-text appraisal 2026-11-17: four-week first manic episode with two short antipsychotic trials, so not chronic or treatment-resistant (criterion 1)"),
    "viglione-2025": ("E1", "full-text appraisal 2026-11-17: catatonia about a day old and untreated, so not chronic or treatment-resistant (criterion 1); propofol relief is near-expected GABAergic pharmacology"),
}

d = json.loads(CASES.read_text())
h = json.loads(HYP.read_text())

# ledger corrections
rows = list(csv.DictReader(LEDGER.open()))
fields = list(rows[0].keys())
superseded = {r["supersedes"] for r in rows if r["supersedes"]}
next_id = max(int(r["record_id"][1:]) for r in rows) + 1
new = []
for cid, (code, note) in EXCL.items():
    current = [r for r in rows if cid in r["library_ids"].split(";") and r["record_id"] not in superseded]
    assert current, cid
    for r in current:
        c = dict(r)
        c.update({"record_id": f"R{next_id:06d}", "retrieved_date": TODAY, "screen_stage": "ft", "decision": "excluded",
                  "reason_code": code, "library_ids": "", "flags": "", "supersedes": r["record_id"], "notes": note})
        next_id += 1
        new.append(c)
with LEDGER.open("a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    for c in new:
        w.writerow(c)

d["records"] = [r for r in d["records"] if r["id"] not in EXCL]
h["entries"] = [e for e in h["entries"] if e["case_id"] not in EXCL]

promoted = []
for r in d["records"]:
    ap = r.get("appraisal") or {}
    if r["record_type"] == "case" and r["status"] == "Provisional" and ap.get("attribution") and ap.get("jbi") and ap.get("unexpectedness"):
        r["status"] = "Included"
        promoted.append(r["id"])

d["updated"] = TODAY
CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
HYP.write_text(json.dumps(h, ensure_ascii=False, indent=1) + "\n")
print(f"excluded {len(EXCL)} ({len(new)} ledger rows); promoted {len(promoted)}: {', '.join(promoted)}")
