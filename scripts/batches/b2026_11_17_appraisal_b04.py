"""Full-text appraisal, batch 4 (2026-11-17): the remaining Included cases with open-access full text.

sciortino-2021 (accelerated iTBS, binge eating, two patients), yuan-2025 (head injury, nicotine), hill-2025 (dulaglutide, alcohol).

hill-2025: outcome.reversal recoded to Natural off-on (insurance lapse: drinking back within two weeks of stopping);
tier B -> A under the section 6 rule.
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="PMC open-access full text, via Europe PMC")

# ------------------------------------------------------------------ sciortino-2021
ITBS = "Accelerated iTBS to left dorsolateral prefrontal cortex: 18 sessions over 6 days in 3 weeks; medicines unchanged for 4 weeks before and throughout"
b.code("sciortino-2021",
       tracks=[
           track("Patient 1", 45, "F", [
               ev("assessment", -32, "years", "Anorexia nervosa at 13, then bulimia for 10 years, then remission", "approx"),
               ev("onset", -7, "years", "Binge eating disorder from 38: night-time fridge binges, waxing and waning", "approx"),
               ev("assessment", -2, "months", "Three or four binges a week; 12 kg gained; bipolar II depression after a switch to vortioxetine; lamotrigine 150 mg, vortioxetine 20 mg", "approx"),
               ev("exposure_start", 0, "days", ITBS, scores=[{"scale": "HAM-D", "value": 12}, {"scale": "MADRS", "value": 25}]),
               ev("first_change", 2, "weeks", "Binges less frequent", "approx", state="Partial", scores=[{"scale": "HAM-D", "value": 12}, {"scale": "MADRS", "value": 23}]),
               ev("best_response", 3, "weeks", "Binges gone (reported at the end of the cycle); depression barely changed", "approx", state="Remitted",
                  scores=[{"scale": "HAM-D", "value": 10}, {"scale": "MADRS", "value": 23}]),
               ev("exposure_stop", 3, "weeks", "End of the stimulation cycle"),
               ev("follow_up", 15, "weeks", "Twelve weeks after the cycle: still no binges; 4 kg lighter", state="Remitted"),
           ]),
           track("Patient 2", 28, "F", [
               ev("onset", -10, "years", "Binge eating since her first depression; daily during depressive phases", "approx"),
               ev("treatment_failed", -10, "years", "Valproate, fluoxetine, citalopram, venlafaxine, bupropion; now clomipramine 150 mg and pregabalin 225 mg", "approx", to=-0.25),
               ev("assessment", -3, "months", "Seasonal bipolar II depression for 3 months; binges almost every evening", "approx"),
               ev("exposure_start", 0, "days", ITBS, scores=[{"scale": "HAM-D", "value": 22}, {"scale": "MADRS", "value": 41}]),
               ev("first_change", 2, "weeks", "Binges less frequent", "approx", state="Partial", scores=[{"scale": "HAM-D", "value": 18}, {"scale": "MADRS", "value": 34}]),
               ev("best_response", 3, "weeks", "Binges gone (reported at the end of the cycle); depression moderate", "approx", state="Remitted",
                  scores=[{"scale": "HAM-D", "value": 17}, {"scale": "MADRS", "value": 34}]),
               ev("exposure_stop", 3, "weeks", "End of the stimulation cycle"),
               ev("follow_up", 15, "weeks", "Twelve weeks after the cycle: still no binges; 2 kg lighter", state="Remitted"),
           ]),
       ],
       unexpectedness=T(era=("borderline", "By 2021 there was a case report and reviews of prefrontal rTMS for binge eating (the authors cite them)."),
                        base_rate=("borderline", "Patient 1's binge eating had waxed and waned for years.")),
       attribution=A(1, 0, 1, 0, 1, "Scored on patient 2. No binge-eating scale or diary; medicines unchanged for 4 weeks before and during, stated."),
       jbi=J("YNUYYYYYUA"))
b.reading("sciortino-2021",
          nulls=N(natural_history=("Possible", "Patient 1's binge eating had come and gone for years."),
                  regression=("Possible", "Patient 1 had just gained 12 kg in two months, a peak."),
                  misdiagnosis=("Unlikely", "Typical binge eating disorder in both."),
                  cointervention=("Unlikely", "Medicines unchanged for 4 weeks before and during."),
                  nonspecific=("Unlikely", "Neither became less active."),
                  expectancy=("Possible", "Open label, though nobody was looking at eating."),
                  reporting=("Possible", "No eating scale; frequency from recall at the end of the cycle; interview-only follow-up.")),
          verdict="Beats the null",
          note="Two patients, the same timing, medicines unchanged, and depression that barely moved: the binge effect looks specific rather than riding on mood. Without a binge diary, though, the size of the change rests on recall.",
          hyps=[H("Prefrontal iTBS strengthened top-down control over binge urges.",
                  "Accelerated iTBS at left dorsolateral prefrontal cortex → more excitable inhibitory-control node → urge-to-binge coupling weakened → binges stop",
                  ["Stimulation of a circuit"], "Fits",
                  "Same timing in both; depression barely improved, so the effect looks specific; echoes Downar's dorsomedial case.",
                  "No eating measures; 12-week follow-up only; open label.",
                  "Moderate", "No binge-eating scale or diary, so frequency comes from recall at the end of the cycle.",
                  "Sham-controlled accelerated iTBS with daily binge diaries.")],
          related=[("downar-2012", "Dorsomedial prefrontal rTMS stopped refractory bulimia, with rechallenge")])

# ------------------------------------------------------------------ yuan-2025
b.code("yuan-2025",
       tracks=[track("87-year-old man", 87, "M", [
           ev("onset", -50, "years", "At least 50 cigarettes a day for decades (about 60 pack-years)", "approx"),
           ev("exposure_start", 0, "days", "Fall: bilateral frontotemporal subdural haematomas, right frontal contusion, subarachnoid haemorrhage, skull fracture; conscious throughout"),
           ev("cointervention", 0, "days", "A month in hospital: pneumonia (ceftazidime), mannitol, nimodipine, levetiracetam, metoprolol; no smoking on the ward"),
           ev("first_change", 1, "weeks", "No craving or withdrawal seen by staff or family", "at most", state="Remitted"),
           ev("assessment", 1, "months", "Recovered and mobile; abstinent, no craving", state="Remitted"),
           ev("assessment", 3, "months", "Abstinent, no craving (patient and daughter separately)", state="Remitted"),
           ev("follow_up", 6, "months", "Abstinent without craving; MRI: right frontal malacia, atrophy, leukoaraiosis", state="Remitted"),
       ])],
       lesion={"kind": "Injury", "side": "Right", "regions": ["Frontal, other"],
               "specific": "Right frontal contusion with haemorrhage, plus bilateral frontotemporal subdural haematomas and subarachnoid blood; right frontal malacia on MRI at 6 months",
               "aetiology": "Trauma", "imaging": "MRI and CT", "mappable": "Figure"},
       unexpectedness=T(era=("borderline", "Smoking stopping after brain lesions was known since the insula studies (2007)."),
                        base_rate=("borderline", "A month in hospital with pneumonia and emphysema at 87 forces abstinence, and many smokers don't restart after such an admission.")),
       attribution=A(1, 0, 1, 0, 0, "No smoking scale; hospital abstinence and the acute illness not separated. The corresponding author is the patient's first-degree relative."),
       jbi=J("YYYYYYYY"),
       fix={"caveat": "A month in hospital with pneumonia enforced abstinence, which explains not smoking, though not the absent craving and withdrawal."})
b.reading("yuan-2025",
          nulls=N(natural_history=("Unlikely", "Fifty a day for decades."),
                  regression=("Unlikely", "Not judged against a peak."),
                  misdiagnosis=("Unlikely", "Plain heavy nicotine dependence."),
                  cointervention=("Possible", "A month of enforced abstinence with pneumonia and emphysema; family supervision afterwards."),
                  nonspecific=("Possible", "Frontal damage, atrophy and age can reduce initiative of every kind."),
                  expectancy=("Unlikely", "Nothing was offered for smoking."),
                  reporting=("Possible", "Reported by the patient's first-degree relative; no scales.")),
          verdict="Undecided",
          note="The striking detail is not that he stopped but that a 50-a-day smoker had no craving or withdrawal. The report, by a relative and without scales, can't carry more than that.",
          hyps=[H("Damage to frontal reward-regulation circuitry removed nicotine craving.",
                  "Right frontal contusion and diffuse injury → disrupted frontostriatal reward circuitry → nicotine loses its pull → no craving or withdrawal",
                  ["Lesion disconnection"], "Fits",
                  "Abrupt loss of craving with no withdrawal; persisting right frontal damage on MRI.",
                  "Right frontal cortex isn't the insula; diffuse atrophy and leukoaraiosis blur any localisation.",
                  "Low", "Localisation is coarse (contusion plus bilateral subdurals), so no network can be tested.",
                  "Lesion network mapping of the contusion against the addiction remission network."),
                H("Hospital-enforced abstinence during an acute illness broke the habit, and post-injury apathy kept it broken.",
                  "A month on the ward with pneumonia → no cigarettes → habit interrupted; less initiative after the injury → doesn't restart",
                  ["Social and environmental change", "Global suppression (sedation, apathy, cognitive loss)"], "Fits",
                  "A month in hospital at 87; family supervision afterwards.",
                  "Enforced abstinence in a 50-a-day smoker normally brings withdrawal and craving.",
                  "Low", "No withdrawal or craving scale, and the reporter is a relative.",
                  "Withdrawal ratings in comparable smokers admitted without brain injury.")],
          related=[("naqvi-2007", "Insula lesions ending smoking"),
                   ("haque-2025", "Orbitofrontal contusion ending alcohol craving")])

# ------------------------------------------------------------------ hill-2025
b.code("hill-2025",
       tracks=[track("44-year-old man", 44, "M", [
           ev("exposure_start", 0, "days", "Dulaglutide 0.75 mg weekly for prediabetes and weight (semaglutide not covered). BMI 41.8; about 90 beers a month, never treated, not wanting to change",
              scores=[{"scale": "AUDIT", "value": 19}]),
           ev("cointervention", 0, "days", "Diet and exercise counselling; bupropion continued for mood"),
           ev("first_change", 56, "days", "About 30 beers a month; feels full after drinking, fewer urges; still binges in the two days before each injection", "at most", state="Partial"),
           ev("cointervention", 56, "days", "Dulaglutide increased to 1.5 mg"),
           ev("best_response", 84, "days", "Four to eight beers a month, no cravings; BMI 37.3", state="Remitted", scores=[{"scale": "AUDIT", "value": 6}]),
           ev("exposure_stop", 6, "months", "Lost his insurance on retiring; dulaglutide stopped, other medicines continued", "approx"),
           ev("relapse", 6.5, "months", "Drinking again two weeks after stopping", "approx"),
           ev("assessment", 10, "months", "Back to about 90 beers a month within four months", "approx", state="Worse"),
           ev("follow_up", 334, "days", "90–100 beers a month; naltrexone tried, poorly tolerated and not taken", state="Worse"),
       ])],
       unexpectedness=T(era=("borderline", "By the mid-2020s GLP-1 agonists were known to reduce drinking in animals and early human studies.")),
       attribution=A(0, 1, 1, 2, 0, "Duration of the drinking not stated; AUDIT before and after; diet counselling alongside; drinking returned within two weeks of a documented stop."),
       jbi=J("YYYYYYYY"),
       fix={"tier": "A", "outcome.reversal": "Natural off-on",
            "summary": "A 44-year-old drinking about 90 beers a month cut down to a few a month within 12 weeks of dulaglutide for weight loss, binged mainly in the days before each injection, and was back to 90 a month within four months of losing the drug with his insurance.",
            "caveat": "Diet and exercise counselling started with the drug, and he never wanted to cut down, so expectation and contact are an incomplete explanation."})
b.reading("hill-2025",
          nulls=N(natural_history=("Unlikely", "Drinking fell on the drug and came straight back off it."),
                  regression=("Unlikely", "Came for weight, not at a drinking crisis."),
                  misdiagnosis=("Unlikely", "Moderate-to-severe alcohol use disorder on AUDIT."),
                  cointervention=("Possible", "Diet and exercise counselling and clinic contact; bupropion continued."),
                  nonspecific=("Possible", "Feeling full after drinking: slowed gastric emptying blunts intake of anything."),
                  expectancy=("Unlikely", "Pre-contemplative about drinking; the drug was for weight."),
                  reporting=("Possible", "Self-reported beers and AUDIT; wife confirmed adherence.")),
          verdict="Beats the null",
          note="On the drug, drinking fell 90 to about 6 a month; off it (insurance lost) it returned within two weeks and reached baseline within four months; and on it, binges clustered in the two days before each weekly dose. That is reversal and a dose-timing effect in one man.",
          hyps=[H("GLP-1 receptor activation reduced alcohol reward and craving.",
                  "Dulaglutide → GLP-1 receptors in reward and satiety regions → less dopamine response to alcohol, reduced urges → drinking falls; wears off before each dose and on stopping",
                  ["Neuropeptide (oxytocin, orexin, other)", "Dopamine"], "Fits",
                  "Reduced urges and cravings, not just fullness; end-of-dose binges; relapse within two weeks of stopping.",
                  "Fullness after drinking suggests a gut contribution; diet counselling ran alongside.",
                  "Moderate", "Self-reported drinking with no biomarker, so the size of the effect is uncertain.",
                  "Phosphatidylethanol across the dosing week and through a stop-restart."),
                H("Slowed gastric emptying and satiety made drinking physically unappealing.",
                  "Dulaglutide → delayed gastric emptying → fullness after a few beers → less drinking",
                  ["Interoceptive and visceral input"], "Fits",
                  "He reported feeling full after drinking.",
                  "He also reported fewer urges, and binges returned exactly when the drug's effect waned.",
                  "Low", "Satiety and craving weren't rated separately.",
                  "Separate satiety and craving ratings across the dosing week.")],
          related=[("kelly-2026", "Semaglutide ending an impulse control disorder, with rechallenge"),
                   ("meilinger-2026", "Semaglutide for obesity, drinking fell"),
                   ("takizawa-2026", "Tirzepatide, three heavy drinkers drank less")])

b.save()
