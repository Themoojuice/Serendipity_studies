"""Full-text appraisal, batch 16 (2026-11-17): four conference abstracts read on their PMC pages (the abstract is
the whole publication): bedell-2025 (semaglutide; pica), pardo-gonzalez-2023 (DRESS on cariprazine; bipolar
decompensation), felizardo-2023 (clozapine seizures; delusional disorder), silva-2021 (IVIG for myasthenia; BPD).
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="Conference abstract read on its PMC page (WebFetch); the abstract is the whole publication")

b.code("bedell-2025",
       tracks=[track("50-year-old woman", 50, "F", [
           ev("onset", -20, "years", "Pica: about a pound of cornstarch a day; long-standing iron deficiency (Hb 7.4, saturation 5%); iron trials hadn't stopped the craving", "at least"),
           ev("exposure_start", 0, "days", "Semaglutide for weight, titrated to 2.4 mg weekly; on escitalopram; stopped prescribed iron for side effects"),
           ev("first_change", 4, "months", "No cornstarch since reaching the maximum dose", "at most", state="Remitted"),
           ev("follow_up", 5, "months", "Craving eliminated; 34 lb lost", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 0, 0, 1, "Twenty years of daily pica before; gone at five months; iron was not repleted (she stopped it), which removes the obvious alternative; no dates for the change."),
       jbi=J("YYYYYYUY"))
b.reading("bedell-2025",
          nulls=N(natural_history=("Unlikely", "Twenty years, daily."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Possible", "Pica secondary to iron deficiency, though iron wasn't corrected."),
                  cointervention=("Unlikely", "Iron stopped; escitalopram unchanged as far as stated."),
                  nonspecific=("Possible", "Appetite suppression reduces all eating."),
                  expectancy=("Unlikely", "Nothing aimed at pica."),
                  reporting=("Possible", "Self-report in a conference abstract.")),
          verdict="Beats the null",
          note="Twenty years of daily cornstarch eating stopped on semaglutide while the iron deficiency that usually drives pica went uncorrected. That last detail is what makes it interesting.",
          hyps=[H("GLP-1 agonism suppressed the craving itself, not just appetite.",
                  "Semaglutide → GLP-1 receptors in hypothalamus and reward circuits → specific craving loses its pull",
                  ["Neuropeptide (oxytocin, orexin, other)", "Dopamine"], "Fits",
                  "Stopped at full dose; iron deficiency persisted.",
                  "Could be general appetite suppression.",
                  "Low", "No dates, no iron studies after.",
                  "Pica outcomes in GLP-1-treated patients with iron deficiency, with and without repletion.")],
          related=[("jarvinen-2019", "Food obsessions easing on liraglutide")])

b.code("pardo-gonzalez-2023",
       tracks=[track("50-year-old woman", 50, "F", [
           ev("onset", -30, "years", "Bipolar disorder from age 20, moderate intellectual disability, generalised epilepsy; on valproate and lithium", "approx"),
           ev("assessment", -14, "days", "Decompensation: irritability, talking to herself, verbosity, hostility, agitation; cariprazine added", "approx"),
           ev("exposure_start", 0, "days", "Necrotic papulovesicular rash compatible with DRESS; cariprazine stopped"),
           ev("best_response", 2, "weeks", "Affective symptoms in almost complete remission", "approx", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(0, 0, 0, 0, 0, "No measure, no dates, no follow-up; remission coincided with stopping cariprazine and a systemic drug reaction."),
       jbi=J("YYYYYNYY"),
       fix={"caveat": "Bipolar decompensations end on their own, and she was on lithium and valproate throughout."})
b.reading("pardo-gonzalez-2023",
          nulls=N(natural_history=("Likely", "An acute bipolar decompensation weeks old, on mood stabilisers."),
                  regression=("Likely", "Caught at a peak."),
                  misdiagnosis=("Unlikely", "Long-known bipolar disorder."),
                  cointervention=("Possible", "Hospital care for DRESS; cariprazine stopped."),
                  nonspecific=("Possible", "Systemic illness can flatten agitation."),
                  expectancy=("Unlikely", "None."),
                  reporting=("Possible", "Conference abstract without detail.")),
          verdict="Doesn't beat the null",
          note="An acute bipolar episode ending during a severe drug reaction is unremarkable on its own. Kept for the intercurrent-illness pattern.",
          hyps=[H("The immune storm of DRESS damped the manic decompensation, as fevers and infections sometimes do.",
                  "DRESS → systemic cytokine surge and steroids → mood circuitry quietened",
                  ["Inflammation and cytokines", "Sickness behaviour"], "Can't judge",
                  "Remission coincided with the reaction.",
                  "Episodes end anyway; no detail.",
                  "Low", "No timeline or measure.", "Mood ratings through drug reactions in bipolar patients.")],
          related=[("arora-2006", "Remission during Stevens-Johnson syndrome")])

b.code("felizardo-2023",
       tracks=[track("78-year-old man", 78, "M", [
           ev("onset", -1, "years", "Persistent delusional disorder, no prior psychiatric history; resistant to three antipsychotics", "at least"),
           ev("cointervention", -14, "days", "Clozapine 100 mg/day started", "approx"),
           ev("exposure_start", 0, "days", "Two epileptic seizures (attributed to clozapine in the methods, called spontaneous in the conclusions)"),
           ev("best_response", 3, "days", "Almost immediate complete remission of the delusions", "approx", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 1, 0, 0, "Resistant to three antipsychotics; remission said to be almost immediate after the seizures; clozapine, itself the standard rescue drug, had just been started."),
       jbi=J("YNYUYUUY"))
b.reading("felizardo-2023",
          nulls=N(natural_history=("Unlikely", "Persistent and treatment-resistant."),
                  regression=("Possible", "Admitted at a decompensation."),
                  misdiagnosis=("Possible", "First psychosis at 78 needs an organic work-up the abstract doesn't describe."),
                  cointervention=("Likely", "Clozapine had just been started and is the expected treatment for resistance."),
                  nonspecific=("Possible", "Post-ictal state."),
                  expectancy=("Unlikely", "None."),
                  reporting=("Possible", "No measure or dates.")),
          verdict="Doesn't beat the null",
          note="Remission right after two seizures is an ECT-like story, but clozapine had just been started and late-onset psychosis at 78 has organic possibilities the abstract doesn't address.",
          hyps=[H("The seizures worked like ECT.",
                  "Generalised seizures → ECT-like network reset → delusions dissolve within days",
                  ["Network reset (seizure, coma, anaesthesia)"], "Fits",
                  "'Almost immediate' resolution after seizures.",
                  "Clozapine onset can't be excluded.",
                  "Low", "No dates.", "Similar cases with seizures before clozapine had time to act.")],
          related=[("kim-2016", "Depression remitting after a seizure"), ("silverstone-1991", "Spontaneous seizures after failed ECT")])

b.code("silva-2021",
       tracks=[track("39-year-old woman", 39, "F", [
           ev("onset", -1, "years", "Borderline personality disorder with self-injury and acting out; myasthenia; on valproate, aripiprazole and gabapentin", "at least"),
           ev("assessment", -3, "days", "Admitted with self-injury ideation, acting out and a depressive episode (ISAS, HAM-A, MADRS, ABUSI, BIS-11 79)", "approx"),
           ev("exposure_start", 0, "days", "Intravenous immunoglobulin for a myasthenia flare; no other treatment change"),
           ev("best_response", 1, "days", "Self-injury ideation down, acting out stopped, depression fully remitted, mild anxiety", "approx", state="Remitted"),
           ev("follow_up", 3, "weeks", "Still in remission (one month in the conclusions)", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 1, 1, 0, 0, "Scales at baseline, immediately after and at follow-up (values in figures only); no drug changes, but the infusion came days into an admission for a crisis."),
       jbi=J("YNYYYYUY"),
       fix={"caveat": "Three weeks of follow-up in a condition that fluctuates by the week; admission itself often settles self-harm."})
b.reading("silva-2021",
          nulls=N(natural_history=("Possible", "Crises in borderline personality disorder settle quickly, especially after admission."),
                  regression=("Likely", "Admitted at a crisis peak; three weeks of follow-up."),
                  misdiagnosis=("Unlikely", "Known diagnosis."),
                  cointervention=("Possible", "Admission and attention."),
                  nonspecific=("Unlikely", "Mood lifted."),
                  expectancy=("Possible", "A new infusion and medical attention."),
                  reporting=("Possible", "Numbers only in figures; short follow-up.")),
          verdict="Doesn't beat the null",
          note="Immunoglobulin for myasthenia and a borderline crisis lifted at once. Admission-peak regression explains most crisis improvements over three weeks.",
          hyps=[H("Immunoglobulin dampened an inflammatory contribution to mood and impulsivity.",
                  "IVIG → reduced cytokines and autoantibody effects → mood and impulse control improve",
                  ["Inflammation and cytokines"], "Can't judge",
                  "Immediate change with no other modification.",
                  "Crisis regression.",
                  "Low", "Very short follow-up.", "Repeat IVIG courses with mood ratings.")],
          related=[])

b.save()
