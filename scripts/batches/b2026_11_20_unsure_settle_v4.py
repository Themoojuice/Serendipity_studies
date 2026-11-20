"""Batch 2026-11-20: unsure pile, part 4 (protocol v1.7.4), Brendan signed in to CKN.

Read one at a time: ClinicalKey (Biol Psychiatry x3, Semin Pediatr Neurol, Lancet), EBSCO through LibKey (Neurocase),
PMC page scans from a cdn.ncbi.nlm.nih.gov tab with local OCR (BMJ 1881 and 1897, West J Med Surg 1845,
Buffalo Med Surg J 1888, Hospital 1902), and Cambridge's open European Psychiatry archive (Granato 1994, found
through Embase's record and Crossref).

Result: 4 cases (D'Andrea & Sewell 2013 ketamine for depression lifting chronic PTSD for two weeks; Macleod 1897
accidental bromide poisoning ending a seven-year morphine habit; the 1888 Norristown typhoid epidemic curing
chronic melancholia; Granato 1994 midazolam for an MRI lifting stuporous depression), 8 exclusions.
Not reachable tonight: Psychiatry Online (Cloudflare), SAGE, Wiley, Lippincott, the HARCP archive (reader login),
non-English 1960s journals; those rows stay unsure.
Run from the repo root:  python3 scripts/batches/b2026_11_20_unsure_settle_v4.py
"""
import csv
import json
import sys

sys.path.insert(0, "scripts")
from lib_add import CASES, LEDGER, Ledger, add_records  # noqa: E402

