"""Full-text appraisal, batch 32 (2026-11-22, night): roadmap step 1b, a CKN session with Brendan signed in.

Read one at a time through the EBSCO Full Text Finder (CKN's link resolver) and the EBSCO viewer:
  mallet-2002        Lancet research letter: coded. The abstract's 58% and 64% are the obsession subscores;
                     total Yale-Brown fell 26 to 5 and 23 to 4 (81% and 83%). Summary corrected.
  kalenderoglu-2011  Turkiye Klinikleri J Med Sci, read in Turkish: coded. The abstract never said the OCD came
                     back off heroin and went again when he restarted; the full text does (reversal, tier A).
  graham-2018        Australas Psychiatry: excluded E1. Two acute inpatient depressions (one after a prednisolone
                     taper), neither chronic for six months nor through two adequate trials before the embolus.
  terao-1999         excluded E4. What lifted was an exacerbation the authors tie to the pain and discomfort of a
                     large bladder stone; the refractory schizophrenia itself carried on.
Ledger only:
  R072119 (Raj 2026, Indian J Psychiatry e-poster, open at Ovid): excluded E4. The authors present the drinking as
                     self-medication of the PTSD, so it settled when the PTSD was treated.
Run from the repo root:  python3 scripts/batches/b2026_11_22_appraisal_b32.py
"""
import csv
import sys

sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H, LEDGER  # noqa: E402

TODAY = "2026-11-22"
b = Batch(TODAY, source="Full text through CKN (EBSCO)")

Y = lambda v: [{"scale": "Y-BOCS", "value": v}]  # noqa: E731

# ---------------------------------------------------------------- Mallet 2002
b.code("mallet-2002",
       tracks=[
           track("51-year-old woman", 51, "F", [
               ev("onset", -33, "years", "OCD: repetitive house cleaning, arranging bottles on the bathroom shelf, fear of being found dead in a dirty house; constant over the years, including the five years of Parkinson's disease", "approx"),
               ev("assessment", -1, "months", "Structured psychiatric assessment before surgery: Y-BOCS 26 (obsessions 12, compulsions 14), MADRS 8, Brief Anxiety Scale 14; UPDRS-III 30; levodopa equivalent 800 mg a day (ropinirole and levodopa 600 mg) for severe levodopa-induced motor complications", scores=Y(26)),
               ev("exposure_start", 0, "days", "December 2000: bilateral subthalamic stimulation for Parkinson's disease; one electrode between the anteromedial subthalamic nucleus and the zona incerta, the other in the anterior zona incerta; 3.1 V, 185 Hz, 60 µs"),
               ev("cointervention", 0, "days", "Dopaminergic treatment withdrawn after surgery (levodopa equivalent 800 mg a day to none by six months); timing of the cuts not given", "approx"),
               ev("first_change", 2, "weeks", "OCD symptoms gone; she was more pleased about that than about the moderate motor improvement", "approx"),
               ev("best_response", 6, "months", "Y-BOCS 5 (obsessions 5, compulsions 0), MADRS 2, Brief Anxiety Scale 4; UPDRS-III 22 (27% better); frontal score and Mattis unchanged", state="Remitted", scores=Y(5)),
               ev("follow_up", 15, "months", "Last seen March 2002: no recurrence of the compulsions", "approx", state="Remitted"),
           ]),
           track("50-year-old man", 50, "M", [
               ev("onset", -40, "years", "OCD, mostly repeated checking of locks; milder in adulthood, then worse with the onset of Parkinson's disease 16 years before surgery, checking up to 3 hours a day", "approx"),
               ev("assessment", -1, "months", "Structured psychiatric assessment before surgery: Y-BOCS 23 (obsessions 11, compulsions 12), MADRS 2, Brief Anxiety Scale 2; UPDRS-III 36; levodopa equivalent 2,200 mg a day (pergolide 2.75 mg, levodopa 1,900 mg) for severe dyskinesia and fluctuations", scores=Y(23)),
               ev("exposure_start", 0, "days", "June 2001: bilateral subthalamic stimulation; one electrode in the anteromedial subthalamic nucleus, the other between it and the zona incerta; 3.2 V, 130 Hz, 90 µs"),
               ev("cointervention", 0, "days", "Levodopa stopped and pergolide cut to 2 mg (levodopa equivalent 2,200 to 200 mg a day by six months); timing of the cuts not given", "approx"),
               ev("first_change", 2, "weeks", "Compulsions gone; obsessions about orderliness and checking greatly diminished", "approx"),
               ev("best_response", 6, "months", "Y-BOCS 4 (obsessions 4, compulsions 0), MADRS 0, Brief Anxiety Scale 0; UPDRS-III 6 (84% better)", state="Remitted", scores=Y(4)),
               ev("follow_up", 9, "months", "Last seen March 2002: no recurrence of the compulsions", "approx", state="Remitted"),
           ]),
       ],
       unexpectedness=T(),
       attribution=A(1, 1, 1, 0, 1, "OCD stable for 33 and 40 years, Y-BOCS a month before and six months after, change at two weeks. No stimulation-off test. Confounders addressed in the paper: dopaminergic doses were cut heavily, but the OCD predated Parkinson's disease by decades and had held steady on long-term levodopa; anxiety relief and motor relief are argued against (patient 1 improved little in motor terms)."),
       jbi=J("UYYUUYYYYA"),
       lesion={"kind": "Stimulation target", "side": "Bilateral", "regions": ["Subthalamic nucleus"],
               "specific": "Anteromedial subthalamic nucleus and zona incerta, medial to the usual motor target (patient 1: STN–zona incerta border and anterior zona incerta; patient 2: anteromedial STN and the STN–zona incerta border); contacts localised on postoperative T1 MRI against the Schaltenbrand–Wahren atlas",
               "aetiology": "Not applicable", "imaging": "MRI", "mappable": "Figure"},
       fix={"summary": "Two patients with 33 and 40 years of OCD had subthalamic stimulators implanted for Parkinson's disease; two weeks later their compulsions were gone, and Yale-Brown totals fell from 26 to 5 and from 23 to 4, still holding 9 and 15 months on.",
            "caveat": "Dopaminergic doses were cut from 800 mg levodopa equivalent to none and from 2,200 mg to 200 mg after surgery, and dopaminergic drugs can drive compulsive behaviour.",
            "outcome.resolution": "Complete",
            "syndrome.specific": "Severe lifelong obsessive-compulsive disorder (33 and 40 years) that preceded Parkinson's disease by decades"},
       note="Research letter, three pages with a table and an electrode-location figure. The abstract's 58% and 64% are the obsession subscores.")
