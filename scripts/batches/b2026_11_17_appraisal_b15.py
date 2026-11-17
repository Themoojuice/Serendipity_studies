"""Full-text appraisal, batch 15 (2026-11-17): xie-2026 (right amygdala radiofrequency ablation for epilepsy; PTSD)."""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-17", source="PMC open-access full text, via Europe PMC")

b.code("xie-2026",
       tracks=[track("41-year-old man", 41, "M", [
           ev("onset", -25, "years", "Severe PTSD after civilian trauma in adolescence; refractory temporal lobe epilepsy", "approx"),
           ev("assessment", -2, "weeks", "Before admission: severe PTSD; fearful reading of ambiguous faces exceeds 16 epilepsy controls; right lateral amygdala late ERPs separate fearful from happy faces", "approx",
              scores=[{"scale": "PCL-5", "value": 50, "higher_is_better": False}]),
           ev("exposure_start", 0, "days", "SEEG-guided radiofrequency ablation of the right amygdala, for seizures"),
           ev("first_change", 1, "days", "Fear bias on the face task reduced; amygdala and network late ERPs fall in step", "at most", state="Partial"),
           ev("best_response", 2, "months", "PTSD much improved, especially hyperarousal and reactivity; less awareness of tachycardia and auras; seizure frequency unchanged", state="Partial",
              note="Post-ablation PCL-5, BAI and BDI-II shown in a figure."),
           ev("cointervention", 2, "months", "Laser ablation of right hippocampus and entorhinal cortex for the seizures"),
           ev("follow_up", 6, "months", "Authors describe the PTSD improvement as persistent", "approx", state="Partial"),
       ])],
       unexpectedness=T(era=("borderline", "Prospective replication of Bijanki 2020: the team expected and measured the PTSD effect.")),
       attribution=A(1, 1, 1, 0, 1, "PCL-5 before and two months after; face-task bias before and after; seizure frequency unchanged, so relief isn't simply better seizure control."),
       jbi=J("YYYYYYUY"),
       lesion={"kind": "Resection or ablation", "side": "Right", "regions": ["Temporal, medial (amygdala, hippocampus)"],
               "specific": "Right amygdala (lateral nucleus sampled), radiofrequency ablation through SEEG contacts; hippocampus and entorhinal cortex ablated two months later",
               "aetiology": "Surgery", "imaging": "MRI", "mappable": "Figure"},
       fix={"tier": "A"})
b.reading("xie-2026",
          nulls=N(natural_history=("Unlikely", "PTSD for about 25 years."),
                  regression=("Unlikely", "Chronic."),
                  misdiagnosis=("Unlikely", "PCL-5 severe; behavioural bias measured."),
                  cointervention=("Possible", "Hospital admission, medication withdrawal for monitoring; hippocampal ablation only after the 2-month rating."),
                  nonspecific=("Unlikely", "The bias change was specific to fearful faces."),
                  expectancy=("Possible", "A research team expecting PTSD relief, and a patient aware of the hypothesis."),
                  reporting=("Unlikely", "Standard scales, a behavioural task and neural recordings.")),
          verdict="Beats the null",
          note="The best-instrumented case in the library: behaviour, scalp and intracranial signals before and after, with seizures unchanged. The cost is that the team expected the result, which is why it is a replication rather than a serendipity.",
          hyps=[H("The right amygdala drove threat interpretation; ablating it removed the bias and the hyperarousal that rests on it.",
                  "Right lateral amygdala hyper-responsive to fear → negative interpretation bias and arousal → ablation → bias and arousal fall, late ERPs fall in step",
                  ["Lesion disconnection", "Threat and arousal"], "Fits",
                  "Bias and neural signal dropped together immediately; hyperarousal cluster improved most; left amygdala didn't show the signal.",
                  "Two months of follow-up before a second ablation muddles the long term.",
                  "High", "One patient, team expecting the result.",
                  "Prospective PCL-5 in all patients with PTSD having amygdala ablation for epilepsy.")],
          related=[("bijanki-2020", "The original right amygdala ablation PTSD case")])

b.save()
