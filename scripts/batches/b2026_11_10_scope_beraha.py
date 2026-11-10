"""Batch 2026-11-10 (late): scope decision on Beraha 2017 (protocol v1.3.2).

Brendan: include Beraha 2017 on the strength of its on-off rechallenge evidence. Stuttering is not a target
syndrome for this library, so there is no stuttering sweep; this is a one-off inclusion.

Run from the repo root:  python3 scripts/batches/b2026_11_10_scope_beraha.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import Ledger, add_records  # noqa: E402

TODAY = "2026-11-10"
core = {r["nr"]: r for r in json.loads(Path("/home/claude/work/raw/rr_cand_abs.json").read_text())}
cand = {"439": core[439]}

R = [dict(id="beraha-2017", src=439, design="Case report", n=1, cats=["Neurodevelopmental"],
          spec="Stuttering (childhood-onset fluency disorder) in a man with alcohol dependence", chronic=None, tr=None,
          tcat="Medication for another condition", tspec="Baclofen 120 mg/day for alcohol dependence",
          intent="Treatment for another condition", res="Complete", rev="On-off rechallenge", dl=0,
          summary="A man's stuttering stopped on baclofen given for alcohol dependence, came back when it was stopped, "
                  "and stopped again when it was restarted.",
          caveat="Onset and duration of the stuttering need the full text; reduced drinking and anxiety are confounders. "
                 "Included as a one-off for its rechallenge evidence; stuttering is not a target syndrome.",
          tags=["baclofen", "gaba-b", "stuttering", "alcohol-dependence", "rechallenge"], tier="B")]

if __name__ == "__main__":
    add_records(R, cand, collection="phase1c", found_via="Europe PMC (v1.2 broad query, re-ranked tail v1)", today=TODAY)
    L = Ledger(TODAY)
    o = next(r for r in L.rows if r["record_id"] == "R053524")
    L.add(o["source_db"], o["query_id"], "beraha-2017", doi=o["doi"], pmid=o["pmid"], pmcid=o["pmcid"],
          other=o["other_id"], title=o["title"], au=o["first_author"], yr=o["year"], jn=o["journal"], lang=o["language"],
          note=f"scope decision (Brendan, {TODAY}): included for its on-off rechallenge evidence; no stuttering sweep",
          supersedes="R053524")
    L.write()
