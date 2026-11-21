"""Batch 2026-11-22: calibration v1, adjudication and the library changes it forced (protocol v1.8.6).

Brendan screened the 100 blinded step 1.1 records on 21 Nov (calibration.html, 78 minutes). Against Claude's first
title/abstract decisions: binary kappa 0.52 (stratified bootstrap 95% 0.35-0.68), raw agreement 78%, 3-way kappa 0.41
(he used no Unsure). Target 0.7 not met. Agreement was near-total on clear exclusions (39 of 40 in the top-ranked and
random strata); all 22 disagreements sat in the boundary strata. Abstracts re-read through the PubMed connector.

Brendan in, Claude out (11): Claude's exclusion stands for 10 at full-text level (Brendan's includes were liberal
title/abstract screening, as the protocol asks). One goes to full text: Albertini 2006, where Claude screened the
headline syndrome (compulsive masturbation, treated on purpose) and missed the second one the authors call unexpected
(the autism itself improving on mirtazapine).

Claude in, Brendan out (11): Brendan's call stands for 10. Claude's abstract-level includes were generous in three ways:
  T1  the abstract says the exposure was aimed at both conditions (fontaine-2004);
  T2  the effect was already known for that drug class or stimulation target when reported (GLP-1 drugs and drinking
      from 2025: takizawa-2026; prefrontal stimulation and binge eating after Downar 2012: sciortino-2021);
  T3  the syndrome was part of the treated illness (psychiatric syndromes of temporal lobe epilepsy clearing with
      seizure control: shahani-2019; acute psychosis the authors attribute to coeliac disease: serratrice-2002).
  Already settled the same way: romeo-2025 (E3, 17 Nov), Kaltenboeck 2023 (E3, 14 Nov). Not a case: pintor-2022 is a
  review kept as a context record. Settled now: Yashkov 2006 (E3). Claude's call stands for one: liu-2016, where the
  PsycInfo abstract showed the dopamine was given for septic shock (the title alone reads as deliberate treatment).

Consistency: the same three rules applied across the library (judgement calls, all reversible through the ledger):
  excluded  marchetti-2001, juiz-fernandez-2022 (T3, epilepsy); meilinger-2026, de-filippis-2026 (T2, GLP-1 drugs and
            substance use from 2025); nakama-2013 (T2, prefrontal rTMS trialled for PTSD before 2013).
  context   hill-2025 (T2, kept for its off-on pattern, linked from richards-2024); sciortino-2021 (linked from
            downar-2012); fontaine-2004 (T1/T2, linked from mallet-2002).
  kept, same question open: GLP-1 drugs and binge eating (jarvinen-2019, richards-2022, gong-2024), pica (bedell-2025)
            and a dopamine-agonist impulse control disorder (kelly-2026); rammouz-2024 (smoking on low-frequency rTMS);
            the gluten cases de-santis-1997 and jansson-1984 (chronic illness, attribution contested).

Run from the repo root:  python3 scripts/batches/b2026_11_22_calibration_v1_adjudication.py
"""
import csv
import json
import sys

sys.path.insert(0, "scripts")
from lib_code import Batch, CASES, HYP, LEDGER  # noqa: E402

TODAY = "2026-11-22"
CAL = "calibration v1 adjudication (protocol v1.8.6)"

EXCLUDE = {
    "shahani-2019": ("E4", "calibration v1 (Brendan out): the psychosis, depression and irritability of temporal lobe epilepsy improved as the seizures were controlled by surgery; a syndrome of the epilepsy resolving with its cause (T3)"),
    "marchetti-2001": ("E4", "calibration v1 consistency: an interictal psychosis grown out of postictal psychoses cleared once the seizure focus was removed; a syndrome of the epilepsy resolving with its cause (T3), as shahani-2019"),
    "juiz-fernandez-2022": ("E4", "calibration v1 consistency: anxious depression and phobias of drug-resistant epilepsy improved with seizure control after lobectomy (T3), as shahani-2019"),
    "serratrice-2002": ("E4", "calibration v1 (Brendan out): the authors present the sudden psychosis as a brain expression of coeliac disease (v1.7.2: the authors' own attribution means E4), and its sudden onset fails the chronicity criterion"),
    "guerdjikova-2026": ("E8", "calibration v1 (Brendan out): letter without an abstract; tirzepatide's indication is not stated, the authors' group studies these drugs for impulsive-compulsive problems, and less compulsive behaviour on GLP-1 drugs was widely reported by 2026 (T2). Revisit if the full text turns up"),
    "takizawa-2026": ("E3", "calibration v1 (Brendan out): by 2026 a GLP-1 drug cutting drinking was expected, after the 2025 randomised trial linked from richards-2024 (T2); only one of the three had alcohol use disorder"),
    "meilinger-2026": ("E3", "calibration v1 consistency: by 2026 a GLP-1 drug cutting drinking was expected (T2), as takizawa-2026"),
    "de-filippis-2026": ("E3", "calibration v1 consistency: less substance craving on GLP-1 drugs was expected by 2026 (T2); preprint"),
    "nakama-2013": ("E3", "calibration v1 consistency: prefrontal rTMS had been trialled for PTSD before 2013 (T2), and the PTSD improved alongside the depression being treated"),
}

