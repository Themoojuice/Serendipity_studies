# Schema 1.4: field reference and extraction guide

Schema 1.4 (2026-11-16) gets the library ready for three jobs: full-text appraisal (next item 5), a case page that shows the course of each case at a glance, and the hypothesis layer, our own reading of what happened. Every change is additive. Records appraised before 1.4 stay valid.

**Worked examples:** `maddigan-2004` (fever, medication-hold confounder) and `oh-2011` (lesion block). Read them alongside this file. They were coded by `scripts/batches/b2026_11_16_schema14_examples.py`.

## 1. Three layers, kept apart

| Layer | Where | Who writes it | Rule |
|---|---|---|---|
| What the paper reports | `data/cases.json`: the record, `appraisal`, `timeline`, `lesion` | Extraction and appraisal | Facts and our scoring of the paper. No mechanism talk. |
| What follows from it | `data/cases.json`: `derived` | `scripts/derive.py` only | Never typed by hand. The validator recomputes it and fails if it's stale. |
| What we think happened | `data/hypotheses.json` | Claude drafts, Brendan reviews | Ours, not the papers'. It never changes a fact. If hypothesising finds a factual error, fix the record in `cases.json`. |

The site shows the first two as the case card and the third as a separate, labelled panel called "Our reading".

## 2. `appraisal` (every record)

```json
"appraisal": {
  "basis": "Full text",
  "date": "2026-11-16", "by": "Claude",
  "unexpectedness": { "target": {"result": "pass", "note": ""}, "era": {...}, "secondary": {...}, "base_rate": {...} },
  "attribution": { "baseline": 1, "measure": 0, "timing": 1, "reversal": 0, "confounders": 1, "note": "" },
  "jbi": { "checklist": "Case report", "answers": ["Y","U","Y","Y","Y","Y","Y","Y"] },
  "note": ""
}
```

- **basis**: what the appraisal rests on: `Title`, `Abstract`, `Full text`, `Secondary source` (a later paper or review that describes the case) or `Unrecorded` (the first rounds, before the basis was recorded). The migration set it from each record's `verified` text.
- **unexpectedness**: protocol §2, T1 to T4 (`target`, `era`, `secondary`, `base_rate`). Library cases are `pass` or `borderline`; a fail is an exclusion. A `borderline` needs a one-line note naming the specific doubt.
- **attribution**: protocol §4, one entry per item: baseline 0/1, measure 0/1, timing 0/1, reversal 0/2, confounders 0/1. Score every item or leave the whole block null. A partial score is not allowed. Use `note` for any judgement call. Reversal scores 2 only when the timeline shows it: a documented stop followed by a return (natural off-on), or a restart after a return followed by improvement (rechallenge). If the paper never says the exposure ended, the return can't be tied to it, so it scores 0 (see Maddigan).
- **jbi**: protocol §5. `Case report` has 8 answers and `Case series` has 10, each `Y`, `N`, `U` or `NA`. For exposures that aren't treatments (lesions, infections, life events), read item 5 as *the exposure is described clearly* and item 7 as *its other effects are described* (side effects, deficits). Otherwise every lesion case loses two points for being a lesion.
- **Case series**: score the best-documented patient and say so in `attribution.note`.
- Scores, grades and the tier the rule gives appear in `derived`, not here.

## 3. `timeline` (optional; fill it at the full-text read)

A list of patient tracks. Each track is one patient with individual data:

```json
"timeline": [{
  "patient": "74-year-old woman", "age": 74, "sex": "F",
  "events": [
    {"kind": "onset", "t": -6, "to": -5, "unit": "years", "precision": "approx", "label": "Rituals began (family report)"},
    {"kind": "exposure_start", "t": 0, "unit": "days", "precision": "exact", "label": "Left internal capsule genu infarct"},
    {"kind": "first_change", "t": 0, "unit": "days", "precision": "approx", "label": "Rituals stopped abruptly"},
    {"kind": "follow_up", "t": 4, "unit": "months", "precision": "exact", "label": "Rituals still absent", "state": "Remitted"}
  ]
}]
```

**Coding rules**

