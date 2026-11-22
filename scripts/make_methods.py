#!/usr/bin/env python3
"""Write data/methods.json, the counts behind the site's methods page (methods.html).

Run after every batch, with make_fulltext_queue.py and make_progress.py.
Counts come from the ledger (append-only; a row's current state is the last row that supersedes it),
the library (data/cases.json) and the calibration and re-screen files in queries/.
"""
import csv
import datetime
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_GROUP = {
    "Europe PMC": "Europe PMC (MEDLINE and more)", "Europe PMC full text": "Europe PMC (MEDLINE and more)",
    "Europe PMC citations": "Citation chasing (Europe PMC)",
    "Embase via CKN": "Embase", "Embase (CKN)": "Embase",
    "PsycInfo via CKN (EBSCO)": "PsycInfo",
    "PubMed": "PubMed", "Consensus": "Consensus", "Web search": "Other", "Supplied by Brendan": "Other",
}
RANK = {"included": 4, "candidate": 3, "unsure": 2, "excluded": 1, "": 0}


def key(r):
    return r["pmid"] or r["doi"].lower() or re.sub(r"\W+", " ", r["title"].lower()).strip()[:90]


def main():
    rows = list(csv.DictReader((ROOT / "ledger/records.csv").open()))
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    cur = [r for r in rows if r["record_id"] not in sup]

    best, reasons, sources = {}, defaultdict(Counter), defaultdict(set)
    for r in cur:
        k = key(r)
        sources[k].add(SOURCE_GROUP.get(r["source_db"], "Other"))
        if k not in best or RANK.get(r["decision"], 0) > RANK.get(best[k], 0):
            best[k] = r["decision"]
        if r["decision"] == "excluded" and r["reason_code"]:
            reasons[k][r["reason_code"]] += 1
    dec = Counter(best.values())
    excl_reason = Counter(reasons[k].most_common(1)[0][0] for k, v in best.items() if v == "excluded" and reasons[k])
    excl_unreasoned = sum(1 for k, v in best.items() if v == "excluded" and not reasons[k])
    by_source = Counter(s for k in best for s in sources[k])

    d = json.loads((ROOT / "data/cases.json").read_text())
    h = json.loads((ROOT / "data/hypotheses.json").read_text())
    hyp = {e["case_id"] for e in h["entries"]}
    cases = [r for r in d["records"] if r["record_type"] == "case"]
    coded = [r for r in cases if r["id"] in hyp and (r.get("appraisal") or {}).get("jbi")]
    ids = {r["id"] for r in cases}

    # capture-recapture: cases found through PsycInfo rows against cases found through any other source
    found = defaultdict(set)
    for r in rows:
        for cid in filter(None, r["library_ids"].split(";")):
            if cid in ids:
                found[cid].add("psy" if r["source_db"].startswith("PsycInfo") else "other")
    n1 = sum("psy" in v for v in found.values())
    n2 = sum("other" in v for v in found.values())
    m = sum(v >= {"psy", "other"} for v in found.values())
    chap = (n1 + 1) * (n2 + 1) / (m + 1) - 1
    var = (n1 + 1) * (n2 + 1) * (n1 - m) * (n2 - m) / ((m + 1) ** 2 * (m + 2))
    sd = math.sqrt(var)

    cal = []
    for f in sorted((ROOT / "queries").glob("calibration_v*_brendan.json")):
        s = json.loads(f.read_text())["stats"]
        cal.append({"round": int(re.search(r"_v(\d+)_", f.name).group(1)), "kappa": s["binary_kappa"], "ci": s["binary_kappa_boot95"],
                    "agreement": s["binary_agreement"], "three_way": s["three_way_kappa"], "target": s["target"], "met": s["met"]})
    rs = ROOT / "queries/rescreen_second_syndrome_v1.json"
    rescreen = json.loads(rs.read_text())["meta"] if rs.exists() else None
    proto = (ROOT / "protocol/PROTOCOL.md").read_text()
    versions = re.findall(r"· v(\d+\.\d+(?:\.\d+)?) ·", proto)

    out = {
        "updated": datetime.date.today().isoformat(),
        "protocol_version": versions[-1] if versions else "",
        "searches": len({r["query_id"] for r in rows}),
        "retrievals": len(cur),
        "distinct": len(best),
        "screened": len(best) - dec.get("", 0),
        "not_screened": dec.get("", 0),
        "excluded": dec.get("excluded", 0), "excluded_by_reason": dict(sorted(excl_reason.items())), "excluded_without_code": excl_unreasoned,
        "unsure": dec.get("unsure", 0) + dec.get("candidate", 0),
        "by_source": dict(by_source.most_common()),
        "library": {"cases": len(cases), "context": len(d["records"]) - len(cases), "coded": len(coded),
                    "tiers": dict(Counter(r["tier"] for r in cases)),
                    "antique": sum(1 for r in cases if "antique" in (r.get("collections") or [])),
                    "coded_basis": dict(Counter(r["appraisal"]["basis"] for r in coded))},
        "capture_recapture": {"psycinfo": n1, "other": n2, "both": m, "estimate": round(chap), "ci95": [round(chap - 1.96 * sd), round(chap + 1.96 * sd)]},
        "calibration": cal, "rescreen": rescreen,
    }
    (ROOT / "data/methods.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("distinct", "screened", "not_screened", "excluded", "unsure", "capture_recapture")}))


if __name__ == "__main__":
    main()