b.reading("mallet-2002",
          nulls=N(natural_history=("Unlikely", "Stable for decades before surgery; change within two weeks."),
                  regression=("Unlikely", "Lifelong, not a peak."),
                  misdiagnosis=("Unlikely", "Classic contamination and checking OCD that began decades before Parkinson's disease, so not parkinsonian obsessionality."),
                  cointervention=("Possible", "Large cuts in levodopa and dopamine agonists after surgery; the paper argues against them but cannot separate them."),
                  nonspecific=("Unlikely", "Mood, anxiety and frontal scores stayed normal or improved; no apathy reported."),
                  expectancy=("Possible", "Open, unblinded ratings by the treating team after a major operation."),
                  reporting=("Unlikely", "Structured scales before and after, numbers in a table.")),
          verdict="Beats the null",
          note="The founding case for subthalamic stimulation in OCD: decades-stable illness, two-week onset, Yale-Brown totals down by four fifths in both patients, and the 2008 randomised crossover trial (Mallet, NEJM) later showed the effect in OCD without Parkinson's disease. The dopaminergic dose cuts are the competitor this letter can't exclude on its own; the trial could.",
          hyps=[H("Stimulation of the limbic (anteromedial) subthalamic nucleus damped the cortico-striato-thalamic loop that sustains compulsions.",
                  "High-frequency stimulation at the anteromedial STN and zona incerta → inhibition or decoupling of the associative-limbic STN → reduced pallidal–thalamic drive to orbitofrontal and anterior cingulate cortex → compulsions stop, obsessions fade",
                  ["Stimulation of a circuit"], "Fits", "Abrupt, within two weeks, in both patients; contacts sat medial to the motor target; the effect was reproduced in a randomised crossover trial.",
                  "Only two patients and no stimulation-off test here; contacts extended into the zona incerta, so the active structure is uncertain.",
                  "Moderate", "Which structure carried the effect (STN versus zona incerta fibres) is not resolved by two electrode plots.",
                  "Blinded stimulation on/off crossover at the same contacts (done later in the 2008 trial)."),
                H("Withdrawing dopaminergic drugs removed a dopamine-driven layer of compulsive behaviour.",
                  "Levodopa and agonists cut heavily after surgery → less mesolimbic dopamine stimulation → less compulsive checking and arranging",
                  ["Dopamine"], "Fits", "Doses fell steeply in both patients; patient 2's checking had worsened with Parkinson's disease and its treatment.",
                  "Both had OCD for decades before any dopaminergic drug; patient 1's OCD was constant through four years of optimum treatment.",
                  "Low", "The timing of the dose cuts relative to the two-week change is not reported.",
                  "Ratings across stimulation on/off at a fixed dopaminergic dose."),
                H("Zona incerta fibres, including ascending serotonergic axons, were activated, mimicking an SSRI.",
                  "Current spread to zona incerta fibre bundles → more forebrain serotonin release → OCD improves",
                  ["Serotonin"], "Can't judge", "The authors raise it; both electrodes sat partly in the zona incerta.",
                  "SSRI benefit in OCD is slow and partial; this was abrupt and near-complete.",
                  "Low", "Contact-level current spread is unknown.", "Compare contacts confined to the STN with zona incerta contacts in a blinded crossover.")],
          related=[("fontaine-2004", "Subthalamic stimulation for Parkinson's, a 16-year OCD from Yale-Brown 32 to 1 (context)"),
                   ("mira-2024", "Subthalamic stimulation for dyskinesia ending 20 years of cocaine use")])

