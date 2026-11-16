"""Full-text appraisal, batch 3 (2026-11-17): the GLP-1 receptor agonist trio, all Included.

kelly-2026 (semaglutide, dopamine-agonist impulse control disorder), meilinger-2026 (semaglutide, alcohol),
takizawa-2026 (tirzepatide, three heavy drinkers, one with alcohol use disorder).

kelly-2026: outcome.reversal recoded to On-off rechallenge (weekly end-of-dose return; relapse when he ran out,
gone again on restarting); tier B -> A under the section 6 rule.
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="PMC open-access full text, via Europe PMC")
GLP_ERA = ("borderline", "By the mid-2020s GLP-1 agonists were known to reduce alcohol and nicotine craving (trials and a meta-analysis), so a reward effect was conceivable.")

# ------------------------------------------------------------------ kelly-2026
b.code("kelly-2026",
       tracks=[track("46-year-old man", 46, "M", [
           ev("assessment", 0, "days", "Young-onset Parkinson's on pramipexole 1.5 mg three times daily and levodopa. Pramipexole had brought intrusive infidelity thoughts; a dose cut helped but he raised it again for motor benefit. Now hypersexual thoughts with affairs, and compulsive shopping (US$30,000)"),
           ev("exposure_start", 0, "days", "Semaglutide 1 mg weekly for proteinuria; pramipexole and levodopa unchanged"),
           ev("first_change", 1, "months", "Hypersexual thoughts stopped completely ('water on a fire')", "at most", state="Remitted"),
           ev("assessment", 1, "months", "Mild return of the thoughts the day before each weekly dose, gone after each injection", "approx", to=5),
           ev("exposure_stop", 4, "months", "Ran out of semaglutide by accident", "approx", note="Order as reported; timing not stated."),
           ev("relapse", 4.1, "months", "Impulse control disorder returned", "approx"),
           ev("exposure_restart", 4.2, "months", "Semaglutide resumed", "approx"),
           ev("best_response", 4.3, "months", "Thoughts gone again", "approx", state="Remitted"),
           ev("follow_up", 6, "months", "Six months on semaglutide: no hypersexuality or compulsive spending; motor control good on unchanged dopaminergic drugs", state="Remitted"),
       ])],
       unexpectedness=T(era=GLP_ERA),
       attribution=A(0, 0, 1, 2, 1, "Duration of the impulse control disorder not stated; dopaminergic regimen explicitly unchanged; no ICD scale."),
       jbi=J("YUYYYYNY"),
       fix={"tier": "A", "outcome.reversal": "On-off rechallenge",
            "summary": "A 46-year-old's pramipexole-induced hypersexuality and compulsive shopping stopped on semaglutide given for proteinuria, crept back the day before each weekly dose and when he ran out, and stayed away for six months on an unchanged agonist.",
            "caveat": "The impulse control disorder had driven affairs and a large debt just before, and that crisis may have prompted restraint of its own."})
b.reading("kelly-2026",
          nulls=N(natural_history=("Unlikely", "Agonist-driven impulse control disorder on an unchanged dose doesn't usually stop by itself."),
                  regression=("Possible", "Started at a crisis: affairs and a US$30,000 spending debt."),
                  misdiagnosis=("Unlikely", "A typical dopamine-agonist impulse control disorder."),
                  cointervention=("Possible", "The marital and financial fallout may have motivated restraint."),
                  nonspecific=("Possible", "GLP-1 agonists suppress appetite and may blunt drive in general."),
                  expectancy=("Unlikely", "Semaglutide was for his kidneys; nobody expected this."),
                  reporting=("Possible", "Self-report only; no impulse control scale.")),
          verdict="Beats the null",
          note="An effect that wears off the day before each weekly dose and returns when the drug runs out is a dose-response and a rechallenge in one patient, with the agonist that caused the disorder held constant.",
          hyps=[H("GLP-1 receptor activation damped the mesolimbic reward signalling that the dopamine agonist had sensitised.",
                  "Semaglutide → GLP-1 receptors in ventral tegmental area and nucleus accumbens → less dopamine release to rewards → over-valuation of sexual and shopping rewards dampened",
                  ["Neuropeptide (oxytocin, orexin, other)", "Dopamine"], "Fits",
                  "End-of-dose return and relapse on running out; semaglutide blunts alcohol-evoked dopamine release in rodents (authors).",
                  "Semaglutide's half-life is about a week, so a sharp wear-off the day before the next dose is more than drug levels alone predict.",
                  "Moderate", "Self-report only: no impulse control rating across the dosing cycle or the run-out.",
                  "A validated impulse control rating (such as QUIP-RS) across the injection cycle and a documented pause."),
                H("General suppression of appetite and drive, not a specific effect on the impulse control disorder.",
                  "Semaglutide → less hunger and less 'wanting' in general → fewer impulsive acts of every kind",
                  ["Global suppression (sedation, apathy, cognitive loss)"], "Fits",
                  "GLP-1 agonists reduce food reward broadly.",
                  "He kept working and playing pickleball; motor drive and function stayed good.",
                  "Low", "Mood, apathy and other rewards weren't assessed.",
                  "An apathy scale alongside impulse control ratings.")],
          related=[("meilinger-2026", "Semaglutide for obesity, drinking fell"),
                   ("takizawa-2026", "Tirzepatide, three heavy drinkers drank less")])

# ------------------------------------------------------------------ meilinger-2026
b.code("meilinger-2026",
       tracks=[track("34-year-old man", 34, "M", [
           ev("onset", -4, "years", "Heavy drinking and weight gain for four years: couldn't stop once started; a drink-driving conviction", "approx"),
           ev("exposure_start", 0, "days", "Semaglutide 0.25 mg weekly for obesity (BMI 37), titrated to 2.4 mg; about 15 drinks a week with weekly binges; 9 of 11 DSM-5 criteria",
              scores=[{"scale": "AUDIT", "value": 27}]),
           ev("cointervention", 0, "days", "Testosterone 100 mg intramuscularly weekly for hypogonadism, started the same week"),
           ev("best_response", 10, "months", "Desire to drink gone: about half a beer a month; BMI 28.6", "at most", state="Remitted",
              scores=[{"scale": "AUDIT", "value": 7}]),
           ev("follow_up", 10, "months", "Better mood, relationships and bipolar control", "approx", state="Remitted"),
       ])],
       unexpectedness=T(era=GLP_ERA),
       attribution=A(1, 1, 0, 0, 0, "AUDIT before and after; when the drinking fell isn't reported; testosterone started the same week and wasn't discussed."),
       jbi=J("YUYYYYNY"),
       fix={"caveat": "Testosterone replacement began the same week, and improved mood or energy could have cut his drinking too."})
b.reading("meilinger-2026",
          nulls=N(natural_history=("Possible", "Heavy drinking fluctuates, and four years is not long."),
                  regression=("Unlikely", "He came for weight loss, not at a drinking crisis."),
                  misdiagnosis=("Unlikely", "Severe alcohol use disorder by DSM-5 count and AUDIT."),
                  cointervention=("Possible", "Testosterone started the same week; weight-clinic contact; bipolar care elsewhere."),
                  nonspecific=("Possible", "Appetite suppression and nausea cut intake of anything."),
                  expectancy=("Possible", "He started semaglutide after hearing about others' success, though for weight."),
                  reporting=("Possible", "Self-report and AUDIT only.")),
          verdict="Undecided",
          note="A 20-point AUDIT fall is real, but with testosterone started the same week, no timing and no biomarker, the case can only join the GLP-1 tally.",
          hyps=[H("GLP-1 receptor activation reduced the reward value of alcohol.",
                  "Semaglutide → GLP-1 receptors in reward circuits → less dopamine response to alcohol → craving falls",
                  ["Neuropeptide (oxytocin, orexin, other)", "Dopamine"], "Can't judge",
                  "He described the desire to drink disappearing; consistent with trials and the other GLP-1 cases here.",
                  "No record of when drinking fell relative to the dose steps.",
                  "Low", "No timeline of drinking against the titration schedule.",
                  "A drinking diary against the dose steps; drinking returning if semaglutide stops."),
                H("Testosterone replacement improved mood and energy, and drinking fell with it.",
                  "Testosterone for hypogonadism → better mood, energy and confidence → less drinking",
                  ["Sex steroids and reproduction"], "Can't judge",
                  "Started the same week; hypogonadism can lower mood.",
                  "Testosterone isn't known to end heavy drinking.",
                  "Low", "No mood ratings, and the two drugs started together.",
                  "Drinking after either drug is stopped alone.")],
          related=[("kelly-2026", "Semaglutide ending a dopamine-agonist impulse control disorder, with rechallenge"),
                   ("takizawa-2026", "Tirzepatide, three heavy drinkers drank less")])

# ------------------------------------------------------------------ takizawa-2026
b.code("takizawa-2026",
       tracks=[
           track("Case 1", 49, "M", [
               ev("onset", -27, "years", "Heavy drinking since his twenties (107–284 g ethanol a day)", "approx"),
               ev("diagnosis", -6, "years", "Alcohol use disorder and alcohol-related liver disease (biopsy A2F2) at 43", "approx"),
               ev("treatment_failed", -1, "years", "Nalmefene cut intake to 40 g a day; later back to 55 g a day despite drunken falls and an admission", "at least"),
               ev("exposure_start", 0, "days", "Tirzepatide 2.5 mg weekly for new type 2 diabetes and obesity; 55 g a day; GGT 904, HbA1c 8.8%"),
               ev("first_change", 1, "months", "28 g a day; cravings down; transient lethargy after meals", state="Partial"),
               ev("follow_up", 5, "months", "FIB-4 2.57, HbA1c 5.7%, 85 kg", state="Partial"),
           ]),
           track("Case 2", 66, "M", [
               ev("onset", -46, "years", "413–553 g ethanol a week since 20; no alcohol use disorder diagnosis", "approx"),
               ev("exposure_start", 0, "days", "Tirzepatide 2.5 mg weekly"),
               ev("cointervention", 4, "weeks", "Increased to 5 mg"),
               ev("best_response", 8, "months", "56–78 g a week; 'became gradually bored while drinking'; GGT 220 → 59", "at most", state="Partial"),
               ev("follow_up", 8, "months", "Liver and metabolic indices improved", state="Partial"),
           ]),
           track("Case 3", 52, "F", [
               ev("onset", -32, "years", "276–620 g ethanol a week since 20; no alcohol use disorder diagnosis", "approx"),
               ev("assessment", -1, "months", "Intake already down to 42–84 g a week after the first clinic visit", "approx"),
               ev("exposure_start", 0, "days", "Tirzepatide 2.5 mg weekly; nausea for 3 days after each dose"),
               ev("cointervention", 11, "weeks", "Increased to 5 mg"),
               ev("best_response", 6, "months", "14 g a month; 65 kg", "at most", state="Remitted"),
               ev("follow_up", 6, "months", "Liver and metabolic indices normal", state="Remitted"),
           ]),
       ],
       unexpectedness=T(era=GLP_ERA,
                        secondary=("borderline", "New diabetes and liver-disease diagnoses are themselves reasons to drink less."),
                        base_rate=("borderline", "Two of the three had no alcohol use disorder, and case 3 had already cut down after the first visit.")),
       attribution=A(1, 0, 1, 0, 1, "Scored on case 1 (the one with alcohol use disorder). Intake self-reported; the authors state no extra counselling or effort."),
       jbi=J("NUYUUYYYNA"),
       note="Only case 1 meets criterion 1; cases 2 and 3 are heavy drinking without a diagnosis.")
b.reading("takizawa-2026",
          nulls=N(natural_history=("Possible", "Heavy drinking falls with age and illness."),
                  regression=("Possible", "Case 3 had already cut down after the first visit, before tirzepatide."),
                  misdiagnosis=("Possible", "Two of three didn't have alcohol use disorder, so the 'syndrome' is mostly heavy drinking."),
                  cointervention=("Possible", "New diabetes and liver diagnoses, clinic visits and metabolic improvement all came with the drug."),
                  nonspecific=("Possible", "Nausea after each dose (case 3) and post-meal lethargy (case 1)."),
                  expectancy=("Unlikely", "Tirzepatide was for diabetes, and no one framed it as an alcohol treatment."),
                  reporting=("Possible", "Self-reported intake; no AUDIT or biomarker of drinking for case 1.")),
          verdict="Undecided",
          note="Three heavy drinkers drinking less on tirzepatide fits the GLP-1 pattern, but only one has the syndrome and every patient got a new diagnosis and clinic contact at the same time. Case 2's 'bored while drinking' is the most specific detail.",
          hyps=[H("GLP-1/GIP receptor activation reduced the reward value of alcohol.",
                  "Tirzepatide → GLP-1 (and GIP) receptor signalling in reward circuits → less dopamine response to alcohol → drinking becomes boring",
                  ["Neuropeptide (oxytocin, orexin, other)", "Dopamine"], "Fits",
                  "Case 1's craving fell within a month; case 2 found drinking boring; the other GLP-1 cases here.",
                  "Low doses; no measure of craving or reward.",
                  "Low", "Self-reported intake with no biomarker, in patients who all got new reasons to cut down.",
                  "Phosphatidylethanol or GGT tracked against dose, and craving ratings."),
                H("Gastrointestinal effects made drinking unpleasant.",
                  "Tirzepatide → nausea, slowed gastric emptying, post-meal lethargy → alcohol less pleasant → less drinking",
                  ["Interoceptive and visceral input"], "Fits",
                  "Case 3 had nausea for 3 days after each dose; case 1 had lethargy after meals.",
                  "The authors say drinking didn't fall because of lasting GI effects; case 3's nausea eased while intake stayed low.",
                  "Low", "Side effects weren't tracked against drinking.",
                  "Drinking across the weekly cycle: less on nausea days would favour this.")],
          related=[("kelly-2026", "Semaglutide ending a dopamine-agonist impulse control disorder, with rechallenge"),
                   ("meilinger-2026", "Semaglutide for obesity, drinking fell")])

b.save()
