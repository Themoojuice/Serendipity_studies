"""Turn fetched full texts into short reading dumps for appraisal (next item 5). Nothing here is committed.

Fetching (laptop browser, a tab on www.ebi.ac.uk): GET /europepmc/webservices/rest/<PMCID>/fullTextXML returns
JATS XML for open-access PMC articles (500 for the rest, e.g. scanned back issues and author manuscripts). Parse
in the page with DOMParser into {id, status, type, title, abstract, secs: [{t, x}], tables, figs}, keep results in
window.FT, then return JSON.stringify of ~200 KB chunks so each lands in a /tmp/claude-tool-results file.
Hidden browser panes throttle timers to about once a minute: use parallel fetches with no setTimeout pacing.

Usage:  python3 scripts/ft_dump.py <tool-result files...>   writes /tmp/ft/<case-id>.json and /tmp/ft/<case-id>.txt
"""
import json
import re
import sys
from pathlib import Path

OUT = Path("/tmp/ft")
INTRO = re.compile(r"intro|background", re.I)
DISC = re.compile(r"discussion|conclusion|comment|summary", re.I)
SKIP = re.compile(r"reference|competing|conflict|contribution|consent|acknowledg|funding|abbreviation|declaration|availability|ethic|contributor|supplementary|author", re.I)


def load(files):
    recs = []
    for f in files:
        t = json.load(open(f))[0]["text"]
        if "(captured at origin" in t:
            t = t[:t.rfind("\n\n(captured at origin")]
        v = json.loads(t)
        recs += json.loads(v) if isinstance(v, str) else v
    return recs


def dump(o, r):
    lines = [f"# {r['id']} · {o['id']} · {o.get('type')}", f"TITLE: {o.get('title')}",
             f"LIBRARY: {r['summary']} | caveat: {r['caveat']} | trigger: {r['trigger']['specific']} | "
             f"syndrome: {r['syndrome']['specific']} | reversal: {r['outcome']['reversal']} | tier {r['tier']} | "
             f"n={r['n_patients']} | flags {r['flags']}",
             "", "ABSTRACT: " + (o.get("abstract") or "")]
    for s in o.get("secs") or []:
        x = s["x"]
        if SKIP.search(s["t"] or ""):
            continue
        if INTRO.search(s["t"] or ""):
            x = x[:500] + (" […]" if len(x) > 500 else "")
        elif DISC.search(s["t"] or ""):
            x = x[:3000] + (" […]" if len(x) > 3000 else "")
        else:
            x = x[:10000] + (" […]" if len(x) > 10000 else "")
        lines += ["", f"=== {s['t'] or '(untitled)'}", x]
    if o.get("tables"):
        lines += ["", "TABLES: " + o["tables"][:3000]]
    if o.get("figs"):
        lines += ["", "FIGURES: " + o["figs"][:1000]]
    return "\n".join(lines)


def main(files):
    OUT.mkdir(exist_ok=True)
    d = json.loads(Path("data/cases.json").read_text())
    bypmc = {r["ids"]["pmcid"]: r for r in d["records"] if r["ids"].get("pmcid")}
    n = 0
    for o in load(files):
        r = bypmc.get(o["id"])
        if not r:
            continue
        (OUT / f"{r['id']}.json").write_text(json.dumps(o))
        (OUT / f"{r['id']}.txt").write_text(dump(o, r))
        n += 1
    print(f"{n} dumps in {OUT}")


if __name__ == "__main__":
    main(sys.argv[1:])
