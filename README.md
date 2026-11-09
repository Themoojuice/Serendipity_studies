# Serendipity Studies

A case library of published reports where a serious psychiatric syndrome resolved unexpectedly, after a stroke, a stimulator, a fever or a drug given for something else. The aim is an exhaustive, appraised collection: quality of evidence over sensationalism.

**Library:** https://themoojuice.github.io/Serendipity_studies/

| Path | What it is |
|---|---|
| `index.html` | The library viewer (served by GitHub Pages) |
| `data/cases.json` | The library: one record per study, controlled vocabularies, schema 1.1 |
| `ledger/` | Every search hit and every search run, append-only |
| `queries/` | Search strings, versioned per database |
| `protocol/PROTOCOL.md` | Inclusion rules, appraisal, era labels, screening and stopping rules |
| `scripts/validate_cases.py` | Run before every commit |

Each card links to the free full text where one exists, otherwise to the abstract and DOI.

Era labels: discoveries that were unexpected when reported but are established since stay in, labelled **Known now**. Findings that later failed controlled testing are labelled **Refuted**.
