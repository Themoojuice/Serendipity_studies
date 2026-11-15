"""Batch 2026-11-15: unsure pile, part 3 (protocol v1.7.4): PDFs Brendan downloaded himself through CKN.

Brendan supplied five PDFs (read locally, not committed): Benazzi 1993 and Khouzam 1996 (both on the unsure list),
Patten 1991 (captopril-induced mania; he grabbed it instead of Deicken 1986), Boyd & Weissman 1981 (epidemiology review)
and Torrey & Davis 2012 (review of repurposed drugs for schizophrenia and bipolar disorder). The Torrey review's text
settles Levine 1996's indication (minocycline for sinusitis) and adds two leads from its reference list.

Result: 2 cases (Benazzi 1993: etizolam for the anxiety caused by 15 years of voices, voices gone, three on-off-on
cycles; Levine 1996: depression in bipolar disorder improving on minocycline for sinusitis), Khouzam 1996 excluded (E4),
logged rows for the supplied papers and the Torrey leads (Miyaoka 2007 E3; Chouinard 1987 unsure, letter).
Run from the repo root:  python3 scripts/batches/b2026_11_15_unsure_fulltext_v3.py
"""
import csv
import json
import sys

sys.path.insert(0, "scripts")
from lib_add import CASES, LEDGER, U, Ledger, add_records  # noqa: E402

TODAY = "2026-11-15"
OTHER = "Treatment for another condition"
QID, SRC = "BRENDAN_PDFS_2026_11_15", "Supplied by Brendan"
cand = {
    "benazzi-1993": dict(pmid="7902201", pmcid="", doi="10.1177/070674379303800810",
                         title="Auditory hallucinations suppressed by etizolam in a patient with schizophrenia.",
                         authorString="Benazzi F, Mazzoli M, Rossi E", journal="Can J Psychiatry", year=1993, vol="38", issue="8",
                         pages="574-5", lang="eng"),
    "levine-1996": dict(pmid="8599421", pmcid="", doi="10.1176/ajp.153.4.582b", title="Possible antidepressant effect of minocycline.",
                        authorString="Levine J, Cholestoy A, Zimmerman J", journal="Am J Psychiatry", year=1996, vol="153",
                        issue="4", pages="582", lang="eng"),
}
R = [
    dict(id="benazzi-1993", src="benazzi-1993", design="Letter", n=1, cats=["Psychotic"],
         spec="Persistent accusatory second-person auditory hallucinations in a 32-year-old woman with 15 years of schizophrenia, "
              "unchanged by years of depot fluphenazine and haloperidol", chronic=True, tr=True,
         tcat="Medication for another condition", tspec="Etizolam 2 mg/day added for the anxiety the voices caused",
         intent=OTHER, res="Complete", rev="On-off rechallenge", dl=1,
         era=("emerging", "Reviews of the time suggested benzodiazepines could have antipsychotic effects as add-ons; etizolam "
                          "itself had not been reported (the authors found nothing)."),
         summary="A 32-year-old woman whose accusing voices had outlasted years of depot antipsychotics was given etizolam for the "
                 "anxiety they caused; to her doctors' surprise the voices went within a week, came back each time the drug was "
                 "stopped and went again when it was restarted, three times over, and estazolam could not stand in for it.",
         caveat="Reviews of the day already credited benzodiazepines with some antipsychotic effect, so the surprise was the drug more than the class.",
         tags=["etizolam", "thienodiazepine", "benzodiazepine", "auditory-hallucinations", "schizophrenia", "rechallenge"], tier="B"),
    dict(id="levine-1996", src="levine-1996", design="Letter", n=1, cats=["Mood"],
         spec="Depression in a woman with bipolar disorder", chronic=None, tr=None, tcat="Medication for another condition",
         tspec="Minocycline 150 mg/day for sinusitis", intent=OTHER, res="Partial", rev="None reported", dl=2,
         era=("emerging", "Minocycline was later tested as an antidepressant in small trials, pooled in a 2017 meta-analysis "
                          "(Rosenblat and McIntyre); not standard treatment."),
         summary="A woman with bipolar disorder whose depression improved markedly while she took minocycline for sinusitis; "
                 "the first report of the antidepressant effect later tested in trials.",
         caveat="The sinus infection itself may have been deepening her depression, so clearing it could have lifted her mood without any direct drug effect.",
         tags=["minocycline", "antibiotic", "bipolar-depression", "sinusitis", "inflammation"], tier="C"),
]
SETTLE = {
    "R065949": "benazzi-1993",
    "R058978": "levine-1996",
    "R065987": ("E4", "full text (supplied): mania and hallucinations largely from a benztropine overdose; physostigmine was the "
                      "antidote, and its brief antimanic effect was already known"),
}
VERIFIED = {"benazzi-1993": f"{TODAY}: full text read (PDF supplied by Brendan via CKN); identifiers from Europe PMC",
            "levine-1996": f"{TODAY}: letter not read; indication (minocycline for sinusitis) and outcome from the Torrey & Davis "
                           f"2012 review (supplied by Brendan); identifiers from Europe PMC"}
