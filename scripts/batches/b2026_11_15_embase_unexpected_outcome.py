"""Batch 2026-11-15: Embase via CKN, Emtree 'unexpected outcome of drug treatment' (protocol v1.7.5).

EMB_unexpOutcome_v1 (queries/strings_embase_unexpected_outcome_v1.json): the Emtree term x psychiatric disorder as major
focus x case design x humans (2,381), narrowed to resolution wording and away from drug-induced titles (814 returned).
Matched to the ledger by Embase ID, DOI or normalised title: 579 new, 64 blank, 162 excluded, 9 library cases.
All 643 new or blank titles screened; abstracts read for 16 candidates; one full text (psychiatrist.com, free).

Result: 1 case (Riestra 2026: bupropion for depression, OCD near-absent for 3 years). Most of the set is deliberate
treatment the indexers judged surprising in size, or drug-induced syndromes the title filter missed.
Working files: /home/claude/work/raw/emb3_all.json, emb3_match.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_15_embase_unexpected_outcome.py
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, "scripts")
from lib_add import CASES, Ledger, add_records, log_runs  # noqa: E402

TODAY = "2026-11-15"
SRC, QID = "Embase via CKN", "EMB_unexpOutcome_v1"
M = json.loads(Path("/home/claude/work/raw/emb3_match.json").read_text())
TODO = M["todo"]
RANK = {x[0]: i for i, x in enumerate(TODO)}
OTHER = "Treatment for another condition"

cand = {"riestra-2026": dict(pmid="", pmcid="", doi="10.4088/pcc.26cr04209",
                             title="Unexpected Improvement in Obsessive-Compulsive Disorder Symptoms Following Initiation of Bupropion",
                             authorString="Riestra JM, Munsar Z, Opler DJ", journal="Prim Care Companion CNS Disord", year=2026,
                             vol="28", issue="4", pages="26cr04209", lang="eng")}
R = [dict(id="riestra-2026", src="riestra-2026", design="Case report", n=1, cats=["Obsessive-compulsive & tic"],
          spec="OCD (contamination aversions, musical obsessions, ordering rituals) with comorbid major depression in a "
               "23-year-old woman who could not tolerate SSRIs", chronic=True, tr=True, tcat="Medication for another condition",
          tspec="Bupropion 150 mg/day for the depression and amotivation", intent=OTHER, res="Complete", rev="None reported", dl=1,
          era=("emerging", "Bupropion is not an OCD treatment; a few earlier reports were mixed, and Canan 2012 described body "
                           "dysmorphic disorder remitting on it."),
          summary="A 23-year-old woman whose OCD had kept her out of any job that involved touching fruit was started on bupropion "
                  "for depression after two SSRIs failed; within a month her obsessions and rituals had faded, and three years "
                  "later they had not come back.",
          caveat="She was also taking N-acetylcysteine, which has some evidence in OCD, and lifting her depression may have loosened the rituals.",
          tags=["bupropion", "ocd", "dopamine", "noradrenaline", "depression"], tier="C")]
DEC = {
    1: "riestra-2026",
    5: ("E7", "review"),
    18: ("E2", "pain persisted; psychiatric stabilisation came with psychiatric treatment"),
    49: ("E4", "persistent genital arousal and the depression it caused resolved after discectomy for the disc that caused it"),
    68: ("E2", "levodopa helped the movement disorder, not the schizoaffective disorder"),
    70: ("E3", "methylphenidate added deliberately for PTSD"),
    71: ("E7", "conceptual review with three illustrative cases"),
    83: ("E2", "on-off-on pattern was in headache frequency, not the psychiatric disorders"),
    103: ("E8", "self-reported benefit from self-administered Hawaiian baby woodrose; too little detail on the mood disorder"),
    120: ("E3", "olanzapine given deliberately for the opioid craving"),
    177: ("E1", "rhythmic movement disorder (head banging), a sleep disorder"),
    181: ("E3", "cholinesterase inhibitor switched with the neuropsychiatric symptoms in view"),
    188: ("E4", "self-injury eased after managing somatic pain and mood, within a multimodal plan"),
    413: ("E3", "psychosis treated with antipsychotics"),
    476: ("E3", "cingulotomy chosen for pain with severe depression, aimed at both"),
}


def emb_url(eid):
    return "https://go.openathens.net/redirector/ckn.qldhealth.com?url=" + quote(
        f"https://www.embase.com/records?subaction=viewrecord&id={eid}", safe="")


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1f", found_via=f"{SRC} ({QID})", today=TODAY)
    d = json.loads(CASES.read_text())
    for r in d["records"]:
        if r["id"] == "riestra-2026":
            r["verified"] = f"{TODAY}: full text read (psychiatrist.com, free); no PMID yet"
            r["access"] = "Free full text"
            r["links"]["full_text"] = "https://www.psychiatrist.com/pcc/improvement-obsessive-compulsive-disorder-symptoms-bupropion/"
            r["outcome"]["time_to_resolution"] = "about 1 month"
            r["outcome"]["follow_up"] = "3 years"
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = {r["record_id"]: r for r in L.rows if r["record_id"] not in sup}
    n = {"screened": 0, "corrections": 0, "already": 0, "included": 0}
    for x in M["all"]:
        eid, q, title, otitle, ol, au, jn, yr, vol, iss, pg, doi, pt, srcdb, score, kind, blanks, libs, decided = x
        first = re.sub(r"\s+[A-Z][A-Za-z.\-]*\.$", "", (au or "").split(",")[0].strip())
        base = dict(doi=doi, other=eid, title=title, au=first, yr=yr, jn=jn, lang=ol or "")
        olds = [o for o in dict.fromkeys(blanks.split(";")) if o and o in current and not current[o]["decision"]]
        if eid in RANK:
            i = RANK[eid]
            dec = DEC.get(i)
            L.add(SRC, QID, dec, **base, screened=True, supersedes=olds[0] if olds else "",
                  note=f"rerank_v1 rank {i} of 643, score {score}; all titles screened; {kind}; {TODAY}")
            n["screened"] += 1
            for o in olds[1:]:
                L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o,
                      screened=True, note=f"screened via Embase record {eid} ({QID}); {TODAY}")
                n["corrections"] += 1
            continue
        prev = [current[r] for r in decided.split(";") if r in current]
        if kind == "included":
            dec = libs.split(";")[0]
            L.add(SRC, QID, dec, **base, note=f"library case, also found as {decided}; {TODAY}")
            n["included"] += 1
        else:
            p = next(r for r in prev if r["decision"] == "excluded")
            dec = (p["reason_code"], f"decided earlier as {p['record_id']}")
            row = L.add(SRC, QID, dec, **base, note=TODAY)
            row["screen_stage"] = p["screen_stage"]
            n["already"] += 1
        for o in olds:
            row = L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o,
                        screened=True, note=f"same record as {decided}, met again by {QID}; {TODAY}")
            n["corrections"] += 1
    L.write()
    print(n)
    log_runs([(QID, SRC, "'unexpected outcome of drug treatment'/exp x mental disease/mj x case design x humans, narrowed "
               "to resolution wording (see queries/strings_embase_unexpected_outcome_v1.json)", 814, TODAY,
               "643 new or blank, all titles screened; 1 case")])