# ---------------------------------------------------------------- Kalenderoglu 2011
b.code("kalenderoglu-2011",
       tracks=[track("43-year-old man", 43, "M", [
           ev("onset", -26, "years", "Contamination obsessions and cleaning compulsions, checking and symmetry, from age 16", "approx"),
           ev("treatment_failed", -26, "years", "Continuous drug treatment, each trial at least eight weeks: fluoxetine 80 mg, sertraline 200 mg, citalopram 60 mg, mirtazapine 90 mg, buspirone 30 mg, diazepam 30 mg, clomipramine 300 mg, haloperidol 10 mg, quetiapine 900 mg, risperidone 2 mg; combinations including sertraline + buspirone for two years and clomipramine + quetiapine for four years. Never fully better", "approx", to=-1),
           ev("exposure_start", 0, "months", "Street heroin snorted twice a day, about 0.2–0.3 g a dose, 'like a medicine', started on the mistaken belief that it would lower his blood sugar (type 2 diabetes for four years, glucose around 300)", "approx"),
           ev("best_response", 12, "months", "About a year later: admitted asking to stop heroin, in withdrawal (last use two days before; urine opioid-positive). No antidepressant for the past year. DSM-IV opioid dependence and OCD in remission; Y-BOCS 0. When the OCD first eased during that year is not reported", "at most", state="Remitted", scores=Y(0)),
           ev("exposure_stop", 12, "months", "Detoxification with diazepam 40 mg a day (60–80 mg at worst); withdrawal scale 0 by day 5, craving gone by day 8; diazepam tapered off; discharged on day 20"),
           ev("relapse", 14, "months", "Eight weeks after stopping heroin he came back with returning OCD; no other drug use, non-adherence or organic cause found; Y-BOCS 25; clomipramine 75 mg started", "approx", scores=Y(25)),
           ev("assessment", 15, "months", "Worse, especially symmetry and checking; Y-BOCS 30; clomipramine raised slowly to 300 mg (irregular attendance), quetiapine 300 mg added", "approx", state="Worse", scores=Y(30)),
           ev("treatment_failed", 19, "months", "End of week 20 of treatment: obsessions continuing, Y-BOCS 30; agitated, quetiapine raised to 600 mg", "approx", scores=Y(30)),
           ev("exposure_restart", 20, "months", "A month later: had stopped his medication two days earlier and gone back to heroin (toxicology opioid-positive)", "approx"),
           ev("best_response", 20, "months", "Reports fewer obsessions; Y-BOCS 11. Blood glucose still 430 despite oral drugs and insulin. Referred to the addiction unit; never attended", "approx", state="Partial", scores=Y(11)),
       ])],
       unexpectedness=T(era=("borderline", "Tramadol and morphine had been reported to ease OCD (open reports and a placebo-controlled single-dose morphine study), which the authors cite; heroin itself had not been reported.")),
       attribution=A(1, 1, 1, 2, 0, "Twenty-six years of OCD through ten drugs; Y-BOCS 0 on heroin, 25–30 eight to twenty weeks after detoxification despite clomipramine 300 mg and quetiapine, 11 on resuming heroin: a stop-return-restart sequence. Timing is scored on the return and the restart; the first improvement was never dated (he arrived a year into heroin already at zero). Confounders 0: he had also stopped antidepressants that year, and the low scores were taken while he was using, neither addressed by the authors."),
       jbi=J("YYYYYYYY"),
       fix={"summary": "A 43-year-old man with OCD since 16, unmoved by ten drugs, started snorting street heroin in the belief it would lower his blood sugar; a year later his Yale-Brown score was 0. Eight weeks after detoxification the OCD was back (25, then 30 on clomipramine 300 mg and quetiapine), and when he went back to heroin it fell to 11.",
            "caveat": "Every low score was taken while he was using heroin, so opioid sedation and indifference could pass for fewer obsessions.",
            "trigger.specific": "Street heroin, snorted twice a day, started to lower his blood sugar on a mistaken belief",
            "outcome.resolution": "Complete",
            "outcome.reversal": "On-off rechallenge",
            "syndrome.specific": "Treatment-refractory OCD for 26 years (ten drugs, including clomipramine 300 mg and quetiapine 900 mg)",
            "links.alternates": [{"label": "Embase record (CKN login)", "url": "https://www.embase.com/records?subaction=viewrecord&id=L362359202"}],
            "citation.authors": "Kalenderoglu A, Selek S, Yumru M, Savas HA",
            "citation.volume": "31", "citation.issue": "2", "citation.pages": "475-478"},
       note="Full text read in Turkish (four pages). Presented as a poster at the 42nd National Psychiatry Congress, Istanbul, 2006.")
