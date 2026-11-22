"""Helpers for coding cases into schema 1.4 (full-text appraisal batches, next item 5).

A batch script imports these, codes each case as plain data, and saves. Then run
python3 scripts/derive.py && python3 scripts/validate_cases.py.

    from lib_code import Batch, ev, T, A, J, N, H
    b = Batch("2026-11-17", source="PMC full text (Europe PMC open-access XML)")
    b.code("smith-2010", tracks=[track("Patient", 40, "F", [ev(...), ...])],
           unexpectedness=T(secondary=("borderline", "why")), attribution=A(1, 0, 1, 2, 1, "note"),
           jbi=J("YYYYYYYY"), lesion=None, note="", fix={"caveat": "..."})
    b.reading("smith-2010", nulls=N(natural_history=("Unlikely", "why"), ...), verdict="...", note="...",
              hyps=[H(...)], related=[("other-id", "why")], questions="")
    b.save()
"""
import csv
import json
from pathlib import Path

CASES = Path("data/cases.json")
HYP = Path("data/hypotheses.json")
LEDGER = Path("ledger/records.csv")


def ev(kind, t, unit, label, precision="exact", **kw):
    """One timeline event. kw: to (range end), state, scores=[{"scale":..,"value":..}], note."""
    e = {"kind": kind, "t": t, "unit": unit, "precision": precision, "label": label}
    e.update({k: v for k, v in kw.items() if v is not None})
    return e


def track(patient, age, sex, events):
    return {"patient": patient, "age": age, "sex": sex, "events": events}


def T(target="pass", era="pass", secondary="pass", base_rate="pass"):
    """Unexpectedness T1-T4. Each argument is "pass" or ("borderline", "the specific doubt")."""
    def one(v):
        return {"result": "pass", "note": ""} if v == "pass" else {"result": v[0], "note": v[1]}
    return {"target": one(target), "era": one(era), "secondary": one(secondary), "base_rate": one(base_rate)}


def A(baseline, measure, timing, reversal, confounders, note=""):
    """Attribution items (protocol section 4): 0/1, 0/1, 0/1, 0/2, 0/1."""
    return {"baseline": baseline, "measure": measure, "timing": timing, "reversal": reversal,
            "confounders": confounders, "note": note}


def J(answers):
    """JBI answers as a string of Y/N/U/A (A = NA): 8 letters for a case report, 10 for a series."""
    a = ["NA" if c == "A" else c for c in answers]
    return {"checklist": {8: "Case report", 10: "Case series"}[len(a)], "answers": a}


def N(**kw):
    """The seven boring explanations: name=(rating, why)."""
    return {k: {"rating": v[0], "why": v[1]} for k, v in kw.items()}


def H(claim, chain, mechanisms, latency_fit, pro, con, confidence, driver, test):
    return {"claim": claim, "chain": chain, "mechanisms": list(mechanisms), "latency_fit": latency_fit,
            "for": pro, "against": con, "confidence": confidence, "uncertainty_driver": driver, "test": test}


class Batch:
    def __init__(self, today, source, by="Claude"):
        self.today, self.source, self.by = today, source, by
        self.d = json.loads(CASES.read_text())
        self.h = json.loads(HYP.read_text())
        self.by_id = {r["id"]: r for r in self.d["records"]}
        self.done = []
        self.excluded = {}

    def code(self, cid, tracks, unexpectedness, attribution, jbi, lesion=None, note="", fix=None, basis="Full text"):
        r = self.by_id[cid]
        if tracks:
            r["timeline"] = tracks
            r["outcome"]["time_to_resolution"] = None
            r["outcome"]["follow_up"] = None
        if lesion:
            r["lesion"] = lesion
        for k, v in (fix or {}).items():
            node = r
            parts = k.split(".")
            for p in parts[:-1]:
                node = node[p]
            node[parts[-1]] = v
        r["appraisal"] = {"basis": basis, "date": self.today, "by": self.by, "unexpectedness": unexpectedness,
                          "attribution": attribution, "jbi": jbi, "note": note}
        if basis == "Full text":
            r["verified"] = f"{self.today}: full text read ({self.source})"
        self.done.append(cid)

    def reading(self, cid, nulls, verdict, note, hyps, related=(), questions="", based_on="Full text"):
        self.h["entries"] = [e for e in self.h["entries"] if e["case_id"] != cid]
        e = {"case_id": cid, "status": "draft", "written_by": self.by, "date": self.today, "based_on": based_on,
             "nulls": nulls, "verdict": verdict, "verdict_note": note, "hypotheses": list(hyps),
             "related": [{"id": i, "why": w} for i, w in related]}
        if questions:
            e["questions"] = questions
        self.h["entries"].append(e)

    def exclude(self, cid, code, note):
        """Exclude a library record after full text: dropped from cases.json and hypotheses.json; ledger rows appended on save."""
        self.excluded[cid] = (code, f"full-text appraisal {self.today}: {note}")

    def _write_exclusions(self):
        if not self.excluded:
            return
        rows = list(csv.DictReader(LEDGER.open()))
        fields = list(rows[0].keys())
        sup = {r["supersedes"] for r in rows if r["supersedes"]}
        nid = max(int(r["record_id"][1:]) for r in rows) + 1
        with LEDGER.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            for cid, (code, note) in self.excluded.items():
                cur = [r for r in rows if cid in r["library_ids"].split(";") and r["record_id"] not in sup]
                assert cur, cid
                for r in cur:
                    c = dict(r)
                    c.update({"record_id": f"R{nid:06d}", "retrieved_date": self.today, "screen_stage": "ft", "decision": "excluded",
                              "reason_code": code, "library_ids": "", "flags": "", "supersedes": r["record_id"], "notes": note})
                    nid += 1
                    w.writerow(c)
        self.d["records"] = [r for r in self.d["records"] if r["id"] not in self.excluded]
        self.h["entries"] = [e for e in self.h["entries"] if e["case_id"] not in self.excluded]
        for e in self.h["entries"]:  # drop cross-references to records that no longer exist
            e["related"] = [x for x in e.get("related", []) if x["id"] not in self.excluded]

    def save(self):
        self._write_exclusions()
        for cid in self.done:
            r = self.by_id[cid]
            if r["status"] == "Provisional" and cid not in self.excluded:
                r["status"] = "Included"
            if cid not in self.excluded:  # tier always follows the section 6 rule once coded
                from derive import derive_record, rule_tier
                dv = derive_record(r, self.d["vocabularies"])
                rt = rule_tier(dv.get("attribution_grade"), dv.get("jbi_score"), r.get("flags"))
                if rt and rt != r.get("tier"):
                    print(f"  {cid}: tier {r.get('tier')} -> {rt} (rule)")
                    r["tier"] = rt
        self.d["updated"] = self.today
        self.h["updated"] = self.today
        CASES.write_text(json.dumps(self.d, ensure_ascii=False, indent=1) + "\n")
        HYP.write_text(json.dumps(self.h, ensure_ascii=False, indent=1) + "\n")
        print(f"coded {len(self.done)}: {', '.join(self.done)}" + (f"; excluded {', '.join(self.excluded)}" if self.excluded else ""))
