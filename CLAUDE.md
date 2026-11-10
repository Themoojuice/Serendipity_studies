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
- 2026-11-10: **phase 1b.**
  - Europe PMC broad set fully loaded by `PUB_YEAR` slices: 43,109 of 43,112. The 22,109 records beyond the first pass: batch 2 (20,669, **ranks 0–399 screened**; gold cases at ranks 41, 100, 115, 122, 1467, 7808) and batch 3 (1,440, ranks 0–59, nothing). Browser export in `/home/claude/work/raw/epmc_b2b3.txt` (gone when the session ends; the ledger holds every row).
  - Theme sweeps (`queries/strings_themes_v1.json`): ketogenic/metabolic (Europe PMC 208 cases + 54 trials; Embase 394) and temporal lobe (577). Keto: **no new serendipitous cases**; almost all reports are deliberate metabolic therapy (E3). 5 keto trials and 3 temporal reviews added as context records.
  - **+15 provisional cases** from Europe PMC batch 2.
  - Left-sided temporal sweep (`EPMC_temporal_left_v1_3`, 275 new records, all screened): +1 case (Ohara 2004, `Personality` category added). The temporal sweep is now symmetric (852).
  - Laterality (lesion/TBI/neurosurgery cases, side as stated in the trigger, 44 cases): 10 left, 8 right, 3 bilateral, 23 unstated. Temporal: 6 right vs 1 left (3 of the right are epilepsy surgery). Left-sided cases are mostly frontal, basal ganglia or thalamic. 6 vs 1 is about what a coin gives 1 time in 8.
  - 138 records (126 cases, 12 context); ledger 47,184 rows; 13 `unsure`.
- 2026-11-10 (later): **phase 1c — deeper Europe PMC screening, no reload needed.** The ledger already holds every ranked ID, so each chunk is fetched by ID (`EXT_ID:(…)` in batches of 100, per source) and screened. Shared helpers now in `scripts/lib_add.py`; screened rows are appended as new ledger rows with `supersedes` pointing at the blank row.
  - Batch 2 ranks 400–1,499 (1,100): +3 cases (Ueki 2004, Tsolaki 2010, Diamond 2006), 7 unsure.
  - First-pass ranks 700–1,799 (1,100): +8 cases (Bijanki 2020, Xie 2026, Gillespie 2019, Malur 2000, Baek 2022, Solmi 2013, Choo 2024, Romeo 2025), 2 unsure; all 8 known cases in range recognised.
  - First-pass ranks 1,800–2,899 (1,100): +3 cases (Basheikh 2017, Shahani 2019, Hamdani 2013), 1 unsure; all 4 known cases recognised.
  - 152 records (140 cases, 12 context; 91 Provisional); ledger 50,484 rows (47,184 current); 23 `unsure`.
  - Laterality (lesion/TBI/neurosurgery, side from `trigger.specific`, 48 cases): 10 left, 11 right, 3 bilateral, 24 unstated. Temporal: 9 right vs 1 left, but most right-temporal cases are epilepsy surgery or amygdala ablation, where side follows the seizure focus and the right-amygdala PTSD hypothesis makes right-sided relief more publishable.
  - Scope questions for Brendan (in the unsure pile): persistent genital arousal disorder (not DSM-5) abolished by varenicline with repeated off-on (Korda 2009); persistent sexual arousal syndrome remitting with ECT for bipolar depression (Yero 2006).
- 2026-11-10 (evening): **phase 1c — stopping-rule checks on the Europe PMC broad set.** The browser now reads the queue straight from the committed ledger (`raw.githubusercontent.com/.../<commit>/ledger/records.csv`), so no IDs are pasted.
  - First pass ranks 2,900–3,999 (1,100, nearly all score-4 cohort studies): no includes; 1,328 consecutive irrelevant since rank 2,671.
  - Seeded samples (`queries/stopping_samples_2026_11_10.json`, seed 20261110). First pass: random 300 of 16,999 → **1 include** (rank 9,842, Makris 2021: resignation syndrome lifting after tethered-cord surgery) → **queue not stopped**. Batch 2: ranks 1,500–1,799 + random 300 of 18,868 → 0 → criteria met. Batch 3: ranks 60–359 + random 300 of 1,080 → 0 → criteria met.
  - Pooled (1/600 of the 35,867-record tail), roughly 60 relevant records may remain (95% interval about 2–330): sparse but not empty. Makris scored low because the ranking lexicon has no unresponsiveness / resignation syndrome / functional coma terms.
  - 153 records (141 cases, 12 context); ledger 53,084 rows (47,184 current); 23 `unsure`.
- **Finding unscreened rows now:** current rows (no one `supersedes` them) with a **blank decision**. First pass = notes starting `rank `; batch 2 = `year-slice batch 2`; batch 3 = `year-slice batch 3`.
- **Stopping-rule state (protocol §10), Europe PMC broad:** first pass screened 0–3,999 plus a 300 sample → not stopped (1 include in the sample). Batch 2 and batch 3 → both criteria met, but the pooled estimate says the tail still matters.
- **Next, in order:**
  1. Re-rank the Europe PMC tail (first pass 4,000+ and batch 2 1,800+, ~35,600 records) instead of reading it in rank order: add the missing lexicon (unresponsive, resignation syndrome, functional coma, stupor, mutism) and train a simple classifier (TF-IDF + logistic regression) on the ~11,000 screened decisions, score the tail in the browser, screen the top of the new order, then repeat the stopping check. Log it as a protocol change.
  2. Strings v1.3: make the Embase keto term ketogenic-only and rerun it (left-sided temporal terms done).
  3. Embase title set ranks 309–1,374 (mostly the score-9 band): screen, or random-sample per the stopping rule.
  4. PsycInfo via EBSCOhost (CKN) — not yet run.
  5. Full-text appraisal of the 91 provisional records and 23 unsure (PMC free first, then CKN), with attribution grade, JBI score and `lesion.side` / `lesion.region` for the laterality analysis; promote to Included.
  6. Calibration: 100 blinded records for Brendan.
- Library restyle ("more Claude") is still due with the rebuild after step 5, alongside the new appraisal fields.

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
