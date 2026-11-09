# Working notes for Claude sessions

Brendan (psychiatry registrar, Cairns) and Claude are building an exhaustive, appraised library of published cases where serious psychiatric syndromes resolved unexpectedly. This repo is the durable store. Cloud sessions lose their files, so **everything that matters gets committed here**.

## Read first

- `protocol/PROTOCOL.md`: the rules. Follow them, and log any change in its changelog.
- Search dossier, the long-form reasoning (private Claude Doc): https://claude.ai/artifact/N5fSAMhVmsKzty2aSujAcY
- Phase plan: free English sources (Phase 1, steps 1.0–1.9), then Spanish/Portuguese, then European, then Asian.

## Current status

- 2026-11-09 (evening): repo set up; 50 cases, schema 1.1.
- 2026-11-09 (night, CKN live): **phase 1, first pass.** Strings v1.2 (`queries/strings_v1.json`): gold recall 42/50 (33/40 tuning, 9/10 holdout).
  - Europe PMC broad query 43,112 hits; only 21,000 loaded (cursor paging stops at ~21k). Ranked by `scripts/rank_titles.py`; **ranks 0–699 screened.** In the loaded set, 25/36 gold cases sit above rank 700, so this pass reached roughly 70%.
  - Embase-only (via CKN): S1 578 (all screened); title-restricted set 1,375, **ranks 0–308 screened**; broad Embase-only 30,333 counted, not pulled.
  - **+60 provisional includes** → 110 cases (schema 1.2: `links.ckn`, `flags`, tier C, new vocab). All appraisal so far is abstract-level.
  - Ledger: 23,566 rows; 7 `unsure` awaiting full text.
- **Next, in order:**
  1. Load the rest of the Europe PMC broad set by splitting on `PUB_YEAR` ranges (each slice < 20k), re-rank, continue screening from rank 700 (gold says to ~3,000).
  2. Embase title set ranks 309–1,374 (mostly the score-9 band): screen, or random-sample per the stopping rule.
  3. PsycInfo via EBSCOhost (CKN) — not yet run.
  4. Full-text appraisal of the 60 provisional records (PMC free first, then CKN), with attribution grade and JBI score; promote to Included.
  5. Calibration: 100 blinded records for Brendan.
- Library restyle ("more Claude") is still due with the rebuild after step 4, alongside the new appraisal fields.

## How searches actually run (the network matters)

- The cloud sandbox **blocks** literature APIs (403). Don't route around it.
- **PubMed connector:** max 20 Boolean operators, no wildcards, returns PMIDs.
- **Consensus connector:** free plan, first page only, page_size ≤300, rate-limited (at most 3 calls at a time).
- **Brendan's laptop built-in browser** (`mcp__remote-devices__Claude_Browser__*`): open a tab on `www.ebi.ac.uk`, then run `fetch()` against the Europe PMC REST API with `javascript_tool`. Crossref, OpenAlex and Semantic Scholar the same way if their hosts are allowed. It only works while the laptop is awake and the Claude app is open.
- **Embase via CKN** (tab on www.embase.com, reached through the CKN OpenAthens redirector): create a search with `POST /rest/searches` and JSON `{"query": "...", "queryType": "ADVANCED"}` (long GET URLs fail with 414); read results with `GET /rest/searches/{id}/articles?offset=N&size=100&order=PUBLICATION_DATE`. Limit to Embase-only with `[embase]/lim NOT [medline]/lim`. Pace requests (~0.5 s) and pull only what will be screened: no bulk downloading.
- **Europe PMC**: use `POST /europepmc/webservices/rest/searchPOST` for long queries. Cursor paging returns empty pages after ~21,000 records, so split big queries by `PUB_YEAR`.
- **Getting data out of the browser**: return text over ~60 KB from `javascript_tool` and it is saved to a file under /tmp/claude-tool-results (cap ~260k characters per call); parse it with Python instead of reading it into context.
- **CKN full text**: `https://go.openathens.net/redirector/ckn.qldhealth.com?url=` + the URL-encoded `https://doi.org/<doi>` (stored as `links.ckn`). Read full texts one at a time for appraisal; never bulk-download.
- Laptop folder access was denied once. Don't re-request it; this repo replaced it.

## Rules for this repo

- **It's public, and GitHub Pages serves `main`.** Commit only metadata, our own summaries, and links. **Never commit abstracts, full texts or PDFs.**
- Published case details only. Nothing from Brendan's clinical work, ever.
- `data/cases.json` is the source of truth for the library. Edit it with a script, then run `python3 scripts/validate_cases.py`. It must print OK before any commit.
- `ledger/records.csv` is append-only (see `ledger/README.md`).
- Every library record must trace to at least one ledger row.
- Every new record carries `era`. A `known` or `refuted` label needs a note saying when and how.
- **Links:** `full_text` = the PMC page if there's a PMCID, else a verified free PDF. `abstract` = PubMed. Always a DOI where one exists.
- Commit in small, labelled batches, e.g. `1.1: PubMed psychotic × lesion — 312 hits, 9 includes`.
