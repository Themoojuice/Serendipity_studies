"""Full-text appraisal, batch 33 (2026-11-22, night): roadmap step 1b, CKN session continued.

Found tonight: the EBSCO Full Text Finder shows 'EBSCOhost SmartLinks 1981 - present' for the International Journal of
Eating Disorders and 1998-2011 for the Australian & New Zealand Journal of Psychiatry, so those Wiley papers open in the
EBSCO viewer even though Wiley's own site blocks Claude's browser. The resolver also accepts a PMID (pmid=...) where a
record has no DOI. Scanned back-issue PDFs (Ho 2001, Ozawa 1999) were rendered page by page with the viewer's pdf.js and
read with tesseract.

  ho-2001            coded (Int J Eat Disord, scanned)
  schweickert-1997   coded (Int J Eat Disord)
  ozawa-1999         coded (Int J Eat Disord, scanned)
  solmi-2013         coded (Int J Eat Disord)
  coutinho-2016      coded (Neurocase, EBSCO by PMID); DOI added
  mclaughlin-2013    coded (Biol Psychiatry, ClinicalKey); DOI added
  arora-2006         excluded E1: an acute manic episode that had responded to ECT, then worsened over about two weeks
                     on carbamazepine and olanzapine (lithium for two days); neither chronic nor through two adequate trials.
  yates-1988         excluded E3: the women sought cosmetic surgery to fix the body dissatisfaction at the core of their
                     eating disorder, and the authors present the short remissions (one and three months) as the expected
                     psychological effect of looking better; chronicity isn't documented either.
Run from the repo root:  python3 scripts/batches/b2026_11_22_appraisal_b33.py
"""
import sys
from urllib.parse import quote

sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-22", source="Full text through CKN (EBSCO, ClinicalKey)")


def add_doi(cid, doi):
    r = b.by_id[cid]
    assert not r["ids"]["doi"], cid
    r["ids"]["doi"] = doi
    r["links"]["doi"] = "https://doi.org/" + doi
    r["links"]["ckn"] = "https://go.openathens.net/redirector/ckn.qldhealth.com?url=" + quote("https://doi.org/" + doi, safe="")


W = lambda v: [{"scale": "Weight (kg)", "value": v}]  # noqa: E731
BMI = lambda v: [{"scale": "BMI", "value": v}]  # noqa: E731

