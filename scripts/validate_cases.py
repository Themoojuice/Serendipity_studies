"""Validate data/cases.json before every commit.

Checks: unique ids, every controlled value is in its vocabulary, every record
has a clickable link, identifiers look right, same_patient_as points somewhere
real. Exits non-zero on any failure.

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
    if not (r["links"]["full_text"] or r["links"]["abstract"] or r["links"]["doi"]):
        err(rid, "no clickable link")
    if r["ids"]["doi"] and not DOI.match(r["ids"]["doi"]):
        err(rid, f"malformed DOI {r['ids']['doi']}")
    if r["ids"]["doi"] and r["ids"]["doi"] != r["ids"]["doi"].lower():
        err(rid, "DOI not lowercased")
    if r["ids"]["pmid"] and not str(r["ids"]["pmid"]).isdigit():
        err(rid, f"malformed PMID {r['ids']['pmid']}")
    if r["ids"]["pmcid"] and not re.match(r"^PMC\d+$", r["ids"]["pmcid"]):
        err(rid, f"malformed PMCID {r['ids']['pmcid']}")
    if not r["ids"]["doi"] and r["links"]["abstract"] is None and r["links"]["full_text"] is None:
        err(rid, "abstract-only records need a DOI or PMID so the PDF can be found")
    sp = r.get("same_patient_as")
    if sp and sp not in idset:
        err(rid, f"same_patient_as points to unknown id {sp}")

if errors:
    print(f"FAILED: {len(errors)} problem(s)")
    print("\n".join(errors))
    sys.exit(1)

cases = [r for r in R if r["record_type"] == "case"]
print(f"OK  schema {d['schema_version']} · {len(R)} records · {len(cases)} cases · "
      f"{sum(1 for r in cases if r['links']['full_text'])} free full text · "
      f"era {dict(Counter(r['era']['label'] for r in R))}")
