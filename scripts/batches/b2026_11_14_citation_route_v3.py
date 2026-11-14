"""Batch 2026-11-14: citation route v3 (protocol v1.7.3), one more hop from the cases added by citation route v2.

Seeds: Schweickert 1997, Taira 2003, Pozzi 2014, Miyazaki 2023 (the Embase round's new cases have no PMID, except
Matsui 2004, already a v2 seed). Europe PMC citations + references: 175 distinct records with IDs, 3 untitled-ID-less
references with titles (logged). Matched as in v2: 4 library cases, 48 excluded, 2 unsure, 4 blank, 117 new. All 121 new
or blank titles screened, abstracts read for every candidate.

Result: no new cases, 1 unsure (Kmetz 1997, kleptomania and mixed mania on valproate, letter without abstract).
The citation route has converged: a round added nothing (protocol v1.4: chase until a round adds nothing).
Working files: /home/claude/work/raw/cit3_all.json, cit3_match.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_14_citation_route_v3.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import U, Ledger, log_runs  # noqa: E402

TODAY = "2026-11-14"
QID, SRC = "CIT_EPMC_v3", "Europe PMC citations"
M = json.loads(Path("/home/claude/work/raw/cit3_match.json").read_text())
TODO = M["todo"]
RANK = {x[0]: i for i, x in enumerate(TODO)}
DEC = {
    0: ("E3", "posterior hypothalamic DBS aimed at the self-mutilation after brain injury"),
    16: ("E2", "intrathecal baclofen for dystonia in Lesch-Nyhan disease; no behavioural outcome reported"),
    35: (U, "letter, no abstract: valproate for mixed mania; did the kleptomania respond incidentally?"),
    69: ("E1", "psychological distress scores in a 15-patient spasticity study; no serious syndrome resolved"),
}
NOID_DEC = {}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = {r["record_id"]: r for r in L.rows if r["record_id"] not in sup}
    norm = lambda t: re.sub(r"[^a-z0-9]", "", (t or "").lower())[:80]  # noqa: E731
    idx = {}
    for r in current.values():
        if r["decision"]:
            for k in (r["other_id"], "pmid:" + r["pmid"] if r["pmid"] else "", "doi:" + r["doi"] if r["doi"] else "",
                      "t:" + norm(r["title"]) if len(norm(r["title"])) > 15 else ""):
                if k:
                    idx.setdefault(k, []).append(r)
    n = {"screened": 0, "corrections": 0, "already": 0, "included": 0, "unsure": 0, "noid": 0}
    done = set()
    for x in M["all"]:
        key, title, yr, doi, pmid, pmcid, au, jn, pt, lang, via, has_abs, score, kind, blanks, libs = x
        base = dict(doi=doi, pmid=pmid, pmcid=pmcid, other=key, title=title, au=au, yr=yr, jn=jn, lang=lang)
        olds = [o for o in dict.fromkeys(blanks.split(";")) if o and o not in done]
        if key in RANK:
            i = RANK[key]
            dec = DEC.get(i)
            L.add(SRC, QID, dec, **base, screened=True, supersedes=olds[0] if olds else "",
                  note=f"citation v3 rank {i} of 121, score {score}; via {via}; all titles screened; {kind}; {TODAY}")
            n["screened"] += 1
            for o in olds[1:]:
                L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o, screened=True,
                      note=f"screened via {key} ({QID}); {TODAY}")
                n["corrections"] += 1
            done.update(olds)
            continue
        if kind == "included":
            L.add(SRC, QID, libs.split(";")[0], **base, note=f"library case; via {via}; {TODAY}")
            n["included"] += 1
        elif kind == "unsure":
            L.add(SRC, QID, (U, "same record as an earlier unsure row, still unsure"), **base, note=f"via {via}; {TODAY}")
            n["unsure"] += 1
            print("unsure match:", key, title[:90])
        else:
            prev = next(r for k in (key, "pmid:" + pmid if pmid else "", "doi:" + doi if doi else "",
                                    "t:" + norm(title) if len(norm(title)) > 15 else "") if k for r in idx.get(k, [])
                        if r["decision"] == "excluded")
            row = L.add(SRC, QID, (prev["reason_code"], f"decided earlier as {prev['record_id']}"), **base, note=f"via {via}; {TODAY}")
            row["screen_stage"] = prev["screen_stage"]
            n["already"] += 1
        for o in olds:   # a blank row elsewhere for the same record: settle it the same way as the decided row
            dec = (libs.split(";")[0] if kind == "included" else (U, "as the decided row") if kind == "unsure"
                   else (prev["reason_code"], f"decided earlier as {prev['record_id']}"))
            L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o, screened=True,
                  note=f"same record as {key}, met again by {QID}; {TODAY}")
            n["corrections"] += 1
        done.update(olds)
    for i, y in enumerate(M["noid"]):
        seed, cr, title, au, jn, yr, doi, kind = y
        if not title:
            continue
        L.add(SRC, QID, NOID_DEC.get(i), title=title, au=au, yr=yr, jn=jn, doi=doi,
              pmid="23909968" if i == 69 else "", other=f"ref:{seed}:{i}", screened=True,
              note=f"reference of {seed} without an ID in Europe PMC; title screened; {TODAY}")
        n["noid"] += 1
    L.write()
    print(n)
    log_runs([(QID, SRC, "Europe PMC /citations + /references of the 4 cases added by CIT_EPMC_v2 (one more hop)",
               175, TODAY, "121 new or blank, all titles screened; no cases, 1 unsure; citation route converged")])
