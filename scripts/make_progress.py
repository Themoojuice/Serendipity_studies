#!/usr/bin/env python3
"""Write data/progress.json, the live counts behind the site's roadmap page (roadmap.html).

Run after every batch, after scripts/make_fulltext_queue.py (it reads the queue's section counts).
Manual milestones (presentation build, launch) are set in MILESTONES below.
"""
import csv
import datetime
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MILESTONES = {  # id: done?
    "1a": True,   # free-copy sweep (done 2026-11-22) (OpenAlex / Crossref) of the queue and unsure rows
    "2b": False,  # calibration round 2
    "2c": False,  # readings review page
    "3a": True,   # case pages (v1 2026-11-22: #case/<id> on the library page)
    "3b": True,   # patterns (v1 2026-11-22: the library's Patterns tab, #patterns)
    "3c": True,   # methods page (v1 2026-11-22: methods.html, counts from data/methods.json)
    "3d": False,  # front page restyle, downloads, how to cite
    "4": False,   # launch: tagged version, README, archive
}


def main():
    d = json.loads((ROOT / "data/cases.json").read_text())
    h = json.loads((ROOT / "data/hypotheses.json").read_text())
    hyp = {e["case_id"]: e for e in h["entries"]}
    cases = [r for r in d["records"] if r["record_type"] == "case"]

    def coded(r):
        ap = r.get("appraisal") or {}
        return bool(ap.get("unexpectedness") and ap.get("attribution") and ap.get("jbi") and r["id"] in hyp)

    n_coded = sum(coded(r) for r in cases)
    basis = Counter((r.get("appraisal") or {}).get("basis", "Unrecorded") for r in cases if coded(r))
    tiers = Counter(r["tier"] for r in cases)

    queue = []
    q = ROOT / "docs/fulltext_queue.md"
    if q.exists():
        for m in re.finditer(r"^## (.+?) \((\d+)\)\s*$", q.read_text(), re.M):
            if not m.group(1).startswith("Unsure"):
                queue.append({"route": m.group(1), "n": int(m.group(2))})

    rows = list(csv.DictReader((ROOT / "ledger/records.csv").open()))
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = [r for r in rows if r["record_id"] not in sup]
    unsure = sum(r["decision"] == "unsure" for r in cur)

    cal = []
    for f in sorted((ROOT / "queries").glob("calibration_v*_brendan.json")):
        s = json.loads(f.read_text())["stats"]
        cal.append({"round": int(re.search(r"_v(\d+)_", f.name).group(1)), "kappa": s["binary_kappa"],
                    "ci": s["binary_kappa_boot95"], "target": s["target"], "met": s["met"]})

    rescreen = {"total": 0, "done": 0, "flagged": 0}
    rs = ROOT / "queries/rescreen_second_syndrome_v1.json"
    if rs.exists():
        x = json.loads(rs.read_text())
        rescreen = {k: x["meta"].get(k, 0) for k in ("total", "done", "flagged")}

    out = {
        "updated": datetime.date.today().isoformat(),
        "cases": len(cases), "coded": n_coded, "coded_basis": dict(basis), "tiers": dict(tiers),
        "queue": queue, "queue_total": sum(x["n"] for x in queue), "unsure_rows": unsure,
        "readings": {"total": len(hyp), "draft": sum(e.get("status") == "draft" for e in hyp.values()),
                     "reviewed": sum(e.get("status") == "reviewed" for e in hyp.values())},
        "calibration": cal, "rescreen": rescreen, "milestones": MILESTONES,
    }
    (ROOT / "data/progress.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"progress: {n_coded}/{len(cases)} coded, queue {out['queue_total']}, unsure {unsure}, "
          f"readings {out['readings']}, calibration {[c['kappa'] for c in cal]}")


if __name__ == "__main__":
    main()