b.reading("kalenderoglu-2011",
          nulls=N(natural_history=("Unlikely", "Twenty-six years, ten drugs; the OCD came back within eight weeks of stopping heroin."),
                  regression=("Unlikely", "Chronic; and the stop-return-restart sequence is not what regression looks like."),
                  misdiagnosis=("Unlikely", "Long-standing contamination, checking and symmetry OCD with DSM-IV diagnosis and Y-BOCS."),
                  cointervention=("Possible", "He was off antidepressants during the heroin year, and stopped clomipramine and quetiapine two days before the restart; neither stop would be expected to help OCD."),
                  nonspecific=("Possible", "Scores of 0 and 11 were self-reported while opioid-positive; sedation and indifference were not separated from fewer obsessions."),
                  expectancy=("Unlikely", "He took heroin for his blood sugar, not his OCD."),
                  reporting=("Possible", "Short report, single clinic; the first improvement was never dated.")),
          verdict="Beats the null",
          note="Heroin started for a mistaken reason, Yale-Brown 0 a year in, back to 25–30 off heroin despite clomipramine 300 mg, down to 11 on resuming: an unplanned off-on-off sequence that sits with the morphine and tramadol reports in OCD. What it can't separate is relief of obsessions from opioid indifference, since every good score was taken while he was using.",
          hyps=[H("Mu-opioid agonism damped the obsessional loop directly.",
                  "Heroin → morphine at mu receptors in orbitofrontal–striatal and limbic circuits → reduced anxiety-driven salience of intrusive thoughts and of the urge to neutralise → fewer obsessions and compulsions; withdrawal removes it, and naloxone is reported to worsen OCD",
                  ["Opioid"], "Fits", "Return within eight weeks of stopping and improvement on restarting; consistent with the placebo-controlled single-dose morphine effect in refractory OCD.",
                  "Self-report under intoxication; the restart effect was measured once.",
                  "Moderate", "One patient, scores taken while using, so a specific anti-obsessional effect is not separated from sedation.",
                  "Blinded morphine or tramadol versus active placebo in refractory OCD, with ratings away from peak sedation."),
                H("Opioid sedation and emotional blunting lowered the reported distress without changing the obsessions.",
                  "Heroin → global sedation and indifference → less distress and less time spent resisting → lower Y-BOCS self-report",
                  ["Global suppression (sedation, apathy, cognitive loss)"], "Fits", "All low scores were opioid-positive; the restart score came on the first day back.",
                  "He functioned well enough to seek treatment and attend; Y-BOCS 0 implies no time on obsessions at all.",
                  "Low", "No observer rating or measure of sedation.",
                  "Y-BOCS and a sedation scale rated by an observer at trough and peak heroin levels.")],
          related=[("moussawi-2016", "Pallidal lesion ending opioid and alcohol dependence (an opioid case seen from the other side)")])

# ---------------------------------------------------------------- exclusions
b.exclude("graham-2018", "E1", "two acute inpatient depressions (case 1 after a prednisolone taper; case 2 untreated beforehand, two ECT titration sessions); neither chronic for six months nor through two adequate trials when enoxaparin started, so not a serious syndrome by criterion 1")
b.exclude("terao-1999", "E4", "the improvement was in an exacerbation the authors attribute to the pain and discomfort of a large bladder stone; the refractory schizophrenia itself continued after surgery")
b.save()

# ---------------------------------------------------------------- ledger-only settle
rows = list(csv.DictReader(LEDGER.open()))
fields = list(rows[0].keys())
sup = {r["supersedes"] for r in rows if r["supersedes"]}
nid = max(int(r["record_id"][1:]) for r in rows) + 1
SETTLE = {"R072119": ("excluded", "E4", f"full-text appraisal {TODAY} (e-poster, open at Ovid): the authors present the drinking as self-medication of the PTSD, so it settled when the PTSD was treated; secondary syndrome resolving with its cause")}
with LEDGER.open("a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    for rid, (dec, code, note) in SETTLE.items():
        old = next(r for r in rows if r["record_id"] == rid)
        assert rid not in sup, rid
        c = dict(old)
        c.update({"record_id": f"R{nid:06d}", "retrieved_date": TODAY, "screen_stage": "ft", "decision": dec,
                  "reason_code": code, "library_ids": "", "flags": "", "supersedes": rid, "notes": note})
        nid += 1
        w.writerow(c)
print("ledger settled:", ", ".join(SETTLE))
