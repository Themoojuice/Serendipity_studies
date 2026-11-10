# Protocol — v1.0 (2026-11-09)

The operative rules. The reasoning behind them is in the search dossier (a private Claude Doc, linked in `CLAUDE.md`). If the two disagree, this file wins, and the change gets a line in the changelog at the bottom.

## 1. What counts

Unit of record: a **patient**. Library entries are papers; `n_patients` and `same_patient_as` keep patient counts honest.

A patient qualifies when **all** of these hold:

1. **Serious syndrome:** diagnostic-level psychiatric syndrome, chronic (≥6 months) or treatment-resistant (≥2 adequate trials).
2. **Resolution:** complete, or ≥50% on a standardised scale, or clearly described remission.
3. **Off-target exposure:** the exposure was not aimed at that syndrome, or was aimed at it with no plausible expectation of benefit at the time.
4. **Passes the unexpectedness test (§2).**

**Excluded:** expected resolution of secondary syndromes (delirium, substance-induced, treated autoimmune or infectious encephalitis); deliberate trials, which are linked as downstream evidence instead; placebo responders; press-only anecdotes; animal work.

## 2. Unexpectedness test (answered for every full-text candidate)

| # | Question | Fails when |
|---|---|---|
| T1 | Target: was the exposure aimed at this syndrome? | Yes, and benefit was plausible at the time |
| T2 | Era: would a competent clinician *of that period* have predicted it? | Yes |
| T3 | Primary vs secondary: was the syndrome caused by what the exposure treated? | Yes (e.g. psychosis clearing as encephalitis is treated) |
| T4 | Base rate: is spontaneous remission at this chronicity common? | Yes, and there's nothing else (reversal, timing) to separate it from chance |

## 3. Era labels: where the finding stands now

Discoveries that were unexpected when reported **stay in**, labelled. The `era` field is required on every record.

| Label | Meaning |
|---|---|
| `novel` | Still unexplained: nothing comparable established since |
| `emerging` | Similar cases, pooled data or trials, not yet settled |
| `known` | Unexpected when reported, established since. **Needs a note** saying when and how |
| `refuted` | Failed under controlled testing. **Needs a note** |

`era.basis` is `judged` or `from downstream level` (a provisional default). All provisional labels are reviewed at step 1.9.

A case reported *after* an effect became known (e.g. an insula-stroke smoking cessation in 2011, after Naqvi 2007) is still logged. It passes T2 only if a typical clinician of that period would not have predicted it, and its era note says it's a replication.

## 4. Attribution grade (A–D, out of 6)

| Item | Points |
|---|---|
| Documented chronic baseline (≥6 months, or ≥2 failed treatments) | 1 |
| Standardised measure before and after | 1 |
| Temporal specificity: change in a plausible window after exposure | 1 |
| **Reversal: natural off-on, or rechallenge** | **2** |
| Confounders addressed (medication changes, admission, life events) | 1 |

A = 5–6 · B = 4 · C = 2–3 · D = 0–1

## 5. Reporting quality

JBI Critical Appraisal Checklist for Case Reports, 8 items, scored Yes = 1 (out of 8). Case series: the JBI case-series checklist (10 items). CARE (13 items) is the completeness reference and isn't scored.

## 6. Tiers

- **A:** attribution A, or B with JBI ≥6, and no integrity flag
- **B:** attribution B or C, and JBI ≥4
- **C:** qualifies, but falls short of B; this includes every flagged case. Counted and shown, never promoted.

## 7. Integrity and sensationalism flags

Flags are logged in the ledger's `flags` column (semicolon-separated), never hidden, and each one caps the case at tier C.

`retracted` (exclude, keep the ledger row) · `concern` (expression of concern) · `venue` (open-access journal not in DOAJ, journal not in MEDLINE with no other quality signal, or a hijacked title) · `mill` (paper-mill signals) · `media-first` (a lead only, never a case) · `overclaim` · `coi-trigger` (conflict of interest with the trigger) · `altmed` · `no-followup` · `preprint`

## 8. Exclusion reason codes

