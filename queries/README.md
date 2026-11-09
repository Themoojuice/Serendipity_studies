# Queries

- `runs/`: one JSON file per search run: date, database, strings, hit IDs. Each one's `query_id` matches `ledger/records.csv`.
- `strings_v1.json` (step 1.0): the master concept blocks A–E, with a translation for each database. A new version means a new file; old files are never edited.
- `gold_holdout.json` (step 1.0): the 10 held-out gold cases and the random seed used to pick them.

`runs/2026-11-09_pubmed_rounds1-2.json` holds the informal pre-protocol PubMed runs (Q1–Q15).
