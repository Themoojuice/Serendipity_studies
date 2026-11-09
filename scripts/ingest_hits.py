"""Append search hits to ledger/records.csv and build a screening queue.

Input: a JSON file of hits, either
  {"source_db": "...", "date": "YYYY-MM-DD", "runs": {query_id: [hit, ...]}}
where each hit is a dict with any of: doi, pmid, pmcid, other_id, title,
first_author, year, journal, language, pub_type.

Every hit becomes a ledger row (append-only). Rows get a cluster_id from
normalised identifiers (doi > pmid > pmcid > title hash). A cluster that is
already decided in the ledger keeps its decision; new clusters go to the
screening queue: work/queue_<tag>.tsv.

Usage: python3 scripts/ingest_hits.py hits.json <tag>
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

LEDGER = Path("ledger/records.csv")
COLS = ["record_id", "source_db", "query_id", "retrieved_date", "doi", "pmid", "pmcid", "other_id",
        "title", "first_author", "year", "journal", "language", "cluster_id", "screen_stage",
        "decision", "reason_code", "library_ids", "flags", "supersedes", "notes"]


def norm_doi(d):
    d = (d or "").strip().lower()
    d = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", d)
    return d.rstrip(".;,")


def norm_title(t):
    t = re.sub(r"<[^>]+>", " ", t or "").lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"^(a|an|the) ", "", re.sub(r"\s+", " ", t).strip())
    return t


def title_key(t):
    return "t:" + hashlib.sha1(norm_title(t).encode()).hexdigest()[:12]


def load_ledger():
    with LEDGER.open() as f:
        return list(csv.DictReader(f))


def main(path, tag):
    data = json.loads(Path(path).read_text())
    rows = load_ledger()
    next_id = max(int(r["record_id"][1:]) for r in rows) + 1

    # identifier -> cluster map from the existing ledger
    idmap, decided = {}, {}
    for r in rows:
        c = r["cluster_id"] or ""
        for k in (("doi:" + norm_doi(r["doi"])) if r["doi"] else None,
                  ("pmid:" + r["pmid"]) if r["pmid"] else None,
                  ("pmcid:" + r["pmcid"].upper()) if r["pmcid"] else None,
                  title_key(r["title"]) if r["title"] else None):
            if k and c:
                idmap.setdefault(k, c)
        if c and r["decision"]:
            decided[c] = r["decision"]

    new_rows, queue = [], {}
    for qid, hits in data["runs"].items():
        for h in hits:
            doi, pmid, pmcid = norm_doi(h.get("doi")), str(h.get("pmid") or ""), (h.get("pmcid") or "").upper()
            keys = [k for k in (("doi:" + doi) if doi else None, ("pmid:" + pmid) if pmid else None,
                                ("pmcid:" + pmcid) if pmcid else None,
                                title_key(h["title"]) if h.get("title") else None) if k]
            cluster = next((idmap[k] for k in keys if k in idmap), None)
            if not cluster:
                cluster = keys[0] if keys else f"x:{data['source_db']}:{h.get('other_id')}"
            for k in keys:
                idmap.setdefault(k, cluster)
            row = {c: "" for c in COLS}
            row.update(record_id=f"R{next_id:06d}", source_db=data["source_db"], query_id=qid,
                       retrieved_date=data["date"], doi=doi, pmid=pmid, pmcid=pmcid,
                       other_id=h.get("other_id", ""), title=(h.get("title") or "")[:300],
                       first_author=h.get("first_author", ""), year=str(h.get("year") or ""),
                       journal=h.get("journal", ""), language=h.get("language", ""),
                       cluster_id=cluster, screen_stage="")
            next_id += 1
            new_rows.append(row)
            if cluster not in decided and cluster not in queue:
                queue[cluster] = row

    with LEDGER.open("a", newline="") as f:
        csv.DictWriter(f, fieldnames=COLS).writerows(new_rows)

    Path("/home/claude/work").mkdir(exist_ok=True)
    qpath = Path(f"/home/claude/work/queue_{tag}.tsv")
    with qpath.open("w") as f:
        for c, r in queue.items():
            f.write("\t".join([c, r["year"], r["title"].replace("\t", " ")[:200], r["journal"][:40], r["query_id"]]) + "\n")
    print(f"appended {len(new_rows)} ledger rows; {len(queue)} clusters need screening -> {qpath}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
