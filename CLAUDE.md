# Working notes for Claude sessions

Brendan (psychiatry registrar, Cairns) and Claude are building an exhaustive, appraised library of published cases where serious psychiatric syndromes resolved unexpectedly. This repo is the durable store. Cloud sessions lose their files, so **everything that matters gets committed here**.

## Read first

- `protocol/PROTOCOL.md`: the rules. Follow them, and log any change in its changelog.
- Search dossier, the long-form reasoning (private Claude Doc): https://claude.ai/artifact/N5fSAMhVmsKzty2aSujAcY
- Phase plan: free English sources (Phase 1, steps 1.0–1.9), then Spanish/Portuguese, then European, then Asian.

## Current status

- 2026-11-09: repo set up. 50 cases plus 4 context records, schema 1.1 (era labels). Ledger seeded with the informal rounds 1–2 (613 rows, `legacy`).
- **Next: step 1.0.** Write strings v1 into `queries/`, hold out 10 gold cases (record the seed), tune on the rest, report sensitivity. Then step 1.1 (PubMed/PMC).
- Pending from Brendan: the calibration screen after 1.1, a CKN sign-in for Embase/PsycInfo (optional), the Scite trial at 1.8.
- Library restyle ("more Claude") is due with the rebuild at the end of 1.1, alongside new fields: attribution grade, JBI score, flags, tier C.

## How searches actually run (the network matters)

- The cloud sandbox **blocks** literature APIs (403). Don't route around it.
- **PubMed connector:** max 20 Boolean operators, no wildcards, returns PMIDs.
- **Consensus connector:** free plan, first page only, page_size ≤300, rate-limited (at most 3 calls at a time).
- **Brendan's laptop built-in browser** (`mcp__remote-devices__Claude_Browser__*`): open a tab on `www.ebi.ac.uk`, then run `fetch()` against the Europe PMC REST API with `javascript_tool`. Crossref, OpenAlex and Semantic Scholar the same way if their hosts are allowed. It only works while the laptop is awake and the Claude app is open.
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
