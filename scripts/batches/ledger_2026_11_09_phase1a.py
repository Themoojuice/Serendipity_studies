"""Append the 2026-11-09 phase-1 runs to the ledger, with screening decisions.

Sources (exported from the browser, kept out of git):
  raw/epmc_ledger_chunks.json  Europe PMC v1.2 broad query, 21,000 of 43,112 records, in rank order
  raw/emb_s1.tsv               Embase strategy 1 (Embase-only), 578 records
  emb_title_ranked.tsv         Embase v1.2 title-restricted set (Embase-only), 1,375 records, in rank order

Screening state: Europe PMC ranks 0-699 title-screened; Embase S1 all 578; Embase title set ranks 0-308.
Unscreened rows get a blank decision.
Run from the repo root.
"""
import csv
import json
from pathlib import Path

W = Path("/home/claude/work")
LEDGER = Path("ledger/records.csv")
COLS = ["record_id", "source_db", "query_id", "retrieved_date", "doi", "pmid", "pmcid", "other_id", "title", "first_author",
        "year", "journal", "language", "cluster_id", "screen_stage", "decision", "reason_code", "library_ids", "flags",
        "supersedes", "notes"]
DATE = "2026-11-09"

lib = json.loads(Path("data/cases.json").read_text())["records"]
by_doi = {r["ids"]["doi"]: r["id"] for r in lib if r["ids"]["doi"]}
by_pmid = {r["ids"]["pmid"]: r["id"] for r in lib if r["ids"]["pmid"]}


def lib_match(doi, pmid):
    return by_pmid.get(pmid or "") or by_doi.get((doi or "").lower(), "")


# abstract-stage decisions by rank index: include -> library id, or (reason) / "unsure"
EP_DEC = {3: "zhang-2024", 12: "liu-2026", 13: "lipov-2024", 55: "gong-2024", 66: "tsang-2023", 75: "sun-2023", 81: "moccia-2022",
          148: "bright-2018", 170: "funayama-2016", 173: "jawaid-2016", 175: "donoghue-2015", 178: "lauritsen-2015", 189: "setsaas-2014",
          193: "rosenblat-2013", 197: "harrison-2013", 200: "muskens-2012", 210: "mantione-2010", 219: "etches-2009", 232: "guarnieri-2005",
          235: "thomas-2003", 236: "levine-2003", 239: "de-filippis-2026", 350: "viglione-2025", 374: "mira-2024", 658: "brasic-2018",
          17: ("E3",), 26: ("E4",), 31: ("E3",), 33: ("E3",), 53: ("E3",), 56: ("E4",), 68: ("E3",), 73: ("E3",), 76: ("E3",),
          90: ("E1", "Acute stress disorder remitted after an anaesthetic dream; fails only the chronicity criterion"), 117: ("E3",),
          133: ("E3",), 155: ("E3",), 169: ("E3",), 176: ("E3",), 476: ("E3",), 493: ("E3",), 62: "unsure", 171: "unsure"}
ET_DEC = {0: "hosseini-2026", 119: "fernandes-2020", 201: "kim-2016", 68: "pardo-gonzalez-2023", 69: "felizardo-2023", 80: "gerken-2022",
          85: "durbin-2022", 94: "aminzade-2021", 96: "huhne-2021", 110: "vendrell-serres-2021", 111: "van-den-hoven-2021", 115: "collyer-2020",
          125: "achamrah-2020", 155: "jarvinen-2019", 162: "shreedhara-2018", 167: "sair-2018", 187: "sumner-2017", 211: "ali-2015",
          214: "coffey-2014", 223: "brieler-2014", 226: "nakama-2013", 237: "zakrzewski-2013", 238: "bagnati-2013", 241: "sandeep-2013",
          247: "boudjani-2012", 252: "boudjani-2012", 253: "boudjani-2012", 257: "hosseini-2012", 270: "kalenderoglu-2011",
          283: "vartian-2004", 287: "stuve-2003", 297: "curran-1995", 300: "kanner-1993",
          268: ("dup", "brasic-2018", "2011 conference abstract of the same patient"),
          42: ("E3",), 62: ("E3",), 72: ("E3",), 95: ("E3",), 127: ("E3",), 178: ("E3",), 191: ("E8",), 255: ("E4",), 281: ("E4",),
          302: ("E4",), 308: ("E2",), 3: "unsure", 206: "unsure", 249: "unsure", 278: "unsure"}
ES1_DEC = {23: "hosseini-2026", 52: "bedell-2025", 217: "richards-2022", 296: "fernandes-2020", 342: "mathew-2019", 453: "kim-2016",
           542: "canan-2013", 30: ("E3",), 91: ("E3",), 199: ("E2",), 406: ("E8",), 263: "unsure"}

rows = list(csv.DictReader(LEDGER.open()))
nid = max(int(r["record_id"][1:]) for r in rows) + 1
new = []


