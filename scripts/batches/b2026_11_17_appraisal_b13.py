"""Full-text appraisal, batch 13 (2026-11-17): vendrell-serres-2021 (esketamine for depression; functional paralysis),
hosseini-2026 (clomiphene dispensed in error for clomipramine; OCD). romeo-2025 excluded (E3): the full text says
semaglutide was chosen partly to reduce cocaine craving, so the target was treated on purpose.
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="PMC open-access full text, via Europe PMC")

b.exclude("romeo-2025", "E3", "semaglutide was chosen 'on the basis of evidence supporting its efficacy in ... potentially reducing drug cravings', with behavioural counselling: deliberate treatment of the target.")

b.code("vendrell-serres-2021",
       tracks=[track("49-year-old man", 49, "M", [
           ev("onset", -12, "months", "Sudden functional paralysis and numbness of the left arm with a major depressive episode; CT, MRI and EMG normal; needs help with daily tasks", "approx"),
           ev("treatment_failed", -12, "months", "Paroxetine to 60 mg with clonazepam; then mirtazapine and aripiprazole; CBT every 2 weeks from month 4 (ongoing); then venlafaxine 300 mg: partial help for mood, none for the arm", "approx", to=-1),
           ev("exposure_start", 0, "days", "Esketamine nasal spray 56 mg, then 84 mg twice weekly for 4 weeks, for treatment-resistant depression"),
           ev("first_change", 2, "hours", "Almost complete recovery of arm movement 2 hours after the first dose, easing back a little over following days", state="Partial"),
           ev("best_response", 4, "weeks", "Full movement, MRC power 5/5, numbness gone; depression in remission (MADRS)", "approx", state="Remitted",
              scores=[{"scale": "MRC power", "value": 5}]),
           ev("follow_up", 5, "months", "Esketamine every 2 weeks: depression and arm both still well", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 1, 0, 1, "A year of fixed paralysis, then near-recovery 2 hours after the first dose; MRC power only after; other treatments unchanged for months. Movement improved after each dose and eased a little between doses, which is suggestive but not a documented stop and return."),
       jbi=J("YYYYYYYY"),
       fix={"caveat": "Functional symptoms respond to expectation and to dramatic new treatments; a dissociative drug given with ceremony is exactly that."})
b.reading("vendrell-serres-2021",
          nulls=N(natural_history=("Unlikely", "A year of fixed paralysis; functional paralysis at a year has a poor prognosis."),
                  regression=("Unlikely", "Steady for a year."),
                  misdiagnosis=("Unlikely", "Positive signs and normal investigations."),
                  cointervention=("Unlikely", "CBT and medicines unchanged for months before."),
                  nonspecific=("Unlikely", "Movement improved, not reduced."),
                  expectancy=("Possible", "Functional disorder plus a novel, dramatic treatment; suggestion may be part of the mechanism."),
                  reporting=("Possible", "No motor measure before treatment.")),
          verdict="Undecided",
          note="A year-long functional paralysis moved within two hours of the first esketamine dose and improved after each dose. Whether that is ketamine or the theatre of a new treatment is exactly what can't be told from one case.",
          hyps=[H("Esketamine's dissociation loosened the fixed predictive model of a paralysed limb.",
                  "NMDA blockade → dissociation and weakened top-down priors → the brain's prediction of 'no movement' loosens → voluntary movement returns",
                  ["Glutamate", "Suggestion and belief update"], "Fits",
                  "Recovery within hours, at the time of dissociation, repeated each dose.",
                  "No measure of dissociation or of belief.",
                  "Low", "Expectancy can't be separated from drug effect.",
                  "Blinded esketamine versus active placebo (midazolam) in functional paralysis."),
                H("Lifting depression released the functional symptom.",
                  "Rapid antidepressant effect → less low mood and helplessness → functional symptom loses its hold",
                  ["Glutamate", "Neuroplasticity"], "Fits",
                  "Mood and arm improved together from the first dose.",
                  "Mood had partly improved before without the arm changing.",
                  "Low", "Mood and motor change concurrent.", "Separate time courses of mood and motor function on esketamine.")],
          related=[("corte-2025", "Functional seizures gone after ECT given for depression")])

b.code("hosseini-2026",
       tracks=[track("50-year-old woman", 50, "F", [
           ev("onset", -18, "years", "OCD after second childbirth (contamination, cleaning, harm fears); Y-BOCS 30; good response to sertraline, clonazepam and clomipramine 75 mg (Y-BOCS 12)", "approx"),
           ev("assessment", -10, "months", "Clomipramine tapered over 4 months for tremor and dry mouth: OCD and anxiety relapse", "approx"),
           ev("treatment_failed", -3, "months", "Sertraline raised to 200 mg for 12 weeks: no meaningful change", to=-0.1, scores=[{"scale": "Y-BOCS", "value": 23, "higher_is_better": False}]),
           ev("exposure_start", 0, "days", "Prescribing error: clomiphene 25 mg/day dispensed instead of clomipramine; taken with sertraline 100 mg and clonazepam 2 mg"),
           ev("best_response", 12, "weeks", "Dramatic remission; back to social and work activity; Y-BOCS about 7 by her own retrospective estimate", "at most", state="Remitted",
              scores=[{"scale": "Y-BOCS", "value": 7, "higher_is_better": False}]),
           ev("exposure_stop", 12, "weeks", "Error discovered; clomiphene tapered, clomipramine restarted at 75 mg"),
           ev("follow_up", 6, "months", "Controlled again on clomipramine, but not as well as during the clomiphene weeks", "approx", state="Partial"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 0, 0, 0, "Y-BOCS 23 before; afterwards only her recalled estimate (about 7); onset of improvement within the 12 weeks not dated; sertraline was cut from 200 to 100 mg at the same time."),
       jbi=J("YYYYYUYY"),
       fix={"caveat": "OCD can respond late to an SSRI, and sertraline at 200 mg had only just completed 12 weeks; the improvement was rated by recall."})
b.reading("hosseini-2026",
          nulls=N(natural_history=("Possible", "Relapse was recent and OCD fluctuates; perimenopause adds hormonal flux."),
                  regression=("Possible", "Error came at the point of seeking a change."),
                  misdiagnosis=("Unlikely", "Long-documented OCD."),
                  cointervention=("Possible", "A late response to 12 weeks of high-dose sertraline; dose then lowered."),
                  nonspecific=("Unlikely", "More active."),
                  expectancy=("Possible", "She believed she was back on the drug that had worked for 15 years."),
                  reporting=("Possible", "Y-BOCS after was a recalled estimate.")),
          verdict="Undecided",
          note="The striking detail is expectancy: she thought she was restarting clomipramine, the drug that had kept her well for 15 years. That makes this as much a placebo case as a clomiphene case.",
          hyps=[H("Expectation of the trusted drug produced the response.",
                  "Believed she was back on clomipramine → strong positive expectation → OCD eased",
                  ["Suggestion and belief update"], "Fits",
                  "Fifteen years of good response to clomipramine; remission in the weeks she thought she was taking it.",
                  "The real clomipramine afterwards worked less well, which expectancy doesn't explain.",
                  "Moderate", "No blind and no dated ratings.",
                  "None possible in this patient; placebo-response rates in OCD trials are low, which counts against."),
                H("Clomiphene's oestrogen-receptor modulation steadied a hormonally sensitive OCD in perimenopause (the authors' speculation).",
                  "Clomiphene → hypothalamic oestrogen-receptor blockade → gonadotrophins and oestradiol rise → serotonergic tone changes → OCD eases",
                  ["Sex steroids and reproduction", "Serotonin"], "Can't judge",
                  "OCD began postpartum and worsened around perimenopause.",
                  "No hormone measurements.",
                  "Low", "No hormonal data.", "Hormone levels across OCD fluctuations in women with reproductive-linked onset.")],
          related=[])

b.save()
