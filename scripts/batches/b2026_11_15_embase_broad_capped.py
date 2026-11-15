"""Batch 2026-11-15: Embase broad Embase-only set, capped pull (protocol v1.7.6).

EMB_broad_v1_2 rerun through the UI (search #4): 30,456 Embase-only records. Pulled the top 2,000 by Embase relevance
(queries/strings_embase_broad_capped_v1.json). Matched to the ledger: 1,209 new, 124 blank, 619 excluded, 47 library
cases, 1 unsure. Screened in classifier order: ranks 0-333 (abstracts read for 10 candidates), then a seeded random 300
of ranks 334-1,332 (3 abstracts read) -> stopping rule met with no includes. The 699 unsampled records get blank rows.

Result: no new cases. With 47 library cases already inside the top 2,000, the existing routes have caught what this
set holds near the top; the remaining 28,456 records were not pulled.
Working files: /home/claude/work/raw/emb4_all.json, emb4_match.json, emb4_sample.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_15_embase_broad_capped.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import Ledger, log_runs  # noqa: E402

TODAY = "2026-11-15"
SRC, QID = "Embase via CKN", "EMB_broad_v1_2_capped"
M = json.loads(Path("/home/claude/work/raw/emb4_match.json").read_text())
SAMPLE = set(json.loads(Path("/home/claude/work/raw/emb4_sample.json").read_text()))
TODO = M["todo"]
RANK = {x[0]: i for i, x in enumerate(TODO)}
DEC = {
    0: ("E6", "conference version of Bijanki 2020 (same group, same amygdalotomy patients)"),
    3: ("E3", "pallidal DBS in Parkinson's with Tourette syndrome, Tourette parameters deliberate"),
    52: ("E7", "systematic review"),
    76: ("E1", "sleep-related eating disorder (a parasomnia) with sleep apnoea"),
    94: ("E7", "registry case series"),
    189: ("E3", "tiagabine trialled for the impulse control disorders"),
    203: ("E3", "oral contraceptive chosen for premenstrual dysphoric disorder"),
    229: ("E1", "oedema regressed on dulaglutide; not psychiatric"),
    252: ("E2", "schizophrenia unchanged after gastric bypass"),
    312: ("E3", "amantadine trialled for gambling"),
    591: ("E2", "atypical anorexia emerging during weight loss; no resolution"),
    592: ("E3", "HRT started after hormone testing in the depression work-up"),
    1121: ("E2", "pramipexole-induced gambling; no resolution described"),
}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = {r["record_id"]: r for r in L.rows if r["record_id"] not in sup}
    n = {"screened": 0, "unscreened": 0, "corrections": 0, "already": 0, "included": 0, "unsure": 0}
    for x in M["all"]:
        eid, q, title, otitle, ol, au, jn, yr, vol, iss, pg, doi, pt, rel, score, kind, blanks, libs, decided = x
        first = re.sub(r"\s+[A-Z][A-Za-z.\-]*\.$", "", (au or "").strip())
        base = dict(doi=doi, other=eid, title=title, au=first, yr=yr, jn=jn, lang=ol or "")
        olds = [o for o in dict.fromkeys(blanks.split(";")) if o and o in current and not current[o]["decision"]]
        if eid in RANK:
            i = RANK[eid]
            screened = i <= 333 or i in SAMPLE
            dec = DEC.get(i)
            how = "ranks 0-333" if i <= 333 else ("random sample, seed 20261115" if i in SAMPLE else "not screened (stopping rule met)")
            note = f"capped pull, relevance rank {rel}; rerank_v1 rank {i} of 1,333, score {score}; {how}; {kind}; {TODAY}"
            if screened:
                L.add(SRC, QID, dec, **base, screened=True, supersedes=olds[0] if olds else "", note=note)
                n["screened"] += 1
                for o in olds[1:]:
                    L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o,
                          screened=True, note=f"screened via Embase record {eid} ({QID}); {TODAY}")
                    n["corrections"] += 1
            else:
                L.add(SRC, QID, None, **base, screened=False, note=note)
                n["unscreened"] += 1
            continue
        prev = [current[r] for r in decided.split(";") if r in current]
        if kind == "included":
            L.add(SRC, QID, libs.split(";")[0], **base, note=f"library case, also found as {decided}; {TODAY}")
            n["included"] += 1
        elif kind == "unsure":
            from lib_add import U
            L.add(SRC, QID, (U, f"same record as {decided}, still unsure"), **base, note=TODAY)
            n["unsure"] += 1
        else:
            p = next(r for r in prev if r["decision"] == "excluded")
            row = L.add(SRC, QID, (p["reason_code"], f"decided earlier as {p['record_id']}"), **base, note=TODAY)
            row["screen_stage"] = p["screen_stage"]
            n["already"] += 1
    L.write()
    print(n)
    log_runs([(QID, SRC, "EMB_broad_v1_2 rerun (search #4, 30,456); top 2,000 by Embase relevance pulled", 2000, TODAY,
               "1,333 new or blank; ranks 0-333 + random 300 screened; stopping rule met; 0 cases")])