TODAY = "2026-11-20"
OTHER = "Treatment for another condition"
cand = {
    "d-andrea-2013": dict(pmid="23706680", pmcid="", doi="10.1016/j.biopsych.2013.04.019",
                          title="Transient resolution of treatment-resistant posttraumatic stress disorder following ketamine infusion.",
                          authorString="D'Andrea D, Sewell RA", journal="Biol Psychiatry", year=2013, vol="74", issue="9",
                          pages="e13-4", lang="eng", abs=True),
    "macleod-1897": dict(pmid="20757136", pmcid="PMC2407258", doi="10.1136/bmj.2.1906.76",
                         title="Morphine Habit of Long Standing Cured by Bromide Poisoning.", authorString="Macleod N",
                         journal="Br Med J", year=1897, vol="2", issue="1906", pages="76-77", lang="eng"),
    "anon-1888-typhoid": dict(pmid="36668278", pmcid="PMC9474001", doi="", title="The Influence of Typhoid Fever upon Insanity.",
                              authorString="Anonymous", journal="Buffalo Med Surg J", year=1888, vol="27", issue="6",
                              pages="275-276", lang="eng"),
    "granato-1994": dict(pmid="", pmcid="", doi="10.1017/s0924933800002376", title="Midazolam improvement of severe mood disorder",
                         authorString="Granato P, Parquet JP, Goudemand M", journal="Eur Psychiatry", year=1994, vol="9",
                         issue="6", pages="318", lang="eng"),
}
R = [
    dict(id="d-andrea-2013", src="d-andrea-2013", design="Letter", n=1, cats=["Trauma & stressor-related"],
         spec="Severe chronic combat PTSD in a 23-year-old veteran, unchanged by three admissions, exposure therapy, EMDR and ten drugs",
         chronic=True, tr=True, tcat="Medication for another condition",
         tspec="A single ketamine infusion (35 mg with propofol) given for treatment-resistant depression",
         intent=OTHER, res="Temporary", rev="Natural off-on", dl=2,
         era=("emerging", "Perioperative ketamine and later PTSD had mixed reports; the first ketamine trial in PTSD was under way "
                          "(Feder 2014) and esketamine later entered PTSD trials."),
         summary="A veteran with years of severe, treatment-resistant combat PTSD was given one ketamine infusion for depression; "
                 "within hours he was affectionate and calm, nightmares and hyperarousal gone (PTSD checklist 66 to 29), and two "
                 "weeks later it all came back within a day.",
         caveat="Depression and PTSD lifted together, so the PTSD change may ride on the antidepressant effect.",
         tags=["ketamine", "PTSD", "veteran", "NMDA", "transient", "depression"], tier="C"),
    dict(id="macleod-1897", src="macleod-1897", design="Case series", n=2, cats=["Substance & addictive"],
         spec="Morphine habit of seven years in a woman of 32, after injections for neuralgia, despite repeated slow withdrawals",
         chronic=True, tr=True, tcat="Medication for another condition",
         tspec="Sodium bromide for migraine and nervous irritability, taken to the point of bromide poisoning by mistake",
         intent="Medication error", res="Complete", rev="None reported", dl=1,
         era=("emerging", "Bromide 'sleep' and deep-narcosis treatments of morphinism were tried around 1900 and abandoned; "
                          "nothing like it is used now."),
         summary="In Shanghai in 1896 a woman with a seven-year morphine habit was given sodium bromide for migraine and slid into "
                 "bromide poisoning; after two weeks of delirium she woke with no desire for morphine, to her own and the "
                 "nurses' astonishment. Her doctor then tried it on purpose in a pilot, who also lost the craving.",
         caveat="The second, deliberate case shows the doctor's interest; the first rests on a single follow-up of about a year.",
         tags=["bromide", "morphine", "opioid", "delirium", "accidental", "antique"], tier="C",
         flags=["antique-bar"]),
    dict(id="anon-1888-typhoid", src="anon-1888-typhoid", design="Case series", n=3, cats=["Mood"],
         spec="Chronic melancholia of several years in a woman of about 50, an asylum inpatient (and two younger patients with mania)",
         chronic=True, tr=None, tcat="Fever / infection",
         tspec="Typhoid fever during an outbreak at the State Hospital for the Insane, Norristown, Pennsylvania",
         intent="Injury or illness", res="Complete", rev="None reported", dl=1,
         era=("emerging", "Intercurrent fever ending insanity was a recurring 19th-century observation and led to Wagner-Jauregg's "
                          "fever therapy (1917); fever in modern psychiatric illness is anecdotal."),
         summary="During a typhoid outbreak at the Norristown asylum in 1888, a woman with several years of chronic melancholia "
                 "caught the fever and was discharged perfectly well; a young man in his second attack of mania also went home well.",
         caveat="A reprinted news item from the Medical and Surgical Reporter; the manic patients were already improving.",
         tags=["typhoid", "fever", "melancholia", "asylum", "antique", "infection"], tier="C", flags=["antique-bar"]),
    dict(id="granato-1994", src="granato-1994", design="Letter", n=1, cats=["Mood", "Catatonia"],
         spec="Severe depression of 15 months in a 70-year-old man, stuporous and mute for the last 8, resistant to antidepressants; "
              "too cachectic for ECT", chronic=True, tr=True, tcat="Medication for another condition",
         tspec="Intravenous midazolam 5 mg to sedate him for an MRI", intent=OTHER, res="Partial", rev="None reported", dl=1,
         era=("emerging", "Benzodiazepines were known to lift catatonic stupor by 1994 (lorazepam challenge), but not to relieve "
                          "depression itself."),
         summary="A 70-year-old with 15 months of antidepressant-resistant depression, mute and stuporous for months, was given "
                 "midazolam to sedate him for an MRI; the next day his mood, speech and behaviour had improved spectacularly, "
                 "and he was still better ten days later.",
         caveat="Benzodiazepines lift catatonic stupor, so the depressive core may not have changed; amineptine had been started four weeks earlier.",
         tags=["midazolam", "benzodiazepine", "stupor", "depression", "MRI", "catatonia"], tier="C"),
]
HIST = {
    "macleod-1897": {"original_terms": "Morphine habit", "modern_reading": "Opioid use disorder (iatrogenic, injected)",
                     "why_read": "An accidental poisoning that a doctor then tried to reproduce: the shape of many deliberate therapies that followed."},
    "anon-1888-typhoid": {"original_terms": "Chronic melancholia; acute mania", "modern_reading": "Chronic depression; manic episodes",
                          "why_read": "One of the asylum fever cures that led, 30 years on, to malaria therapy."},
}
OBSERVED = {"macleod-1897": 1896, "anon-1888-typhoid": 1888}
VERIFIED = {
    "d-andrea-2013": f"{TODAY}: full text read (ClinicalKey through CKN)",
    "macleod-1897": f"{TODAY}: full text read (PMC page scans, OCR)",
    "anon-1888-typhoid": f"{TODAY}: full text read (PMC page scans, OCR)",
    "granato-1994": f"{TODAY}: full text read (Cambridge open archive)",
}
SETTLE = {
    "R023588": "d-andrea-2013", "R061088": "d-andrea-2013", "R065544": "d-andrea-2013",
    "R059292": "macleod-1897", "R059264": "anon-1888-typhoid", "R059923": "granato-1994",
    "R023570": ("E3", "full text (ClinicalKey): pramipexole was chosen to correct a measured dopamine-synthesis deficit and treat her symptoms"),
    "R047684": ("E1", "full text (ClinicalKey): first words in two non-verbal children with epileptic encephalopathy after VNS for seizures; language gain, not a psychiatric syndrome"),
    "R049657": ("E2", "full text (EBSCO): bulimia unchanged after COVID smell and taste loss (EDE-Q unchanged; craving rose)"),
    "R068547": ("E3", "full text (ClinicalKey): voices in substance users managed deliberately without antipsychotics; the author's point is that they settle"),
    "R066153": ("E4", "full text (ClinicalKey): the authors attribute the refractory depression to myasthenia gravis; it lifted as the myasthenia was treated"),
    "R059208": ("E3", "full text (PMC scan): the trephine was applied to cure him (a suspected depressed fracture); a reprinted anecdote"),
    "R059255": ("E2", "full text (PMC scan, OCR): an outbreak report; no change in any patient's insanity is described"),
    "R059304": ("E7", "full text (PMC scan, OCR): an editorial summarising Warren, Brooklyn Med J, April 1902, on acute disease and insanity; chase Warren"),
}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1f", found_via="unsure pile, full-text appraisal", today=TODAY)
    d = json.loads(CASES.read_text())
    for r in d["records"]:
        if r["id"] in VERIFIED:
            r["verified"] = VERIFIED[r["id"]]
        if r["id"] in HIST:
            r["historical"] = HIST[r["id"]]
            r["collections"] = ["antique"]
            r["observed_year"] = OBSERVED[r["id"]]
        if r["id"] == "granato-1994":
            r["links"]["full_text"] = "https://www.cambridge.org/core/journals/european-psychiatry/article/midazolam-improvement-of-severe-mood-disorder/4EA4330E18D33559D914DE09469D9D91"
            r["access"] = "Free full text"
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    rows = list(csv.DictReader(LEDGER.open()))
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    by_id = {r["record_id"]: r for r in rows}
    L = Ledger(TODAY)
    for rid, dec in SETTLE.items():
        old = by_id[rid]
        assert old["decision"] == "unsure" and rid not in sup, rid
        row = L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=rid,
                    note=f"was unsure; settled from the full text; {TODAY}")
        row["screen_stage"] = "ft"
    L.write()
