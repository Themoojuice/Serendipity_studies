"""Full-text appraisal, batch 14 (2026-11-17): two lesion series in addiction, coded at group level.
jing-2021 (dorsal striatal infarcts, smoking), yousefzadeh-fard-2013 (insular infarcts, opium).
Mixed-side series take lesion side 'Unstated', with the split in `specific`.
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="PMC open-access full text, via Europe PMC")

b.code("jing-2021",
       tracks=[track("Dorsal striatum group (11 smokers)", 65, "Not stated", [
           ev("onset", -30, "years", "Over 10 cigarettes a day for over 10 years; all highly dependent (Fagerström 7–10)", "approx",
              scores=[{"scale": "FTND", "value": 8, "higher_is_better": False}], note="Group range 7–10; value shown is mid-range."),
           ev("exposure_start", 0, "days", "Acute ischaemic infarct confined to the dorsal striatum (5 right, 6 left), 2017–2019"),
           ev("first_change", 1, "days", "Quit within a day of the stroke, rated easy, no urge since", "at most", state="Remitted"),
           ev("follow_up", 2, "years", "Phone interview June 2020: 10 of 11 met all four disruption criteria (no smoking for 6 months, quit within a day, easy, no urge), against 2 of 20 stroke controls", "approx", state="Remitted"),
       ])],
       unexpectedness=T(base_rate=("borderline", "Strokes often prompt quitting; the comparison group exists to deal with that.")),
       attribution=A(1, 0, 1, 0, 1, "Fagerström dependence before; outcome is the Naqvi disruption criteria by phone interview; stroke controls (other sites) give a comparison for the general effect of stroke."),
       jbi=J("YYYNNYYYYY"),
       lesion={"kind": "Lesion", "side": "Unstated", "regions": ["Caudate", "Putamen"],
               "specific": "Dorsal striatum only (5 right, 6 left); controls had thalamus, capsule, cortical and brainstem infarcts",
               "aetiology": "Ischaemic stroke", "imaging": "MRI", "mappable": "Figure"})
b.reading("jing-2021",
          nulls=N(natural_history=("Unlikely", "Decades of heavy smoking."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Unlikely", "Heavy dependence documented."),
                  cointervention=("Possible", "Hospital abstinence and stop-smoking advice, though controls had the same."),
                  nonspecific=("Possible", "Two of 20 controls also had disruption; a general effect of brain injury is possible."),
                  expectancy=("Unlikely", "No treatment."),
                  reporting=("Possible", "Phone recall years later; 78 of 608 unreachable, some dead.")),
          verdict="Beats the null",
          note="Ten of 11 dorsal striatal infarcts against 2 of 20 controls is a big split, and it extends Naqvi's insula finding to the habit circuit. Small, retrospective and phone-based, so it needs replication.",
          hyps=[H("The dorsal striatum stores smoking as a habit; destroying it removes the automatic urge and act.",
                  "Infarct in caudate or putamen → loss of stimulus-response habit circuitry → cues no longer trigger smoking → effortless quitting",
                  ["Lesion disconnection", "Dopamine"], "Fits",
                  "Immediate, effortless, durable quitting, as in the insula cases; similar with either side.",
                  "Phone recall; tiny groups.",
                  "Moderate", "Eleven cases, retrospective classification.",
                  "Prospective stroke cohorts with lesion mapping and verified abstinence."),
                H("Disruption follows damage to a common network that the striatum, insula and other lesions share.",
                  "Lesion anywhere in an addiction network connected to the insula and striatum → disruption",
                  ["Lesion disconnection"], "Fits",
                  "Two controls with other lesions also had disruption; Joutsa 2022 lesion-network mapping.",
                  "Not tested here.",
                  "Moderate", "No network analysis.", "Lesion-network mapping of this cohort.")],
          related=[("naqvi-2007", "Insula damage disrupting smoking addiction"),
                   ("yousefzadeh-fard-2013", "Insular infarcts and opium use")])

b.code("yousefzadeh-fard-2013",
       tracks=[track("Insula group (8 opium users)", 62, "Not stated", [
           ev("onset", -1, "years", "Opium use for at least a year before the stroke (amount in grams a day by questionnaire)", "at least"),
           ev("exposure_start", 0, "days", "Ischaemic stroke involving the insula (6 right, 2 left; one also basal ganglia), Tehran 2009–2011"),
           ev("assessment", 1, "months", "Six of 8 changed amount or route; neuroimaging read blind to opium use", state="Partial"),
           ev("follow_up", 6, "months", "Three of 8 abstinent since the stroke (37.5%), against fewer in the non-insula group (odds about 31, p = 0.03)", state="Partial"),
       ])],
       unexpectedness=T(),
       attribution=A(1, 0, 0, 0, 1, "Amount and route by questionnaire before and at 1, 3 and 6 months; non-insula stroke group as comparison; financial change checked; insula patients used less before the stroke and were younger, both linked to change."),
       jbi=J("YYYNUYYYYY"),
       lesion={"kind": "Lesion", "side": "Unstated", "regions": ["Insula"],
               "specific": "Insula (6 right, 2 left; one with basal ganglia); right-insula analysis alone also significant",
               "aetiology": "Ischaemic stroke", "imaging": "MRI and CT", "mappable": "Description only"},
       fix={"caveat": "The insula group used less opium before the stroke, and younger patients changed more, so lighter, younger users may simply have found it easier to stop."})
b.reading("yousefzadeh-fard-2013",
          nulls=N(natural_history=("Unlikely", "Long-standing use."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Unlikely", "Documented use."),
                  cointervention=("Possible", "Hospitalisation and medical advice; all groups cut down."),
                  nonspecific=("Possible", "All three groups reduced use after stroke."),
                  expectancy=("Unlikely", "No treatment."),
                  reporting=("Possible", "Self-reported use; 8 patients in the key group.")),
          verdict="Beats the null",
          note="The opioid echo of Naqvi: right insular strokes freed most opium users from the habit. Eight patients, self-report and a baseline imbalance keep confidence down.",
          hyps=[H("The insula carries the interoceptive urge that drives use; damage removes it.",
                  "Insular infarct → loss of interoceptive representation of drug effects and craving → use stops or falls without effort",
                  ["Lesion disconnection", "Interoceptive and visceral input"], "Fits",
                  "Same pattern and same right-sided lean as Naqvi's smokers.",
                  "Tiny group, baseline imbalance.",
                  "Moderate", "Eight insula patients; lighter users at baseline.",
                  "Larger prospective cohorts with verified abstinence and lesion mapping.")],
          related=[("naqvi-2007", "Insula damage disrupting smoking addiction"),
                   ("jing-2021", "Dorsal striatal infarcts and smoking")])

b.save()