def add(source_db, qid, rank, screened, dec_map, doi="", pmid="", pmcid="", other="", title="", au="", yr="", jn="", note=""):
    global nid
    row = {c: "" for c in COLS}
    doi = (doi or "").lower()
    row.update(record_id=f"R{nid:06d}", source_db=source_db, query_id=qid, retrieved_date=DATE, doi=doi, pmid=pmid,
               pmcid=pmcid, other_id=other, title=title[:300], first_author=au, year=str(yr), journal=jn,
               cluster_id=("pmid:" + pmid) if pmid else (("doi:" + doi) if doi else ("x:" + other)), notes=note)
    nid += 1
    m = lib_match(doi, pmid)
    dec = dec_map.get(rank) if screened else None
    if isinstance(dec, str) and dec not in ("unsure",):
        row.update(screen_stage="ab", decision="included", library_ids=dec)
    elif dec == "unsure":
        row.update(screen_stage="ab", decision="unsure")
    elif isinstance(dec, tuple) and dec[0] == "dup":
        row.update(screen_stage="ab", decision="included", library_ids=dec[1], reason_code="", notes=dec[2])
    elif isinstance(dec, tuple):
        row.update(screen_stage="ab", decision="excluded", reason_code=dec[0], notes=(dec[1] if len(dec) > 1 else note))
    elif m:
        row.update(screen_stage="ta", decision="included", library_ids=m)
    elif screened:
        row.update(screen_stage="ta", decision="excluded")
    new.append(row)


# Europe PMC
chunks = json.loads((W / "raw/epmc_ledger_chunks.json").read_text())
for head, lines in chunks:
    for l in lines:
        p = l.split("\t")
        rank = int(p[0])
        if head.startswith("#FULL"):
            _, src, id_, pmid, pmcid, doi, yr, s, t, jn, au = p
        else:
            _, src, id_, pmid, doi, yr, s = p
            pmcid = id_ if src == "PMC" else ""
            t = jn = au = ""
        add("Europe PMC", "EPMC_broad_v1_2", rank, rank < 700, EP_DEC, doi=doi, pmid=pmid, pmcid=pmcid, other=f"{src}:{id_}",
            title=t, au=au, yr=yr, jn=jn, note=f"rank {rank}, score {s}")

# Embase strategy 1
for l in (W / "raw/emb_s1.tsv").read_text().splitlines():
    i, eid, doi, yr, pt, t, jn, au = (l.split("\t") + [""] * 8)[:8]
    add("Embase (CKN)", "EMB_S1_v1_1", int(i), True, ES1_DEC, doi=doi, other=eid, title=t, au=au, yr=yr, jn=jn, note=pt)

# Embase title-ranked set
for l in (W / "emb_title_ranked.tsv").read_text().splitlines():
    i, s, eid, yr, pt, doi, t, jn, au = l.split("\t")
    add("Embase (CKN)", "EMB_title_v1_2", int(i), int(i) <= 308, ET_DEC, doi=doi, other=eid, title=t, au=au, yr=yr, jn=jn,
        note=f"rank {i}, score {s}")

with LEDGER.open("a", newline="") as f:
    csv.DictWriter(f, fieldnames=COLS).writerows(new)

log = Path("ledger/search_log.csv")
runs = [
    ("EPMC_S1_v1_1", "Europe PMC (browser)", "v1.1 S1: syndrome AND resolution AND unexpected AND case design", 554, "tuning run"),
    ("EPMC_S2_v1_1", "Europe PMC (browser)", "v1.1 S2: 14 trigger families, union with S1", 8627, "gold recall 27/50; replaced by v1.2"),
    ("EPMC_broad_v1_2", "Europe PMC (browser)", "v1.2 broad: A2 AND B2 AND (D_all OR C) AND E", 43112,
     "gold recall 42/50 (33/40 tuning, 9/10 holdout); 21,000 loaded (deep paging stopped); ranked by title score; ranks 0-699 screened"),
    ("EPMC_S1_v1_2", "Europe PMC (browser)", "v1.2 S1 only", 2881, "gold 12/50; count only"),
    ("EMB_S1_v1_1", "Embase via CKN", "v1.1 S1, Embase-only records ([embase]/lim NOT [medline]/lim, humans)", 578, "all screened"),
    ("EMB_broad_v1_2", "Embase via CKN", "v1.2 broad, Embase-only", 30333, "count only; not pulled (bulk-download caution)"),
    ("EMB_title_v1_2", "Embase via CKN", "v1.2 with syndrome AND (resolution OR unexpected) restricted to title, Embase-only", 1375,
     "ranked; ranks 0-308 screened"),
]
with log.open("a", newline="") as f:
    w = csv.writer(f)
    for qid, src, q, n, note in runs:
        w.writerow([qid, src, q, n, DATE, note])

from collections import Counter
print(len(new), "rows appended;", Counter(r["decision"] or "unscreened" for r in new))
print("library ids traced:", len({r["library_ids"] for r in new if r["library_ids"]}))
