"""Schema 1.4 worked examples (2026-11-16): two cases coded in full from their PMC full texts.

  maddigan-2004   mania clearing during febrile influenza (letter; Can Child Adolesc Psychiatr Rev)
  oh-2011         OC behaviour ending after a left capsular genu infarct (Case Rep Neurol)

Each gets a timeline, the scored appraisal (protocol sections 2, 4, 5), a lesion block where it applies,
and a draft hypothesis entry in data/hypotheses.json. Claude read both full texts on the PMC pages through
its web reader, not the PDFs; Brendan to check. Grootendorst-van Mil 2018 was the intended third example,
but PMC served a captcha and the publisher page would not load.

Run from the repo root, then:  python3 scripts/derive.py && python3 scripts/validate_cases.py
"""
import json
from pathlib import Path

CASES = Path("data/cases.json")
HYP = Path("data/hypotheses.json")
TODAY = "2026-11-16"
d = json.loads(CASES.read_text())
by = {r["id"]: r for r in d["records"]}


def ev(kind, t, unit, label, precision="exact", **kw):
    e = {"kind": kind, "t": t, "unit": unit, "precision": precision, "label": label}
    e.update(kw)
    return e


# ---------------------------------------------------------------- maddigan-2004 (t = 0: fever, admission day 19)
r = by["maddigan-2004"]
r["timeline"] = [{
    "patient": "Ms B.", "age": 14, "sex": "F",
    "events": [
        ev("cointervention", -109, "days", "Venlafaxine switched to paroxetine; lorazepam as needed (3 months before admission)", "approx"),
        ev("onset", -25, "days", "Insomnia, overactivity, psychotic symptoms (a week before admission)", "approx"),
        ev("assessment", -18, "days", "Admitted with psychotic mania and suicidal thoughts"),
        ev("treatment_failed", -18, "days", "Risperidone 0.75 mg twice daily with divalproex and temazepam"),
        ev("cointervention", -11, "days", "Benztropine for stiffness; visual hallucinations followed; risperidone and benztropine stopped", "approx"),
        ev("treatment_failed", -11, "days", "Chlorpromazine (150 mg a day by day 18) with divalproex 500 mg twice daily; still manic", "approx"),
        ev("exposure_start", 0, "days", "Fever 38.8 °C; influenza B on throat swab"),
        ev("cointervention", 1, "days", "All medicines held: acute hepatitis with jaundice; IV fluids"),
        ev("best_response", 2, "days", "Mental state all but normal: no delusions or hallucinations, insight back; mild pressure of speech", "at most", state="Partial"),
        ev("relapse", 4, "days", "Manic symptoms back"),
        ev("cointervention", 4, "days", "Lithium started, oxazepam added"),
        ev("follow_up", 58, "days", "Discharged on lithium, mania well controlled (about 2½ months after admission; the date is garbled in the text)", "approx", state="Remitted"),
    ],
}]
r["outcome"]["reversal"] = "None reported"
r["caveat"] = ("All medicines were held the day after the fever began, and the paper never says when the fever ended, "
               "so neither the improvement nor the return of mania can be pinned on the fever.")
r["verified"] = f"{TODAY}: full text read (PMC page, through Claude's web reader); identifiers from PubMed"
r["appraisal"] = {
    "basis": "Full text", "date": TODAY, "by": "Claude",
    "unexpectedness": {
        "target": {"result": "pass", "note": ""},
        "era": {"result": "pass", "note": ""},
        "secondary": {"result": "borderline", "note": "Paroxetine began three months before and visual hallucinations followed benztropine, so part of the picture may have been drug-induced."},
        "base_rate": {"result": "borderline", "note": "A four-week episode in a 14-year-old can fluctuate; the window is two days."},
    },
    "attribution": {"baseline": 0, "measure": 0, "timing": 1, "reversal": 0, "confounders": 0,
                    "note": "Mania returned on day 23, but the fever's end isn't reported, so the return can't be tied to the exposure stopping (outcome.reversal recoded from Natural off-on)."},
    "jbi": {"checklist": "Case report", "answers": ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "U"]},
    "note": "Criterion 1 is doubtful: a first manic episode about four weeks old, with two short antipsychotic trials. Left Provisional for Brendan.",
}

# ---------------------------------------------------------------- oh-2011 (t = 0: stroke onset)
r = by["oh-2011"]
r["timeline"] = [{
    "patient": "74-year-old woman", "age": 74, "sex": "F",
    "events": [
        ev("onset", -6, "years", "Cleaning, hand-washing, white gloves outdoors; daily milk, cold medicine and herbal pills (family report)", "approx", to=-5),
        ev("exposure_start", 0, "days", "Left internal capsule genu infarct: sudden memory loss and odd behaviour"),
        ev("first_change", 0, "days", "Family: the rituals stopped abruptly with the stroke", "approx"),
        ev("assessment", 9, "days", "First seen (CT on day 10): memory, language and executive deficits, little speech or facial expression; still wearing her gloves", state="Partial"),
        ev("follow_up", 4, "months", "No gloves; rituals still absent (the only follow-up)", state="Remitted"),
    ],
}]
r["lesion"] = {"kind": "Lesion", "side": "Left", "regions": ["Internal capsule"],
               "specific": "Genu of the left internal capsule (low density on CT, shown in figure 1)",
               "aetiology": "Ischaemic stroke", "imaging": "CT", "mappable": "Figure"}
