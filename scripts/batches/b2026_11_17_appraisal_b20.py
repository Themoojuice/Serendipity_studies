"""Full-text appraisal, batch 20 (2026-11-17): PMC pages read in the laptop browser.
brasic-2018 (hot-tub dehydration, Tourette syndrome), valadez-cuen-2024 (left caudate infarct, smoking and soda craving).
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="PMC article page, read in the laptop browser")

b.code("brasic-2018",
       tracks=[track("24-year-old man", 24, "M", [
           ev("onset", -17, "years", "Motor and phonic tics from age 7, worse with cold, fatigue and anxiety; episodic regurgitation since 10", "approx"),
           ev("treatment_failed", -2, "years", "Clonidine and topiramate: minimal effect; occasional cannabis relieved tics for 3–4 days", "approx", to=-1),
           ev("assessment", -7, "months", "Research baseline", scores=[{"scale": "YGTSS", "value": 55, "higher_is_better": False}, {"scale": "AIMS", "value": 9, "higher_is_better": False}, {"scale": "CGI-S", "value": 4, "higher_is_better": False}]),
           ev("exposure_start", 0, "days", "Deliberately sat in a 39–40 °C hot tub for about 3.5 hours to dehydrate himself (reason not given); vomiting, cramps, pink-orange urine for 2 days"),
           ev("first_change", 2, "hours", "Tics subsided during the last 1.5 hours in the tub", state="Remitted"),
           ev("assessment", 1, "months", "Motor 13, phonic 0, impairment 0; urine THC positive", state="Partial",
              scores=[{"scale": "YGTSS", "value": 13, "higher_is_better": False}, {"scale": "AIMS", "value": 0, "higher_is_better": False}, {"scale": "CGI-S", "value": 3, "higher_is_better": False}]),
           ev("assessment", 11, "months", "Very much improved; working full time; urine THC positive", state="Remitted",
              scores=[{"scale": "AIMS", "value": 1, "higher_is_better": False}, {"scale": "CGI-S", "value": 2, "higher_is_better": False}]),
           ev("relapse", 3, "years", "Worst-ever exacerbation for two weeks after a tetanus vaccination, then settled to mild tics", "approx", state="Partial"),
           ev("follow_up", 5, "years", "Mild tics on nightly THC vaping; carries eggs at work without trouble", "approx", state="Partial"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 1, 1, 0, 0, "YGTSS 55 → 13, AIMS 9 → 0, with video; tics went during the exposure itself; but urine was positive for THC after the remission although he denied cannabis, and cannabis had relieved his tics before."),
       jbi=J("YYYYYYYY"),
       fix={"caveat": "His urine was positive for cannabis at both follow-ups although he denied using it, and cannabis had eased his tics before; tics also wax and wane."})
b.reading("brasic-2018",
          nulls=N(natural_history=("Possible", "Tics wax and wane, though remission at 24 after 17 years is uncommon."),
                  regression=("Possible", "Baseline was seven months earlier."),
                  misdiagnosis=("Unlikely", "Classic Tourette syndrome."),
                  cointervention=("Possible", "Cannabis in his urine at both follow-ups."),
                  nonspecific=("Unlikely", "Worked full time; not sedated."),
                  expectancy=("Possible", "He chose to do it, so he presumably expected something."),
                  reporting=("Unlikely", "YGTSS, AIMS and video.")),
          verdict="Undecided",
          note="Tics stopped in the tub and stayed largely gone for two years, with video and standard scales. Positive urine cannabis screens, denied by the patient, keep it from being clean.",
          hyps=[H("Severe heat stress reset hypothalamic-basal ganglia dopamine signalling (the authors' idea).",
                  "Prolonged hyperthermia and dehydration → anterior hypothalamic dopamine release and possible minor injury → lasting change in striatal dopamine tone → fewer tics",
                  ["Fever and heat", "Dopamine"], "Fits",
                  "Tics went during the heat exposure; Gilles de la Tourette noted fever relieved tics.",
                  "Heat usually worsens tics in laboratory studies.",
                  "Low", "Cannabis confound; one exposure.", "Tic counts during controlled passive heating."),
                H("Covert cannabis use maintained the remission.",
                  "THC → CB1 activation in basal ganglia → tic suppression",
                  ["Endocannabinoid"], "Doesn't fit",
                  "Positive urine screens; cannabis had helped before.",
                  "Tics stopped in the tub, before any cannabis; cannabis had only given 3–4 days of relief.",
                  "Low", "As above.", "None in this patient.")],
          related=[("ripsman-2025", "Tics changing after surgery")])

b.code("valadez-cuen-2024",
       tracks=[track("63-year-old woman", 63, "F", [
           ev("onset", -40, "years", "Two packs a day (80 pack-years); three 20-ounce bottles of citrus soda a day; previous strokes", "approx"),
           ev("exposure_start", 0, "days", "Acute infarct of the left caudate and basal ganglia (old infarct on the right); MoCA 13; not thrombolysed"),
           ev("first_change", 3, "days", "Family notice she hasn't asked for a cigarette since the stroke; no interest in soda; cognition improving", "approx", state="Remitted"),
           ev("follow_up", 1, "weeks", "Still not smoking, no desire for sweet drinks; lost to follow-up at a year", state="Remitted"),
       ])],
       unexpectedness=T(base_rate=("borderline", "Many smokers stop in hospital after a stroke; one week can't separate that from a lesion effect.")),
       attribution=A(1, 0, 1, 0, 0, "Heavy smoking and soda intake before; loss of desire noticed in hospital; follow-up one week, with in-hospital cessation counselling."),
       jbi=J("YYYYYYYY"),
       lesion={"kind": "Lesion", "side": "Left", "regions": ["Caudate", "Ventral striatum (nucleus accumbens)"],
               "specific": "Acute left caudate and basal ganglia infarct (authors suggest nucleus accumbens involvement); old contralateral basal ganglia infarct",
               "aetiology": "Ischaemic stroke", "imaging": "MRI and CT", "mappable": "Figure"},
       fix={"caveat": "Follow-up was one week, in and just out of hospital with cessation counselling; acute stroke confusion (MoCA 13) can also remove wanting."})
b.reading("valadez-cuen-2024",
          nulls=N(natural_history=("Likely", "Hospital abstinence after a stroke is common, and a week is all that was seen."),
                  regression=("Unlikely", "Lifelong habit."),
                  misdiagnosis=("Unlikely", "Heavy dependence."),
                  cointervention=("Possible", "Cessation counselling; hospital."),
                  nonspecific=("Possible", "Confusion and slowed thinking after the stroke."),
                  expectancy=("Unlikely", "None."),
                  reporting=("Possible", "Family report; lost to follow-up.")),
          verdict="Doesn't beat the null",
          note="Losing both cigarettes and soda after a caudate stroke fits the striatal story (Jing 2021), but a week of follow-up after a stroke with confusion can't show it.",
          hyps=[H("The caudate and ventral striatal infarct removed reward-driven wanting for both nicotine and sugar.",
                  "Infarct in caudate and accumbens → loss of incentive salience → no urge to smoke or drink soda",
                  ["Lesion disconnection", "Dopamine"], "Fits",
                  "Two unrelated rewards lost at once; striatal lesion cohorts show the same.",
                  "One week of follow-up.", "Low", "Lost to follow-up.", "Longer follow-up in striatal infarcts with verified abstinence.")],
          related=[("jing-2021", "Dorsal striatal infarcts and smoking"), ("naqvi-2007", "Insula and smoking")])

b.save()
