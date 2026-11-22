"""Full-text appraisal, batch 31 (2026-11-22): roadmap step 1a, the free-copy sweep.

OpenAlex was queried from the laptop browser for the 98 uncoded cases and the 30 unsure rows (123 distinct items).
One free full text was readable: Lauritsen & Vinberg 2015 (Ugeskr Laeger, the journal's own PDF), coded here.
Other free copies exist but sit behind bot checks in Claude's browser (Wiley, ScienceDirect, the Edinburgh and Udine
repositories, Turkiye Klinikleri, UNT, psychiatrist.com, Psychiatry Online); they are listed on the full-text page for
Brendan to open in his own browser. OpenAlex also supplied DOIs for five cases listed without one (title and year checked).
"""
import sys
sys.path.insert(0, "scripts")
from lib_code import Batch, ev, track, T, A, J, N, H  # noqa: E402

b = Batch("2026-11-22", source="Full text, the journal's free PDF (ugeskriftet.dk), read in Danish")

LAURITSEN_PDF = "https://content.ugeskriftet.dk/sites/default/files/scientific_article_files/2015-01/artikel_13240.pdf"

b.code("lauritsen-2015",
       tracks=[track("65-year-old man", 65, "M", [
           ev("onset", -3, "years", "Anxiety without a trigger, then gradually deepening depression; one brief episode of depression and anxiety 30 years earlier", "approx"),
           ev("treatment_failed", -3, "years", "SSRIs, SNRIs and psychotherapy; lithium twice (side effects); nortriptyline with level monitoring plus reboxetine; aripiprazole for fatigue (no effect); isocarboxazid at therapeutic dose (side effects). Tertiary affective disorders clinic: treatment-resistant depression", "approx", to=-2),
           ev("assessment", -2, "months", "Off medication for a period: still moderate to severe depression, dominated by fatigue, low drive, overwhelm, mild sadness and tension; dementia, thyroid disease, lung and heart disease and sleep apnoea excluded", "approx"),
           ev("cointervention", -1, "months", "Lamotrigine 150 mg a day; the haemorrhage came 'shortly after'", "approx"),
           ev("exposure_start", 0, "days", "Subarachnoid haemorrhage from a right pericallosal aneurysm (sudden severe headache, no loss of consciousness); aneurysm clipped. Follow-up CT: a small right frontal infarct beside the clip"),
           ev("best_response", 0, "days", "Symptoms vanished promptly after the haemorrhage; discharged from neurosurgery without sequelae and without psychiatric symptoms", "at least", state="Remitted"),
           ev("cointervention", 0, "days", "Stopped the small, occasional cannabis use he disclosed afterwards", "at least"),
           ev("assessment", 15, "months", "Psychiatric outpatient follow-up throughout: full clinical remission; handed back to his GP", state="Remitted"),
           ev("follow_up", 4, "years", "Still symptom-free after the stroke, on lamotrigine 200 mg a day", state="Remitted"),
       ])],
       unexpectedness=T(secondary=("borderline", "The authors raise the unruptured aneurysm itself (mass effect or ischaemia) as a possible cause of the depression.")),
       attribution=A(1, 0, 1, 0, 0, "Three documented years of resistant depression, observed off medication; abrupt remission at the haemorrhage, sustained four years. No scale; lamotrigine was started shortly before and continued, and occasional cannabis stopped."),
       jbi=J("YYYUYYYY"),
       lesion={"kind": "Lesion", "side": "Right", "regions": ["Frontal, other"],
               "specific": "Subarachnoid blood in the basal cisterns and over the corpus callosum from a right pericallosal aneurysm; after clipping, a small right frontal infarct beside the clip (medial frontal, pericallosal territory)",
               "aetiology": "Haemorrhage", "imaging": "CT", "mappable": "Figure"},
       fix={"links.full_text": LAURITSEN_PDF, "access": "Free full text",
            "caveat": "Lamotrigine 150 mg had been started shortly before the haemorrhage and was continued for the four years of remission."},
       note="Full text read in Danish (two pages).")
b.reading("lauritsen-2015",
          nulls=N(natural_history=("Unlikely", "Three years, moderate to severe even when observed off medication."),
                  regression=("Unlikely", "Chronic, not a peak."),
                  misdiagnosis=("Possible", "The authors wonder whether the unruptured aneurysm drove the depression; nothing else organic was found."),
                  cointervention=("Possible", "Lamotrigine reached 150 mg shortly before and was continued; cannabis stopped."),
                  nonspecific=("Unlikely", "Discharged without sequelae; remission, not apathy, held for four years."),
                  expectancy=("Unlikely", "A haemorrhage, not a treatment."),
                  reporting=("Possible", "No rating scale; two-page report.")),
          verdict="Undecided",
          note="Three years of resistant depression stopped at a right pericallosal subarachnoid haemorrhage with a small right frontal infarct, and stayed gone for four years. It joins Etches 2009 and Wilcox 2008. Lamotrigine, started just before and kept going, is the competitor the paper can't rule out.",
          hyps=[H("A small right medial frontal infarct disconnected a depressive circuit.",
                  "Pericallosal haemorrhage → clip-related right medial frontal infarct (pericallosal territory, near the anterior cingulate) → loss of cingulate-prefrontal drive sustaining the depression → remission",
                  ["Lesion disconnection"], "Fits", "Abrupt at the event after three static years; matches other right frontal stroke remissions.",
                  "Infarct site described only as frontal near the clip; no lesion-network data.",
                  "Low", "Lesion location is approximate and lamotrigine overlaps.",
                  "Map the infarct against lesion-network maps of depression remission (Padmanabhan-style)."),
                H("Lamotrigine responded, and the haemorrhage was coincidental.",
                  "Lamotrigine titrated to 150 mg → slow antidepressant effect in resistant depression → remission at about the same time",
                  ["Ion channels and excitability"], "Can't judge", "Within lamotrigine's onset window.",
                  "The change was abrupt at the haemorrhage, and lamotrigine's evidence in unipolar resistant depression is weak.",
                  "Low", "Lamotrigine start date not given.", "Remission durability if lamotrigine were tapered.")],
          related=[("etches-2009", "Bipolar II and panic gone after subarachnoid haemorrhage"), ("wilcox-2008", "Depression cured by a right frontal stroke")])

# DOIs found by OpenAlex for cases listed without one (title and year match checked)
for cid, doi in {"vartian-2004": "10.1097/01.adt.0000129084.99647.20", "curran-1995": "10.1017/s0790966700014543",
                 "yates-1988": "10.1002/1098-108x(198807)7:4<557::aid-eat2260070414>3.0.co;2-r", "puente-1985": "10.1037/h0099655",
                 "kastner-2016": "10.1515/ijdhd-2015-0003"}.items():
    r = b.by_id[cid]
    assert not r["ids"]["doi"], cid
    r["ids"]["doi"] = doi
    r["links"]["doi"] = "https://doi.org/" + doi
    r["links"]["ckn"] = "https://go.openathens.net/redirector/ckn.qldhealth.com?url=" + __import__("urllib.parse").parse.quote("https://doi.org/" + doi, safe="")

b.save()
