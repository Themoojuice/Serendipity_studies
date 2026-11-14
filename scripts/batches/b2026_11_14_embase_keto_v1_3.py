"""Batch 2026-11-14: Embase keto rerun (strings v1.3, ketogenic-only term), via CKN in the laptop browser.

Query (Embase advanced search, run through the UI as search #1, records read from the results endpoint):
  A(syndrome block, strings_v1_embase.json) AND ('ketogenic' OR 'nutritional ketosis' OR 'ketone ester' OR
  'exogenous ketone*' OR 'beta hydroxybutyrate' OR 'beta-hydroxybutyrate' OR 'low carbohydrate' OR 'low-carbohydrate'
  OR 'very low carbohydrate' OR carnivore OR 'modified atkins' OR 'atkins diet' OR 'medium chain triglyceride*' OR
  'intermittent fasting' OR 'therapeutic fasting' OR 'metabolic therapy' OR 'metabolic psychiatry'):ti,ab
  AND E(case block) AND [embase]/lim NOT [medline]/lim AND [humans]/lim
121 records: 107 already excluded, 2 library cases, 12 new or unscreened, all irrelevant (ketoacidosis noise remains
via beta-hydroxybutyrate). No new cases; the keto theme is closed in both databases.
Run from the repo root:  python3 scripts/batches/b2026_11_14_embase_keto_v1_3.py
"""
import json, sys
from pathlib import Path
sys.path.insert(0, "scripts")
from lib_add import Ledger, log_runs  # noqa: E402

TODAY = "2026-11-14"
recs = json.loads(Path("/home/claude/work/raw/emb_keto_v13_scored.json").read_text())
L = Ledger(TODAY)
for i, x in enumerate(recs):
    L.add("Embase via CKN", "EMB_keto_v1_3", None, doi=x["doi"], other=x["id"], title=x["title"],
          au=(x["au"] or "").split(" ")[0].rstrip(","), yr=x["yr"], jn=x["jn"],
          note=f"keto rerun v1.3, classifier order {i} (score {x['s']}); prior decision: {x['prior'] or 'none'}; {TODAY}")
L.write()
log_runs([("EMB_keto_v1_3", "Embase via CKN", "A AND ketogenic-only block AND E, Embase-only, humans", 121, TODAY,
           "107 previously excluded, 2 library, 12 new: no includes")])
