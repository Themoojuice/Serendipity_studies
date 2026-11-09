"""Title score used to rank broad search results for screening (protocol §10).

Same rules as the in-browser scorer used on 2026-11-09 (Europe PMC and Embase).
Higher = more likely to describe an unexpected resolution. The score orders the
queue; it never excludes anything. Screening runs down the ranked list until
the stopping rule is met.

Validation on 2026-11-09 (first 12,000 Europe PMC records of the v1.2 broad
query): 20 of 29 gold cases present ranked in the top 2%, all 29 in the top 14%.
"""
import re

R = {
    "syn": re.compile(r"schizophren|psychos|psychotic|obsessi|compuls|\bocd\b|tourette|\btics?\b|depress|bipolar|\bmania\b|manic|anorexia|bulimi|binge|eating disorder|alcohol(ism| use| dependen| addict| abuse)|addict|dependen|smok|nicotine|cigarette|tobacco|gambl|cocaine|heroin|opioid use|methamphetamine|kleptoman|pyroman|trichotill|paraphil|pedophil|paedophil|conversion disorder|functional neurological|ptsd|post-?traumatic stress|panic|anxiety|hoarding|body dysmorphic|catatoni|delusion|hallucinat|impulse.control|\bpica\b|craving|mental illness|psychiatric (illness|disorder|symptom)", re.I),
    "chg": re.compile(r"remission|remit|resol|disappear|abolish|cessation|ceased|cured|\bcure\b|relief|reliev|improv|ameliorat|disrupt|\bquit|stopp|abstinen|loss of|\blost\b|reduc|decreas|attenuat|alleviat|normali[sz]|recover|benefi|free of|eliminat|vanish|suppress|effective|response to|responded", re.I),
    "unx": re.compile(r"unexpect|incidental|serendip|fortuit|surpris|accident|unanticipat|paradox|unintend|side benefit|off-target|collateral|inadvertent|mistaken|coincident|unforeseen|unusual (effect|benefit|improvement)|curious|dramatic", re.I),
    "trg": re.compile(r"stroke|infarct|lesion|damage|injur|hemorrhag|haemorrhag|tumou?r|glioma|meningioma|surgery|neurosurg|stimulation|\bdbs\b|rtms|\bect\b|electroconvuls|seizure|epilep|fever|malaria|infection|sepsis|covid|transplant|dialysis|coma\b|anesthe|anaesthe|chemotherap|rituximab|immun|semaglutide|liraglutide|tirzepatide|glp-?1|dulaglutide|exenatide|antibiotic|minocycline|\bdiet|ketogenic|gluten|bariatric|cannabi|marijuana|psilocyb|\blsd\b|ketamine|mdma|leucotomy|lobotomy|botulinum|baclofen|propranolol|statin|thiamine|wernicke|hypoxi|anoxi|cardiac arrest|\bafter\b|following|\bduring\b", re.I),
    "ind": re.compile(r"(induced|associated|related|precipitated|triggered|onset)\s+(\w+[\s-]+){0,2}(psychos|psychotic|mania|manic|depress|catatoni|delirium|hallucinat|obsess|compuls|tics|gambl|hypersex|impuls|anxiety|panic)", re.I),
    "neg": re.compile(r"presenting (as|with)|masquerad|mimick|new[- ]onset|de novo|\bcaused by\b|toxicity|overdose|poisoning|withdrawal|neuroleptic malignant|serotonin syndrome|delirium|encephalitis|exacerbat|worsen|relapse|emergence|unmask|misdiagnos|diagnostic challenge|secondary (psychosis|mania|depression)", re.I),
}


def score(title, pub_type=""):
    t = title or ""
    syn, chg, unx, trg = (bool(R[k].search(t)) for k in ("syn", "chg", "unx", "trg"))
    s = 3 * syn + 3 * chg + 4 * unx + 1 * trg
    if syn and chg:
        s += 3
    if syn and chg and trg:
        s += 2
    if R["ind"].search(t):
        s -= 5
    if R["neg"].search(t):
        s -= 3
    pt = (pub_type or "").lower()
    if "case report" in pt:
        s += 1
    if "review" in pt and "case" not in pt:
        s -= 1
    if "clinical trial" in pt or "randomized" in pt:
        s -= 3
    return s


if __name__ == "__main__":
    for t in ["Disruption of cigarette smoking addiction after posterior cingulate damage.",
              "Steroid-induced psychosis in a patient with lupus",
              "Unexpected remission of OCD after stroke: a case report"]:
        print(score(t, "case reports"), t)