1. **t = 0 is the start of the exposure**: first dose, stroke onset, day of surgery, fever onset. Each track has exactly one `exposure_start`, at t = 0. Everything else is timed from it, negative before and positive after.
2. **Use the paper's units** (`minutes` to `years`); don't convert. If the paper numbers days from admission, subtract to re-centre on the exposure (Maddigan: fever on admission day 19, so admission is t = −18 days).
3. **Ranges**: `t` to `to` ("5 to 6 years" → t −6, to −5). Derived values use the midpoint.
4. **precision**: `exact` as stated; `approx` for about, several, early; `at most` when a change was first found at a visit (it happened by then, an upper bound); `at least` for a lower bound. These are censoring codes. They let latency be analysed honestly later instead of pretending every date is exact.
5. **first_change and best_response are for responses the exposure might explain**, or re-exposure. A response to some other treatment (lithium after the fever) is an `assessment` or the follow-up `state`, never a `first_change`. Durability depends on this.
6. **exposure_stop only when the paper documents it.** Never infer an end.
7. **cointervention for anything else that changed**: drug starts and holds, admission, an intercurrent illness, a life event. These are the confounders, and putting them on the timeline is what makes them visible.
8. **treatment_failed** for prior treatments: name, dose and duration in the label.
9. **state** (`Remitted`, `Partial`, `Unchanged`, `Worse`) on `assessment`, `best_response` and `follow_up` events. **scores** (`[{"scale": "Y-BOCS", "value": 32}]`, plus `"higher_is_better": true` for scales like GAF) on any event. A standardised measure before and after is just two scored events.
10. **follow_up** is the last observation, at most one per track, and it comes last.
11. **Labels are our words**: short, specific, no copied sentences (the repo is public).
12. **Series**: one track per patient with individual data. The site draws up to six. Pooled-only series get no tracks.
13. When a record has a timeline, the legacy free-text `outcome.time_to_resolution` and `outcome.follow_up` must be null; the derived values replace them.

## 4. `lesion` (brain triggers only)

For acquired lesions, brain injury, neurosurgery and brain stimulation:

```json
"lesion": {"kind": "Lesion", "side": "Left", "regions": ["Internal capsule"],
           "specific": "Genu of the left internal capsule (low density on CT, figure 1)",
           "aetiology": "Ischaemic stroke", "imaging": "CT", "mappable": "Figure"}
```

- **kind**: `Lesion`, `Injury`, `Resection or ablation`, `Stimulation target`.
- **side** as the paper states it; `Unstated` otherwise. This replaces parsing side out of `trigger.specific` for the laterality analysis.
- **regions** from the `lesion_region` list (several allowed); the detail goes in `specific`.
- **mappable** decides whether a case can go into lesion network mapping later: `Coordinates` (or a mask), `Figure` (images shown, so the lesion can be traced onto a template), `Description only`, or `No`.

## 5. `derived` (written by `scripts/derive.py`)

Computed from the first track and the appraisal. Run `python3 scripts/derive.py` after any edit; the validator fails if it's stale.

| Field | Meaning |
|---|---|
| `latency_days`, `latency_band`, `latency_bound` | Exposure to first improvement (else best response). Bands: under a day, 1–13 days, 2 weeks to 3 months, over 3 months. Bound carries `at most` / `at least`. |
| `baseline_years` | Syndrome onset to exposure |
| `follow_up_days` | Exposure to last follow-up |
| `durability` | `Sustained` (improved and confirmed at a later assessment or follow-up), `Lost`, `Lost, then regained`, `Unknown` |
| `timeline_reversal` | The reversal the events themselves show. The validator warns if `outcome.reversal` claims more. |
| `measures` | Each scale scored before and after: last score at or before t = 0 against the best after it, with % change |
| `attribution_score`, `attribution_grade` | Out of 6; A 5–6, B 4, C 2–3, D 0–1 |
| `jbi_score`, `jbi_of` | Count of Y answers; checklist length |
| `rule_tier` | The tier protocol §6 gives. Any flag caps it at C. For an **Included** record, `tier` must equal `rule_tier`; for a Provisional one, the validator only warns. |

