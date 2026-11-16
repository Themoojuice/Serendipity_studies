"""Compute each record's `derived` block from its timeline and appraisal (schema 1.4).

Derived values are never typed by hand. This script is the only thing that writes them, and
validate_cases.py recomputes them and fails if the stored copy is stale.

From the first timeline track (the index patient):
  latency_days, latency_band, latency_bound   exposure start -> first improvement (else best response)
  baseline_years                              syndrome onset -> exposure
  follow_up_days                              exposure -> last follow-up
  durability                                  Sustained / Lost / Lost, then regained / Unknown
  timeline_reversal                           the reversal the events themselves show
  measures                                    standardised scores before and after the exposure
From the appraisal (protocol sections 4 to 6):
  attribution_score, attribution_grade        out of 6; A 5-6, B 4, C 2-3, D 0-1
  jbi_score, jbi_of                           count of Y answers, checklist length
  rule_tier                                   the tier section 6 gives; flags cap at C

Usage:  python3 scripts/derive.py            rewrite every record's derived block
"""
import json
from pathlib import Path

IMPROVE = ("first_change", "best_response")
BANDS = [(1, "Under a day"), (14, "1-13 days"), (91.3125, "2 weeks to 3 months"), (float("inf"), "Over 3 months")]


def days(e, V):
    """Event time in days from the exposure. A range (t to `to`) counts as its midpoint."""
    f = V["time_unit"][e["unit"]]
    t = e["t"] if e.get("to") is None else (e["t"] + e["to"]) / 2
    return t * f


def grade(score):
    return "A" if score >= 5 else "B" if score == 4 else "C" if score >= 2 else "D"


def rule_tier(att_grade, jbi_score, flags):
    if att_grade is None or jbi_score is None:
        return None
    if flags:
        return "C"
    if att_grade == "A" or (att_grade == "B" and jbi_score >= 6):
        return "A"
    if att_grade in ("B", "C") and jbi_score >= 4:
        return "B"
    return "C"


def timeline_part(track, V):
    out = {}
    ev = sorted(track["events"], key=lambda e: days(e, V))
    imp = [e for e in ev if e["kind"] in IMPROVE and days(e, V) >= 0]
    if imp:
        first = next((e for e in imp if e["kind"] == "first_change"), imp[0])
        lat = days(first, V)
        out["latency_days"] = round(lat, 3)
        out["latency_band"] = next(label for lim, label in BANDS if lat < lim)
        if first.get("precision") in ("at most", "at least"):
            out["latency_bound"] = first["precision"]
    onset = [e for e in ev if e["kind"] == "onset"]
    if onset and days(onset[0], V) < 0:
        out["baseline_years"] = round(-days(onset[0], V) / 365.25, 2)
    fu = [e for e in ev if e["kind"] == "follow_up"]
    if fu:
        out["follow_up_days"] = round(days(fu[-1], V), 3)

    # Durability: only events that belong to the exposure's effect move it. A later response to some other
    # treatment is coded as an assessment or the follow-up state, not as first_change/best_response.
    if imp:
        state, confirmed = "improved", False
        for e in ev[ev.index(imp[0]) + 1:]:
            k = e["kind"]
            if k == "relapse":
                state = "lost"
            elif k in IMPROVE and state == "lost":
                state = "regained"
            elif k in ("follow_up", "assessment") and e.get("state") in ("Remitted", "Partial") and state != "lost":
                confirmed = True
            elif k in ("follow_up", "assessment") and e.get("state") in ("Unchanged", "Worse") and state != "lost":
                state = "lost"
        out["durability"] = {"improved": "Sustained" if confirmed else "Unknown", "lost": "Lost",
                             "regained": "Lost, then regained"}[state]

    # Reversal shown by the events: a stop then a return (natural off-on); a restart after a return,
    # then improvement (rechallenge).
    rev, phase = "None reported", "on"
    for e in ev:
        k = e["kind"]
        if k == "exposure_stop" and phase == "on":
            phase = "stopped"
        elif k == "relapse" and phase == "stopped":
            phase, rev = "returned", "Natural off-on"
        elif k == "exposure_restart" and phase == "returned":
            phase = "restarted"
        elif k in IMPROVE and phase == "restarted":
            phase, rev = "rechallenged", "On-off rechallenge"
    out["timeline_reversal"] = rev

    scales = {}
    for e in ev:
        for s in e.get("scores") or []:
            scales.setdefault(s["scale"], []).append((days(e, V), s))
    measures = []
    for name, pts in scales.items():
        pre = [s for t, s in pts if t <= 0]
        post = [s for t, s in pts if t > 0]
        if pre and post:
            hib = pre[-1].get("higher_is_better", False)
            best = max(post, key=lambda s: s["value"]) if hib else min(post, key=lambda s: s["value"])
            b, a = pre[-1]["value"], best["value"]
            measures.append({"scale": name, "before": b, "after": a,
                             "change_pct": round((a - b) / b * 100, 1) if b else None})
    if measures:
        out["measures"] = measures
    return out


def derive_record(r, V):
    out = {}
    tracks = r.get("timeline") or []
    if tracks:
        out.update(timeline_part(tracks[0], V))
    ap = r.get("appraisal") or {}
    att = ap.get("attribution")
    g = None
    if att and all(att.get(k) is not None for k in ("baseline", "measure", "timing", "reversal", "confounders")):
        s = sum(att[k] for k in ("baseline", "measure", "timing", "reversal", "confounders"))
        g = grade(s)
        out["attribution_score"], out["attribution_grade"] = s, g
    jbi = ap.get("jbi")
    js = None
    if jbi and jbi.get("answers"):
        js = sum(1 for a in jbi["answers"] if a == "Y")
        out["jbi_score"], out["jbi_of"] = js, len(jbi["answers"])
    if r.get("record_type") == "case":
        t = rule_tier(g, js, r.get("flags") or [])
        if t:
            out["rule_tier"] = t
    return out or None


def main(path=Path("data/cases.json")):
    d = json.loads(path.read_text())
    n = 0
    for r in d["records"]:
        dv = derive_record(r, d["vocabularies"])
        if dv:
            r["derived"] = dv
            n += 1
        else:
            r.pop("derived", None)
    path.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    print(f"derived: {n} records with derived values")


if __name__ == "__main__":
    main()
