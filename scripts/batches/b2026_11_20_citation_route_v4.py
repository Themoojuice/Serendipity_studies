"""Batch 2026-11-20: citation route v4 (protocol v1.4: rerun one hop from any later includes).

Seeds: the 8 cases with a PMID added since route v3 (ray-2016, andreou-2008, abe-2016, benazzi-1993, levine-1996,
d-andrea-2013, macleod-1897, anon-1888-typhoid; riestra-2026 and granato-1994 have no PMID). Europe PMC /citations and
/references from the laptop browser: 111 links, 109 distinct records. Matched to current ledger rows by Europe PMC key,
PMID, DOI or normalised title: 1 library case, 12 already excluded, 13 blank rows, 83 new. All 96 new or blank titles
screened; abstracts read for the three possible cases.

Result: no new cases. The two case reports among the links were deliberate (hormone therapy for menstrual psychosis;
etizolam tried after Benazzi's report). Two reviews logged as leads for later: Brockington 1998 'Menstrual psychosis'
(old menstrual psychosis cases) and Sneader's 'The prehistory of psychotherapeutic agents' (serendipitous drug history).
The citation route stays converged.
Working file: /home/claude/work/raw/cit4_match.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_20_citation_route_v4.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import U, Ledger, log_runs  # noqa: E402

TODAY = "2026-11-20"
QID, SRC = "CIT_EPMC_v4", "Europe PMC citations"
M = json.loads(Path("/home/claude/work/raw/cit4_match.json").read_text())
DEC = {
    5: ("E3", "menstrual psychosis remitting once hormonal therapy was started for it"),
    8: ("E7", "Brockington 1998 review 'Menstrual psychosis' (title from Crossref); lead: its old case reports"),
    20: ("E3", "comment letter on Benazzi 1993; any etizolam given after that report was given for the voices"),
    33: ("E5", "randomised trial"), 51: ("E5", "trial protocol"), 52: ("E5", "open-label trial"), 57: ("E5", "open-label trial"),
    70: ("E5", "randomised trial"), 71: ("E5", "trial protocol"),
    74: ("E5", "retrospective cohort of ketamine and later PTSD"), 88: ("E5", "cohort of burned service members"),
    92: ("E5", "detoxification outcome series"), 93: ("E5", "review of anaesthesia-assisted detoxification"),
    94: ("E7", "Sneader, history of psychotherapeutic drugs and serendipity; lead for antique and serendipitous-drug sources"),
    95: ("E3", "prolonged sodium amytal narcosis used as a deliberate therapy"),
}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = {r["record_id"]: r for r in L.rows if r["record_id"] not in sup}
    todo_keys = {x["key"]: i for i, x in enumerate(M["todo"])}
    n = {"screened": 0, "corrections": 0, "already": 0, "included": 0}
    done = set()
    for x in M["all"]:
        title = x.get("title") or ("Menstrual psychosis" if x["doi"] == "10.1007/s007370050001" else "")
        base = dict(doi=x["doi"], pmid=x["pmid"], pmcid=x.get("pmcid", ""), other=x["key"], title=title, au=x.get("au") or "",
                    yr=x.get("yr") or "", jn=x.get("jn") or "")
        via = ",".join(x["via"])
        olds = [o for o in dict.fromkeys(x["blanks"].split(";")) if o and o not in done]
        if x["key"] in todo_keys:
            i = todo_keys[x["key"]]
            dec = DEC.get(i)
            L.add(SRC, QID, dec, **base, screened=True, supersedes=olds[0] if olds else "",
                  note=f"citation v4 item {i} of {len(M['todo'])}; via {via}; all titles screened; {x['kind2']}; {TODAY}")
            n["screened"] += 1
            for o in olds[1:]:
                L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o, screened=True,
                      note=f"screened via {x['key']} ({QID}); {TODAY}")
                n["corrections"] += 1
            done.update(olds)
            continue
        if x["kind2"] == "library":
            L.add(SRC, QID, None, **base, note=f"library case; via {via}; {TODAY}")
            n["included"] += 1
        else:
            prev = x["prev"][0]
            row = L.add(SRC, QID, (prev[2] or "", f"decided earlier as {prev[0]}"), **base, note=f"via {via}; {TODAY}")
            n["already"] += 1
    L.write()
    print(n)
    log_runs([(QID, SRC, "Europe PMC /citations + /references of the 8 cases with a PMID added since CIT_EPMC_v3",
               109, TODAY, "96 new or blank, all titles screened; no cases; 2 review leads (Brockington 1998, Sneader)")])
