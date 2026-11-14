"""Batch 2026-11-14: citation route v2 (protocol v1.7.3), one more hop from the cases added since route v1.

Seeds: the 56 library cases with a PMID added on 2026-11-13/14 (route v1's own includes, the antique sweep, Embase,
PsycInfo), plus Sharma 2008, whose PMID (18615165) and PMCID turned up via Europe PMC during seeding. Europe PMC
`/MED/{id}/citations` and `/references` in the laptop browser: 805 links, 709 distinct records with IDs and 78
reference entries without IDs (65 of them have no title either, so cannot be screened; the 13 with titles are logged).
Records fetched by ID (core) and scored with queries/rerank_model_v1.json.

Matched to current ledger rows by source:ID, PMID, DOI or normalised title: 23 library cases, 76 excluded, 1 unsure,
91 blank, 518 new. All 609 new or blank titles screened (classifier order used only for reading), abstracts read for
every candidate, so no stopping rule was needed.

Result: 4 cases (Schweickert 1997 methylphenidate and bulimia; Taira 2003 pallidal DBS for dystonia ending self-mutilation
in Lesch-Nyhan syndrome; Pozzi 2014 intrathecal baclofen in Lesch-Nyhan syndrome; Miyazaki 2023 methylphenidate and
kleptomania), 5 unsure (letters without abstracts). Sharma 2008 gains its PMID and PMCID.
Working files: /home/claude/work/raw/cit2_all.json, cit2_match.json (not committed).
Run from the repo root:  python3 scripts/batches/b2026_11_14_citation_route_v2.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from lib_add import CASES, U, Ledger, add_records, log_runs  # noqa: E402

TODAY = "2026-11-14"
QID, SRC = "CIT_EPMC_v2", "Europe PMC citations"
M = json.loads(Path("/home/claude/work/raw/cit2_match.json").read_text())
# all/todo rows: [key, title, year, doi, pmid, pmcid, first author, journal, pubtype, lang, via, hasAbs, score, kind,
#                 blank record_ids, library ids]; noid rows: [seed, cit|ref, title, first author, journal, year, doi, kind]
TODO = M["todo"]
RANK = {x[0]: i for i, x in enumerate(TODO)}
OTHER = "Treatment for another condition"

cand = {
    "schweickert-1997": dict(pmid="9097204", pmcid="", doi="10.1002/(sici)1098-108x(199704)21:3<299::aid-eat11>3.0.co;2-w",
                             title="Efficacy of methylphenidate in bulimia nervosa comorbid with attention-deficit hyperactivity disorder: a case report.",
                             authorString="Schweickert LA, Strober M, Moskowitz A", journal="Int J Eat Disord", year=1997, vol="21",
                             issue="3", pages="299-301", lang="eng"),
    "taira-2003": dict(pmid="12593632", pmcid="", doi="10.3171/jns.2003.98.2.0414",
                       title="Disappearance of self-mutilating behavior in a patient with lesch-nyhan syndrome after bilateral chronic stimulation of the globus pallidus internus. Case report.",
                       authorString="Taira T, Kobayashi T, Hori T", journal="J Neurosurg", year=2003, vol="98", issue="2",
                       pages="414-6", lang="eng"),
    "pozzi-2014": dict(pmid="25497359", pmcid="PMC4266221", doi="10.1186/s13023-014-0208-3",
                       title="Treatment of motor and behavioural symptoms in three Lesch-Nyhan patients with intrathecal baclofen.",
                       authorString="Pozzi M, Piccinini L, Gallo M, Motta F, Radice S, Clementi E", journal="Orphanet J Rare Dis",
                       year=2014, vol="9", issue="", pages="208", lang="eng"),
    "miyazaki-2023": dict(pmid="37921065", pmcid="PMC10739163", doi="10.1002/npr2.12394",
                          title="An adolescent boy with kleptomania and attention-deficit hyperactivity disorder treated with methylphenidate and guanfacine: A case report.",
                          authorString="Miyazaki K, Uchiyama M", journal="Neuropsychopharmacol Rep", year=2023, vol="43", issue="4",
                          pages="650-653", lang="eng"),
}
STIM = ("emerging", "Methylphenidate and other stimulants given for ADHD were reported to curb binge eating from 1997 on "
                    "(this record, Drimmer 2003, Dukarm 2005); lisdexamfetamine was later approved for binge-eating disorder in "
                    "the US (recalled, not checked).")
R = [
    dict(id="schweickert-1997", src="schweickert-1997", design="Case report", n=1, cats=["Eating"],
         spec="Bulimia nervosa (binge eating) with comorbid ADHD", chronic=None, tr=None, tcat="Medication for another condition",
         tspec="Methylphenidate for comorbid ADHD", intent=OTHER, res="Partial", rev="None reported", dl=2, era=STIM,
         summary="A patient with bulimia nervosa binged much less after methylphenidate was prescribed for comorbid ADHD.",
         caveat="Methylphenidate dulls appetite, so fewer binges need not mean the bulimia itself changed.",
         tags=["methylphenidate", "stimulant", "adhd", "bulimia", "binge-eating"], tier="C"),
    dict(id="taira-2003", src="taira-2003", design="Case report", n=1, cats=["Neurodevelopmental"],
         spec="Self-mutilation in Lesch-Nyhan syndrome", chronic=True, tr=None, tcat="Brain stimulation",
         tspec="Bilateral chronic stimulation of the globus pallidus internus to control dystonic movements", intent=OTHER,
         res="Complete", rev="None reported", dl=2,
         era=("known", "Pallidal DBS in Lesch-Nyhan syndrome was repeated in later reports and series (Deon 2012; clinical "
                       "outcome series 2021) and gathered in a 2023 systematic review; self-injury is now one of its aims."),
         summary="A 19-year-old man with Lesch-Nyhan syndrome given bilateral pallidal stimulation to control dystonia stopped "
                 "self-mutilating, an effect the surgeons had not sought; the first report of its kind.",
         caveat="The authors allow that the self-injury may have been partly secondary to the dystonia, which the stimulation treated.",
         tags=["lesch-nyhan", "self-injury", "deep-brain-stimulation", "globus-pallidus", "dystonia"], tier="B"),
    dict(id="pozzi-2014", src="pozzi-2014", design="Case series", n=3, cats=["Neurodevelopmental"],
         spec="Behavioural symptoms of Lesch-Nyhan syndrome (self-injurious behaviour indexed) no longer helped by earlier treatments",
         chronic=True, tr=True, tcat="Medication for another condition", tspec="Intrathecal baclofen for motor symptoms",
         intent=OTHER, res="Partial", rev="None reported", dl=0,
         summary="Three men with Lesch-Nyhan syndrome who no longer benefited from earlier treatments were given intrathecal "
                 "baclofen for their motor symptoms; their behaviour improved too, which the authors had not expected.",
         caveat="Less spasticity and pain could ease distress-driven behaviour without acting on it directly.",
         tags=["lesch-nyhan", "baclofen", "gaba-b", "self-injury", "intrathecal"], tier="C"),
    dict(id="miyazaki-2023", src="miyazaki-2023", design="Case report", n=1, cats=["Impulse-control"],
         spec="Kleptomania with ADHD in a 16-year-old boy", chronic=None, tr=None, tcat="Medication for another condition",
         tspec="Extended-release methylphenidate for ADHD (guanfacine added later for the hours when it wore off)", intent=OTHER,
         res="Partial", rev="Natural off-on", dl=1,
         era=("emerging", "Earlier letters (2011, Yilmaz 2014) had reported methylphenidate for ADHD reducing stealing."),
         summary="A 16-year-old boy who stole things he did not need stole far less once methylphenidate was started for his "
                 "ADHD; at 19 the stealing returned only when the drug wore off, and guanfacine covered those hours.",
         caveat="At 16, impulsive stealing from ADHD is hard to tell apart from kleptomania.",
         tags=["methylphenidate", "guanfacine", "kleptomania", "adhd", "adolescent"], tier="C"),
]
DEC = {
    0: "schweickert-1997", 3: "taira-2003", 151: "miyazaki-2023", 264: "pozzi-2014",
    2: ("E3", "capsulotomy undertaken for life-threatening comorbid anorexia nervosa and OCD, aimed at both"),
    7: (U, "no abstract: three cases of stimulants for bulimia with and without ADD; in the ADD cases, were stimulants for the ADD?"),
    8: ("E3", "mouth guard aimed at the self-mutilation"),
    13: ("E3", "pallidal DBS aimed at both dystonia and self-injury (2015, after Taira 2003)"),
    27: ("E2", "missed temporal lobe epilepsy; no resolution described"),
    32: ("E3", "lorazepam given for the stupor (with reproducible antagonist reversal)"),
    33: (U, "OCD after thalamic infarct responding to dronabinol: given for the OCD or for something else?"),
    36: (U, "letter, no abstract: methylphenidate for ADHD in an adolescent with kleptomania; did the stealing stop, and was it aimed at both?"),
    49: ("E5", "double-blind trial of methylamphetamine in bulimia"),
    54: ("E3", "stimulants chosen for comorbid bulimia and ADHD with the bulimia in view ('some clinicians have used psychostimulants in this population')"),
    65: (U, "letter, no abstract, citing Koethe 2007: which non-antipsychotic drug, given for what?"),
    112: ("E4", "aggression from temporal lobe tumour seizures, resolving with resection"),
    115: ("E3", "nucleus accumbens DBS for anorexia nervosa"),
    135: ("E3", "fluoxetine aimed at the paraphilic fantasies"),
    157: ("E3", "methylphenidate tried deliberately for bulimia with cluster B traits"),
    202: (U, "methylphenidate started after an appendectomy in long-standing bulimia: prescribed for what?"),
    236: ("E3", "diazepam given for the catatonia"),
    262: ("E2", "skin picking with polyarteritis nodosa; standard treatment recommended, no unexpected resolution"),
    588: ("E1", "transvestism developing in Ehlers-Danlos syndrome; no resolution"),
}
NOID_DEC = {0: ("E3", "leucotomy for anorexia nervosa"), 69: ("E3", "Tagai 2013 (PMID 23909968): mirtazapine given deliberately for Parkinson's psychosis")}


def copy_fields(r):
    return dict(doi=r["doi"], pmid=r["pmid"], pmcid=r["pmcid"], other=r["other_id"], title=r["title"], au=r["first_author"],
                yr=r["year"], jn=r["journal"], lang=r["language"])


if __name__ == "__main__":
    add_records(R, cand, collection="phase1f", found_via=f"{SRC} ({QID})", today=TODAY)
    d = json.loads(CASES.read_text())
    ids = {k["id"] for k in R}
    for r in d["records"]:
        if r["id"] in ids:
            r["verified"] = f"{TODAY}: abstract-level appraisal (Europe PMC record); identifiers from PubMed"
            if r["ids"]["pmcid"] and not r["links"].get("full_text"):
                r["links"]["full_text"] = f"https://pmc.ncbi.nlm.nih.gov/articles/{r['ids']['pmcid']}/"
            if r["id"] == "schweickert-1997":
                r["links"]["doi"] = r["links"]["doi"].replace("<", "%3C").replace(">", "%3E")
        if r["id"] == "sharma-2008" and not r["ids"].get("pmid"):
            r["ids"].update(pmid="18615165", pmcid="PMC2446483")
            r["links"].update(abstract="https://pubmed.ncbi.nlm.nih.gov/18615165/",
                              full_text="https://pmc.ncbi.nlm.nih.gov/articles/PMC2446483/")
            r["access"] = "Free full text"
            r["verified"] = (r.get("verified") or "") + f"; {TODAY}: PMID and PMCID found via Europe PMC (citation route v2)"
    CASES.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

    L = Ledger(TODAY)
    sup = {r["supersedes"] for r in L.rows if r["supersedes"]}
    current = {r["record_id"]: r for r in L.rows if r["record_id"] not in sup}
    norm = lambda t: re.sub(r"[^a-z0-9]", "", (t or "").lower())[:80]  # noqa: E731
    idx = {}
    for r in current.values():
        if r["decision"]:
            for k in (r["other_id"], "pmid:" + r["pmid"] if r["pmid"] else "", "doi:" + r["doi"] if r["doi"] else "",
                      "t:" + norm(r["title"]) if len(norm(r["title"])) > 15 else ""):
                if k:
                    idx.setdefault(k, []).append(r)
    n = {"screened": 0, "corrections": 0, "already": 0, "included": 0, "unsure": 0, "noid": 0}
    done = set()
    for x in M["all"]:
        key, title, yr, doi, pmid, pmcid, au, jn, pt, lang, via, has_abs, score, kind, blanks, libs = x
        base = dict(doi=doi, pmid=pmid, pmcid=pmcid, other=key, title=title, au=au, yr=yr, jn=jn, lang=lang)
        olds = [o for o in dict.fromkeys(blanks.split(";")) if o and o not in done]
        if key in RANK:
            i = RANK[key]
            dec = DEC.get(i)
            L.add(SRC, QID, dec, **base, screened=True, supersedes=olds[0] if olds else "",
                  note=f"citation v2 rank {i} of 609, score {score}; via {via}; all titles screened; {kind}; {TODAY}")
            n["screened"] += 1
            for o in olds[1:]:
                L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o, screened=True,
                      note=f"screened via {key} ({QID}); {TODAY}")
                n["corrections"] += 1
            done.update(olds)
            continue
        if kind == "included":
            L.add(SRC, QID, libs.split(";")[0], **base, note=f"library case; via {via}; {TODAY}")
            n["included"] += 1
        elif kind == "unsure":
            L.add(SRC, QID, (U, "same record as an earlier unsure row, still unsure"), **base, note=f"via {via}; {TODAY}")
            n["unsure"] += 1
            print("unsure match:", key, title[:90])
        else:
            prev = next(r for k in (key, "pmid:" + pmid if pmid else "", "doi:" + doi if doi else "",
                                    "t:" + norm(title) if len(norm(title)) > 15 else "") if k for r in idx.get(k, [])
                        if r["decision"] == "excluded")
            row = L.add(SRC, QID, (prev["reason_code"], f"decided earlier as {prev['record_id']}"), **base, note=f"via {via}; {TODAY}")
            row["screen_stage"] = prev["screen_stage"]
            n["already"] += 1
        for o in olds:   # a blank row elsewhere for the same record: settle it the same way as the decided row
            dec = (libs.split(";")[0] if kind == "included" else (U, "as the decided row") if kind == "unsure"
                   else (prev["reason_code"], f"decided earlier as {prev['record_id']}"))
            L.add(current[o]["source_db"], current[o]["query_id"], dec, **copy_fields(current[o]), supersedes=o, screened=True,
                  note=f"same record as {key}, met again by {QID}; {TODAY}")
            n["corrections"] += 1
        done.update(olds)
    for i, y in enumerate(M["noid"]):
        seed, cr, title, au, jn, yr, doi, kind = y
        if not title:
            continue
        L.add(SRC, QID, NOID_DEC.get(i), title=title, au=au, yr=yr, jn=jn, doi=doi,
              pmid="23909968" if i == 69 else "", other=f"ref:{seed}:{i}", screened=True,
              note=f"reference of {seed} without an ID in Europe PMC; title screened; {TODAY}")
        n["noid"] += 1
    L.write()
    print(n)
    log_runs([(QID, SRC, "Europe PMC /citations + /references of 57 library cases added since CIT_EPMC_v1 (one more hop)",
               709, TODAY, "609 new or blank, all titles screened; 4 cases, 5 unsure; 13 titled references without IDs logged")])
