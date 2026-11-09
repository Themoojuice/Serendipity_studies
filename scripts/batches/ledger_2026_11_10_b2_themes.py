"""Append the 2026-11-10 runs to the ledger, with screening decisions.

Sources (exported from the browser, kept out of git):
  raw/epmc_b2b3.txt    Europe PMC v1.2 broad query, year-sliced reload: batch 2 (20,669 records) and
                       batch 3 (1,440), each in title-score rank order
  raw/themes_epmc.tsv  Europe PMC theme sweeps: keto cases (208), keto trials (54), temporal (577)
  raw/themes_emb.tsv   Embase keto sweep (394)

Screening state: batch 2 ranks 0-399; batch 3 ranks 0-59; theme sweeps in full.
Unscreened rows get a blank decision.  Run from the repo root.
"""
import csv
import json
from collections import Counter
from pathlib import Path

W = Path("/home/claude/work")
LEDGER = Path("ledger/records.csv")
COLS = ["record_id", "source_db", "query_id", "retrieved_date", "doi", "pmid", "pmcid", "other_id", "title", "first_author",
        "year", "journal", "language", "cluster_id", "screen_stage", "decision", "reason_code", "library_ids", "flags",
        "supersedes", "notes"]
DATE = "2026-11-10"

lib = json.loads(Path("data/cases.json").read_text())["records"]
by_doi = {r["ids"]["doi"]: r["id"] for r in lib if r["ids"]["doi"]}
by_pmid = {r["ids"]["pmid"]: r["id"] for r in lib if r["ids"]["pmid"]}


def lib_match(doi, pmid):
    return by_pmid.get(pmid or "") or by_doi.get((doi or "").lower(), "")


U = "unsure"
B2_DEC = {5: "takano-2002", 14: "spiers-2016", 20: "galati-2013", 52: "wilcox-2008", 65: "dusoir-2005", 78: "ferrao-2003",
          84: "freeman-2001", 94: "behar-1999", 107: "calache-1991", 112: "odeh-1989", 120: "rubin-1985", 280: "martin-santos-1950",
          281: "wahed-1934", 303: "hoirisch-clapauch-2013", 339: "ho-2001",
          0: ("E1", "Neurological recovery from toxic leukoencephalopathy, not a psychiatric syndrome"),
          79: ("E3",), 105: ("E4",), 367: ("E4",), 372: ("E4",),
          336: ("E4", "Symptoms eased when a workplace solvent exposure was removed"),
          366: ("E2", "Negative case: eating disorder did not remit after head injury with loss of taste and smell"),
          371: ("E3", "Leucotomy was given for the depression; the meningioma was found later"),
          3: (U, "Dopamine agonist in a CNV carrier: was it given for the psychosis? Needs full text"),
          7: (U, "Title only; trigger not stated"),
          21: (U, "Ketamine indication not stated; may be deliberate"),
          23: (U, "Phenytoin may have been aimed at suspected seizures driving the self-injury"),
          72: (U, "Hormones may have been given for the psychosis or for hypoestrogenaemia (possible E4)"),
          108: (U, "Danish; abstract is about ECT and case details need the full text")}
B3_DEC = {9: ("E3",)}
KETO_DEC = {**{k: ("E3", "Ketogenic therapy given for the psychiatric disorder") for k in
               ("k2", "k3", "k4", "k5", "k7", "k8", "k12", "k14", "k16", "k19", "k22", "k24", "k59", "k64")},
            "k34": ("E2", "Psychopathology did not improve"),
            "k70": ("E4", "Mood symptoms tied to diabetes management eased as glucose control improved"),
            "k98": ("E3", "Diet prescribed with psychotherapy and exercise to treat both conditions"),
            "k101": ("E1", "Mild anxiety and depression in Parkinson's disease"),
            "k150": ("E3", "Diet adopted to stabilise mood"),
            "ek70": ("E3",), "ek71": ("E3",), "ek97": ("E3",), "ek73": ("E2",), "ek57": ("E5",)}

rows = list(csv.DictReader(LEDGER.open()))
nid = max(int(r["record_id"][1:]) for r in rows) + 1
new = []


def add(source_db, qid, key, screened, dec_map, doi="", pmid="", pmcid="", other="", title="", au="", yr="", jn="", note="",
        default_code=""):
    global nid
    row = {c: "" for c in COLS}
    doi = (doi or "").lower()
    row.update(record_id=f"R{nid:06d}", source_db=source_db, query_id=qid, retrieved_date=DATE, doi=doi, pmid=pmid,
               pmcid=pmcid, other_id=other, title=title[:300], first_author=au, year=str(yr), journal=jn,
               cluster_id=("pmid:" + pmid) if pmid else (("doi:" + doi) if doi else ("x:" + other)), notes=note)
    nid += 1
    m = lib_match(doi, pmid)
    dec = dec_map.get(key) if screened else None
    if isinstance(dec, str):
        row.update(screen_stage="ab", decision="included", library_ids=dec)
    elif isinstance(dec, tuple) and dec[0] == U:
        row.update(screen_stage="ab", decision="unsure", notes=f"{note}; {dec[1]}")
    elif isinstance(dec, tuple):
        row.update(screen_stage="ab", decision="excluded", reason_code=dec[0], notes=(f"{note}; {dec[1]}" if len(dec) > 1 else note))
    elif m:
        row.update(screen_stage="ta", decision="included", library_ids=m)
    elif screened:
        row.update(screen_stage="ta", decision="excluded", reason_code=default_code)
    new.append(row)