# Era-expected replications worth keeping: reclassified as context records and linked from the founding case.
CONTEXT = {
    "hill-2025": ("richards-2024", "Context, not a case (calibration v1, protocol v1.8.6): by 2025 a GLP-1 drug cutting drinking was expected (T2). Kept for its natural off-on pattern, which the founding case series lacks.",
                  {"label": "Hill et al. 2025: dulaglutide, drinking off-on (context record)", "doi": "10.3389/fpsyt.2025.1420316"}),
    "sciortino-2021": ("downar-2012", "Context, not a case (calibration v1, protocol v1.8.6): after Downar 2012 and the same group's later series, prefrontal stimulation easing binge eating was expected, and the paper's own introduction calls neuromodulation a promising treatment for binge eating (T2).",
                       {"label": "Sciortino et al. 2021: theta-burst for bipolar depression, binge eating remitted (context record)", "doi": "10.3389/fpsyt.2021.732066"}),
    "fontaine-2004": ("mallet-2002", "Context, not a case (calibration v1, protocol v1.8.6): the abstract says stimulation was used to treat both the Parkinson's disease and the OCD (T1), and Mallet 2002 had already reported the effect (T2).",
                      {"label": "Fontaine et al. 2004: subthalamic stimulation, Yale-Brown 32 to 1 (context record)", "doi": "10.3171/jns.2004.100.6.1084"}),
}

ERA = {
    "richards-2024": {"label": "emerging", "basis": "judged", "note": "Among the first human reports. After the 2025 randomised trial, later reports of GLP-1 drugs cutting drinking count as expected (protocol v1.8.6); hill-2025 is kept as a context record for its off-on pattern."},
    "downar-2012": {"label": "emerging", "basis": "judged", "note": "The founding observation: the same group's dorsomedial rTMS series in binge-purge disorders followed. Later reports of prefrontal stimulation easing binge eating count as expected (protocol v1.8.6); sciortino-2021 is a context record."},
    "kelly-2026": {"label": "novel", "basis": "judged", "note": "By 2026 GLP-1 drugs were expected to cut drinking, but abolishing a dopamine-agonist impulse control disorder had not been predicted; the off-on pattern with each weekly dose is the strongest evidence in the GLP-1 group."},
}

LEDGER_SETTLE = {
    # record_id: (decision, reason, note)
    "R047390": ("excluded", "E3", "calibration v1 adjudication 2026-11-22: biliopancreatic diversion presented as a treatment for severe bulimia (4 of 6 not morbidly obese) by a surgical centre advocating it; settled from the abstract"),
    "R053690": ("unsure", "", "calibration v1 adjudication 2026-11-22 (Brendan in): mirtazapine was given for the compulsive masturbation, but the authors call the improvement in the autism itself (social interaction, communication, first pragmatic language) unexpected; that second syndrome needs the full text (Pediatr Neurol, Elsevier: ClinicalKey)"),
}


def append_rows(rows_new):
    rows = list(csv.DictReader(LEDGER.open()))
    fields = list(rows[0].keys())
    nid = max(int(r["record_id"][1:]) for r in rows) + 1
    with LEDGER.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        for r in rows_new:
            r["record_id"] = f"R{nid:06d}"
            nid += 1
            w.writerow(r)
    return nid


if __name__ == "__main__":
    b = Batch(TODAY, CAL)
    for cid, (code, note) in EXCLUDE.items():
        assert cid in b.by_id and b.by_id[cid]["record_type"] == "case", cid
        b.exclude(cid, code, note)
    b.save()  # drops the excluded records, writes their ledger rows

    d = json.loads(CASES.read_text())
    h = json.loads(HYP.read_text())
    R = {r["id"]: r for r in d["records"]}
    for cid, (founder, why, link) in CONTEXT.items():
        r = R[cid]
        assert r["record_type"] == "case", cid
        r["record_type"] = "context"
        r["tier"] = None
        r["caveat"] = why + (" " + r["caveat"] if r.get("caveat") else "")
        if "replication" not in r["tags"]:
            r["tags"] = sorted(r["tags"] + ["replication"])
        f = R[founder]
        if link["doi"] not in [x.get("doi") for x in f["downstream"]["links"]]:
            f["downstream"]["links"].append(link)
        f["downstream"]["level"] = max(f["downstream"]["level"], 1)
    h["entries"] = [e for e in h["entries"] if e["case_id"] not in CONTEXT]
    for e in h["entries"]:  # cross-references to excluded records go; context records stay referable
        e["related"] = [x for x in e.get("related") or [] if x["id"] not in EXCLUDE]
        if e["case_id"] == "kelly-2026" and "hill-2025" not in [x["id"] for x in e["related"]]:
            e["related"].append({"id": "hill-2025", "why": "Dulaglutide, drinking off-on with each weekly dose (context record)"})
    for cid, era in ERA.items():
        R[cid]["era"] = era
    d["updated"] = TODAY
    h["updated"] = TODAY
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    HYP.write_text(json.dumps(h, ensure_ascii=False, indent=1) + "\n")

    rows = list(csv.DictReader(LEDGER.open()))
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    new = []
    for cid, (founder, why, _) in CONTEXT.items():
        cur = [r for r in rows if cid in r["library_ids"].split(";") and r["record_id"] not in sup]
        assert cur, cid
        for r in cur:
            c = dict(r)
            c.update({"retrieved_date": TODAY, "screen_stage": "ft", "decision": "included", "reason_code": "",
                      "supersedes": r["record_id"], "notes": f"{CAL}: reclassified as a context record linked from {founder}. {why}"})
            new.append(c)
    for rid, (dec, code, note) in LEDGER_SETTLE.items():
        old = next(r for r in rows if r["record_id"] == rid)
        assert rid not in sup, rid
        c = dict(old)
        c.update({"retrieved_date": TODAY, "screen_stage": "ab", "decision": dec, "reason_code": code, "library_ids": "",
                  "supersedes": rid, "notes": note})
        new.append(c)
    append_rows(new)
    print(f"excluded {len(EXCLUDE)}, context {len(CONTEXT)}, ledger rows {len(new)} + exclusion rows")