r["verified"] = f"{TODAY}: full text read (PMC page, through Claude's web reader); identifiers from Europe PMC"
r["appraisal"] = {
    "basis": "Full text", "date": TODAY, "by": "Claude",
    "unexpectedness": {
        "target": {"result": "pass", "note": ""},
        "era": {"result": "pass", "note": ""},
        "secondary": {"result": "borderline", "note": "Onset around 68 with hypertension and diabetes: late-onset OC behaviour is often secondary to brain disease, and the cold-medicine habit may be dependence rather than compulsion."},
        "base_rate": {"result": "pass", "note": ""},
    },
    "attribution": {"baseline": 1, "measure": 0, "timing": 1, "reversal": 0, "confounders": 1,
                    "note": "Medicines, infection and dehydration ruled out; abulia and amnesia argued away rather than assessed."},
    "jbi": {"checklist": "Case report", "answers": ["Y", "U", "Y", "Y", "Y", "Y", "Y", "Y"]},
    "note": "",
}

d["updated"] = TODAY
CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

# ---------------------------------------------------------------- hypotheses
H = json.loads(HYP.read_text())
H["entries"] = [e for e in H["entries"] if e["case_id"] not in ("maddigan-2004", "oh-2011")]
H["entries"] += [
    {
        "case_id": "maddigan-2004", "status": "draft", "written_by": "Claude", "date": TODAY, "based_on": "Full text",
        "nulls": {
            "natural_history": {"rating": "Possible", "why": "Adolescent mania can swing within days; a two-day lull mid-episode is possible with no trigger."},
            "regression": {"rating": "Unlikely", "why": "She was getting worse, and the change was abrupt and brief rather than a drift back."},
            "misdiagnosis": {"rating": "Possible", "why": "Paroxetine started three months earlier, and visual hallucinations followed benztropine: some of the picture may have been drug-induced."},
            "cointervention": {"rating": "Likely", "why": "Every medicine was stopped the day before she improved, and she had acute hepatitis on IV fluids."},
            "nonspecific": {"rating": "Possible", "why": "A febrile, vomiting, jaundiced teenager does less anyway, though restored insight and no delusions are more than lethargy."},
            "expectancy": {"rating": "Unlikely", "why": "Nothing was offered as a treatment."},
            "reporting": {"rating": "Possible", "why": "A letter: no rating scales, one team's impressions, a garbled discharge date."},
        },
        "verdict": "Doesn't beat the null",
        "verdict_note": "Stopping every medicine the day before is a co-intervention no single case can separate from the fever. It earns its place by its shape: abrupt clearing during an acute infection and a return within two days, like the 1844 pleuropneumonia case and Setsaas 2014.",
        "hypotheses": [
            {
                "claim": "The infection damped the mania for as long as she was ill, through cytokine-driven sickness behaviour.",
                "chain": "Influenza B → interferon, IL-1 and IL-6 surge → less drive and arousal, more sleep → mania damped → back as the illness passes",
                "mechanisms": ["Sickness behaviour", "Inflammation and cytokines"],
                "latency_fit": "Fits",
                "for": "Change within two days of the fever; short-lived; the same shape as other intercurrent-infection cases.",
                "against": "Insight came back and the delusions went, which sickness behaviour alone doesn't usually do.",
                "confidence": "Low",
                "uncertainty_driver": "No fever curve: we can't tell whether mania returned as the fever settled (for) or while she was still febrile (against).",
                "test": "In this or a similar case, mania returning as temperature and inflammatory markers fall, with no medication change.",
            },
            {
                "claim": "Holding the medicines cleared a drug-induced layer (anticholinergic load, possible antidepressant activation); the mania underneath came back without antimanic cover.",
                "chain": "Chlorpromazine, diphenhydramine and earlier benztropine plus paroxetine → hallucinations and activation on top of mania → all held on day 20 → that layer clears → core mania back by day 23",
                "mechanisms": ["Acetylcholine", "Serotonin"],
                "latency_fit": "Fits",
                "for": "Visual hallucinations began after benztropine; improvement came the day after everything stopped.",
                "against": "Mania came back while she was still off every medicine; paroxetine's effects outlast a one-day hold.",
                "confidence": "Low",
                "uncertainty_driver": "No drug levels and no delirium assessment, so the size of any drug-induced layer is unknown.",
                "test": "Mental state notes separating delirium features (attention, orientation) from manic ones before and after the hold.",
            },
            {
                "claim": "Fever or immune activation has a specific antimanic effect, the idea behind fever therapy.",
                "chain": "Fever → heat-shock or immune signalling → transient change in mood circuits → mania lifts while febrile",
                "mechanisms": ["Fever and heat", "Inflammation and cytokines"],
                "latency_fit": "Fits",
                "for": "Matches the library's other intercurrent-fever cases with mania (1844 pleuropneumonia; Setsaas 2014).",
                "against": "In one case it can't be told apart from the first hypothesis; its only edge is that insight returned.",
                "confidence": "Low",
                "uncertainty_driver": "One case, no fever curve and a simultaneous drug hold: nothing separates a specific immune effect from being unwell.",
                "test": "Across the library's fever cases: does improvement track temperature, illness severity, or neither?",
            },
        ],
        "related": [
            {"id": "setsaas-2014", "why": "Treatment-resistant mania settling during recurrent fevers"},
            {"id": "anon-1844-pleuropneumonia", "why": "Acute mania cured during pleuropneumonia"},
            {"id": "zuschlag-2016", "why": "Schizoaffective psychosis improving with bacteraemia and high fever"},
            {"id": "wagner-jauregg-1883", "why": "The founding intercurrent-fever observation"},
        ],
        "questions": "Is criterion 1 met? A four-week first manic episode with two short trials is below the protocol's chronic or treatment-resistant bar.",
    },
    {
        "case_id": "oh-2011", "status": "draft", "written_by": "Claude", "date": TODAY, "based_on": "Full text",
        "nulls": {
            "natural_history": {"rating": "Unlikely", "why": "Five or six years of rituals stopping on the day of a stroke."},
            "regression": {"rating": "Unlikely", "why": "No peak at presentation; the change was abrupt."},
            "misdiagnosis": {"rating": "Possible", "why": "Onset around 68, no diagnosis, no scale, no treatment; five or six bottles of cold medicine a day looks as much like habitual use as compulsion."},
            "cointervention": {"rating": "Unlikely", "why": "No new medicines and nothing else changed."},
            "nonspecific": {"rating": "Likely", "why": "She couldn't recall breakfast, said she knew nothing, and had little speech or facial expression: genu infarcts cause amnesia and abulia, and someone who initiates less and forgets more drops rituals along with everything else."},
            "expectancy": {"rating": "Unlikely", "why": "Nothing to expect from."},
            "reporting": {"rating": "Possible", "why": "Family report only; she still wore her gloves at day 10, against the 'abrupt' stop."},
        },
        "verdict": "Doesn't beat the null",
        "verdict_note": "The timing is striking, but the documented amnesia and loss of drive explain the change without anything OCD-specific. Drive and memory were never re-measured at 4 months, the one measurement that would have decided it.",
        "hypotheses": [
            {
                "claim": "A strategic thalamocortical disconnection took away drive and memory, and the rituals went with other self-started behaviour.",
                "chain": "Genu infarct → cuts the anterior and inferior thalamic peduncles (thalamus to frontal cortex) → abulia and amnesia → fewer self-initiated acts, rituals included",
                "mechanisms": ["Lesion disconnection", "Global suppression (sedation, apathy, cognitive loss)"],
                "latency_fit": "Fits",
                "for": "Amnesia, reduced speech and facial expression documented; the recognised capsular genu syndrome.",
                "against": "Daily activities were said to be relatively preserved, and the rituals were still gone at 4 months, when abulia often eases.",
                "confidence": "Moderate",
                "uncertainty_driver": "Apathy and memory weren't re-measured at 4 months, so we don't know whether drive recovered while the rituals stayed away.",
                "test": "Rituals still absent after drive and memory recover points to the second hypothesis; rituals returning as apathy lifts confirms this one.",
            },
            {
                "claim": "The infarct interrupted the orbitofrontal-thalamic loop that sustains compulsions, a natural capsulotomy (the authors' reading).",
                "chain": "Genu lies beside the anterior limb targeted by capsulotomy → frontothalamic fibres cut → loop activity damped → compulsions stop",
                "mechanisms": ["Lesion disconnection"],
                "latency_fit": "Can't judge",
                "for": "Close to the capsulotomy target; still gone at 4 months; the library's other OCD-ending lesions sit in the same loop (putamen, thalamus, frontal).",
                "against": "Genu, not anterior limb; no scale; the diagnosis is uncertain; the global deficits explain the change without it.",
                "confidence": "Low",
                "uncertainty_driver": "The OCD diagnosis itself is uncertain (no criteria, no scale), so even a specific effect may not be an effect on OCD.",
                "test": "Lesion network mapping from the published CT figure: does it connect to the same network as the library's other OCD-ending lesions?",
            },
        ],
        "related": [
            {"id": "erbay-2022", "why": "Refractory OCD remitting after a thalamic infarct"},
            {"id": "yaryura-tobias-2003", "why": "Severe OCD ending after a left basal ganglia haemorrhage"},
            {"id": "fujii-2005", "why": "15-year OCD ending after a left putaminal haemorrhage"},
            {"id": "gerken-2022", "why": "Contamination OCD ending after a basal ganglia stroke"},
        ],
        "questions": "Was the daily cold-medicine intake compulsion or dependence? If dependence, this is partly a substance case.",
    },
]
H["updated"] = TODAY
HYP.write_text(json.dumps(H, ensure_ascii=False, indent=1) + "\n")
print("worked examples written: maddigan-2004, oh-2011")