Latency is the variable most worth getting right. Hours suggest pharmacology, days to weeks suggest immune or plastic change, months suggest natural history. That's a working heuristic, and the hypothesis entries test it rather than assume it.

## 6. The hypothesis layer: `data/hypotheses.json`

One entry per case, in its own file with its own vocabularies (status, the seven boring explanations, verdicts, mechanisms by level, confidence, latency fit).

```json
{
  "case_id": "oh-2011", "status": "draft", "written_by": "Claude", "date": "2026-11-16", "based_on": "Full text",
  "nulls": { "natural_history": {"rating": "Unlikely", "why": "..."}, "...": {} },
  "verdict": "Doesn't beat the null", "verdict_note": "...",
  "hypotheses": [{
    "claim": "...", "chain": "exposure → intermediate step → change in the syndrome",
    "mechanisms": ["Lesion disconnection"], "latency_fit": "Fits",
    "for": "...", "against": "...",
    "confidence": "Low", "uncertainty_driver": "the specific variable that keeps it uncertain",
    "test": "the observation that would tell this hypothesis apart from the next one"
  }],
  "related": [{"id": "erbay-2022", "why": "..."}],
  "questions": "..."
}
```

**Boring explanations first.** Every entry rates all seven before proposing a mechanism (`Unlikely`, `Possible`, `Likely`, `Can't judge`, with a why for Possible and Likely):

| Code | Explanation |
|---|---|
| `natural_history` | Spontaneous or episodic remission at this chronicity |
| `regression` | Presented at a peak, then drifted back |
| `misdiagnosis` | The syndrome was driven by the condition being treated, or was something else |
| `cointervention` | Another treatment change, admission, adherence or circumstance at the same time |
| `nonspecific` | Sedation, sickness, apathy, cognitive or motor loss reduced all behaviour, not the syndrome itself. This is the main rival in lesion and sedating-drug cases. |
| `expectancy` | Placebo, expectancy, attention. For functional disorders, suggestion may be the mechanism itself, so say so rather than dismiss it. |
| `reporting` | Selective reporting, single observer, no measure, overclaim |

**Verdict**: `Beats the null` only when no boring explanation is Likely and something specific (reversal, timing, specificity) separates the case from chance; `Doesn't beat the null` when any is Likely (the validator enforces this); `Undecided` when the paper doesn't give enough. Expect most cases not to beat the null. That isn't failure: the cases that do are the point of the library.

**Candidate hypotheses** are ranked, most likely first. Each has a mechanistic chain, mechanism tags from the vocabulary (each tag belongs to a level: pharmacokinetic, neurotransmitter, cellular, systemic, circuit, psychological, non-specific), how well the latency fits, evidence for and against within the case, a confidence, **the specific variable driving the uncertainty** ("uncertain" alone is not allowed), and **a discriminating test**. The test is what turns a story into something checkable.

**Status**: Claude's drafts stay `draft` until Brendan has read them, then become `discussed` or `settled`. Git history keeps every revision of our thinking.

**Across cases**: tags make convergence countable. Different exposures landing on the same mechanism is worth more than any single striking case. `related` links the cases a hypothesis leans on or contradicts.

## 7. Full-text appraisal workflow (next item 5)

1. Read the full text: PMC first, then CKN, one article at a time.
2. Recheck eligibility (protocol §1) and fill `unexpectedness`.
3. Code the `timeline`, including co-interventions and any scores.
4. Score `attribution` and `jbi`, and add `lesion` for brain triggers.
5. Correct record facts the full text changes (summary, caveat, reversal, resolution), and set `verified` and `appraisal.basis`/`date`/`by`.
6. `python3 scripts/derive.py`, then `python3 scripts/validate_cases.py`. Read the warnings: a tier that differs from `rule_tier` is a question for Brendan, not something to fix silently.
7. Brendan promotes Provisional to Included; at that point `tier` must equal `rule_tier`.
8. Hypotheses are a separate, later pass, not part of appraisal.

## 8. Changing a vocabulary

Add the value to the vocabulary in `cases.json` or `hypotheses.json` and log it in the protocol changelog. The validator rejects anything not in a vocabulary, so a typo can't become a new category.
