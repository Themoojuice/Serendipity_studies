"""Full-text appraisal, batch 29 (2026-11-20, Brendan signed in to CKN).
Conference abstracts read in Embase through CKN (protocol v1.8.2: the abstract is the full publication):
richards-2022, mathew-2019, coffey-2014, boudjani-2012, auffret-2020, grunstein-2017.
Excluded: durbin-2022 (E3): the follow-up abstract says the patient sat in the hot tub on purpose, believing
dehydration would change his dopamine and help his tics; brasic-2018, the same patient, goes too (E3) now that the
reason is known.
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-20", source="Conference abstract read in Embase through CKN")

b.code("richards-2022",
       tracks=[track("Five patients, mean age 41, four women", 41, "Not stated", [
           ev("assessment", -1, "days", "Moderate or severe binge eating disorder on the Binge Eating Scale (mean 25); obesity (210–606 lb)", "approx",
              scores=[{"scale": "Binge Eating Scale (mean)", "value": 25, "higher_is_better": False}]),
           ev("exposure_start", 0, "days", "Semaglutide (mean 1.7 mg) per the clinic's obesity protocol"),
           ev("follow_up", 7, "months", "All five in remission from binge eating disorder (Binge Eating Scale down by a mean of 21); 19% weight loss; no stops for side effects", "approx", state="Remitted",
              scores=[{"scale": "Binge Eating Scale (mean)", "value": 4, "higher_is_better": False}]),
       ])],
       unexpectedness=T(era=("borderline", "GLP-1 agonists had already been tried for binge eating (liraglutide, dulaglutide)."),
                        secondary=("borderline", "Appetite suppression may stop binges without touching the disorder.")),
       attribution=A(1, 1, 0, 0, 0, "Validated Binge Eating Scale before and after; no timing of the change; charts chosen in retrospect; weight loss alongside."),
       jbi=J("YYYUUYNYNY"),
       basis="Full text", note="Conference abstract; the abstract is the full publication.")
b.reading("richards-2022",
          nulls=N(natural_history=("Unlikely", "All five remitting within months."),
                  regression=("Possible", "Treated when they presented."),
                  misdiagnosis=("Unlikely", "Validated scale."),
                  cointervention=("Possible", "A multidisciplinary obesity programme."),
                  nonspecific=("Possible", "Appetite suppression rather than a change in loss of control."),
                  expectancy=("Possible", "Open treatment in an obesity clinic."),
                  reporting=("Possible", "Five charts chosen for review; a meeting abstract.")),
          verdict="Beats the null",
          note="Five obesity-clinic patients with moderate-to-severe binge eating disorder all remitted on semaglutide, by a validated scale. An early marker of the GLP-1 story; appetite versus loss of control is the open question.",
          hyps=[H("GLP-1 agonism damped food reward and craving in mesolimbic circuits, beyond satiety.",
                  "Semaglutide → GLP-1 receptors in hypothalamus, VTA and accumbens → lower food-cue reward and craving → binges stop",
                  ["Neuropeptide (oxytocin, orexin, other)", "Dopamine"], "Can't judge",
                  "All five remitted; GLP-1 receptors sit in reward areas.", "Timing unknown; weight loss confounds.",
                  "Moderate", "Abstract only; selected charts.", "Randomised semaglutide trials in binge eating disorder.")],
          related=[("richards-2024", "The same clinic's fuller report"), ("gong-2024", "Semaglutide and binge eating"),
                   ("jarvinen-2019", "Liraglutide and binge eating")])

b.code("mathew-2019",
       tracks=[track("44-year-old man", 44, "M", [
           ev("onset", -31, "years", "Smoking from 13, 1–2 packs a day for most of his life", "approx"),
           ev("exposure_start", 0, "days", "Erenumab 70 mg for refractory migraine (October 2018); marked nausea, which smoking turned into vomiting"),
           ev("first_change", 1, "days", "Stopped smoking (last cigarette before the first dose)", "at most", state="Remitted"),
           ev("exposure_stop", 2, "months", "Erenumab stopped after two doses"),
           ev("follow_up", 7, "months", "Still not smoking; even second-hand smoke disgusts him", "approx", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 1, 0, 1, "Thirty years of heavy smoking; stopped with the first dose because smoking made the nausea unbearable; stayed abstinent after the drug was stopped; no other cessation aid; a meeting abstract."),
       jbi=J("YYYAYYYY"),
       basis="Full text", note="Conference abstract; the abstract is the full publication.")
b.reading("mathew-2019",
          nulls=N(natural_history=("Unlikely", "Thirty years of heavy smoking."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Unlikely", "Clear dependence."),
                  cointervention=("Unlikely", "No cessation treatment."),
                  nonspecific=("Unlikely", "Nausea was specific to smoking."),
                  expectancy=("Unlikely", "None."),
                  reporting=("Possible", "Self-report; a meeting abstract.")),
          verdict="Beats the null",
          note="Erenumab made smoking nauseating, and the disgust outlasted the drug: an accidental aversion therapy that stuck. Unusual for an aversion to last once the pairing stops, which is the interesting part.",
          hyps=[H("Drug-induced nausea paired with smoking conditioned a lasting disgust, as in aversion therapy.",
                  "Erenumab nausea → smoking provokes vomiting → conditioned aversion to smoke → disgust persists after the drug",
                  ["Extinction and exposure", "Interoceptive and visceral input"], "Fits",
                  "Disgust at even second-hand smoke after the drug stopped.", "Aversions usually extinguish.",
                  "Moderate", "One case, self-report.", "Smoking status in erenumab-treated smokers who had nausea."),
                H("CGRP blockade altered nicotine's interoceptive effects directly.",
                  "CGRP receptor antibody → altered vagal and brainstem signalling → smoking provokes nausea",
                  ["Neuropeptide (oxytocin, orexin, other)"], "Can't judge", "Authors unsure whether nicotine or other smoke constituents were the trigger.",
                  "No mechanism data.", "Low", "Speculative.", "Nicotine challenge on and off CGRP antagonists.")])

b.code("coffey-2014",
       tracks=[track("16-year-old boy", 16, "M", [
           ev("onset", -9, "years", "Combined-type ADHD diagnosed in second grade, supported by school neuropsychology; stimulant-responsive into adolescence", "approx"),
           ev("treatment_failed", -1, "years", "Major depression unresponsive to fluoxetine, venlafaxine and CBT; left school, drug misuse, suicide attempt", "approx", to=0),
           ev("exposure_start", 0, "days", "Index course of bifrontal brief-pulse ECT for depression, all medication stopped beforehand; then maintenance ECT"),
           ev("first_change", 1, "months", "Depression remitted; no ADHD symptoms recurred off stimulants", "approx", state="Remitted"),
           ev("assessment", 18, "months", "His psychiatrist judged he no longer met ADHD criteria; back at school, graduated, entered college", state="Remitted"),
           ev("follow_up", 2, "years", "Remission sustained on maintenance ECT", state="Remitted"),
       ])],
       unexpectedness=T(base_rate=("borderline", "ADHD symptoms fall below threshold by late adolescence in a sizeable minority.")),
       attribution=A(1, 0, 1, 0, 0, "Childhood ADHD documented and stimulant-treated; no symptoms after the ECT course off stimulants, and criteria unmet at 18 months; no rating scale; maintenance ECT and recovery from depression alongside."),
       jbi=J("YYYYYYYY"),
       basis="Full text", note="Conference abstract; the abstract is the full publication.")
b.reading("coffey-2014",
          nulls=N(natural_history=("Possible", "ADHD often fades below threshold in late adolescence."),
                  regression=("Unlikely", "Lifelong condition."),
                  misdiagnosis=("Possible", "Some 'ADHD' may have been mood-driven inattention."),
                  cointervention=("Possible", "Recovery from depression and maintenance ECT."),
                  nonspecific=("Unlikely", "He went on to college."),
                  expectancy=("Unlikely", "None."),
                  reporting=("Possible", "No scales; a meeting abstract.")),
          verdict="Undecided",
          note="Childhood ADHD did not return after ECT for adolescent depression, with criteria unmet 18 months on. ECT's broad network effects make it plausible, but maturation and the lifting of depression are just as plausible at 16.",
          hyps=[H("ECT-driven plasticity reorganised fronto-striatal attention networks.",
                  "Repeated seizures → BDNF and synaptic remodelling → altered prefrontal-striatal network → attention normalises",
                  ["Network reset (seizure, coma, anaesthesia)", "Neuroplasticity"], "Fits", "Immediate and lasting off stimulants.",
                  "Maturation confounds.", "Low", "No ratings.", "Attention measures before and after ECT in adolescents with ADHD.")])

b.code("boudjani-2012",
       tracks=[track("45-year-old man", 45, "M", [
           ev("onset", -21, "years", "Cocaine up to 7 g a day, intravenous or smoked, from 24 (drugs and smoking from 9); antisocial traits", "approx"),
           ev("treatment_failed", -1, "months", "Behavioural abstinence programme: continuous intense daily urges and headaches", to=0),
           ev("assessment", -1, "days", "DAST-10 9 for the preceding year", scores=[{"scale": "DAST-10", "value": 9, "higher_is_better": False}]),
           ev("exposure_start", 0, "days", "Acute infarct of the left dorsolateral striatum (carotid dissection, mitral vegetations): hemiparesis, gone within days"),
           ev("first_change", 1, "days", "No further cocaine craving from the stroke on", "at most", state="Remitted"),
           ev("follow_up", 14, "months", "Abstinent apart from 5 days of social use without craving; unannounced urine screens negative; DAST-10 0; antisocial traits unchanged", state="Remitted",
              scores=[{"scale": "DAST-10", "value": 0, "higher_is_better": False}]),
       ])],
       unexpectedness=T(),
       attribution=A(1, 1, 1, 0, 0, "Heavy use for two decades and intense craving the month before; craving gone from the stroke; DAST-10 9 to 0 and negative unannounced screens over 14 months; but he had just started an abstinence programme."),
       jbi=J("YYYYYYYY"),
       lesion={"kind": "Lesion", "side": "Left", "regions": ["Putamen"],
               "specific": "Acute infarct of the left dorsolateral striatum on MRI",
               "aetiology": "Ischaemic stroke", "imaging": "MRI", "mappable": "Description only"},
       basis="Full text", note="Conference abstract; the abstract is the full publication.")
b.reading("boudjani-2012",
          nulls=N(natural_history=("Unlikely", "Two decades of heavy use, intense craving the month before."),
                  regression=("Possible", "In treatment at the peak of craving."),
                  misdiagnosis=("Unlikely", "Severe cocaine dependence."),
                  cointervention=("Possible", "An abstinence programme began a month earlier."),
                  nonspecific=("Unlikely", "Antisocial behaviour unchanged; he still went out with friends."),
                  expectancy=("Possible", "A frightening stroke."),
                  reporting=("Unlikely", "Unannounced urine screens.")),
          verdict="Beats the null",
          note="Craving vanished after a left dorsolateral striatal infarct in a man using up to 7 g of cocaine a day, confirmed by unannounced urine screens over 14 months; when he used socially he felt no craving. The dorsolateral striatum is the habit node in addiction models.",
          hyps=[H("The lesion cut the dorsolateral striatal habit circuit that carries compulsive drug seeking.",
                  "Left dorsolateral striatum infarct → loss of habitual, cue-driven cocaine seeking → craving gone; goal-directed use (social) still possible without craving",
                  ["Lesion disconnection", "Dopamine"], "Fits",
                  "Immediate; social use without craving fits a habit-system lesion.", "Abstinence programme overlapped.",
                  "Moderate", "Abstract only.", "Craving outcomes after dorsal striatal strokes (Muskens 2012 series).")],
          related=[("muskens-2012", "Dorsal striatal damage easing addictions"), ("valadez-cuen-2024", "Caudate infarct ending smoking and soda craving")])

b.code("auffret-2020",
       tracks=[track("52-year-old woman with Parkinson's disease", 52, "F", [
           ev("onset", -33, "years", "Smoking from 19, about 20 a day; nicotine replacement attempts at 30 and 38 failed; smoked more after her Parkinson's diagnosis", "approx"),
           ev("assessment", -1, "days", "Fagerström 8", scores=[{"scale": "Fagerström", "value": 8, "higher_is_better": False}]),
           ev("exposure_start", 0, "days", "A quit attempt with an app, for money reasons, while on continuous subcutaneous apomorphine (3–3.5 mg/h, started in 2015)"),
           ev("first_change", 1, "days", "Stopped overnight without withdrawal; the smell of cigarettes became disgusting", state="Remitted"),
           ev("follow_up", 30, "days", "Abstinent apart from one cigarette, smoked without pleasure or craving", state="Remitted"),
       ])],
       unexpectedness=T(target=("borderline", "She was trying to stop; the surprise was how easy it was."),
                        era=("borderline", "Apomorphine and smoking cessation had earlier reports, including from this group."),
                        base_rate=("borderline", "Some quit attempts succeed; 30 days is short.")),
       attribution=A(1, 0, 0, 0, 0, "Fagerström 8 and failed attempts before; time from starting apomorphine to quitting not given; a motivated quit attempt with an app; 30-day follow-up."),
       jbi=J("YYYAYYUY"),
       basis="Full text", note="Conference abstract; the abstract is the full publication.")
b.reading("auffret-2020",
          nulls=N(natural_history=("Possible", "Motivated quit attempts sometimes succeed."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Unlikely", "Heavy dependence."),
                  cointervention=("Possible", "A cessation app and a financial motive."),
                  nonspecific=("Unlikely", "None."),
                  expectancy=("Possible", "She wanted to stop."),
                  reporting=("Likely", "Thirty days' follow-up in a meeting abstract.")),
          verdict="Doesn't beat the null",
          note="An effortless quit, with new disgust for smoke, in a heavily dependent woman on an apomorphine pump. Interesting beside the dopamine-agonist literature, but it was a deliberate attempt with 30 days of follow-up.",
          hyps=[H("Continuous dopamine-receptor stimulation replaced the dopamine signal nicotine supplied, so withdrawal and craving never arrived.",
                  "Apomorphine (D1/D2 agonist) → tonic dopaminergic tone in reward circuits → no withdrawal dip → cigarettes unrewarding",
                  ["Dopamine"], "Can't judge", "No withdrawal; disgust at smoke.", "Latency from pump start unknown.",
                  "Low", "Thirty days.", "Smoking outcomes in apomorphine-pump cohorts.")])

b.code("grunstein-2017",
       tracks=[track("65-year-old man, electrician", 65, "M", [
           ev("onset", -22, "months", "Schizophrenia-like illness from about November 2013: believes he is Michael Jackson, hallucinations, disorganised thought, flat affect, stopped working; never took antipsychotics", "approx"),
           ev("assessment", -14, "months", "Referred for snoring and sleepiness (July 2014): 54 obstructive apnoeas an hour, lowest SpO2 75%, BMI 40", "approx"),
           ev("exposure_start", 0, "days", "CPAP (September 2015), 100% adherence, about 6 hours a night"),
           ev("first_change", 3, "months", "Back at work", "approx", state="Partial"),
           ev("follow_up", 7, "months", "No features of schizophrenia (April 2016), still never medicated", state="Remitted"),
       ])],
       unexpectedness=T(secondary=("borderline", "If intermittent hypoxia caused the psychosis, CPAP treated its cause (protocol v1.7.2: tier C with a secondary caveat).")),
       attribution=A(1, 0, 1, 0, 1, "Nearly two years of untreated psychosis before; back at work three months into CPAP and free of symptoms at seven; no antipsychotics ever; no scales."),
       jbi=J("YYYYYYAY"),
       basis="Full text", note="Conference abstract; the abstract is the full publication.")
b.reading("grunstein-2017",
          nulls=N(natural_history=("Possible", "Late-onset psychoses can remit, though rarely after two years untreated."),
                  regression=("Unlikely", "Chronic course."),
                  misdiagnosis=("Possible", "A hypoxic or organic psychosis at 65 rather than schizophrenia."),
                  cointervention=("Unlikely", "No psychiatric treatment."),
                  nonspecific=("Unlikely", "Back at work."),
                  expectancy=("Unlikely", "He denied being ill."),
                  reporting=("Possible", "No scales; a meeting abstract.")),
          verdict="Beats the null",
          note="Nearly two years of never-treated psychosis cleared within months of CPAP for severe sleep apnoea, with no drug to confound it. The likeliest reading is a psychosis driven by intermittent hypoxia, which makes it a secondary syndrome treated at its cause rather than schizophrenia cured.",
          hyps=[H("Repetitive nocturnal hypoxia disturbed striatal dopamine and glutamate signalling; CPAP removed it.",
                  "Severe OSA → repetitive intermittent hypoxaemia and sleep fragmentation → dopamine/glutamate dysregulation → psychosis; CPAP → normal oxygenation and sleep → remission",
                  ["Respiratory and blood gases", "Sleep and circadian rhythm"], "Fits",
                  "Remission over months on CPAP with no other treatment.", "Late onset suggests an organic cause.",
                  "Moderate", "One case, no scales.", "Screen first-episode psychosis for OSA and test CPAP.")],
          related=[("taylor-1978", "Schizophrenia clearing after an unrelated physiological insult")])

b.exclude("durbin-2022", "E3",
          "Embase conference abstract read: the patient entered the hot bath deliberately, believing dehydration would favourably alter his dopamine metabolism; a self-treatment aimed at the tics.")
b.exclude("brasic-2018", "E3",
          "Same patient as durbin-2022, whose follow-up abstract gives the reason the 2018 report lacked: he dehydrated himself on purpose to treat his tics.")

b.save()