# ---------------------------------------------------------------- Ho & Birmingham 2001
b.code("ho-2001",
       tracks=[track("25-year-old woman", 25, "F", [
           ev("onset", -12, "years", "Anorexia nervosa, binge-eating/purging subtype, with multiple earlier admissions for renourishment", "approx"),
           ev("assessment", -1, "weeks", "Admitted after an outpatient check found extremely low weight and body fat (37.8 kg; body fat 7.5% by skinfold); a year of daily chest pain, abnormal ECG, no cardiac disease found", "approx", scores=W(37.8)),
           ev("exposure_start", 0, "days", "Shortly after admission: sudden fever, headache, photophobia and rash, aspiration pneumonia, rapid neurological decline; intubated in intensive care; three tonic-clonic seizures. CT: diffuse cerebral swelling and pallidal calcification consistent with anoxic injury; CSF pleocytosis with raised protein; MRI later: atrophy and bilateral temporal white matter changes (likely gliosis), consistent with encephalitis", "approx"),
           ev("first_change", 6, "months", "On the rehabilitation ward (date not given, within the six months), after nasogastric feeding, she began eating a full normal diet, which she had not done for many years; the whole team saw it consistently, and it did not seem to perturb her. Residual nonfluent aphasia, paraphasias and jargon, polyneuropathy and an abnormal gait", "at most"),
           ev("best_response", 6, "months", "Weight 51.1 kg, body fat 18.5%, gained steadily over six months", "approx", state="Remitted", scores=W(51.1)),
           ev("exposure_stop", 6, "months", "Neurological sequelae resolved and rehabilitation completed", "at least"),
           ev("relapse", 6, "months", "Began restricting again and returned to her premorbid anorexic behaviour; weight and body fat fell back to premorbid levels", "at least"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 1, 2, 0, "Twelve years of anorexia with repeated renourishment admissions; eating normally without distress during rehabilitation after the encephalitis, weight 37.8 to 51.1 kg; anorexic behaviour back once the neurological deficits cleared (natural off-on). Weight and skinfold only, no eating-disorder scale. Supervised inpatient rehabilitation and nasogastric feeding not addressed."),
       jbi=J("YYYYYYYY"),
       fix={"summary": "A 25-year-old woman with 12 years of binge-purge anorexia ate a full normal diet without distress while recovering from encephalitis with hypoxic brain injury, going from 37.8 to 51.1 kg over six months; once the neurological deficits cleared, the restriction came back and the weight went with it.",
            "caveat": "Her aphasia and cognitive slowing could have removed the preoccupation along with much else, since the restriction returned exactly as cognition did.",
            "syndrome.chronic": True,
            "syndrome.specific": "Anorexia nervosa, binge-eating/purging subtype, for 12 years with repeated renourishment admissions (37.8 kg, body fat 7.5%)"},
       note="Three-page report, scanned back issue read by OCR. Brain findings (no lesion block, since the trigger is an infection): diffuse swelling and pallidal calcification on CT, atrophy and bilateral temporal white matter changes on MRI.")
b.reading("ho-2001",
          nulls=N(natural_history=("Unlikely", "Twelve years and many admissions; the remission ended as the brain recovered."),
                  regression=("Unlikely", "Chronic, and the return is the opposite of regression."),
                  misdiagnosis=("Unlikely", "Long-standing binge-purge anorexia; nothing suggests the eating disorder was secondary."),
                  cointervention=("Possible", "Six months of supervised inpatient rehabilitation with nasogastric feeding at first; the relapse came when rehabilitation ended."),
                  nonspecific=("Likely", "Nonfluent aphasia, jargon and cognitive slowing, and eating 'did not seem to perturb her': loss of the cognitive apparatus would remove the preoccupation with weight, and the anorexia returned exactly as cognition recovered."),
                  expectancy=("Unlikely", "An illness, not a treatment."),
                  reporting=("Possible", "Brief report; the first change is not dated, and the relapse is described without weights or times.")),
          verdict="Doesn't beat the null",
          note="The return of the anorexia as the brain recovered makes the brain injury the cause rather than chance, but what it shows is that the illness needs intact cognition, not that something specific was switched off: the aphasia and slowing explain the change without an anorexia-specific mechanism. Formal cognitive testing alongside the eating would have decided it.",
          hyps=[H("Diffuse hypoxic-encephalitic injury removed the cognitive and affective machinery that sustains restriction; recovery restored it.",
                  "Encephalitis and hypoxia → widespread cortical and white matter dysfunction (aphasia, slowing) → loss of weight-and-shape rumination and of the anxiety attached to eating → eats normally without distress → cognition recovers → restriction returns",
                  ["Global suppression (sedation, apathy, cognitive loss)"], "Fits", "Indifference to eating while impaired; relapse timed to neurological recovery.",
                  "She was not apathetic about everything that is reported; no cognitive measures were taken.",
                  "Moderate", "No cognitive or mood testing over the six months.",
                  "Serial cognitive testing and eating-disorder ratings through recovery from a comparable diffuse injury."),
                H("Bilateral temporal damage released feeding drive (a partial Klüver-Bucy picture) that overrode restriction.",
                  "Bilateral temporal white matter injury → disinhibited, hyperphagic feeding → weight gain → temporal function recovers → restriction re-emerges",
                  ["Lesion disconnection"], "Fits", "The authors draw the parallel with hyperphagia after temporal encephalitis.",
                  "No hyperphagia, orality or other Klüver-Bucy signs are described; she ate a normal diet, not excess.",
                  "Low", "Lesion described only as temporal white matter change.",
                  "Detailed lesion mapping and feeding observation in post-encephalitic eating changes.")],
          related=[("dusoir-2005", "Anorexia remitting after a stroke"), ("israel-2010", "Anorexia remitting after subgenual stimulation for depression")])

# ---------------------------------------------------------------- Schweickert, Strober & Moskowitz 1997
b.code("schweickert-1997",
       tracks=[track("25-year-old woman", 25, "F", [
           ev("onset", -12, "years", "Binge eating from 13, after her parents' divorce, ended by self-induced vomiting; up to five binge-purge episodes a day at worst. Previous treatment nonspecific, with limited results", "approx"),
           ev("assessment", 0, "days", "Presented to an outpatient psychopharmacology clinic for ADHD (diagnosed at 7; stimulants stopped at 12). Bingeing at least three to five times a week, more with coursework demands; 115 lb at 5 ft 3 in; crying spells, hopelessness"),
           ev("exposure_start", 0, "days", "Methylphenidate 5 mg morning and noon for ADHD"),
           ev("first_change", 1, "weeks", "ADHD much improved; dose raised to 5 mg three times a day. Appetite unchanged, but a complete stop to her binges, which she put down to better concentration and less restlessness", "approx", state="Remitted"),
           ev("assessment", 5, "weeks", "No bingeing; weight stable", state="Remitted"),
           ev("assessment", 9, "weeks", "No bingeing; weight stable", state="Remitted"),
           ev("follow_up", 16, "weeks", "Still not bingeing, weight stable: her longest abstinence since 13", state="Remitted"),
       ])],
       unexpectedness=T(era=("borderline", "The authors cite small placebo-controlled reports of methylamphetamine and fenfluramine reducing bingeing in bulimia (Ong 1983, Robinson 1985)."),
                        secondary=("borderline", "The authors' other reading: her bingeing was an expression of ADHD impulsivity, so treating the ADHD treated its consequence.")),
       attribution=A(1, 0, 1, 0, 0, "Twelve years of binge-purging with limited response to earlier treatment; bingeing stopped within about a week of methylphenidate and stayed stopped for 16 weeks. Self-reported binge counts only, no scale; no stop or rechallenge; nothing said about other changes."),
       jbi=J("YYYUYYNY"),
       fix={"summary": "A 25-year-old woman who had binged and vomited since 13 stopped bingeing completely within about a week of starting low-dose methylphenidate for her ADHD, with her appetite unchanged; 16 weeks later it was her longest abstinence since the bulimia began.",
            "caveat": "Methylphenidate has anorectic effects, so fewer binges could reflect appetite and impulse dampening rather than a change in the bulimia itself.",
            "outcome.resolution": "Complete",
            "syndrome.chronic": True,
            "syndrome.specific": "Bulimia nervosa for 12 years (binge-purge, up to five times a day at worst) with comorbid ADHD"},
       note="Three-page case report.")
b.reading("schweickert-1997",
          nulls=N(natural_history=("Unlikely", "Twelve years, longest abstinence ever."),
                  regression=("Possible", "She presented at a time of high coursework demand, when bingeing rose; a quieter period would bring it down."),
                  misdiagnosis=("Unlikely", "Classic binge-purge bulimia."),
                  cointervention=("Possible", "Nothing else is said to have changed, but nothing is said to have stayed the same either."),
                  nonspecific=("Possible", "A stimulant's anorectic effect could curb bingeing without touching the disorder, though she reported her appetite unchanged."),
                  expectancy=("Possible", "Open, self-reported, in a clinic that had just helped her ADHD."),
                  reporting=("Possible", "Self-report only, no diary or scale, 16 weeks.")),
          verdict="Undecided",
          note="The founding report of the stimulant-bulimia line: quick, complete and sustained for four months, with appetite reported unchanged. Self-report and a known anorectic drug class leave it short of separating a specific effect on bingeing from appetite or impulse dampening; a stop and restart would have settled it.",
          hyps=[H("Better prefrontal control of impulses removed the binge trigger.",
                  "Methylphenidate → more dopamine and noradrenaline in prefrontal-striatal circuits → better inhibitory control and less restlessness → urges to binge resisted → binge-purge cycle stops",
                  ["Dopamine", "Noradrenaline"], "Fits", "Within a week, alongside the ADHD response; she attributed it to better concentration.",
                  "Bulimia usually has drivers beyond impulsivity (shape concern), and these are not reported.",
                  "Low", "Single self-reported case with no measures.",
                  "Binge diaries across a blinded methylphenidate on/off crossover in bulimia with ADHD."),
                H("Stimulant appetite suppression reduced bingeing without changing the disorder.",
                  "Methylphenidate → reduced hunger and reward value of food → fewer binges",
                  ["Dopamine"], "Fits", "Stimulants are anorectic; lisdexamfetamine later became a binge-eating treatment (recalled, not checked).",
                  "She reported her appetite unchanged at that dose (5 mg three times a day).",
                  "Low", "No appetite or intake measure.", "Measure hunger and intake alongside binge frequency.")],
          related=[("dukarm-2005", "Six women with bulimia abstinent on dextroamphetamine for ADHD"), ("miyazaki-2023", "Methylphenidate for ADHD easing kleptomania")])

# ---------------------------------------------------------------- Ozawa, Koyano & Akama 1999
b.code("ozawa-1999",
       tracks=[track("29-year-old woman", 29, "F", [
           ev("onset", -13, "years", "Bulimic episodes from 16 after repeated diets; vomiting after large meals from 19; daily binge-vomiting by 21–22, then more often; almost uncontrollable craving and guilt", "approx"),
           ev("treatment_failed", -5, "years", "Regular psychotherapy for a year at a hospital psychology department; bingeing and vomiting continued", "approx", to=-4),
           ev("treatment_failed", -1, "years", "Regular psychiatric treatment again, without effect", "approx"),
           ev("assessment", -1, "weeks", "Asked for admission to escape her distress: binges two to three times a day on weekdays, three to five at weekends; very depressed, wished to die; 41 kg, 155.5 cm; DSM-IV bulimia nervosa, purging type. Calcium 11.8 mg/dl, phosphate low, intact PTH 95 pg/ml: primary hyperparathyroidism; adenoma behind the right thyroid lobe on ultrasound and MIBI scan", "approx"),
           ev("exposure_start", 0, "days", "Removal of a 320 mg right parathyroid adenoma; serum calcium normalised"),
           ev("first_change", 1, "weeks", "Eating became normal after surgery without any psychiatric treatment; depression and anxiety gone 'just after' the operation", "at most", state="Remitted"),
           ev("follow_up", 2, "years", "No bingeing or vomiting since the operation; much better mentally; still fears being overweight", state="Remitted"),
       ])],
       unexpectedness=T(secondary=("borderline", "Hypercalcaemia causes nausea, vomiting, low mood and anxiety, and the authors suggest the hyperparathyroidism influenced the bulimia; its duration is unknown because calcium had never been checked.")),
       attribution=A(1, 0, 1, 0, 0, "Thirteen years of bulimia through a year of psychotherapy and later psychiatric treatment; binge-vomiting stopped after parathyroidectomy and stayed gone for two years. No scale; no reversal; the authors raise a placebo effect of surgery but cannot exclude it."),
       jbi=J("YYYYYYUY"),
       fix={"summary": "A 29-year-old woman with 13 years of bulimia, unhelped by psychotherapy and psychiatric care, had a parathyroid adenoma removed for hyperparathyroidism found on admission; she never binged or vomited again over two years, and her depression and anxiety went too.",
            "syndrome.specific": "Bulimia nervosa, purging type, for 13 years (two to five binges a day), unhelped by psychotherapy and psychiatric treatment"},
       note="Four-page report, scanned back issue read by OCR.")
b.reading("ozawa-1999",
          nulls=N(natural_history=("Unlikely", "Thirteen years, daily bingeing; abrupt stop."),
                  regression=("Possible", "She asked for admission at her worst, wishing to die."),
                  misdiagnosis=("Possible", "Hypercalcaemia's nausea, vomiting and dysphoria may have fed the purging and distress; how long the calcium had been high is unknown."),
                  cointervention=("Possible", "Admission and an operation interrupt routines; the authors raise a surgical placebo effect."),
                  nonspecific=("Unlikely", "She improved in mood and energy, not the reverse."),
                  expectancy=("Possible", "A dramatic intervention in a woman desperate for help; the authors name it."),
                  reporting=("Possible", "Self-report, no scale or diary.")),
          verdict="Undecided",
          note="Thirteen years of bulimia gone for two years after a parathyroid adenoma came out. Whether the hyperparathyroidism was driving part of the picture (hypercalcaemic nausea, vomiting and dysphoria) can't be told from the report, which is what keeps this a secondary-cause question rather than a cure of primary bulimia.",
          hyps=[H("Hypercalcaemia was sustaining the binge-purge cycle through its effects on mood and gut.",
                  "Parathyroid adenoma → chronic hypercalcaemia → nausea, dysphoria, anxiety and neuronal excitability changes (calcium-sensing receptor) → amplified craving-purge cycle → calcium normalised → cycle stops",
                  ["Ion channels and excitability", "Interoceptive and visceral input"], "Fits", "Abrupt after surgery; mood and anxiety cleared at the same time.",
                  "The bulimia began at 16 with dieting, and calcium history is unknown, so the hyperparathyroidism may be much younger than the illness.",
                  "Low", "Onset of the hypercalcaemia unknown.",
                  "Screen calcium in bulimia cohorts and follow those with hyperparathyroidism through surgery."),
                H("The admission and operation acted as a psychological turning point.",
                  "Desperate admission → major operation and a medical explanation → hope and reattribution → stops bingeing",
                  ["Suggestion and belief update"], "Fits", "Immediate change.", "Thirteen years of failed psychological treatment; two years sustained.",
                  "Low", "No measures of mood or expectation.", "None from one case.")],
          related=[("achamrah-2020", "Anorexia remitting after a medical procedure")])

# ---------------------------------------------------------------- Solmi et al. 2013
b.code("solmi-2013",
       tracks=[track("26-year-old woman", 26, "F", [
           ev("onset", -12, "years", "Anorexia nervosa from 14 after a failed ballet audition: binge-purge type for six months, then restrictive; dropped out of psychodynamic therapy at 15 after four sessions and refused all other treatment for over 10 years; BMI 14.6–15.8", "approx"),
           ev("cointervention", -1, "months", "Admitted for acute Crohn's disease: weight 37 to 30 kg (BMI 11.8), transfusion, parenteral and enteral nutrition, prednisone and ciclosporin; discharged on day 25 at 37.2 kg (BMI 14.7). Accepted a dietary programme and regular eating-disorder and gastroenterology visits: her first sustained psychiatric care (a session every two to three weeks, psychoeducation)", "approx"),
           ev("exposure_start", 0, "days", "Infliximab at standard dose for Crohn's disease (interval later shortened from eight to six weeks for a perianal fistula)", "approx"),
           ev("first_change", 3, "months", "Within a few months of discharge: growing motivation to follow psychoeducation, better eating, gradual weight gain; shape and weight concerns persisted at first", "approx", state="Partial"),
           ev("cointervention", 6, "months", "Switched to adalimumab after an allergic reaction to infliximab", "approx"),
           ev("best_response", 9, "months", "Menses back; BMI 17.6, the first time above her illness range since onset; weight and shape concerns gradually easing", "approx", state="Partial", scores=BMI(17.6)),
           ev("follow_up", 9, "months", "Living alone; three mild Crohn's flares but no relapse of the eating disorder; better psychosocial functioning", "at least", state="Partial"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 0, 0, 0, "Twelve years of anorexia at BMI 14.6–15.8; gradual improvement over months to BMI 17.6. Timing scored 0: the change was gradual and began alongside her first-ever sustained eating-disorder care after a near-fatal admission. BMI only; no reversal; confounders not separable."),
       jbi=J("YYYYYYYY"),
       fix={"summary": "A 26-year-old woman with 12 years of untreated anorexia began anti-TNF therapy for Crohn's disease after a near-fatal admission and, over the following months, gained weight for the first time since her teens (BMI 17.6, menses back) while attending eating-disorder care for the first time.",
            "caveat": "The improvement began alongside her first ever sustained eating-disorder treatment, after an admission at BMI 11.8, so ordinary treatment response is the obvious alternative."},
       note="Three-page clinical case report.")
b.reading("solmi-2013",
          nulls=N(natural_history=("Possible", "Some chronic anorexia improves in the late twenties; the change was gradual."),
                  regression=("Possible", "She started from a Crohn's-driven nadir (BMI 11.8)."),
                  misdiagnosis=("Unlikely", "Anorexia began a decade before Crohn's disease."),
                  cointervention=("Likely", "Her first sustained eating-disorder care, a dietary programme and a frightening admission all began at the same time as the anti-TNF drug."),
                  nonspecific=("Unlikely", "Functioning improved."),
                  expectancy=("Possible", "Newly engaged in treatment."),
                  reporting=("Possible", "BMI only, no eating-disorder scale; follow-up not dated.")),
          verdict="Doesn't beat the null",
          note="A real and welcome recovery, but it began alongside her first ever eating-disorder treatment after a near-fatal admission, and it was gradual; nothing in the report separates the anti-TNF drug from ordinary treatment response.",
          hyps=[H("Lower TNF-alpha and IL-6 relieved cytokine-driven anorexigenic signalling.",
                  "Anti-TNF therapy → less systemic inflammation → less hypothalamic anorexigenic signalling and leptin sensitisation → hunger and intake recover → weight and cognitions follow",
                  ["Inflammation and cytokines", "Neuropeptide (oxytocin, orexin, other)"], "Can't judge", "Plausible biology in inflammatory anorexia.",
                  "Her anorexia predated Crohn's disease by ten years, and the change was gradual.",
                  "Low", "No inflammatory markers tracked against symptoms.",
                  "Inflammatory markers and eating-disorder ratings in anorexia with and without biologic therapy for comorbid inflammatory disease.")],
          related=[("ho-2001", "Anorexia remitting during encephalitis")])

# ---------------------------------------------------------------- Coutinho et al. 2016
add_doi("coutinho-2016", "10.1080/13554794.2016.1194999")
b.code("coutinho-2016",
       tracks=[track("45-year-old woman", 45, "F", [
           ev("onset", -40, "years", "Lifelong: stubborn, inflexible, low frustration tolerance; lost verbal and physical control over trivial annoyances, breaking furniture and throwing objects; highly emotional, unplanned episodes", "approx"),
           ev("exposure_start", 0, "days", "October 2012: struck from behind with a 1.1 m wooden fence post while jogging; right epidural and left temporal subdural haematomas, decompressive craniotomy, induced coma for a few days"),
           ev("first_change", 3, "months", "First assessment (January 2013): episodes of dyscontrol gone; flexible, affectionate, apologised to her husband 'for the first time in her life'; memory complaints, dysarthria, high-pitched voice, unsteady gait", "at most", state="Remitted"),
           ev("assessment", 12, "months", "Cognition, balance and gait back to premorbid levels; Iowa Scales of Personality Change rated by her husband (premorbid versus now): aggressiveness down moderately, the new traits stable; not manic", state="Remitted"),
           ev("follow_up", 35, "months", "September 2015: Iowa ratings unchanged; no outbursts; more active at church than ever; MRI unchanged at 3, 12 and 36 months", state="Remitted"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 1, 1, 0, 0, "Lifelong outbursts by her husband's account; gone from the first assessment after the injury and still gone at nearly three years, with the Iowa scales rated twice against a retrospective premorbid rating. No reversal possible; the near-fatal assault and the religious community's response as psychological causes are not discussed."),
       jbi=J("YYYYYYYY"),
       lesion={"kind": "Injury", "side": "Bilateral", "regions": ["Temporal, lateral", "White matter, other"],
               "specific": "Atrophy and gliosis of the superior, middle and inferior temporal gyri on both sides (BA 22, 21, 20, 37), sparing the left temporal pole and on the right extending into the posterior temporal pole; tractography: marked thinning of the right uncinate fasciculus, less of the right inferior fronto-occipital fascicle, slight thinning of the left superior longitudinal fascicle; amygdala, hippocampus and insula spared",
               "aetiology": "Trauma", "imaging": "MRI", "mappable": "Figure"},
       fix={"summary": "A 45-year-old preacher whose lifelong rages had her breaking furniture and throwing things was struck on the head while jogging; after recovering from bilateral temporal injuries she had no further outbursts, became flexible and affectionate, and was unchanged nearly three years on.",
            "caveat": "A near-fatal assault followed by an outpouring of support from her church could reorganise a personality without any help from the lesion."},
       note="Seven-page Neurocase report with imaging and tractography figures.")
b.reading("coutinho-2016",
          nulls=N(natural_history=("Unlikely", "Lifelong, unchanged into her mid-forties."),
                  regression=("Unlikely", "A trait-like pattern, not a peak."),
                  misdiagnosis=("Possible", "Episodic dyscontrol was never formally diagnosed or treated; it is reconstructed from her husband's account of a lifelong temperament."),
                  cointervention=("Possible", "A near-fatal assault, long recovery and a church community praying for her: a life event big enough to change a person."),
                  nonspecific=("Unlikely", "She became more active and took more initiative, with cognition back to normal: not apathy."),
                  expectancy=("Unlikely", "An injury, not a treatment."),
                  reporting=("Possible", "Husband's retrospective ratings, endorsed by her; personal memoir published.")),
          verdict="Beats the null",
          note="Lifelong rages gone after bilateral lateral temporal injury that spared the amygdala, with cognition recovered and initiative up rather than down, which argues against blunting. The rival is psychological: a near-death experience and a community's embrace can change a temperament. The selective, lesion-matched change tips it.",
          hyps=[H("Bilateral lateral temporal and right uncinate damage cut the fast temporal-orbitofrontal route that turned annoyance into rage.",
                  "Lateral temporal cortex and right uncinate fasciculus injury → weaker transfer of social-affective appraisal to orbitofrontal and anterior temporal cortex → less rapid escalation from irritation to dyscontrol → outbursts stop, warmth released",
                  ["Lesion disconnection"], "Fits", "Selective change in aggression with recovered cognition; tractography shows the right uncinate thinned.",
                  "Amygdala spared, so the classic taming route is not the one damaged; a single case.",
                  "Moderate", "No premorbid imaging or behaviour measured before the injury.",
                  "Compare lesion networks of post-traumatic calming with those of post-traumatic aggression."),
                H("Surviving a near-fatal assault reorganised her priorities and self-view.",
                  "Near death → gratitude, faith testimony, community support → a new identity incompatible with rages → outbursts stop",
                  ["Meaning and life reorganisation"], "Fits", "She preached her story widely afterwards.",
                  "Lifelong temper changing so completely and stably by meaning alone is unusual.",
                  "Low", "No psychological assessment of the experience.", "None from one case.")],
          related=[("ohara-2004", "Personality change after brain injury")])

# ---------------------------------------------------------------- McLaughlin et al. 2013
add_doi("mclaughlin-2013", "10.1016/j.biopsych.2012.09.015")
b.code("mclaughlin-2013",
       tracks=[track("48-year-old woman", 48, "F", [
           ev("assessment", -1, "days", "Before implantation: intractable childhood-onset OCD (Y-BOCS 32) after extensive exposure therapy and drugs; long-standing anorexia: fear of weight gain, sees herself as overweight, avoids meat, bread and 'fattening' food, small portions, avoids eating at outings, resists clinicians. Lowest lifetime BMI 17.4; 44.4 kg (BMI 18.5) just before surgery; somewhat better during intensive OCD treatment", "approx", scores=BMI(18.5)),
           ev("exposure_start", 0, "days", "Bilateral ventral capsule/ventral striatum DBS for intractable OCD in a controlled trial, programmed for OCD; final setting left unilateral, monopolar, dorsal contact in the ventral caudate, 7.5 V, 120 µs, 120 Hz"),
           ev("first_change", 0, "days", "Early in stimulation: 'different' feelings about food, less bothered by what she ate; larger and broader portions, eats out and asks to, eats sweets she had avoided entirely", "at least", state="Partial"),
           ev("assessment", 0, "days", "Weight since surgery generally 45.4–47.2 kg (BMI 18.9–19.6); still says she has 'to be careful'", "at least", state="Partial", scores=BMI(19.6)),
           ev("assessment", 0, "days", "Adjacent ventral contact (also ventral caudate) added: anxiety, mood and OCD worse and weight down to 41.7 kg", "at least", state="Worse"),
           ev("best_response", 0, "days", "That contact switched off: symptoms better again, 1.8 kg gained in a month, notably less distressed about calories and weight", "at least", state="Partial"),
           ev("follow_up", 4, "years", "Age 52 at the report: long-term reduction in concern about food and weight gain", "approx", state="Partial"),
       ])],
       unexpectedness=T(era=("borderline", "Capsulotomy and limbic leucotomy had been reported to ease anorexia, which the authors cite, and subgenual stimulation remission of anorexia was reported in 2010."),
                        secondary=("borderline", "Her restriction overlapped with contamination and perfectionism obsessions, and the OCD improved with the same stimulation, so the eating change may be part of the OCD response.")),
       attribution=A(1, 0, 1, 0, 0, "Long-standing anorexic restriction at low-normal weight; easier eating early in stimulation and BMI 18.9–19.6 over four years. Adding a second contact worsened anxiety, mood, OCD and weight together, and removing it reversed all of them: a configuration change, not a stop of the exposure, so not scored as a reversal. Weight only; OCD and mood changes not separated."),
       jbi=J("YYYUYYYY"),
       lesion={"kind": "Stimulation target", "side": "Left", "regions": ["Caudate", "Internal capsule"],
               "specific": "Ventral capsule/ventral striatum leads, bilateral, with only the left active: dorsal contact (#3) in the ventral caudate, placed relatively ventromedially, stimulation possibly spreading into the anterior limb of the internal capsule; plotted at −5.8 mm from the commissure in the Mai atlas",
               "aetiology": "Not applicable", "imaging": "MRI and CT", "mappable": "Figure"},
       fix={"summary": "A 48-year-old woman with intractable OCD and long-standing anorexic restriction had ventral capsule/ventral striatum stimulation for the OCD; early on she stopped minding what she ate, ate sweets and meals out for the first time in years, and kept her weight in the healthy range over four years.",
            "caveat": "Her food rules overlapped with her contamination and perfectionism obsessions, and the OCD improved with the same stimulation, so the eating may simply have followed the OCD.",
            "syndrome.chronic": True,
            "syndrome.specific": "Long-standing anorexic restriction (lowest BMI 17.4, 18.5 at surgery) alongside intractable OCD (Y-BOCS 32)"},
       note="Correspondence in Biol Psychiatry, read in ClinicalKey.")
b.reading("mclaughlin-2013",
          nulls=N(natural_history=("Possible", "The anorexia had already eased somewhat during intensive OCD treatment."),
                  regression=("Unlikely", "Long-standing, not a peak."),
                  misdiagnosis=("Possible", "Residual restriction at BMI 18.5 that may be driven by her OCD rather than a separate anorexia."),
                  cointervention=("Possible", "Trial follow-up and the parallel improvement in OCD and mood."),
                  nonspecific=("Unlikely", "More engaged, not blunted."),
                  expectancy=("Possible", "Open stimulation in a trial participant."),
                  reporting=("Possible", "No eating-disorder scale; weights given as ranges; timing of changes not dated.")),
          verdict="Undecided",
          note="Easier eating and healthy weight over four years after ventral striatal stimulation for OCD. The contact change that worsened and then restored her eating moved her OCD, mood and anxiety too, so it doesn't isolate an anorexia-specific effect, and the restriction may have been part of the OCD all along.",
          hyps=[H("Stimulation at the ventral caudate–internal capsule junction reduced the anxiety and value attached to food through orbitofrontal connections.",
                  "Ventral caudate / anterior limb stimulation → modulated orbitofrontal and ventromedial prefrontal loops involved in food reward and threat → food less frightening and more rewarding → broader intake, weight gain",
                  ["Stimulation of a circuit"], "Fits", "Early change; a contact change moved eating and weight in both directions.",
                  "The same contact change moved OCD, mood and anxiety, so specificity to eating is unshown.",
                  "Low", "Eating not measured separately from OCD and mood.",
                  "Rate eating-disorder cognitions separately across blinded contact changes."),
                H("The eating change was part of the OCD response.",
                  "Stimulation relieves OCD and anxiety → food rules driven by contamination and perfectionism loosen → eats more broadly",
                  ["Threat and arousal"], "Fits", "Her restriction overlapped with her obsessions; OCD and eating moved together.",
                  "She described a change in how she felt about food itself, with sweets eaten for the first time.",
                  "Moderate", "Overlap of the two syndromes in one patient.", "Look for eating change in other VC/VS-treated OCD patients with comorbid anorexia.")],
          related=[("israel-2010", "Anorexia remitting after subgenual stimulation for depression"), ("mallet-2002", "Subthalamic stimulation for Parkinson's disease ending lifelong OCD")])

# ---------------------------------------------------------------- exclusions
b.exclude("arora-2006", "E1", "an acute manic episode that had responded to ten ECT sessions, then worsened over about two weeks on carbamazepine and olanzapine (lithium for two days) before Stevens-Johnson syndrome; neither chronic for six months nor through two adequate trials, so not a serious syndrome by criterion 1")
b.exclude("yates-1988", "E3", "the women sought cosmetic surgery to fix the body dissatisfaction at the core of their eating disorder, and the authors present the one- and three-month remissions as the expected psychological effect of looking better; chronicity is not documented")
b.save()
