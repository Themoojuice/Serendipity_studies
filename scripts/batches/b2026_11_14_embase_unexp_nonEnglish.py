"""Batch 2026-11-14: Embase via CKN, two new searches (protocol v1.7.2).

EMB_unexp_v1 (history #6, 693 hits): syndrome block in the title AND unexpectedness terms in the abstract AND case block,
  Embase-only, humans.
EMB_nonEng_v1 (history #7, 462 hits): same syndrome block in the title AND strong resolution terms in the abstract AND
  case block, limited to 21 non-English languages, humans.
Strings: queries/strings_embase_unexp_nonEng_v1.json. Records read from the results endpoint (paced), 1,150 distinct
(5 in both searches), scored with the v1.3 classifier in the browser.

Matched to current ledger rows by Embase ID, DOI or normalised title: 730 new or blank (727 in the queue + 3 the match dropped), the rest decided before.
All 730 titles screened in classifier order, abstracts read for every candidate.

Result: 3 cases from the queue (Vieweg 1985 captopril and hyperosmolar coma in PIP syndrome; Matsui 2004 Parkinson's
hallucinations gone after cataract surgery; Grunstein 2017 late-onset schizophrenia-like illness remitting on CPAP), and
1 earlier unsure row settled in (Corte 2025: PNES gone after ECT given for depression). 3 records the queue match
dropped (shared or stub DOIs) are screened here too.
Working files: /home/claude/work/raw/emb2_all.json, emb2_todo.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_14_embase_unexp_nonEnglish.py
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, "scripts")
from lib_add import CASES, U, Ledger, add_records, log_runs  # noqa: E402

TODAY = "2026-11-14"
SRC = "Embase via CKN"
QID = {"6": "EMB_unexp_v1", "7": "EMB_nonEng_v1"}
RAW = Path("/home/claude/work/raw")
# [id, q, title, original title, original language, authors, journal, year, vol, issue, pages, doi, pub type, source, score]
ALL = json.loads((RAW / "emb2_all.json").read_text())
TODO = json.loads((RAW / "emb2_todo.json").read_text())       # same fields + [new|blank, old record_id], sorted by score
RANK = {x[0]: i for i, x in enumerate(TODO)}
CKN = "https://go.openathens.net/redirector/ckn.qldhealth.com?url="
OTHER = "Treatment for another condition"


def emb_url(eid):
    return CKN + quote(f"https://www.embase.com/records?subaction=viewrecord&id={eid}", safe="")


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:80]


cand = {
    "vieweg-1985": dict(pmid="", pmcid="", doi="",
                        title="Possible ameliorating effect of captopril treatment and hyperosmolar coma in a patient with psychosis, intermittent hyponatremia, and polydipsia",
                        authorString="Vieweg WVR, Rowe WT, David JJ", journal="Psychiatric Hospital", year=1985, vol="16", issue="4",
                        pages="", lang="eng"),
    "matsui-2004": dict(pmid="15237728", pmcid="", doi="",
                        title="[Two cases of Parkinson's disease in which visual hallucinations disappeared after cataract surgery].",
                        authorString="Matsui H, Udaka F, Oda M, Kubori T, Nishinaka K, Kameyama M", journal="No To Shinkei", year=2004,
                        vol="56", issue="4", pages="351-4", lang="jpn"),
    "grunstein-2017": dict(pmid="", pmcid="", doi="", title="Schizophrenia and obstructive sleep apnea: Could CPAP cure both?",
                           authorString="Grunstein PF, Fazleen A, Sankaran P", journal="Am J Respir Crit Care Med", year=2017,
                           vol="195", issue="", pages="", lang="eng"),
    "corte-2025": dict(pmid="", pmcid="", doi="10.1590/0047-2085-2025-0027",
                       title="Electroconvulsive therapy in a patient with psychogenic nonepileptic seizures and treatment-resistant depression: a case report",
                       authorString="Corte AF, Linan CBA, Fillmann GP, Soares AB, Villalobos JRG, de Lima KA, Castro SCC, et al",
                       journal="J Bras Psiquiatr", year=2025, vol="74", issue="", pages="e20250027", lang="por"),
}
EMB_ID = {"corte-2025": "L2043961325", "vieweg-1985": "L16200416", "matsui-2004": "L38855778", "grunstein-2017": "L617706822"}

R = [
    dict(id="vieweg-1985", src="vieweg-1985", design="Case report", n=1, cats=["Psychotic"],
         spec="Disorganised schizophrenia with psychosis, intermittent hyponatraemia and polydipsia (PIP syndrome)", chronic=None,
         tr=None, tcat="Coma / anaesthesia",
         tspec="Captopril, with a transient hyperosmolar coma induced inadvertently at the same time", intent=OTHER,
         res="Partial", rev="None reported", dl=0,
         summary="A 46-year-old man with disorganised schizophrenia and water intoxication improved strikingly, in both his "
                 "psychosis and his drinking, after an accidental hyperosmolar coma that coincided with captopril; all treatment "
                 "could then be stopped.",
         caveat="The coma and the captopril came together, so the coma may deserve the credit, much as insulin coma once did.",
         tags=["captopril", "ace-inhibitor", "hyperosmolar-coma", "polydipsia", "water-intoxication", "schizophrenia"], tier="C"),
    dict(id="matsui-2004", src="matsui-2004", design="Case series", n=2, cats=["Psychotic"],
         spec="Visual hallucinations in Parkinson's disease, poorly controlled by medication (one woman also had musical hallucinations)",
         chronic=None, tr=True, tcat="Surgery or procedure (outside the brain)", tspec="Surgery for severe bilateral cataracts",
         intent=OTHER, res="Complete", rev="None reported", dl=0,
         summary="Two women in their seventies with Parkinson's disease and dense cataracts in both eyes had hallucinations that "
                 "drugs had not settled; both stopped seeing things soon after their cataracts were removed.",
         caveat="Severe cataract may have made these partly Charles Bonnet-type release hallucinations, which better vision would be expected to end.",
         tags=["cataract", "parkinsons", "visual-hallucinations", "charles-bonnet", "surgery"], tier="C"),
    dict(id="grunstein-2017", src="grunstein-2017", design="Conference abstract", n=1, cats=["Psychotic"],
         spec="Schizophrenia-like illness of 8 months in a 65-year-old man (delusions, hallucinations, thought disorder, negative "
              "symptoms), never treated with antipsychotics", chronic=False, tr=None,
         tcat="Surgery or procedure (outside the brain)", tspec="CPAP for severe obstructive sleep apnoea (54 apnoeas an hour)",
         intent=OTHER, res="Complete", rev="None reported", dl=1,
         summary="A 65-year-old man referred for severe sleep apnoea had an untreated 8-month schizophrenia-like illness; three "
                 "months into faithful CPAP use he was back at work and free of psychotic features.",
         caveat="Onset in his sixties alongside severe nocturnal hypoxaemia makes a secondary, hypoxic psychosis plausible, in which case CPAP treated its cause.",
         tags=["cpap", "obstructive-sleep-apnoea", "hypoxaemia", "late-onset-psychosis", "schizophrenia"], tier="C"),
    dict(id="corte-2025", src="corte-2025", design="Case report", n=1, cats=["Functional neurological"],
         spec="Psychogenic non-epileptic seizures with treatment-resistant depression and repeated suicide attempts in a 38-year-old woman",
         chronic=None, tr=True, tcat="Brain stimulation", tspec="Twelve sessions of ECT chosen for the worsening depression",
         intent=OTHER, res="Complete", rev="None reported", dl=1,
         summary="A 38-year-old woman given ECT because her treatment-resistant depression was worsening, with fresh suicide "
                 "attempts, had no further non-epileptic seizures by the end of twelve sessions, which surprised her team.",
         caveat="Functional seizures rise and fall with distress, so the steep drop in her depression scores may explain it.",
         tags=["ect", "psychogenic-nonepileptic-seizures", "functional-neurological-disorder", "treatment-resistant-depression"], tier="C"),
]
# earlier unsure rows settled by the Embase abstract
RESOLVE = {"L2043961325": ("corte-2025", "R062077")}

DEC = {
    18: "vieweg-1985", 199: "matsui-2004", 294: "grunstein-2017",
    0: ("E3", "bright light therapy aimed at the seasonal OCD"),
    3: ("E1", "tardive dyskinesia remitting during mania; not a psychiatric syndrome"),
    11: ("E2", "kleptomania without remission"),
    12: ("E4", "psychosis from a recurrent temporal astrocytoma, remitting after re-resection (and neuroleptics)"),
    13: ("E4", "binge-purge eating disturbance began a year into epigastric pain and subsided with H. pylori eradication; reads as GI-driven"),
    17: ("E2", "OCD presentation only, no resolution reported"),
    39: ("E1", "nocturnal enuresis cured by acupuncture and chiropractic; depression not the outcome"),
    52: ("E2", "probiotics for GI symptoms; ADOS Social Affect 20 to 17 with severity level unchanged"),
    73: ("E3", "remission under treatment; essay on whether schizophrenia can be called cured"),
    180: ("E8", "conversion disorder thrombolysed as stroke; no outcome attributable to thrombolysis, report is about diagnosis"),
    246: ("E2", "alcohol dependence used against cataplexy persisted; no remission"),
    260: ("E3", "anorexia nervosa improved with supportive care and the father's involvement"),
    398: ("E2", "depression did not improve during ECT"),
    432: ("E3", "acupuncture aimed at the tics and anxiety; the tympanic perforation healing is not psychiatric"),
    437: ("E3", "testosterone given as antidepressant augmentation"),
    473: ("E3", "non-convulsive ECT aimed at the delusions; SIADH correction is not psychiatric"),
    523: ("E4", "self-injury driven by headache pain, reduced when Botox relieved the migraine (authors' reading); waned before each dose"),
    546: ("E4", "psychosis attributed to hydroxychloroquine itself"),
    574: ("E2", "suicidal ideation attributed to acne during isotretinoin; no resolution described"),
}


MISSED = {"L2041170851", "L2044832361", "L2010558234"}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1f", found_via=f"{SRC} (EMB_unexp_v1, EMB_nonEng_v1)", today=TODAY)
    d = json.loads(CASES.read_text())
    ids = {k["id"] for k in R}
    for r in d["records"]:
        if r["id"] in ids:
            r["verified"] = f"{TODAY}: abstract-level appraisal (Embase record)" + ("; identifiers from PubMed" if r["ids"]["pmid"] else "")
            if not r["links"].get("ckn"):
                r["links"]["ckn"] = emb_url(EMB_ID[r["id"]])
            if r["id"] == "vieweg-1985":
                r["verified"] += "; not in PubMed; co-author spelled 'Davis' in Embase, 'David' in the group's PubMed records"
            if r["id"] == "grunstein-2017":
                r["outcome"]["time_to_resolution"] = "3 months"
                r["outcome"]["follow_up"] = "about 7 months on CPAP"
                r["verified"] += "; Embase DOI field looks like a session code, not used"
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    lib_titles = {norm(r["citation"]["title"]): r["id"] for r in d["records"]}

    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = [r for r in L.rows if r["record_id"] not in sup]
    by_key = {}
    for r in current:
        for key in (r["other_id"], ("doi:" + r["doi"]) if r["doi"] else "", norm(r["title"])):
            if key:
                by_key.setdefault(key, []).append(r)
    n = {"screened": 0, "corrections": 0, "already": 0, "included": 0, "unsure": 0}
    olds = {x[0]: list(dict.fromkeys(x[16].split(";"))) if x[15] == "blank" else [] for x in TODO}  # some links repeat an ID
    done_sup = {o for v in olds.values() for o in v}   # old rows the queue rows supersede directly
    for x in ALL:
        eid, q, title, otitle, ol, au, jn, yr, vol, iss, pg, doi, pt, srcdb, score = x
        qid = QID[q.split(",")[0]]
        also = "; also retrieved by EMB_nonEng_v1" if q == "6,7" else ""
        first = re.sub(r"\s+[A-Z][A-Za-z.\-]*\.$", "", (au or "").split(",")[0].strip())   # 'Gota Garces J.M.' -> 'Gota Garces'
        base = dict(doi=doi, other=eid, title=title, au=first, yr=yr, jn=jn, lang=ol or "")
        matched = []
        for key in (eid, ("doi:" + doi.lower()) if doi else "", norm(title), norm(otitle)):
            for r in by_key.get(key, []) if key else []:
                if r not in matched:
                    matched.append(r)
        if eid in RANK:
            i = RANK[eid]
            dec = DEC.get(i)
            if dec is None:
                dec = lib_titles.get(norm(title))
            L.add(SRC, qid, dec, **base, screened=True,
                  note=f"rerank_v1 rank {i} of 727, score {score}; all titles screened; {TODO[i][15]}{also}; {TODAY}",
                  supersedes=olds[eid][0] if olds[eid] else "")
            n["screened"] += 1
            for o in olds[eid][1:]:
                old = next(r for r in current if r["record_id"] == o)
                L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=o, screened=True,
                      note=f"screened via Embase record {eid} ({qid}); {TODAY}")
                n["corrections"] += 1
            for old in matched:
                if not old["decision"] and old["record_id"] not in done_sup:
                    done_sup.add(old["record_id"])
                    L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=old["record_id"], screened=True,
                          note=f"screened via Embase record {eid} ({qid}); {TODAY}")
                    n["corrections"] += 1
            continue
        decided = [r for r in matched if r["decision"]]
        if not decided:   # 3 records the queue match dropped (shared or stub DOIs): titles screened here, all irrelevant
            assert eid in MISSED, eid
            L.add(SRC, qid, None, **base, screened=True, note=f"missed by the queue match, title screened; {TODAY}{also}")
            n["screened"] += 1
            continue
        ref = "; ".join(r["record_id"] for r in decided)
        inc = [r for r in decided if r["decision"] == "included"]
        uns = [r for r in decided if r["decision"] == "unsure"]
        if eid in RESOLVE:
            lib, old_id = RESOLVE[eid]
            dec = lib
            L.add(SRC, qid, dec, **base, note=f"was unsure as {old_id}; settled by the Embase abstract (ECT chosen for the depression, PNES gone, 'surprising'){also}; {TODAY}")
            old = next(r for r in current if r["record_id"] == old_id)
            L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=old_id,
                  note=f"settled with the Embase abstract ({qid}, {eid}); {TODAY}")
            n["corrections"] += 1
            n["included"] += 1
            continue
        if inc:
            dec = inc[0]["library_ids"]
            L.add(SRC, qid, dec, **base, note=f"library case, also found as {ref}{also}; {TODAY}")
            n["included"] += 1
        elif uns:
            dec = (U, f"same record as {ref}, still unsure")
            L.add(SRC, qid, dec, **base, note=f"{TODAY}{also}")
            n["unsure"] += 1
            print("unsure match:", eid, title[:90], ref)
        else:
            dec = (decided[0]["reason_code"], f"decided earlier as {ref}")
            row = L.add(SRC, qid, dec, **base, note=f"{TODAY}{also}")
            row["screen_stage"] = decided[0]["screen_stage"]
            n["already"] += 1
        for old in matched:
            if not old["decision"] and old["record_id"] not in done_sup:   # a blank row elsewhere: settle it the same way
                done_sup.add(old["record_id"])
                row = L.add(old["source_db"], old["query_id"], dec, **copy_fields(old), supersedes=old["record_id"], screened=True,
                            note=f"same record as {ref}, met again by {qid}; {TODAY}")
                if not inc and not uns:
                    row["screen_stage"] = decided[0]["screen_stage"]
                n["corrections"] += 1
    L.write()
    print(n)
    log_runs([("EMB_unexp_v1", SRC, "syndrome:ti AND unexpectedness:ab AND case block, Embase-only, humans (search #6); "
               "see queries/strings_embase_unexp_nonEng_v1.json", 693, TODAY, "screened with EMB_nonEng_v1 as one set"),
              ("EMB_nonEng_v1", SRC, "syndrome:ti AND resolution:ab AND case block, 21 non-English languages, humans (search #7); "
               "see queries/strings_embase_unexp_nonEng_v1.json", 462, TODAY,
               "1,150 distinct records, 730 new or blank, all titles screened; 3 cases + 1 unsure settled in")])
