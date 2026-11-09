"""Shared helpers for batch scripts: add provisional library records and append ledger rows.

Factored out on 2026-11-10 from the phase 1b batch scripts, so each new batch only lists its
decisions. Run batch scripts from the repo root.
"""
import csv
import json
from pathlib import Path
from urllib.parse import quote

CASES = Path("data/cases.json")
LEDGER = Path("ledger/records.csv")
SEARCH_LOG = Path("ledger/search_log.csv")
COLS = ["record_id", "source_db", "query_id", "retrieved_date", "doi", "pmid", "pmcid", "other_id", "title", "first_author",
        "year", "journal", "language", "cluster_id", "screen_stage", "decision", "reason_code", "library_ids", "flags",
        "supersedes", "notes"]
LANG = {"eng": None, "swe": "Swedish", "spa": "Spanish", "ger": "German", "dan": "Danish", "fre": "French", "ita": "Italian",
        "jpn": "Japanese", "por": "Portuguese", "pol": "Polish", "dut": "Dutch", "rus": "Russian", "chi": "Chinese"}
U = "unsure"


def ckn(doi):
    return "https://go.openathens.net/redirector/ckn.qldhealth.com?url=" + quote("https://doi.org/" + doi, safe="")


def add_records(R, cand, *, collection, found_via, today):
    """R: list of dicts (id, src, design, n, cats, spec, chronic, tr, tcat, tspec, intent, res, rev, dl, summary,
    caveat, tags, tier, optional era=(label, note), flags). cand[src]: bibliographic fields from the source."""
    d = json.loads(CASES.read_text())
    existing = {r["id"] for r in d["records"]}
    lib_pmids = {r["ids"].get("pmid") for r in d["records"] if r["ids"].get("pmid")}
    added = []
    for k in R:
        c = cand[str(k["src"])]
        if k["id"] in existing or (c.get("pmid") and c["pmid"] in lib_pmids):
            print("skip (already in library):", k["id"])
            continue
        au = c.get("authorString") or ", ".join(c.get("authors", [])[:6])
        au = au.rstrip(".")
        cit = dict(authors=au, title=c["title"], journal=c["journal"], year=int(c["year"]), volume=c.get("vol", ""),
                   issue=c.get("issue", ""), pages=c.get("pages", ""))
        doi, pmid, pmcid = (c.get("doi") or "").lower(), c.get("pmid", ""), c.get("pmcid", "")
        links = {"full_text": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/" if pmcid else None,
                 "abstract": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
                 "doi": f"https://doi.org/{doi}" if doi else None, "alternates": [], "ckn": ckn(doi) if doi else None}
        era = k.get("era") or (("emerging" if k["dl"] >= 1 else "novel"), "")
        lang = LANG.get(c.get("lang"), None)
        caveat = k["caveat"] + (f" Published in {lang}." if lang and lang.lower() not in k["caveat"].lower() else "")
        d["records"].append({
            "id": k["id"], "record_type": "case", "status": "Provisional", "tier": k["tier"], "collections": [collection],
            "citation": cit, "ids": {"doi": doi, "pmid": pmid, "pmcid": pmcid}, "links": links,
            "access": "Free full text" if pmcid else "Paywalled",
            "design": k["design"], "n_patients": k["n"],
            "syndrome": {"categories": k["cats"], "specific": k["spec"], "chronic": k["chronic"], "treatment_resistant": k["tr"]},
            "trigger": {"category": k["tcat"], "specific": k["tspec"], "intent": k["intent"]},
            "outcome": {"resolution": k["res"], "time_to_resolution": None, "follow_up": None, "reversal": k["rev"]},
            "downstream": {"level": k["dl"], "note": "", "links": []},
            "summary": k["summary"], "caveat": caveat,
            "tags": sorted(set(k["tags"])), "same_patient_as": None,
            "found_via": found_via, "date_added": today,
            "verified": f"{today}: {'abstract' if c.get('abs') else 'title'}-level appraisal; identifiers from Europe PMC",
            "era": {"label": era[0], "note": era[1], "basis": "judged" if k.get("era") else "from downstream level"},
            "flags": k.get("flags", []),
        })
        added.append(k["id"])
    d["updated"] = today
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    print(f"library: added {len(added)}; total {len(d['records'])}")
    return added


class Ledger:
    """Append-only writer. Corrections of existing rows go in as new rows with `supersedes`."""

    def __init__(self, date):
        self.date = date
        self.rows = list(csv.DictReader(LEDGER.open()))
        self.nid = max(int(r["record_id"][1:]) for r in self.rows) + 1
        lib = json.loads(CASES.read_text())["records"]
        self.by_doi = {r["ids"]["doi"]: r["id"] for r in lib if r["ids"].get("doi")}
        self.by_pmid = {r["ids"]["pmid"]: r["id"] for r in lib if r["ids"].get("pmid")}
        self.new = []

    def lib_match(self, doi, pmid):
        return self.by_pmid.get(pmid or "") or self.by_doi.get((doi or "").lower(), "")

    def add(self, source_db, qid, dec, *, doi="", pmid="", pmcid="", other="", title="", au="", yr="", jn="", lang="",
            note="", supersedes="", screened=True, default_code=""):
        """dec: library id (str) -> included; (U, note) -> unsure; (code[, note]) -> excluded at abstract level;
        None -> title-level: included if it matches the library, else excluded (if screened) or blank."""
        row = {c: "" for c in COLS}
        doi = (doi or "").lower()
        row.update(record_id=f"R{self.nid:06d}", source_db=source_db, query_id=qid, retrieved_date=self.date, doi=doi,
                   pmid=pmid, pmcid=pmcid, other_id=other, title=(title or "")[:300], first_author=au, year=str(yr),
                   journal=jn, language=lang, cluster_id=("pmid:" + pmid) if pmid else (("doi:" + doi) if doi else ("x:" + other)),
                   supersedes=supersedes, notes=note)
        self.nid += 1
        m = self.lib_match(doi, pmid)
        if isinstance(dec, str):
            row.update(screen_stage="ab", decision="included", library_ids=dec)
        elif isinstance(dec, tuple) and dec[0] == U:
            row.update(screen_stage="ab", decision="unsure", notes=f"{note}; {dec[1]}")
        elif isinstance(dec, tuple):
            row.update(screen_stage="ab", decision="excluded", reason_code=dec[0],
                       notes=(f"{note}; {dec[1]}" if len(dec) > 1 else note))
        elif m:
            row.update(screen_stage="ta", decision="included", library_ids=m)
        elif screened:
            row.update(screen_stage="ta", decision="excluded", reason_code=default_code)
        self.new.append(row)
        return row

    def write(self):
        with LEDGER.open("a", newline="") as f:
            csv.DictWriter(f, fieldnames=COLS).writerows(self.new)
        print(f"ledger: +{len(self.new)} rows; now {len(self.rows) + len(self.new)}")


def log_runs(runs):
    """runs: (query_id, source, string, hits, date, notes)."""
    with SEARCH_LOG.open("a", newline="") as f:
        csv.writer(f).writerows(runs)
