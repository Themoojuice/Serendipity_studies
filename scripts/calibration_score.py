#!/usr/bin/env python3
"""Score Brendan's blind calibration screen (protocol §10) against Claude's first decisions.

Usage:
    python3 scripts/calibration_score.py answers.json      # the text copied from calibration.html
    python3 scripts/calibration_score.py - < answers.json

Writes queries/calibration_v1_brendan.json (his calls, notes and the statistics) and prints:
- raw agreement and Cohen's kappa, binary (include or unsure = "to full text" vs exclude) and 3-way;
- the binary kappa re-weighted to the screened frame (each record counts frame_n / sample_n for its stratum),
  because the sample is enriched (a random 100 would hold about one include);
- a stratified bootstrap 95% interval for the binary kappa (2,000 resamples, seed 20261121);
- every disagreement, Brendan-in/Claude-out first: those records go back for full-text screening.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "queries/calibration_v1_sample.json"
KEY = ROOT / "queries/calibration_v1_key.json"
OUT = ROOT / "queries/calibration_v1_brendan.json"
LAB = {"I": "include", "U": "unsure", "E": "exclude"}


def claude_call(k):
    return {"included": "I", "unsure": "U"}.get(k["decision"], "E")


def binary(x):
    return "E" if x == "E" else "P"


def kappa(pairs, cats, w=None):
    n = agree = 0.0
    row = {c: 0.0 for c in cats}
    col = {c: 0.0 for c in cats}
    for p in pairs:
        wt = w(p) if w else 1.0
        n += wt
        agree += wt * (p["b"] == p["c"])
        row[p["b"]] += wt
        col[p["c"]] += wt
    po = agree / n
    pe = sum((row[c] / n) * (col[c] / n) for c in cats)
    return po, (1.0 if pe == 1 else (po - pe) / (1 - pe))


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    raw = sys.stdin.read() if src == "-" else Path(src).read_text()
    ans = json.loads(raw.strip())
    sample = json.loads(SAMPLE.read_text())["records"]
    key = json.loads(KEY.read_text())
    meta, kk = key["meta"], key["key"]
    assert ans.get("set") == meta["set"], f"answers are for {ans.get('set')}, key is {meta['set']}"
    d = ans["d"]
    assert len(d) == len(sample) == len(kk) and set(d) <= set("IUE"), "need one I/U/E per record"

    p3 = [{"i": k["i"], "s": k["stratum"], "b": d[k["i"]], "c": claude_call(k)} for k in kk]
    p2 = [dict(p, b=binary(p["b"]), c=binary(p["c"])) for p in p3]
    wfn = lambda p: meta["frame_sizes"][p["s"]] / meta["sample_sizes"][p["s"]]
    po2, k2 = kappa(p2, ["P", "E"])
    po3, k3 = kappa(p3, ["I", "U", "E"])
    po2w, k2w = kappa(p2, ["P", "E"], wfn)

    rng = random.Random(20261121)
    by_s = {}
    for p in p2:
        by_s.setdefault(p["s"], []).append(p)
    boots = []
    for _ in range(2000):
        bs = [rng.choice(v) for v in by_s.values() for _ in v]
        try:
            boots.append(kappa(bs, ["P", "E"])[1])
        except ZeroDivisionError:
            pass
    boots.sort()
    lo, hi = boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots)) - 1]

    per_stratum = {}
    for s, v in by_s.items():
        per_stratum[s] = {"n": len(v), "agree": sum(p["b"] == p["c"] for p in v)}

    conf = {b: {c: sum(1 for p in p3 if p["b"] == b and p["c"] == c) for c in "IUE"} for b in "IUE"}
    stats = {
        "binary_kappa": round(k2, 3), "binary_kappa_boot95": [round(lo, 3), round(hi, 3)],
        "binary_agreement": round(po2, 3), "binary_kappa_frame_weighted": round(k2w, 3),
        "binary_agreement_frame_weighted": round(po2w, 3),
        "three_way_kappa": round(k3, 3), "three_way_agreement": round(po3, 3),
        "confusion_brendan_by_claude": conf, "per_stratum": per_stratum, "target": 0.7,
        "met": k2 >= 0.7,
    }
    recs = []
    for p in p3:
        k, r = kk[p["i"]], sample[p["i"]]
        recs.append({"i": p["i"], "record_id": k["record_id"], "src": r["src"], "id": r["id"],
                     "brendan": p["b"], "reason": ans.get("r", {}).get(str(p["i"])) or "",
                     "note": ans.get("n", {}).get(str(p["i"])) or "", "claude": p["c"]})
    OUT.write_text(json.dumps({"meta": {"set": meta["set"], "started": ans.get("started"), "done": ans.get("done")},
                               "stats": stats, "records": recs}, indent=1, ensure_ascii=False) + "\n")

    print(f"binary kappa {k2:.2f} (95% {lo:.2f}–{hi:.2f}), agreement {po2:.0%}; "
          f"frame-weighted kappa {k2w:.2f}; 3-way kappa {k3:.2f} → target {'met' if k2 >= 0.7 else 'NOT met'}")
    print("confusion (rows Brendan, cols Claude, I/U/E):", conf)
    print("per stratum:", {s: f"{v['agree']}/{v['n']}" for s, v in per_stratum.items()})
    dis = [p for p in p3 if binary(p["b"]) != binary(p["c"])]
    dis.sort(key=lambda p: binary(p["b"]) != "P")
    for p in dis:
        k, r = kk[p["i"]], sample[p["i"]]
        note = ans.get("n", {}).get(str(p["i"]))
        print(f"\n#{p['i']} {k['record_id']} [{k['stratum']}] Brendan {LAB[p['b']]} / Claude {LAB[p['c']]}"
              f"{' ' + k['reason'] if k['reason'] else ''}{' → ' + k['library_ids'] if k['library_ids'] else ''}")
        print(f"   {r['title'][:150]}  ({r['au']}, {r['yr']}; {r['src']} {r['id']})")
        if note:
            print(f"   his note: {note}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