LOG = [  # supplied papers and Torrey reference-list leads
    dict(doi="", pmid="", title="Manic symptoms associated with the use of captopril", au="Patten", yr=1991, jn="Can J Psychiatry",
         dec=("E4", "captopril-induced mania resolving when captopril was stopped (supplied PDF)")),
    dict(doi="", pmid="", title="Epidemiology of affective disorders. A reexamination and future directions", au="Boyd", yr=1981,
         jn="Arch Gen Psychiatry", dec=("E7", "epidemiology review (supplied PDF)")),
    dict(doi="", pmid="", title="Adjunct treatments for schizophrenia and bipolar disorder: what to try when you are out of ideas",
         au="Torrey", yr=2012, jn="Clin Schizophr Relat Psychoses",
         dec=("E7", "review of repurposed drugs (supplied PDF); reference list mined: Levine 1996, Miyaoka 2007, Chouinard 1987")),
    dict(doi="10.1016/j.pnpbp.2006.08.013", pmid="17030375", title="Possible antipsychotic effects of minocycline in patients with schizophrenia.",
         au="Miyaoka", yr=2007, jn="Prog Neuropsychopharmacol Biol Psychiatry",
         dec=("E3", "minocycline given to two catatonic schizophrenia patients with its neuroprotective rationale in view")),
    dict(doi="10.1176/ajp.144.6.826a", pmid="3592013", title="Estrogen-progesterone combination: another mood stabilizer?",
         au="Chouinard", yr=1987, jn="Am J Psychiatry",
         dec=(U, "letter, no abstract: two lithium-resistant bipolar women responding to estrogen-progesterone; given for contraception or for mood?")),
]


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1f", found_via="unsure pile, full-text appraisal", today=TODAY)
    d = json.loads(CASES.read_text())
    for r in d["records"]:
        if r["id"] in VERIFIED:
            r["verified"] = VERIFIED[r["id"]]
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    rows = list(csv.DictReader(LEDGER.open()))
    sup = {r["supersedes"] for r in rows if r["supersedes"]}
    by_id = {r["record_id"]: r for r in rows}
    L = Ledger(TODAY)
    for rid, dec in SETTLE.items():
        old = by_id[rid]
        assert old["decision"] == "unsure" and rid not in sup, rid
        row = L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=rid,
                    note=f"was unsure; settled from the full text or a review supplied by Brendan; {TODAY}")
        row["screen_stage"] = "ft"
    for x in LOG:
        row = L.add(SRC, QID, x["dec"], doi=x["doi"], pmid=x["pmid"], title=x["title"], au=x["au"], yr=x["yr"], jn=x["jn"],
                    other=f"supplied:{x['au'].lower()}{x['yr']}", note=f"{TODAY}")
    L.write()
