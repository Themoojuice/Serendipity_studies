"""Full-text appraisal, batch 30 (2026-11-20): the four cases settled in from the unsure pile tonight
(scripts/batches/b2026_11_20_unsure_settle_v4.py), coded from the texts read there.
(grunstein-2017 stays tier B: flags are for integrity problems, and since v1.8.2 coded tiers follow the section 6 rule,
which supersedes v1.7.2's blanket tier C for secondary-cause calls; the secondary reading stays in its caveat and reading.)
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-20", source="Full text read tonight (ClinicalKey, PMC scans, Cambridge)")


b.code("d-andrea-2013",
       tracks=[track("23-year-old army veteran", 23, "M", [
           ev("onset", -3, "years", "Combat PTSD after a 15-month deployment with daily bombardment and 300 firefights: nightmares, 3 hours' sleep, hypervigilant 'guard duty' on the balcony, daily panic, rage", "approx"),
           ev("treatment_failed", -2, "years", "Trauma recovery programme (PCL-M 63 to 44, short-lived), exposure therapy, an 8-week residential programme (49 to 56), EMDR, ten antidepressants and antipsychotics, six hypnotics; three admissions", "approx", to=0),
           ev("assessment", -1, "days", "Despondent and suicidal; PTSD checklist (PCL-M) 66", scores=[{"scale": "PCL-M", "value": 66, "higher_is_better": False}]),
           ev("exposure_start", 0, "days", "Single ketamine infusion (35 mg, with propofol 30 mg) for treatment-resistant depression, after a 24-hour medication washout"),
           ev("first_change", 2, "hours", "Affectionate with his wife, warm toward his team, grieving his old therapist", state="Partial"),
           ev("assessment", 1, "weeks", "Euthymic, anxiety and hyperarousal gone, sleeping normally without hypnotics, no nightmares; PCL-M 29", state="Remitted",
              scores=[{"scale": "PCL-M", "value": 29, "higher_is_better": False}]),
           ev("relapse", 15, "days", "Withdrew from his wife and within 24 hours was back to his previous state; venlafaxine restarted", state="Worse"),
       ])],
       unexpectedness=T(secondary=("borderline", "Depression and PTSD lifted together; the PTSD change may ride on the antidepressant effect."),
                        era=("borderline", "Perioperative ketamine and PTSD had mixed reports and a ketamine PTSD trial was under way.")),
       attribution=A(1, 1, 1, 0, 1, "Years of measured, refractory PTSD; PCL-M 66 to 29 within a week of one infusion, after a washout and with nothing else new; relapse at 15 days as a single dose wore off."),
       jbi=J("YYYYYYYY"),
       fix={"outcome.reversal": "None reported"})
b.reading("d-andrea-2013",
          nulls=N(natural_history=("Unlikely", "Three years of worsening PTSD through every treatment."),
                  regression=("Possible", "Given at a crisis, with suicide risk and a birth approaching."),
                  misdiagnosis=("Unlikely", "Classic combat PTSD, repeatedly measured."),
                  cointervention=("Unlikely", "A 24-hour washout and nothing else new."),
                  nonspecific=("Unlikely", "He was warmer and more engaged, not blunted."),
                  expectancy=("Possible", "A dramatic, much-anticipated infusion."),
                  reporting=("Unlikely", "PCL-M before and after, and his wife's account.")),
          verdict="Beats the null",
          note="One ketamine infusion given for depression wiped out three years of refractory combat PTSD for two weeks, by a standard checklist, and it came back within a day. A clean demonstration of an effect, if a short one; esketamine later went into PTSD trials.",
          hyps=[H("NMDA blockade triggered a burst of synaptic plasticity that loosened entrenched fear and threat circuits.",
                  "Ketamine → NMDA antagonism → glutamate surge, BDNF and mTOR signalling → prefrontal synaptogenesis → stronger top-down control of amygdala threat responses → PTSD symptoms lift until the new synapses fade",
                  ["Glutamate", "Neuroplasticity"], "Fits",
                  "Effect within hours, gone in about two weeks: the time course of ketamine's antidepressant action.",
                  "Depression lifted too, so PTSD-specific action is unproven.", "Moderate", "One case; mood confound.",
                  "Ketamine trials in PTSD without depression.")],
          related=[("ray-2016", "Ketamine for pain lifting refractory panic and agoraphobia")])

b.code("macleod-1897",
       tracks=[track("Married woman of 32, Shanghai", 32, "F", [
           ev("onset", -7, "years", "Hypodermic morphine for neuralgia from 1889, continued without a break; several slow withdrawals failed; she did not want to be cured", "approx"),
           ev("exposure_start", 0, "days", "Sodium bromide for migraine and nervous irritability (May 1896); a bottle and a half taken in two days: unrousable with bromide poisoning"),
           ev("first_change", 1, "days", "No desire for morphine from the day she entered hospital", "approx", state="Remitted"),
           ev("cointervention", 1, "days", "Admitted to hospital: morphine injected for 4 days then stopped; more bromide and chloralamide; then no drugs", to=11),
           ev("assessment", 3, "weeks", "Two weeks of stupor, confusion, delusions and visual illusions, clearing by early June; amnesic for the period", "approx"),
           ev("follow_up", 13, "months", "Left hospital well (June 1896); desire for morphine had not returned when he wrote (July 1897)", "approx", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 1, 0, 0, "Seven years of morphine use despite withdrawals; craving gone from the poisoning and hospital admission, held for about a year; but morphine was withdrawn in hospital under the bromide narcosis."),
       jbi=J("YYYNYYYY"))
b.reading("macleod-1897",
          nulls=N(natural_history=("Unlikely", "Seven years of continuous use."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Unlikely", "Iatrogenic morphine dependence."),
                  cointervention=("Possible", "She was withdrawn from morphine in hospital while narcotised: an accidental rapid detoxification."),
                  nonspecific=("Possible", "Two weeks of delirium and amnesia."),
                  expectancy=("Unlikely", "She had said she did not want to be cured."),
                  reporting=("Possible", "One physician's account, about a year of follow-up.")),
          verdict="Undecided",
          note="A seven-year morphine habit ended after accidental bromide poisoning: she woke from two weeks of delirium with no craving, in a woman who had no wish to stop. Her doctor then reproduced it on purpose in a pilot. Withdrawal under narcosis is the boring explanation; the lost craving is what made him try it again.",
          hyps=[H("Prolonged bromide narcosis and delirium let withdrawal pass unfelt and broke the conditioned craving.",
                  "Bromide intoxication → days of stupor and amnesia → morphine withdrawn without the experience of withdrawal or cue-driven craving → habit loses its reinforcement",
                  ["Network reset (seizure, coma, anaesthesia)", "Extinction and exposure"], "Fits",
                  "No craving from admission; the same happened in the deliberate second case.",
                  "Anaesthesia-assisted detoxification today has poor long-term results.", "Low", "Two cases, one deliberate.",
                  "None now; rapid opioid detoxification under anaesthesia trials are the modern analogue.")])

b.code("anon-1888-typhoid",
       tracks=[track("Woman of about 50, Norristown asylum", 50, "F", [
           ev("onset", -3, "years", "Chronic melancholia for several years", "at least"),
           ev("exposure_start", 0, "days", "Typhoid fever in an outbreak at the State Hospital for the Insane, Norristown (1888)"),
           ev("best_response", 0, "days", "Discharged perfectly well (time not given)", "at least", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 0, 0, 0, "Several years of melancholia before; discharged well after typhoid; no timing, measures or follow-up; a reprinted news item."),
       jbi=J("YNNNYUAY"))
b.reading("anon-1888-typhoid",
          nulls=N(natural_history=("Possible", "Asylum melancholias did remit, though chronic ones less often."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Possible", "Period diagnosis, no description."),
                  cointervention=("Can't judge", "Nothing said."),
                  nonspecific=("Unlikely", "Discharged well."),
                  expectancy=("Unlikely", "None."),
                  reporting=("Likely", "A short reprinted news item.")),
          verdict="Doesn't beat the null",
          note="An asylum typhoid outbreak 'cured' a woman with several years of melancholia and a young man with mania. Too thin to weigh, but one of the fever cures that accumulated until Wagner-Jauregg acted on them.",
          hyps=[H("High fever and the systemic inflammatory response interrupted a chronic depressive state.",
                  "Typhoid → prolonged high fever and cytokine surge → reset of neuroimmune and HPA signalling → melancholia lifts",
                  ["Fever and heat", "Inflammation and cytokines"], "Can't judge", "Echoes many period reports.", "No detail.",
                  "Low", "News item.", "The Medical and Surgical Reporter original (1888).")],
          related=[("wagner-jauregg-1883", "Erysipelas and insanity, 1883"), ("anon-1890-influenza", "Influenza and insanity, 1890")])

b.code("granato-1994",
       tracks=[track("Mr G, 70-year-old man", 70, "M", [
           ev("onset", -15, "months", "Severe depression, resistant to several antidepressants at therapeutic doses; too cachectic for ECT"),
           ev("assessment", -8, "months", "From the seventh month: anorexia, self-neglect, mutism, global slowing: a stuporous depression; MMSE 26/30", "approx"),
           ev("cointervention", -4, "weeks", "Amineptine 200 mg a day", to=0),
           ev("exposure_start", 0, "days", "Intravenous midazolam 5 mg to sedate him for an MRI (diffuse vascular white matter disease)"),
           ev("first_change", 1, "days", "Emotional behaviour, mutism, opposition and depressed mood spectacularly better; smiling returned", state="Partial"),
           ev("follow_up", 10, "days", "Still improved", state="Partial"),
       ])],
       unexpectedness=T(era=("borderline", "Benzodiazepines were already known to lift catatonic stupor (the lorazepam challenge).")),
       attribution=A(1, 0, 1, 0, 0, "Fifteen months of resistant depression, eight of stupor; dramatic change the day after one sedating dose; no scale, ten days' follow-up, and amineptine had been started four weeks earlier."),
       jbi=J("YYYYYYUY"))
b.reading("granato-1994",
          nulls=N(natural_history=("Unlikely", "Fifteen months, worsening."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Possible", "Catatonic stupor rather than depression; benzodiazepines are expected to lift catatonia."),
                  cointervention=("Possible", "Amineptine at four weeks is within antidepressant onset time."),
                  nonspecific=("Unlikely", "He brightened, not sedated."),
                  expectancy=("Unlikely", "Given for a scan."),
                  reporting=("Possible", "No scale; ten days.")),
          verdict="Undecided",
          note="A mute, stuporous depressed man brightened the day after midazolam given for an MRI. It sits with DeLisle and Morena's midazolam catatonia cases; benzodiazepine-responsive catatonia and an antidepressant started four weeks earlier are the two boring explanations.",
          hyps=[H("GABA-A potentiation released a catatonic stupor layered on the depression.",
                  "Midazolam → GABA-A potentiation → relief of catatonic motor and affective inhibition (lorazepam-challenge mechanism) → speech and affect return",
                  ["GABA"], "Fits", "Overnight; stupor features prominent.", "Midazolam is gone within hours, yet the change held ten days.",
                  "Moderate", "No ratings or rechallenge.", "Lorazepam challenge in stuporous depression in the elderly.")],
          related=[("delisle-1991", "Midazolam reversing catatonia, on and off"), ("morena-1994", "Midazolam for MRI lifting catatonia")])

b.save()