# Europe PMC broad set, year-sliced reload
sec = None
for l in (W / "raw/epmc_b2b3.txt").read_text().splitlines():
    if l.startswith("#"):
        sec = l
        continue
    p = l.split("|")
    rank, src, id_, pmid, pmcid, doi, yr, s = p[:8]
    t, jn, au = (p[8], p[9], p[10]) if "FULL" in sec else ("", "", "")
    rank = int(rank)
    b2 = sec.startswith("#B2")
    add("Europe PMC", "EPMC_broad_v1_2", rank, rank < (400 if b2 else 60), B2_DEC if b2 else B3_DEC, doi=doi, pmid=pmid,
        pmcid=pmcid, other=f"{src}:{id_}", title=t, au=au, yr=yr, jn=jn,
        note=f"year-slice batch {2 if b2 else 3}, rank {rank}, score {s}")

# Europe PMC theme sweeps
QID = {"#KETO": "EPMC_keto_cases_v1", "#KETOTRIALS": "EPMC_keto_trials_v1", "#TEMPORAL": "EPMC_temporal_v1"}
for l in (W / "raw/themes_epmc.tsv").read_text().splitlines():
    if l.startswith("#"):
        sec = l
        continue
    key, src, id_, pmid, doi, yr, t, jn, au = (l.split("\t") + [""] * 9)[:9]
    add("Europe PMC", QID[sec], key, True, KETO_DEC, doi=doi, pmid=pmid, pmcid=id_ if src == "PMC" else "", other=f"{src}:{id_}",
        title=t, au=au, yr=yr, jn=jn, note=f"theme sweep {key}", default_code="E5" if sec == "#KETOTRIALS" else "")

# Embase keto sweep (column 9 holds an abstract snippet: not stored)
for l in (W / "raw/themes_emb.tsv").read_text().splitlines():
    if l.startswith("#"):
        continue
    key, eid, doi, yr, pt, t, jn, au = (l.split("\t") + [""] * 8)[:8]
    add("Embase (CKN)", "EMB_keto_v1", key, True, KETO_DEC, doi=doi, other=eid, title=t, au=au, yr=yr, jn=jn,
        note=f"theme sweep {key}; {pt}")

# Targeted lookups made while checking the temporal-lobe theme
add("Europe PMC", "targeted-lookup", "uher", True, {"uher": "uher-2005"}, doi="10.1136/jnnp.2004.048819", pmid="15897510",
    pmcid="PMC1739667", other="MED:15897510", title="Brain lesions and eating disorders.", au="Uher R", yr="2005",
    jn="J Neurol Neurosurg Psychiatry", note="looked up by citation for the temporal-lobe reality check (review of 54 cases)")

with LEDGER.open("a", newline="") as f:
    csv.DictWriter(f, fieldnames=COLS).writerows(new)

runs = [
    ("EPMC_broad_v1_2", "Europe PMC (browser)", "v1.2 broad, reloaded in PUB_YEAR slices (each < 20k)", 43112,
     "43,109 loaded in total; 22,109 beyond the first 21,000 (batch 2: 20,669, ranks 0-399 screened; batch 3: 1,440, ranks 0-59 screened); +15 includes"),
    ("EPMC_keto_cases_v1", "Europe PMC (browser)", "src AND A2 AND ketogenic/metabolic block AND case design", 208,
     "all screened; no new serendipitous cases (index cases already in library)"),
    ("EPMC_keto_trials_v1", "Europe PMC (browser)", "src AND A2 AND ketogenic/metabolic block AND trial terms", 54,
     "all screened; 5 trials linked as context records"),
    ("EPMC_temporal_v1", "Europe PMC (browser)", "src AND A2 AND temporal/right-hemisphere block AND B2 AND case design", 577,
     "all screened; right-sided terms only (bias, fix in v1.3); 3 context records"),
    ("EMB_keto_v1", "Embase via CKN", "ketogenic/ketosis terms AND psychiatric terms", 394,
     "all screened; overbroad (ketoacidosis noise); no includes"),
]
with Path("ledger/search_log.csv").open("a", newline="") as f:
    w = csv.writer(f)
    for qid, src, q, n, note in runs:
        w.writerow([qid, src, q, n, DATE, note])

print(len(new), "rows appended;", Counter(r["decision"] or "unscreened" for r in new))
print("library ids traced:", sorted({r["library_ids"] for r in new if r["library_ids"]}))