E1 not psychiatric, or not serious · E2 not resolved · E3 expected or targeted effect · E4 secondary syndrome resolved with its cause · E5 a trial, not a case · E6 duplicate · E7 no primary data (chase the source) · E8 too little detail to judge · E9 retracted

## 9. Ledger husbandry

- `ledger/records.csv` is **append-only**. Corrections are written as new rows, with `supersedes` set to the old record_id.
- **Metadata only.** No abstracts or full texts in this public repo: they're copyrighted, and they can be re-fetched by ID.
- **Normalisation:** DOI lowercased with the prefix stripped. PMID, PMCID and DOI cross-filled via the PubMed ID converter. Titles lowercased, with punctuation, diacritics, HTML and leading articles stripped.
- **Dedupe cascade:** exact DOI → exact PMID/PMCID → title similarity ≥0.92 plus year ±1 plus same first-author surname (auto-merge) → 0.80–0.92 goes to manual review. Cross-type pairs are *linked*, not deleted: abstract → paper, preprint → published version, erratum → parent, republication → original, the same case reappearing in a later series.
- `cluster_id` is one publication. `library_ids` links a cluster to library records (semicolon-separated).

## 10. Screening and stopping

- **Stages:** title/abstract (liberal) → full-text retrieval → eligibility (§1–2) → extraction → appraisal (§4–7) → library → PRISMA 2020 flow.
- **Calibration:** Brendan screens 100 records from step 1.1, blind; target κ ≥ 0.7. Ongoing, he blind re-screens 10% of full-text exclusions and adjudicates the unsure pile.
- **Stopping a ranked queue requires both:** 300 consecutive irrelevant records, **and** a random sample of 300 from the unscreened remainder with zero includes (≈1% residual ceiling, 95% upper bound). Then check whether that 1% could still hide enough cases to matter.

## 11. Sensitivity and missing-case estimate

- **Gold set:** the library cases as of 2026-11-09. Hold out 10 at random (the seed is recorded in `queries/`). Target ≥90% sensitivity for the union of strategies in each database, measured on the holdout.
- **Capture–recapture** (database route vs citation route), Lincoln–Petersen. Reported as a floor, because the two routes are positively dependent.

## Changelog

- 2026-11-09 · v1.0 · Protocol locked from the dossier. Era labels added (schema 1.1). Storage: this repository.
- 2026-11-09 · v1.1 · Strings tuned to v1.2 on the gold set (resolution block was the recall bottleneck). Broad results are ranked by `scripts/rank_titles.py` and screened in rank order. Schema 1.2: CKN access links, `flags` (adds `preprint`), tier C, vocabulary for catatonia, trauma, neurodevelopmental, non-brain procedures, systemic illness, life events, hormonal triggers, physiological stress, medication errors, conference abstracts and preprints. New includes enter as Provisional until full-text appraisal.
- 2026-11-10 · v1.2 · Theme sweeps allowed alongside the broad query, each with its own string file (`queries/strings_themes_v1.json`) and ledger query id. Large Europe PMC sets are loaded by `PUB_YEAR` slices. A clearly negative case found while screening (trigger present, syndrome unchanged) is excluded E2 with a note, so it can be counted later. Syndrome category `Personality` added (diagnostic-level personality disorder meets criterion 1 when chronic).
- 2026-11-10 · v1.2.1 · Stopping checks run on the Europe PMC broad queues (seeded samples recorded in `queries/`). Batch 2 and batch 3 met both criteria; the first-pass queue did not (1 include in its 300 sample). Screened rows are appended with `supersedes` rather than edited. Planned next: re-rank the tail with an extended lexicon and a classifier trained on screening decisions before further screening.
- 2026-11-10 · v1.2.2 · Scope decisions (Brendan): persistent genital arousal disorder and persistent sexual arousal syndrome are out of scope (not DSM-5 diagnoses); impulse-control disorders and dopamine dysregulation in Parkinson's disease that resolve once DBS allows dopaminergic dose reduction stay excluded as E4 (secondary syndrome resolving with its cause).
