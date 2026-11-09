# Ledger

The record of every search hit, kept so every number in the library traces back to a raw result.

- `records.csv`: one row per hit, exactly as retrieved. **Append-only:** corrections are new rows with `supersedes`. Metadata only, no abstracts.
- `search_log.csv`: one row per search run: source, string, hits, date.

## records.csv columns

| Column | Meaning |
|---|---|
| record_id | `R` + 6 digits, never reused |
| source_db | Where the hit came from (PubMed, Europe PMC, Consensus, OpenAlex, citation chase, …) |
| query_id | Matches a string in `queries/` (`legacy-unlogged` = rounds 1–2, string not kept) |
| retrieved_date | ISO date |
| doi, pmid, pmcid, other_id | Identifiers as retrieved, normalised (DOI lowercased, no prefix) |
| title, first_author, year, journal, language | Bibliographic metadata |
| cluster_id | One publication (`pmid:…`, `doi:…`, or `c:` + hash for no-ID records) |
| screen_stage | `legacy` · `ta` (title/abstract) · `ft` (full text) · `appraised` |
| decision | `included` · `excluded` · `unsure` · `candidate` · blank (not yet screened) |
| reason_code | E1–E9 (see `protocol/PROTOCOL.md`) |
| library_ids | Library record ids this hit supports, `;`-separated |
| flags | Integrity flags, `;`-separated |
| supersedes | record_id this row corrects |
| notes | Free text |

## State on 2026-11-09

The informal rounds 1–2 are seeded as `legacy` rows. Every library case traces to at least one row. The undecided legacy rows get re-screened under the protocol in step 1.1.
