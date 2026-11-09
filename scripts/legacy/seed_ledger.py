"""One-off: seed ledger/records.csv and ledger/search_log.csv from the
informal rounds 1-2 run on 2026-11-09, before the protocol existed.

Rows are marked screen_stage=legacy. Library matches are marked included;
everything else is left undecided, to be re-screened under the protocol in step 1.1.
Metadata only: abstracts are not stored (copyright, and they can be re-fetched).

Run from the repo root:  python3 scripts/legacy/seed_ledger.py /home/claude/serendipity
"""
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd

SRC = Path(sys.argv[1])
DATE = "2026-11-09"
COLS = ["record_id", "source_db", "query_id", "retrieved_date", "doi", "pmid", "pmcid", "other_id",
        "title", "first_author", "year", "journal", "language", "cluster_id", "screen_stage",
        "decision", "reason_code", "library_ids", "flags", "supersedes", "notes"]


def norm_title(t):
    t = re.sub(r"<[^>]+>", " ", t or "").lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


lib = json.loads(Path("data/cases.json").read_text())["records"]
lib_by_pmid = {r["ids"]["pmid"]: r["id"] for r in lib if r["ids"]["pmid"]}
lib_by_doi = {r["ids"]["doi"]: r["id"] for r in lib if r["ids"]["doi"]}
lib_by_title = {norm_title(r["citation"]["title"]): r["id"] for r in lib}

rows = []


def add(**kw):
    row = {c: "" for c in COLS}
    row.update(kw)
    row["record_id"] = f"R{len(rows) + 1:06d}"
    row["retrieved_date"] = DATE
    row["screen_stage"] = "legacy"
    rows.append(row)


# PubMed: one row per (query, PMID), exactly as retrieved
pq = json.loads((SRC / "pubmed_queries.json").read_text())
for qid, q in pq["queries"].items():
    for pmid in q["pmids"]:
        lid = lib_by_pmid.get(str(pmid), "")
        add(source_db="PubMed", query_id=qid, pmid=str(pmid), cluster_id=f"pmid:{pmid}",
            decision="included" if lid else "", library_ids=lid)

# Consensus: three semantic queries
for i in (1, 2, 3):
    data = json.loads((SRC / f"consensus_q{i}.json").read_text())
    txt = "".join(x.get("text", "") for x in data)
    items = re.split(r"\n\[(\d+)\] ", txt)
    for j in range(1, len(items) - 1, 2):
        m = re.match(r"\[(.*?)\]\((.*?)\) \((.*?)\)", items[j + 1])
        if not m:
            continue
        title, url, meta = m.groups()
        parts = [p.strip() for p in meta.split(",")]
        year = next((p for p in parts if re.fullmatch(r"\d{4}", p)), "")
        journal = parts[-1] if len(parts) >= 4 else ""
        lid = lib_by_title.get(norm_title(title), "")
        add(source_db="Consensus", query_id=f"C{i}", other_id=url.split("?")[0], title=title,
            first_author=parts[0].replace(" et al.", ""), year=year, journal=journal,
            decision="included" if lid else "", library_ids=lid)

# Round-2 candidate decisions that came from web search (not in the rows above)
cand = pd.read_excel(SRC / "serendipity_round2_candidates.xlsx", sheet_name="Candidates")
seen_pmids = {r["pmid"] for r in rows if r["pmid"]}
for _, c in cand.iterrows():
    pmid = "" if pd.isna(c["PMID"]) else str(int(c["PMID"]))
    doi = "" if pd.isna(c["DOI"]) else str(c["DOI"]).lower()
    if pmid and pmid in seen_pmids:
        continue
    lid = lib_by_pmid.get(pmid) or lib_by_doi.get(doi, "")
    add(source_db=str(c["Found via"]), query_id="round2-websearch", doi=doi, pmid=pmid,
        first_author=str(c["First author"]), year=str(c["Year"]), journal=str(c["Journal"]),
        cluster_id=f"pmid:{pmid}" if pmid else (f"doi:{doi}" if doi else ""),
        decision="included" if lid else "candidate", library_ids=lid or "",
        notes=f"Round 2 tier {c['Tier']}: {c['What happened (the accident)']}")

# Every library record must trace to at least one ledger row: add the ones
# found by unlogged web searching or citation following in rounds 1-2.
traced = {lid for r in rows for lid in r["library_ids"].split(";") if lid}
for r in lib:
    if r["id"] in traced:
        continue
    c = r["citation"]
    add(source_db=r.get("found_via") or "Web search", query_id="legacy-unlogged", doi=r["ids"]["doi"],
        pmid=r["ids"]["pmid"], pmcid=r["ids"]["pmcid"], title=c["title"], first_author=c["authors"].split(",")[0],
        year=str(c["year"]), journal=c["journal"],
        cluster_id=f"pmid:{r['ids']['pmid']}" if r["ids"]["pmid"] else f"doi:{r['ids']['doi']}",
        decision="included", library_ids=r["id"], notes="Search string not logged (rounds 1-2, pre-protocol)")

Path("ledger").mkdir(exist_ok=True)
with open("ledger/records.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)

log = pd.read_excel(SRC / "serendipity_round2_candidates.xlsx", sheet_name="Search log")
log = log[log["Source"].notna() & ~log["Source"].astype(str).str.startswith("Total")]
log.insert(0, "query_id", "")
log.to_csv("ledger/search_log.csv", index=False)

inc = sum(1 for r in rows if r["decision"] == "included")
print(f"records.csv: {len(rows)} rows, {inc} matched to library; search_log.csv: {len(log)} runs")
