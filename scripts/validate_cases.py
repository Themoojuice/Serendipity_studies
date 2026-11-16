"""Validate data/cases.json before every commit.

Checks: unique ids, every controlled value is in its vocabulary, every record
has a clickable link, identifiers look right, same_patient_as points somewhere
real. Schema 1.4 adds: appraisal, timeline, lesion and derived blocks (derived must match
scripts/derive.py exactly), the section 6 tier rule for Included records, and the hypotheses layer
(data/hypotheses.json). Exits non-zero on any failure; warnings are printed but don't fail.

Usage:  python3 scripts/validate_cases.py [path]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/cases.json")
d = json.loads(path.read_text())
V = d["vocabularies"]
R = d["records"]
errors = []


def err(rid, msg):
    errors.append(f"{rid}: {msg}")


ids = [r["id"] for r in R]
for rid, n in Counter(ids).items():
    if n > 1:
        err(rid, f"duplicate id ({n}x)")
idset = set(ids)

DOI = re.compile(r"^10\.\d{4,9}/\S+$")
FLAGS = {"retracted", "concern", "venue", "mill", "media-first", "overclaim", "coi-trigger", "altmed", "no-followup", "preprint", "antique-bar"}
ANTIQUE_BEFORE = 1970
HIST_KEYS = {"original_terms", "modern_reading", "why_read"}
for r in R:
    rid = r["id"]
    if r["record_type"] not in ("case", "context"):
        err(rid, "record_type must be case or context")
    if r["status"] not in ("Included", "Provisional"):
        err(rid, f"bad status {r['status']}")
    if r["record_type"] == "case" and r.get("tier") not in V["tier"]:
        err(rid, f"bad tier {r.get('tier')}")
    for c in r["syndrome"]["categories"]:
        if c not in V["syndrome_category"]:
            err(rid, f"syndrome_category {c!r} not in vocabulary")
    for field, vocab in [(r["trigger"]["category"], "trigger_category"), (r["trigger"]["intent"], "trigger_intent"),
                         (r["outcome"]["resolution"], "resolution"), (r["outcome"]["reversal"], "reversal"),
                         (r["design"], "design")]:
        if field not in V[vocab]:
            err(rid, f"{vocab} {field!r} not in vocabulary")
    if str(r["downstream"]["level"]) not in V["downstream_level"]:
        err(rid, f"bad downstream level {r['downstream']['level']}")
    era = r.get("era")
    if not era or era.get("label") not in V["era"]:
        err(rid, "missing or bad era label")
    elif era["label"] in ("known", "refuted") and not era.get("note"):
        err(rid, "known/refuted era label needs a note saying when and how")
    if not (r["links"]["full_text"] or r["links"]["abstract"] or r["links"]["doi"] or r["links"].get("ckn")):
        err(rid, "no clickable link")
    if r["ids"]["doi"] and not DOI.match(r["ids"]["doi"]):
        err(rid, f"malformed DOI {r['ids']['doi']}")
    if r["ids"]["doi"] and r["ids"]["doi"] != r["ids"]["doi"].lower():
        err(rid, "DOI not lowercased")
    if r["ids"]["pmid"] and not str(r["ids"]["pmid"]).isdigit():
        err(rid, f"malformed PMID {r['ids']['pmid']}")
    if r["ids"]["pmcid"] and not re.match(r"^PMC\d+$", r["ids"]["pmcid"]):
        err(rid, f"malformed PMCID {r['ids']['pmcid']}")
    if not r["ids"]["doi"] and r["links"]["abstract"] is None and r["links"]["full_text"] is None and not r["links"].get("ckn"):
        err(rid, "records without full text need a DOI, PMID or CKN link so the PDF can be found")
    for fl in r.get("flags", []):
        if fl not in FLAGS:
            err(rid, f"unknown flag {fl}")
    oy = r.get("observed_year")
    if oy is not None and not (isinstance(oy, int) and 1500 <= oy <= 2027):
        err(rid, f"observed_year {oy!r} must be an integer year")
    h = r.get("historical")
    if h is not None:
        if not isinstance(h, dict) or set(h) - HIST_KEYS or not all(isinstance(v, str) for v in h.values()):
            err(rid, f"historical must be an object with only {sorted(HIST_KEYS)} as strings")
    if "antique-bar" in r.get("flags", []):
        if (oy or int(r["citation"]["year"])) >= ANTIQUE_BEFORE:
            err(rid, "antique-bar flag on a record observed in or after 1970")
        if not (h and h.get("why_read")):
            err(rid, "antique-bar records need historical.why_read")
    sp = r.get("same_patient_as")
    if sp and sp not in idset:
        err(rid, f"same_patient_as points to unknown id {sp}")

# ---- schema 1.4: appraisal, timeline, lesion, derived ------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from derive import days, derive_record  # noqa: E402

warnings = []


def warn(rid, msg):
    warnings.append(f"{rid}: {msg}")


DATE = re.compile(r"^\d{4}-\d\d-\d\d$")
BRAIN = {"Acquired brain lesion", "Traumatic brain injury", "Neurosurgery", "Brain stimulation"}
PRE_OK = {"onset", "diagnosis", "treatment_failed", "cointervention", "assessment"}
ATT_ITEMS = {"baseline": (0, 1), "measure": (0, 1), "timing": (0, 1), "reversal": (0, 2), "confounders": (0, 1)}
T_KEYS = {"target", "era", "secondary", "base_rate"}
EV_KEYS = {"kind", "t", "to", "unit", "precision", "label", "state", "scores", "note"}


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


for r in R:
    rid = r["id"]
    ap = r.get("appraisal")
    if not isinstance(ap, dict):
        err(rid, "missing appraisal block (schema 1.4)")
        continue
    if ap.get("basis") not in V["appraisal_basis"]:
        err(rid, f"appraisal.basis {ap.get('basis')!r} not in vocabulary")
    if ap.get("date") is not None and not DATE.match(str(ap["date"])):
        err(rid, "appraisal.date must be YYYY-MM-DD or null")
    if ap.get("by") not in (None, "Claude", "Brendan", "Both"):
        err(rid, "appraisal.by must be Claude, Brendan, Both or null")
    ux = ap.get("unexpectedness")
    if ux is not None:
        if not isinstance(ux, dict) or set(ux) != T_KEYS:
            err(rid, f"appraisal.unexpectedness needs exactly {sorted(T_KEYS)}")
        else:
            for k, v in ux.items():
                if not isinstance(v, dict) or v.get("result") not in V["unexpectedness_result"]:
                    err(rid, f"unexpectedness.{k}.result must be pass or borderline")
                elif v["result"] == "borderline" and not v.get("note"):
                    err(rid, f"unexpectedness.{k} is borderline, so it needs a note")
    att = ap.get("attribution")
    if att is not None:
        for k, allowed in ATT_ITEMS.items():
            if att.get(k) not in allowed:
                err(rid, f"attribution.{k} must be one of {allowed} (score every item, or leave attribution null)")
        extra = set(att) - set(ATT_ITEMS) - {"note"}
        if extra:
            err(rid, f"attribution has unknown keys {sorted(extra)}")
        if r["outcome"]["reversal"] == "None reported" and att.get("reversal") == 2:
            err(rid, "attribution.reversal scores 2 but outcome.reversal is None reported")
        if r["outcome"]["reversal"] != "None reported" and att.get("reversal") == 0 and not att.get("note"):
            warn(rid, "outcome.reversal reported but attribution.reversal is 0; say why in attribution.note")
    jbi = ap.get("jbi")
    if jbi is not None:
        n_items = V["jbi_checklist"].get(jbi.get("checklist"))
        if n_items is None:
            err(rid, "jbi.checklist must be Case report or Case series")
        elif not isinstance(jbi.get("answers"), list) or len(jbi["answers"]) != n_items or \
                any(a not in V["jbi_answer"] for a in jbi["answers"]):
            err(rid, f"jbi.answers must be {n_items} of Y/N/U/NA")
    if ap.get("basis") == "Full text" and r["record_type"] == "case" and ap.get("date", "") and ap["date"] >= "2026-11-16" \
            and not (ux and att and jbi):
        warn(rid, "full-text appraisal since schema 1.4 without unexpectedness, attribution and JBI all filled")

    tl = r.get("timeline")
    if tl is not None:
        if not isinstance(tl, list) or not tl:
            err(rid, "timeline must be a non-empty list of patient tracks, or absent")
            tl = []
        if r["outcome"]["time_to_resolution"] or r["outcome"]["follow_up"]:
            err(rid, "with a timeline, outcome.time_to_resolution and outcome.follow_up must be null (derived instead)")
        for i, tr in enumerate(tl):
            where = f"timeline[{i}]"
            if not isinstance(tr.get("patient"), str) or not tr["patient"]:
                err(rid, f"{where}.patient label missing")
            if tr.get("age") is not None and not num(tr["age"]):
                err(rid, f"{where}.age must be a number of years or null")
            if tr.get("sex") is not None and tr["sex"] not in V["sex"]:
                err(rid, f"{where}.sex not in vocabulary")
            evs = tr.get("events") or []
            if not evs:
                err(rid, f"{where} has no events")
                continue
            ok = True
            for j, e in enumerate(evs):
                w = f"{where}.events[{j}]"
                if set(e) - EV_KEYS:
                    err(rid, f"{w} has unknown keys {sorted(set(e) - EV_KEYS)}")
                if e.get("kind") not in V["timeline_event"]:
                    err(rid, f"{w}.kind {e.get('kind')!r} not in vocabulary"); ok = False; continue
                if not num(e.get("t")) or e.get("unit") not in V["time_unit"]:
                    err(rid, f"{w} needs a numeric t and a unit"); ok = False; continue
                if e.get("to") is not None and (not num(e["to"]) or e["to"] <= e["t"]):
                    err(rid, f"{w}.to must be a number greater than t")
                if e.get("precision") not in V["time_precision"]:
                    err(rid, f"{w}.precision must be one of {list(V['time_precision'])}")
                if not isinstance(e.get("label"), str) or not e["label"].strip():
                    err(rid, f"{w}.label missing")
                if e.get("state") is not None and e["state"] not in V["clinical_state"]:
                    err(rid, f"{w}.state not in vocabulary")
                for s in e.get("scores") or []:
                    if not isinstance(s.get("scale"), str) or not num(s.get("value")):
                        err(rid, f"{w}.scores entries need a scale name and a numeric value")
                if days(e, V) < 0 and e["kind"] not in PRE_OK:
                    err(rid, f"{w}: {e['kind']} cannot come before the exposure")
            if not ok:
                continue
            starts = [e for e in evs if e["kind"] == "exposure_start"]
            if len(starts) != 1 or starts[0]["t"] != 0:
                err(rid, f"{where} needs exactly one exposure_start, at t = 0")
            ts = [days(e, V) for e in evs]
            if ts != sorted(ts):
                err(rid, f"{where} events must be in time order")
            fus = [k for k, e in enumerate(evs) if e["kind"] == "follow_up"]
            if len(fus) > 1 or (fus and fus[0] != len(evs) - 1):
                err(rid, f"{where}: at most one follow_up, and it comes last")

    le = r.get("lesion")
    if le is not None:
        if r["trigger"]["category"] not in BRAIN:
            err(rid, "lesion block only for brain triggers (lesion, injury, neurosurgery, stimulation)")
        for k, vocab in [("kind", "lesion_kind"), ("side", "lesion_side"), ("aetiology", "lesion_aetiology"),
                         ("imaging", "imaging"), ("mappable", "mappable")]:
            if le.get(k) not in V[vocab]:
                err(rid, f"lesion.{k} {le.get(k)!r} not in vocabulary")
        if not le.get("regions") or any(x not in V["lesion_region"] for x in le["regions"]):
            err(rid, "lesion.regions must be a non-empty list from the lesion_region vocabulary")
        if not isinstance(le.get("specific"), str):
            err(rid, "lesion.specific must be a string (the site as the paper describes it)")

    want = derive_record(r, V)
    if want != r.get("derived"):
        err(rid, "derived block is stale or hand-edited: run python3 scripts/derive.py")
    elif want:
        rt = want.get("rule_tier")
        if rt and r.get("tier") != rt:
            (err if r["status"] == "Included" else warn)(rid, f"tier {r.get('tier')} but the section 6 rule gives {rt}")
        tlr = want.get("timeline_reversal")
        rank = {"None reported": 0, "Natural off-on": 1, "On-off rechallenge": 2}
        if tlr is not None and rank[r["outcome"]["reversal"]] > rank[tlr]:
            warn(rid, f"outcome.reversal says {r['outcome']['reversal']}, the timeline shows {tlr}")

# ---- hypotheses layer ---------------------------------------------------------------------------------
HP = path.parent / "hypotheses.json"
n_hyp = 0
if HP.exists():
    H = json.loads(HP.read_text())
    HV = H["vocabularies"]
    byid = {r["id"]: r for r in R}
    seen = set()
    for h in H["entries"]:
        cid = h.get("case_id")
        w = f"hypotheses[{cid}]"
        n_hyp += 1
        if cid not in byid or byid[cid]["record_type"] != "case":
            errors.append(f"{w}: case_id must name a case record in cases.json"); continue
        if cid in seen:
            errors.append(f"{w}: one entry per case")
        seen.add(cid)
        if h.get("status") not in HV["status"]:
            errors.append(f"{w}: status not in vocabulary")
        if h.get("written_by") not in HV["written_by"]:
            errors.append(f"{w}: written_by not in vocabulary")
        if not DATE.match(str(h.get("date", ""))):
            errors.append(f"{w}: date must be YYYY-MM-DD")
        if h.get("based_on") not in V["appraisal_basis"]:
            errors.append(f"{w}: based_on must be an appraisal_basis value")
        nulls = h.get("nulls") or {}
        if set(nulls) != set(HV["null_explanation"]):
            errors.append(f"{w}: rate all seven boring explanations ({', '.join(HV['null_explanation'])})")
        for k, v in nulls.items():
            if v.get("rating") not in HV["null_rating"]:
                errors.append(f"{w}: nulls.{k}.rating not in vocabulary")
            elif v["rating"] in ("Possible", "Likely") and not v.get("why"):
                errors.append(f"{w}: nulls.{k} is {v['rating']}, so it needs a why")
        if h.get("verdict") not in HV["verdict"]:
            errors.append(f"{w}: verdict not in vocabulary")
        elif h["verdict"] == "Beats the null" and any(v.get("rating") == "Likely" for v in nulls.values()):
            errors.append(f"{w}: a case with a Likely boring explanation cannot beat the null")
        hs = h.get("hypotheses") or []
        if not hs:
            errors.append(f"{w}: at least one candidate hypothesis, ranked")
        for i, c in enumerate(hs):
            for k in ("claim", "chain", "for", "against", "uncertainty_driver", "test"):
                if not isinstance(c.get(k), str) or not c[k].strip():
                    errors.append(f"{w}: hypotheses[{i}].{k} missing")
            if not c.get("mechanisms") or any(m not in HV["mechanism"] for m in c["mechanisms"]):
                errors.append(f"{w}: hypotheses[{i}].mechanisms must come from the mechanism vocabulary")
            if c.get("confidence") not in HV["confidence"]:
                errors.append(f"{w}: hypotheses[{i}].confidence not in vocabulary")
            if c.get("latency_fit") not in HV["latency_fit"]:
                errors.append(f"{w}: hypotheses[{i}].latency_fit not in vocabulary")
        for rel in h.get("related") or []:
            if rel.get("id") not in byid or not rel.get("why"):
                errors.append(f"{w}: related entries need a real record id and a why")

if errors:
    print(f"FAILED: {len(errors)} problem(s)")
    print("\n".join(errors))
    sys.exit(1)

for wmsg in warnings:
    print("warning:", wmsg)

cases = [r for r in R if r["record_type"] == "case"]
print(f"OK  schema {d['schema_version']} · {len(R)} records · {len(cases)} cases · "
      f"{sum(1 for r in cases if r['links']['full_text'])} free full text · "
      f"era {dict(Counter(r['era']['label'] for r in R))} · "
      f"{sum(1 for r in R if r.get('timeline'))} timelines · {n_hyp} hypothesis entries")
