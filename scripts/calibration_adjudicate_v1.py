#!/usr/bin/env python3
"""Write queries/calibration_v1_adjudication.json: the final call on each of the 22 calibration v1 disagreements.

final: "in" (a library case or to full text) or "out" (excluded, or not a case: context record).
matched: whose first title/abstract call the final call agrees with.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B = json.loads((ROOT / "queries/calibration_v1_brendan.json").read_text())
K = {k["i"]: k for k in json.loads((ROOT / "queries/calibration_v1_key.json").read_text())["key"]}
S = {r["i"]: r for r in json.loads((ROOT / "queries/calibration_v1_sample.json").read_text())["records"]}

FINAL = {  # i: (final, code, rule, note)
    24: ("out", "E4", "T3", "Miller 2012: the depression had already remitted with ECT; palatal expansion treated sleep-disordered breathing the authors set out to find as the cause."),
    28: ("out", "E2", "", "Sabel'nikova 2013: schizophrenia unchanged after 8 months gluten-free (coeliac remitted)."),
    44: ("out", "E2", "", "Kornhuber 1993: psychosis worsened on amantadine."),
    50: ("out", "E3", "T1", "Min 2022: switched from paroxetine to vortioxetine for the depression (conference abstract)."),
    57: ("out", "E3", "T1", "Paulig 2001: gabapentin given for the Charles Bonnet hallucinations themselves; anticonvulsants had been tried for them before. Letter, no abstract."),
    61: ("out", "E5", "", "Liu 2022: a prospective DBS series in Tourette syndrome with depression scores as a secondary outcome (Claude's first reason, E3, was the wrong code)."),
    68: ("out", "E3", "T1", "Bellamy 2025: ketogenic therapy aimed at the psychiatric syndromes."),
    76: ("out", "E4", "T3", "Nygaard Andersen 2014: contraceptive-induced depression remitting when they stopped."),
    77: ("in", "unsure", "", "Albertini 2006: mirtazapine for compulsive masturbation, but the autism itself improved and the authors call that unexpected. Claude screened only the headline syndrome; to full text."),
    93: ("out", "E3", "T1", "Endres 2017: levetiracetam aimed at the psychosis through a hypothesised paraepileptic mechanism."),
    99: ("out", "E2", "", "Adán 2005: psychosis appeared with vagus nerve stimulation."),
    6: ("out", "context", "T1/T2", "Fontaine 2004: the abstract says stimulation was used to treat both conditions, after Mallet 2002. Now a context record. (The frame's first ledger row had no title, so the screen showed only the abstract.)"),
    7: ("in", "", "", "Liu 2016: the title reads as deliberate treatment, but the PsycInfo abstract shows the dopamine was given for septic shock. Stays a case."),
    20: ("out", "E3", "T1", "Romeo 2025: already excluded after full text on 17 Nov (semaglutide chosen partly for craving)."),
    31: ("out", "context", "T2", "Sciortino 2021: prefrontal stimulation easing binge eating was known after Downar 2012. Now a context record."),
    33: ("out", "E8", "T2", "Guerdjikova 2026: no abstract, indication unstated, effect widely reported by 2026."),
    45: ("out", "E4", "T3", "Serratrice 2002: sudden psychosis the authors attribute to coeliac disease."),
    53: ("out", "E3", "T1", "Kaltenboeck 2023: off-label esketamine aimed at the OCD and depression (settled 14 Nov)."),
    55: ("out", "context", "", "Pintor 2022: a review chapter, kept as a context record, not a case."),
    78: ("out", "E3", "T2", "Takizawa 2026: GLP-1 drugs cutting drinking was expected by 2026; only one of three had alcohol use disorder."),
    82: ("out", "E3", "T1", "Yashkov 2006: bariatric surgery offered as a treatment for severe bulimia."),
    94: ("out", "E4", "T3", "Shahani 2019: psychiatric syndromes of temporal lobe epilepsy improving with seizure control."),
}

out = []
for r in B["records"]:
    if (r["brendan"] == "E") == (r["claude"] == "E"):
        continue
    i = r["i"]
    fin, code, rule, note = FINAL[i]
    first_b = "in" if r["brendan"] != "E" else "out"
    first_c = "in" if r["claude"] != "E" else "out"
    out.append({"i": i, "record_id": K[i]["record_id"], "src": S[i]["src"], "id": S[i]["id"], "stratum": K[i]["stratum"],
                "brendan": first_b, "claude_first": first_c, "final": fin, "code": code, "rule": rule,
                "matched": "brendan" if fin == first_b else "claude", "note": note})
assert len(out) == len(FINAL) == 22
tally = {"brendan_in_claude_out": {}, "claude_in_brendan_out": {}}
for o in out:
    k = "brendan_in_claude_out" if o["brendan"] == "in" else "claude_in_brendan_out"
    tally[k][o["matched"]] = tally[k].get(o["matched"], 0) + 1
(ROOT / "queries/calibration_v1_adjudication.json").write_text(json.dumps(
    {"meta": {"set": "calibration_v1", "adjudicated": "2026-11-22", "by": "Claude, from the abstracts (PubMed) and earlier full texts",
              "protocol": "v1.8.6"}, "tally": tally, "records": out}, indent=1, ensure_ascii=False) + "\n")
print(tally)
