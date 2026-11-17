"""Full-text appraisal, batch 19 (2026-11-17): PMC pages read in the laptop browser.
jawaid-2016 (clozapine seizure, schizophrenia), donoghue-2015 (anaesthetic ketamine twice, 7-year-old with PTSD).
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="PMC article page, read in the laptop browser")

b.code("jawaid-2016",
       tracks=[track("22-year-old woman", 22, "F", [
           ev("onset", -18, "months", "Schizophrenia: voices, mutism, aggression, persecutory delusions, thought block", "approx"),
           ev("treatment_failed", -4, "months", "Risperidone 6 mg for 6 weeks, then olanzapine to 20 mg for 6 weeks: worsening", "approx", to=-1),
           ev("cointervention", -14, "days", "Admitted; clozapine titrated to 175 mg; sedation and drooling"),
           ev("exposure_start", 0, "days", "Fall with head injury, myoclonus, then a generalised seizure during IV divalproex (2 g); midazolam; CT normal; clozapine stopped for a day"),
           ev("best_response", 1, "days", "No preoccupation, thought block or delusions; denies psychotic symptoms; back to her old way of relating, says her mother", state="Remitted"),
           ev("cointervention", 2, "days", "Clozapine restarted at 25 mg with divalproex 500 mg"),
           ev("follow_up", 12, "days", "One week after discharge: no positive or negative symptoms; sedated", state="Remitted"),
       ])],
       unexpectedness=T(era=("borderline", "That seizures help schizophrenia is the premise of ECT.")),
       attribution=A(1, 0, 1, 0, 0, "Overnight remission after the seizure; no scale; two weeks of clozapine, a head injury, IV valproate and midazolam all in the same 24 hours; follow-up under two weeks."),
       jbi=J("YYYYYYYY"),
       fix={"caveat": "Clozapine had been building for two weeks, and follow-up was under two weeks, on clozapine and valproate."})
b.reading("jawaid-2016",
          nulls=N(natural_history=("Unlikely", "Eighteen months, worsening."),
                  regression=("Possible", "Admitted at worst."),
                  misdiagnosis=("Unlikely", "Typical schizophrenia."),
                  cointervention=("Possible", "Clozapine for two weeks, valproate and a benzodiazepine started the same day."),
                  nonspecific=("Possible", "Post-ictal state and sedation."),
                  expectancy=("Unlikely", "None."),
                  reporting=("Possible", "No ratings; very short follow-up.")),
          verdict="Undecided",
          note="Overnight remission after a clozapine seizure, like ECT given by accident. Too short a follow-up, and too much happening on the same day, to call.",
          hyps=[H("The seizure acted as an ECT treatment on a brain primed by clozapine.",
                  "Generalised seizure → ECT-like network reset → rapid loss of psychotic preoccupation",
                  ["Network reset (seizure, coma, anaesthesia)"], "Fits",
                  "Change overnight; clozapine plus ECT is the standard rescue.",
                  "Single seizures rarely do what an ECT course does.", "Low", "Follow-up under two weeks.",
                  "Psychosis ratings after single seizures in clozapine-treated patients.")],
          related=[("felizardo-2023", "Delusional disorder remitting after clozapine seizures"), ("kim-2016", "Depression remitting after a seizure")])

b.code("donoghue-2015",
       tracks=[track("7-year-old boy", 7, "M", [
           ev("onset", -2, "years", "PTSD after severe abuse at 5, reactive attachment and disruptive behaviour; outbursts several times a day often needing restraint; residential care", "approx"),
           ev("treatment_failed", -2, "years", "Antidepressants, stimulants, alpha-2 agonists, antihistamines, mood stabilisers: no substantial improvement", "approx", to=-0.1),
           ev("exposure_start", 0, "days", "Tonsillectomy under anaesthesia with IV ketamine 10 mg (also propofol, nitrous oxide, dexamethasone 12 mg)"),
           ev("first_change", 2, "days", "Aggression much less; no restraints that week; more affectionate; first time talking about the abuse in therapy", "approx", state="Partial"),
           ev("relapse", 13, "days", "Back to baseline outbursts", state="Unchanged"),
           ev("exposure_restart", 3, "months", "Sedated MRI with IV ketamine 10 mg"),
           ev("first_change", 92, "days", "Again less aggression, better regulation, progress in therapy", "approx", state="Partial"),
           ev("follow_up", 98, "days", "Improvement lasted 8 days, then baseline returned", "approx", state="Unchanged"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 1, 2, 0, "Outbursts and restraints documented by residential staff before and after; improvement after each of two ketamine exposures, ending after 13 and 8 days; other anaesthetic drugs and dexamethasone came with the first."),
       jbi=J("YYYYYYYY"),
       fix={"outcome.resolution": "Temporary", "outcome.reversal": "Natural off-on"})
b.reading("donoghue-2015",
          nulls=N(natural_history=("Unlikely", "Daily outbursts for two years."),
                  regression=("Unlikely", "Steady baseline."),
                  misdiagnosis=("Unlikely", "Well-documented trauma-related dysregulation."),
                  cointervention=("Possible", "Dexamethasone, propofol and surgery the first time; the second exposure was ketamine with sedation only."),
                  nonspecific=("Unlikely", "Calmer but more affectionate and more open in therapy."),
                  expectancy=("Possible", "Staff knew he'd had a procedure; children get extra attention after surgery."),
                  reporting=("Possible", "Staff and therapist reports, no scale.")),
          verdict="Beats the null",
          note="Two separate 10 mg ketamine exposures, two windows of calm (13 and 8 days) in a boy with daily violent outbursts, and the first time he spoke about his abuse. Short-lived, but the repetition is what makes it.",
          hyps=[H("Ketamine opened a short plasticity window that eased fear-driven reactivity and let therapy reach the trauma.",
                  "Sub-anaesthetic NMDA blockade → glutamate surge, BDNF and synaptogenesis in prefrontal cortex → better top-down control of threat responses for days",
                  ["Glutamate", "Neuroplasticity"], "Fits",
                  "Improvement starting within days, waning over one to two weeks, as in ketamine depression trials; repeated with ketamine alone.",
                  "Ten milligrams is a small dose, even for a child.",
                  "Moderate", "No rating scale; two exposures only.",
                  "Scheduled, rated ketamine doses with a sedation-only comparison.")],
          related=[])

b.save()
