"""Builds data/cases.json for the Serendipity Case Library.
All identifiers (PMID, PMCID, DOI, volume, pages) were verified against Europe PMC on 2026-11-09.
"""
import json, os

ADDED = "2026-11-09"

VOCAB = {
    "syndrome_category": [
        "Psychotic", "Mood", "Obsessive-compulsive & tic", "Substance & addictive",
        "Eating", "Impulse-control", "Paraphilic", "Functional neurological", "Anxiety"],
    "trigger_category": [
        "Acquired brain lesion", "Traumatic brain injury", "Neurosurgery", "Brain stimulation",
        "Medication for another condition", "Recreational substance", "Diet", "Fever / infection",
        "Seizures", "Immune reset", "Coma / anaesthesia"],
    "trigger_intent": [
        "Treatment for another condition", "Injury or illness", "Self-administered", "Lifestyle change"],
    "resolution": ["Complete", "Partial", "Temporary", "Unclear"],
    "reversal": ["None reported", "Natural off-on", "On-off rechallenge"],
    "design": ["Case report", "Case series", "Lesion series", "Letter", "Historical review",
               "Pooled analysis", "Registry study"],
    "downstream_level": {
        "0": "None yet", "1": "Similar cases reported", "2": "Pooled analysis or pilot study",
        "3": "Randomised trial", "4": "Changed practice or major prize"},
    "tier": {"A": "Strong: high yield or well documented", "B": "Supporting case or replication"},
}

FREE_PDF = {  # free publisher full text where there is no PMC copy
    "richards-2024": "https://www.psychiatrist.com/wp-content/uploads/2023/11/Significant-Decrease-Alcohol-Use-Disorder-Symptoms-jcp-23m15068.pdf",
    "yaryura-tobias-2003": "https://doi.org/10.1590/S1516-44462003000100008",
}

R = []

def rec(id, *, authors, title, journal, year, vol="", issue="", pages="", doi="", pmid="", pmcid="",
        design, n=None, syn_cat, syn, chronic=None, tr=None, trig_cat, trig, intent,
        resolution, time_to=None, follow_up=None, reversal="None reported", down=0, down_note="",
        down_links=None, summary, tags, tier=None, collections=(), record_type="case",
        status="Included", same_patient_as=None, found_via="", caveat="", alt_links=None):
    full = None
    if pmcid:
        full = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
    elif id in FREE_PDF:
        full = FREE_PDF[id]
    R.append({
        "id": id, "record_type": record_type, "status": status, "tier": tier,
        "collections": list(collections),
        "citation": {"authors": authors, "title": title, "journal": journal, "year": year,
                     "volume": vol, "issue": issue, "pages": pages},
        "ids": {"doi": doi, "pmid": pmid, "pmcid": pmcid},
        "links": {
            "full_text": full,
            "abstract": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
            "doi": f"https://doi.org/{doi}" if doi else None,
            "alternates": alt_links or []},
        "access": "Free full text" if full else "Paywalled",
        "design": design, "n_patients": n,
        "syndrome": {"categories": syn_cat, "specific": syn, "chronic": chronic, "treatment_resistant": tr},
        "trigger": {"category": trig_cat, "specific": trig, "intent": intent},
        "outcome": {"resolution": resolution, "time_to_resolution": time_to, "follow_up": follow_up,
                    "reversal": reversal},
        "downstream": {"level": down, "note": down_note, "links": down_links or []},
        "summary": summary, "caveat": caveat, "tags": sorted(set(tags)),
        "same_patient_as": same_patient_as, "found_via": found_via,
        "date_added": ADDED, "verified": f"{ADDED}: Europe PMC record matched",
    })

# ---------------- Original top 12 ----------------
rec("mallet-2002", authors="Mallet L, Mesnage V, Houeto JL, et al.", title="Compulsions, Parkinson's disease, and stimulation.",
    journal="Lancet", year=2002, vol="360", issue="9342", pages="1302-1304", doi="10.1016/S0140-6736(02)11339-0", pmid="12414208",
    design="Case series", n=2, syn_cat=["Obsessive-compulsive & tic"], syn="Severe obsessive-compulsive disorder (comorbid Parkinson's disease)", chronic=True,
    trig_cat="Brain stimulation", trig="Subthalamic nucleus DBS for Parkinson's motor symptoms", intent="Treatment for another condition",
    resolution="Partial", time_to="2 weeks",
    down=3, down_note="French STOC randomised crossover trial of subthalamic stimulation for OCD", down_links=[{"label": "Mallet et al., NEJM 2008", "doi": "10.1056/NEJMoa0708514"}],
    summary="Compulsions disappeared two weeks after subthalamic stimulation for Parkinson's disease; Yale-Brown scores fell 58% and 64%.",
    tags=["dbs", "subthalamic-nucleus", "parkinsons", "ocd", "rct-followed", "replicated"], tier="A", collections=["top12"], found_via="Web search")

rec("naqvi-2007", authors="Naqvi NH, Rudrauf D, Damasio H, Bechara A.", title="Damage to the insula disrupts addiction to cigarette smoking.",
    journal="Science", year=2007, vol="315", issue="5811", pages="531-534", doi="10.1126/science.1135926", pmid="17255515", pmcid="PMC3698854",
    design="Lesion series", n=19, syn_cat=["Substance & addictive"], syn="Tobacco addiction", chronic=True,
    trig_cat="Acquired brain lesion", trig="Insula damage from stroke or surgery", intent="Injury or illness",
    resolution="Complete",
    down=2, down_note="Lesion network mapping pooled such cases into one remission circuit", down_links=[{"label": "Joutsa et al., Nat Med 2022", "doi": "10.1038/s41591-022-01834-y"}],
    summary="Smokers with insula damage were far more likely to quit at once, without relapse or persisting urge, than smokers with lesions elsewhere.",
    tags=["lesion", "insula", "smoking", "addiction", "pooled-analysis", "replicated"], tier="A", collections=["top12"], found_via="Web search",
    caveat="19 insula-lesioned smokers; retrospective comparison with 50 non-insula lesions.")

rec("wagner-jauregg-1883", authors="Whitrow M.", title="Wagner-Jauregg and fever therapy.",
    journal="Med Hist", year=1990, vol="34", issue="3", pages="294-310", doi="10.1017/s0025727300052431", pmid="2214949", pmcid="PMC1036142",
    design="Historical review", n=1, syn_cat=["Psychotic"], syn="Severe psychosis (index patient, Vienna 1883)",
    trig_cat="Fever / infection", trig="Erysipelas with high fever", intent="Injury or illness",
    resolution="Complete",
    down=4, down_note="Malaria fever therapy for general paresis; first psychiatric Nobel Prize (1927)",
    summary="A woman's severe psychosis cleared after erysipelas; decades later Wagner-Jauregg induced fever deliberately and won the Nobel Prize.",
    tags=["fever", "infection", "historical", "nobel", "psychosis"], tier="A", collections=["top12"], found_via="Web search",
    caveat="Secondary source; the 1887 German original is not online.",
    alt_links=[{"label": "Tsay 2013, Yale J Biol Med (free)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3670443/"}])

rec("richards-2024", authors="Richards JR, Dorand MF, Royal K, et al.", title="Significant Decrease in Alcohol Use Disorder Symptoms Secondary to Semaglutide Therapy for Weight Loss: A Case Series.",
    journal="J Clin Psychiatry", year=2024, vol="85", issue="1", pages="23m15068", doi="10.4088/JCP.23m15068", pmid="38019594",
    design="Case series", n=6, syn_cat=["Substance & addictive"], syn="Alcohol use disorder",
    trig_cat="Medication for another condition", trig="Semaglutide for weight loss", intent="Treatment for another condition",
    resolution="Partial",
    down=3, down_note="Phase 2 randomised trial of semaglutide in alcohol use disorder", down_links=[{"label": "Hendershot et al., JAMA Psychiatry 2025", "doi": "10.1001/jamapsychiatry.2024.4789"}],
    summary="All six patients prescribed semaglutide for weight had marked falls in Alcohol Use Disorders Identification Test scores (mean 9.5 points).",
    tags=["glp1", "semaglutide", "alcohol", "rct-followed", "replicated"], tier="A", collections=["top12"], found_via="Web search")

rec("kuhn-2007", authors="Kuhn J, Lenartz D, Huff W, et al.", title="Remission of alcohol dependency following deep brain stimulation of the nucleus accumbens: valuable therapeutic implications?",
    journal="J Neurol Neurosurg Psychiatry", year=2007, vol="78", issue="10", pages="1152-1153", doi="10.1136/jnnp.2006.113092", pmid="17878197", pmcid="PMC2117573",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Alcohol dependence (comorbid)", chronic=True,
    trig_cat="Brain stimulation", trig="Nucleus accumbens DBS for severe anxiety and secondary depression", intent="Treatment for another condition",
    resolution="Complete",
    down=3, down_note="Double-blind randomised trial of accumbens DBS in treatment-resistant alcohol use disorder (Bach et al., Transl Psychiatry 2023)",
    summary="Accumbens stimulation barely helped the target anxiety disorder but produced an unintended remission of alcohol dependence.",
    tags=["dbs", "nucleus-accumbens", "alcohol", "rct-followed"], tier="A", collections=["top12"], found_via="Web search",
    alt_links=[{"label": "Republished in BMJ Case Rep 2009 (free)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3030006/"}])

rec("israel-2010", authors="Israël M, Steiger H, Kolivakis T, McGregor L, Sadikot AF.", title="Deep brain stimulation in the subgenual cingulate cortex for an intractable eating disorder.",
    journal="Biol Psychiatry", year=2010, vol="67", issue="9", pages="e53-4", doi="10.1016/j.biopsych.2009.11.016", pmid="20044072",
    design="Case report", n=1, syn_cat=["Eating"], syn="Chronic intractable eating disorder (restrictive)", chronic=True, tr=True,
    trig_cat="Brain stimulation", trig="Subgenual cingulate DBS for treatment-resistant depression", intent="Treatment for another condition",
    resolution="Complete", follow_up="3 years",
    down=2, down_note="Phase 1 trial of subcallosal cingulate DBS in anorexia nervosa (Lipsman et al., Lancet 2013;381:1361-70)",
    summary="Stimulation aimed at refractory depression put the patient's comorbid chronic eating disorder into lasting remission, with weight normalised.",
    tags=["dbs", "subgenual-cingulate", "anorexia", "eating", "pilot-followed"], tier="A", collections=["top12"], found_via="Web search")

rec("moreno-delgado-1997", authors="Moreno FA, Delgado PL.", title="Hallucinogen-induced relief of obsessions and compulsions.",
    journal="Am J Psychiatry", year=1997, vol="154", issue="7", pages="1037-1038", doi="10.1176/ajp.154.7.1037b", pmid="9210762",
    design="Letter", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Obsessive-compulsive disorder",
    trig_cat="Recreational substance", trig="Psilocybin mushrooms", intent="Self-administered",
    resolution="Partial",
    down=2, down_note="First psilocybin trial in OCD", down_links=[{"label": "Moreno et al., J Clin Psychiatry 2006", "doi": "10.4088/JCP.v67n1110"}],
    summary="A man was free of obsessions during psilocybin intoxication, and relief persisted with repeated use despite tolerance to the psychedelic effects.",
    tags=["psychedelic", "psilocybin", "ocd", "pilot-followed", "replicated"], tier="A", collections=["top12"], found_via="Web search")

rec("miyaoka-2017", authors="Miyaoka T, Wake R, Hashioka S, et al.", title="Remission of Psychosis in Treatment-Resistant Schizophrenia following Bone Marrow Transplantation: A Case Report.",
    journal="Front Psychiatry", year=2017, vol="8", pages="174", doi="10.3389/fpsyt.2017.00174", pmid="28983259", pmcid="PMC5613125",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Treatment-resistant paranoid schizophrenia", chronic=True, tr=True,
    trig_cat="Immune reset", trig="Bone marrow transplant for acute myeloid leukaemia", intent="Treatment for another condition",
    resolution="Complete", time_to="30 days", follow_up="8 years",
    down=1, down_note="Registry studies have since tested the immune-transfer idea (see context records)",
    summary="Psychosis almost vanished within 30 days of a marrow transplant for leukaemia and stayed gone off antipsychotics at 8 years.",
    tags=["transplant", "immune", "schizophrenia", "treatment-resistant"], tier="A", collections=["top12"], found_via="Web search",
    caveat="Confounded by post-transplant methotrexate, ciclosporin and tacrolimus.")

rec("kraft-westman-2009", authors="Kraft BD, Westman EC.", title="Schizophrenia, gluten, and low-carbohydrate, ketogenic diets: a case report and review of the literature.",
    journal="Nutr Metab (Lond)", year=2009, vol="6", pages="10", doi="10.1186/1743-7075-6-10", pmid="19245705", pmcid="PMC2652467",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Schizophrenia with hallucinations since age 17", chronic=True, tr=True,
    trig_cat="Diet", trig="Low-carbohydrate ketogenic diet for weight loss", intent="Lifestyle change",
    resolution="Complete", follow_up="12 months (12 years per Palmer 2019)",
    down=1, down_note="Further ketogenic-diet cases (Palmer 2017, 2019; Laurent 2025)",
    summary="A 70-year-old's hallucinations of 53 years stopped abruptly after she started a ketogenic diet to lose weight.",
    tags=["diet", "ketogenic", "schizophrenia", "replicated"], tier="A", collections=["top12"], found_via="Web search")

rec("de-santis-1997", authors="De Santis A, Addolorato G, Romito A, et al.", title="Schizophrenic symptoms and SPECT abnormalities in a coeliac patient: regression after a gluten-free diet.",
    journal="J Intern Med", year=1997, vol="242", issue="5", pages="421-423", doi="10.1046/j.1365-2796.1997.00200.x", pmid="9408073",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Established 'schizophrenic' disorder (possibly secondary to coeliac disease)", chronic=True,
    trig_cat="Diet", trig="Gluten-free diet for newly diagnosed coeliac disease", intent="Treatment for another condition",
    resolution="Complete",
    down=1, down_note="Later cases of gluten-related psychosis",
    summary="Psychiatric symptoms disappeared on a gluten-free diet, and frontal hypoperfusion on SPECT normalised with them.",
    tags=["diet", "gluten", "coeliac", "psychosis", "imaging"], tier="A", collections=["top12"], found_via="Web search",
    caveat="Arguably a misdiagnosed secondary psychosis.")

rec("solyom-1987", authors="Solyom L, Turnbull IM, Wilensky M.", title="A case of self-inflicted leucotomy.",
    journal="Br J Psychiatry", year=1987, vol="151", pages="855-857", doi="10.1192/bjp.151.6.855", pmid="3502814",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Disabling obsessive-compulsive disorder", chronic=True,
    trig_cat="Traumatic brain injury", trig="Self-inflicted gunshot wound, left frontal lobe", intent="Injury or illness",
    resolution="Partial",
    down=1, down_note="Heads a trail of lesion-OCD cases",
    summary="After a gunshot wound to the left frontal lobe, a 19-year-old's rituals were markedly reduced without intellectual decline.",
    tags=["tbi", "frontal", "gunshot", "ocd", "historical"], tier="A", collections=["top12"], found_via="Web search")

rec("yaryura-tobias-2003", authors="Yaryura-Tobias JA, Neziroglu F.", title="Basal ganglia hemorrhagic ablation associated with temporary suppression of obsessive-compulsive symptoms.",
    journal="Rev Bras Psiquiatr", year=2003, vol="25", issue="1", pages="40-42", doi="10.1590/S1516-44462003000100008", pmid="12975678",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Severe obsessive-compulsive disorder", chronic=True,
    trig_cat="Acquired brain lesion", trig="Left basal ganglia haemorrhage", intent="Injury or illness",
    resolution="Temporary", reversal="Natural off-on",
    down=1, down_note="Cited among lesion-OCD cases",
    summary="Severe OCD disappeared after a basal ganglia haemorrhage and returned as the blood was reabsorbed.",
    tags=["lesion", "basal-ganglia", "ocd", "off-on"], tier="A", collections=["top12"], found_via="Web search")

# ---------------- Round 1 near misses that fit ----------------
rec("leonard-rapoport-1987", authors="Leonard HL, Rapoport JL.", title="Relief of obsessive-compulsive symptoms by LSD and psilocin.",
    journal="Am J Psychiatry", year=1987, vol="144", issue="9", pages="1239-1240", doi="10.1176/ajp.144.9.1239b", pmid="3631327",
    design="Letter", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Severe obsessive-compulsive disorder with substance use",
    trig_cat="Recreational substance", trig="LSD and psilocin", intent="Self-administered",
    resolution="Unclear", down=2, down_note="Same pathway as Moreno & Delgado 1997",
    summary="An adolescent with severe OCD reported relief of symptoms after taking LSD and psilocin.",
    tags=["psychedelic", "lsd", "psilocybin", "ocd"], tier="B", collections=["round1"], found_via="Web search")

rec("palmer-2017", authors="Palmer CM.", title="Ketogenic diet in the treatment of schizoaffective disorder: Two case studies.",
    journal="Schizophr Res", year=2017, vol="189", pages="208-209", doi="10.1016/j.schres.2017.01.053", pmid="28162810",
    design="Case series", n=2, syn_cat=["Psychotic"], syn="Treatment-resistant schizoaffective disorder", chronic=True, tr=True,
    trig_cat="Diet", trig="Ketogenic diet started for weight loss", intent="Lifestyle change",
    resolution="Partial", reversal="On-off rechallenge",
    down=1, summary="Two patients with refractory schizoaffective disorder improved on a ketogenic diet begun for weight loss, worsening when they stopped it.",
    tags=["diet", "ketogenic", "schizoaffective", "rechallenge"], tier="B", collections=["round1"], found_via="Web search",
    caveat="On-off pattern reported in a secondary summary; check the full text.")

rec("palmer-2019", authors="Palmer CM, Gilbert-Jaramillo J, Westman EC.", title="The ketogenic diet and remission of psychotic symptoms in schizophrenia: Two case studies.",
    journal="Schizophr Res", year=2019, vol="208", pages="439-440", doi="10.1016/j.schres.2019.03.019", pmid="30962118",
    design="Case series", n=2, syn_cat=["Psychotic"], syn="Chronic schizophrenia", chronic=True,
    trig_cat="Diet", trig="Ketogenic diet", intent="Lifestyle change",
    resolution="Complete", follow_up="Up to 12 years",
    down=1, summary="Two women with chronic schizophrenia in remission on a ketogenic diet, including a 12-year follow-up of the Kraft & Westman patient.",
    tags=["diet", "ketogenic", "schizophrenia", "follow-up"], tier="B", collections=["round1"], same_patient_as="kraft-westman-2009", found_via="Web search",
    caveat="One of the two patients is the Kraft & Westman 2009 patient: do not double-count.")

rec("fontaine-2004", authors="Fontaine D, Mattei V, Borg M, et al.", title="Effect of subthalamic nucleus stimulation on obsessive-compulsive disorder in a patient with Parkinson disease. Case report.",
    journal="J Neurosurg", year=2004, vol="100", issue="6", pages="1084-1086", doi="10.3171/jns.2004.100.6.1084", pmid="15200126",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Severe obsessive-compulsive disorder of 16 years (comorbid Parkinson's disease)", chronic=True,
    trig_cat="Brain stimulation", trig="Subthalamic nucleus DBS for Parkinson's disease", intent="Treatment for another condition",
    resolution="Complete", follow_up="1 year",
    down=3, down_note="Independent replication of Mallet 2002; STOC trial followed",
    summary="Subthalamic stimulation for Parkinson's took a 16-year OCD from Yale-Brown 32 to 1 at one year.",
    tags=["dbs", "subthalamic-nucleus", "parkinsons", "ocd", "replication"], tier="B", collections=["round1"], found_via="Web search")

rec("oh-2011", authors="Oh JH, Ahn BY, Jo MK, et al.", title="Obsessive-compulsive behavior disappearing after left capsular genu infarction.",
    journal="Case Rep Neurol", year=2011, vol="3", issue="1", pages="18-20", doi="10.1159/000323667", pmid="21327181", pmcid="PMC3037989",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Obsessive-compulsive behaviours (74-year-old woman)",
    trig_cat="Acquired brain lesion", trig="Left capsular genu infarct", intent="Injury or illness",
    resolution="Complete", down=1,
    summary="Obsessive-compulsive behaviours disappeared after an infarct at the internal capsule genu, close to the capsulotomy target.",
    tags=["lesion", "internal-capsule", "ocd"], tier="B", collections=["round1"], found_via="Web search")

rec("sani-2007", authors="Sani G, Manfredi G, Pacchiarotti I, et al.", title="A case of resolution of an acute psychotic episode after high fever.",
    journal="CNS Spectr", year=2007, vol="12", issue="6", pages="447-450", doi="10.1017/s1092852900015327", pmid="17545955",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Acute psychotic episode in schizoaffective disorder", chronic=False,
    trig_cat="Fever / infection", trig="High fever from a urinary infection", intent="Injury or illness",
    resolution="Complete", down=0,
    summary="Psychotic symptoms resolved immediately as a high fever abated, after antipsychotics had been stopped.",
    tags=["fever", "infection", "psychosis"], tier="B", collections=["round1"], found_via="Web search",
    caveat="Acute episode: spontaneous remission is plausible.")

rec("sandyk-1988", authors="Sandyk R, Awerbuch G.", title="Marijuana and Tourette's syndrome.",
    journal="J Clin Psychopharmacol", year=1988, vol="8", issue="6", pages="444-445", doi="10.1097/00004714-198812000-00021", pmid="3235704",
    design="Letter", n=None, syn_cat=["Obsessive-compulsive & tic"], syn="Tourette syndrome",
    trig_cat="Recreational substance", trig="Recreational cannabis", intent="Self-administered",
    resolution="Partial", down=3, down_note="Later THC trials in Tourette syndrome (Müller-Vahl)",
    summary="Patients with Tourette syndrome who smoked cannabis recreationally reported fewer tics, about half in one case.",
    tags=["cannabis", "tourette", "tics"], tier="B", collections=["round1"], found_via="Web search",
    caveat="Number of patients not confirmed from the abstract.")

# ---------------- Round 2, tier A ----------------
rec("moussawi-2016", authors="Moussawi K, Kalivas PW, Lee JW.", title="Abstinence From Drug Dependence After Bilateral Globus Pallidus Hypoxic-Ischemic Injury.",
    journal="Biol Psychiatry", year=2016, vol="80", issue="9", pages="e79-e80", doi="10.1016/j.biopsych.2016.04.005", pmid="27311800", pmcid="PMC5238511",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Severe alcohol and opioid dependence", chronic=True, tr=True,
    trig_cat="Acquired brain lesion", trig="Bilateral globus pallidus hypoxic-ischaemic injury after methadone overdose", intent="Injury or illness",
    resolution="Complete", down=2, down_note="Fed into the Joutsa 2022 pooled lesion analysis",
    summary="After an overdose damaged both globus pallidi, a woman with refractory alcohol and opioid dependence stayed abstinent.",
    tags=["lesion", "globus-pallidus", "hypoxia", "alcohol", "opioid", "addiction"], tier="A", collections=["round2"], found_via="Consensus")

rec("haque-2025", authors="Haque S, Bellmunt-Gil A, Davidson B, et al.", title="Remission of alcohol use disorder following traumatic brain injury with focal orbitofrontal cortex hemorrhage: case report and network mapping.",
    journal="Commun Med (Lond)", year=2025, vol="5", issue="1", pages="69", doi="10.1038/s43856-025-00760-7", pmid="40075136", pmcid="PMC11903661",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Chronic treatment-refractory alcohol use disorder", chronic=True, tr=True,
    trig_cat="Traumatic brain injury", trig="Head injury with focal left orbitofrontal haemorrhage", intent="Injury or illness",
    resolution="Complete", down=1,
    summary="A 42-year-old's refractory alcohol use disorder remitted after a focal orbitofrontal bleed; the lesion was mapped onto the addiction circuit.",
    tags=["tbi", "orbitofrontal", "alcohol", "network-mapping", "addiction"], tier="A", collections=["round2"], found_via="Consensus")

rec("mackillop-2026", authors="MacKillop EJA, McIntyre-Wood C, Vaughn DW, et al.", title="The man who forgot his addiction: Sustained remission of cocaine use disorder following overdose-induced bilateral hippocampus stroke.",
    journal="Clin Neuropsychol", year=2026, pages="1-18", doi="10.1080/13854046.2026.2651223", pmid="42011056",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Severe long-standing cocaine use disorder", chronic=True,
    trig_cat="Acquired brain lesion", trig="Bilateral hippocampal ischaemic stroke after cocaine overdose", intent="Injury or illness",
    resolution="Complete", follow_up="12 months", down=0,
    summary="A 52-year-old with bilateral hippocampal stroke and dense amnesia remained in remission from cocaine use disorder at 12 months.",
    tags=["lesion", "hippocampus", "cocaine", "amnesia", "addiction"], tier="A", collections=["round2"], found_via="Consensus")

rec("jarraya-2010", authors="Jarraya B, Brugières P, Tani N, et al.", title="Disruption of cigarette smoking addiction after posterior cingulate damage.",
    journal="J Neurosurg", year=2010, vol="113", issue="6", pages="1219-1221", doi="10.3171/2010.6.jns10346", pmid="20597598",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Tobacco addiction",
    trig_cat="Acquired brain lesion", trig="Haemorrhage from an arteriovenous malformation, posterior cingulate cortex", intent="Injury or illness",
    resolution="Complete", time_to="Immediate", down=1,
    summary="A 35-year-old's smoking addiction stopped immediately and completely after a posterior cingulate haemorrhage.",
    tags=["lesion", "posterior-cingulate", "smoking", "addiction"], tier="A", collections=["round2"], found_via="Consensus")

rec("yeung-2020", authors="Yeung A, Rapoport M.", title="Paradoxical complete and spontaneous resolution of depression, psychosis, and suicidal ideation following a traumatic brain injury.",
    journal="Brain Inj", year=2020, vol="34", issue="10", pages="1427-1430", doi="10.1080/02699052.2020.1805125", pmid="33331803",
    design="Case report", n=1, syn_cat=["Mood", "Psychotic"], syn="Depression with psychosis and suicidal ideation",
    trig_cat="Traumatic brain injury", trig="Closed-head left-hemisphere injury in a suicide attempt", intent="Injury or illness",
    resolution="Complete", time_to="Immediate", down=0,
    summary="A 65-year-old's depression, psychosis and suicidal ideation resolved immediately after a left-hemisphere closed head injury.",
    tags=["tbi", "depression", "psychosis"], tier="A", collections=["round2"], found_via="Consensus")

rec("smith-2025", authors="Smith S, Kumar M, Absher J.", title="Frontal damage and resolution of schizophrenia in a patient with self-inflicted gunshot wound: a case report.",
    journal="BMC Neurol", year=2025, vol="25", issue="1", pages="78", doi="10.1186/s12883-024-03862-2", pmid="39994665", pmcid="PMC11849385",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Paranoid schizophrenia", chronic=True,
    trig_cat="Traumatic brain injury", trig="Self-inflicted gunshot wound with frontal damage", intent="Injury or illness",
    resolution="Complete", follow_up="7 years", down=0,
    summary="Psychosis resolved after a frontal gunshot wound and was still resolved at reassessment seven years later.",
    tags=["tbi", "frontal", "gunshot", "schizophrenia"], tier="A", collections=["round2"], found_via="PubMed")

rec("erol-durgun-2026", authors="Erol Durgun O, Sivan M, Sapsford H, Haider J.", title="Improvement in psychiatric symptoms after subdural haematoma and decompressive craniotomy.",
    journal="BMJ Case Rep", year=2026, vol="19", issue="4", pages="e266529", doi="10.1136/bcr-2025-266529", pmid="41946537",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Paranoid schizophrenia with autism and a personality disorder", chronic=True,
    trig_cat="Traumatic brain injury", trig="Left subdural haematoma and decompressive craniotomy", intent="Injury or illness",
    resolution="Partial", down=0,
    summary="Long-standing hallucinations and self-harm resolved after a subdural haematoma and craniotomy, and antipsychotics were tapered.",
    tags=["tbi", "neurosurgery", "schizophrenia", "confounded"], tier="A", collections=["round2"], found_via="PubMed",
    caveat="Confounded by a structured rehabilitation setting and reduced polypharmacy.")

rec("diamond-2011", authors="Diamond A, Ondo WG.", title="Resolution of severe obsessive--compulsive disorder after a small unilateral nondominant frontoparietal infarct.",
    journal="Int J Neurosci", year=2011, vol="121", issue="7", pages="405-407", doi="10.3109/00207454.2011.561941", pmid="21426244",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Severe obsessive-compulsive disorder", chronic=True,
    trig_cat="Acquired brain lesion", trig="Small right posterior frontoparietal infarct", intent="Injury or illness",
    resolution="Complete", time_to="Immediate", down=0,
    summary="Severe OCD disappeared immediately after a small right frontoparietal infarct.",
    tags=["lesion", "frontoparietal", "ocd"], tier="A", collections=["round2"], found_via="PubMed")

rec("sosa-gomez-2026", authors="Sosa Gomez AE, Go RM, Valdez D.", title="Seizure-Induced Resolution of Depressive and Psychotic Symptoms in a Pregnant Patient: A Case of Spontaneous Neuromodulation.",
    journal="Cureus", year=2026, vol="18", issue="6", pages="e110418", doi="10.7759/cureus.110418", pmid="42422634", pmcid="PMC13343248",
    design="Case report", n=1, syn_cat=["Mood", "Psychotic"], syn="Treatment-resistant depression with psychotic features", chronic=True, tr=True,
    trig_cat="Seizures", trig="Spontaneous seizures during pregnancy", intent="Injury or illness",
    resolution="Complete", down=0,
    summary="A 23-year-old's treatment-resistant psychotic depression resolved after spontaneous seizures in pregnancy.",
    tags=["seizure", "depression", "psychosis", "pregnancy", "convulsive"], tier="A", collections=["round2"], found_via="Consensus")

rec("gupta-2026", authors="Gupta RR, Ramdurg S.", title="Remission of Psychotic Symptoms Following Seizures in a Patient With an Episodic Psychotic Disorder.",
    journal="Cureus", year=2026, vol="18", issue="3", pages="e104667", doi="10.7759/cureus.104667", pmid="41939690", pmcid="PMC13048452",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Relapse of an episodic psychotic disorder",
    trig_cat="Seizures", trig="Two febrile generalised seizures needing intensive care", intent="Injury or illness",
    resolution="Complete", down=0,
    summary="Psychosis remitted completely after two febrile generalised seizures and stayed in remission at follow-up.",
    tags=["seizure", "fever", "psychosis", "convulsive"], tier="A", collections=["round2"], found_via="PubMed",
    caveat="Episodic illness and partial antipsychotic response beforehand.")

rec("faruqui-2022", authors="Faruqui Z, Kim C.", title="The Incidental Resolution of Severe Alcohol Use Disorder during Esketamine Treatment of Major Depressive Disorder: A Case Report.",
    journal="Case Rep Psychiatry", year=2022, pages="8992697", doi="10.1155/2022/8992697", pmid="36568330", pmcid="PMC9779988",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Severe alcohol use disorder", chronic=True,
    trig_cat="Medication for another condition", trig="Intranasal esketamine for treatment-resistant depression", intent="Treatment for another condition",
    resolution="Complete", down=0,
    summary="A 61-year-old's severe alcohol use disorder resolved during esketamine treatment given for her depression.",
    tags=["ketamine", "esketamine", "alcohol"], tier="A", collections=["round2"], found_via="PubMed")

rec("jewett-2020", authors="Jewett BE, Miller MN, Ligon LA, et al.", title="Rapid and temporary improvement of depression and anxiety observed following niraparib administration: a case report.",
    journal="BMC Psychiatry", year=2020, vol="20", issue="1", pages="171", doi="10.1186/s12888-020-02590-4", pmid="32295563", pmcid="PMC7161116",
    design="Case report", n=1, syn_cat=["Mood", "Anxiety"], syn="Recurrent major depression with generalised anxiety", tr=True,
    trig_cat="Medication for another condition", trig="Niraparib (PARP inhibitor) maintenance for ovarian cancer", intent="Treatment for another condition",
    resolution="Temporary", time_to="Rapid", down=0,
    summary="Depression and anxiety that had resisted several medicines resolved rapidly but temporarily after niraparib was started for ovarian cancer.",
    tags=["parp-inhibitor", "oncology", "depression", "anxiety", "temporary"], tier="A", collections=["round2"], found_via="PubMed")

rec("downar-2012", authors="Downar J, Sankar A, Giacobbe P, Woodside B, Colton P.", title="Unanticipated Rapid Remission of Refractory Bulimia Nervosa, during High-Dose Repetitive Transcranial Magnetic Stimulation of the Dorsomedial Prefrontal Cortex: A Case Report.",
    journal="Front Psychiatry", year=2012, vol="3", pages="30", doi="10.3389/fpsyt.2012.00030", pmid="22529822", pmcid="PMC3330246",
    design="Case report", n=1, syn_cat=["Eating"], syn="Severe refractory bulimia nervosa", chronic=True, tr=True,
    trig_cat="Brain stimulation", trig="Dorsomedial prefrontal rTMS for comorbid depression", intent="Treatment for another condition",
    resolution="Complete", time_to="After session 2", follow_up="More than 2 months", down=1,
    summary="Twice-daily five-hour binge-purge episodes stopped after the second session of rTMS given for depression.",
    tags=["rtms", "dorsomedial-prefrontal", "bulimia", "eating"], tier="A", collections=["round2"], found_via="Europe PMC full text")

rec("abdollahifard-2026", authors="Abdollahifard S, Mostafeenezhad N, Yousefi O, et al.", title="Incidental resolution of pedophilia in a patient undergoing deep brain stimulation (DBS) for obsessive-compulsive disorder (OCD): a case report and long-term follow-up.",
    journal="Neurol Sci", year=2026, vol="47", issue="2", pages="223", doi="10.1007/s10072-026-08808-9", pmid="41629421",
    design="Case report", n=1, syn_cat=["Paraphilic"], syn="Paedophilic disorder (comorbid with refractory OCD)",
    trig_cat="Brain stimulation", trig="Bed nucleus of stria terminalis / anterior capsule DBS for OCD", intent="Treatment for another condition",
    resolution="Complete", follow_up="Long-term", down=0,
    summary="Paedophilic desires resolved gradually after DBS for OCD, documented by serial assessments over long-term follow-up.",
    tags=["dbs", "bnst", "paraphilia", "ocd"], tier="A", collections=["round2"], found_via="PubMed")

rec("klok-2025", authors="Klok PM, Vermeulen M, Stone J, Bloem BR.", title="Improvement of functional paralysis following unexpected comatose states.",
    journal="Pract Neurol", year=2025, vol="25", issue="6", pages="562-565", doi="10.1136/pn-2024-004510", pmid="40335277",
    design="Case series", n=2, syn_cat=["Functional neurological"], syn="Chronic functional paralysis", chronic=True,
    trig_cat="Coma / anaesthesia", trig="Medically induced coma for COVID respiratory distress; coma after an overdose", intent="Injury or illness",
    resolution="Complete", down=0,
    summary="Two patients' long-standing functional paralysis recovered after unplanned comatose states.",
    tags=["coma", "anaesthesia", "functional-neurological"], tier="A", collections=["round2"], found_via="Consensus")

# ---------------- Round 2, tier B ----------------
rec("hefzy-2011", authors="Hefzy H, Silver RW, Silver B.", title="The no smoking sign--insular infarction.",
    journal="J Neuroimaging", year=2011, vol="21", issue="2", pages="e169-70", doi="10.1111/j.1552-6569.2010.00486.x", pmid="20609039",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Tobacco addiction (40 pack-years)", chronic=True,
    trig_cat="Acquired brain lesion", trig="Insular ischaemic stroke", intent="Injury or illness",
    resolution="Complete", follow_up="5 months", down=1,
    summary="A heavy smoker stopped without aids or intent after an insular stroke, replicating Naqvi.",
    tags=["lesion", "insula", "smoking", "replication"], tier="B", collections=["round2"], found_via="PubMed")

rec("najeeb-2016", authors="Najeeb F, Silver B, Khan M.", title="Cessation of Smoking and Alcohol Addiction Following Thalamic Hemorrhage.",
    journal="Neurologist", year=2016, vol="21", issue="6", pages="91-92", doi="10.1097/nrl.0000000000000091", pmid="27801766",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Tobacco and alcohol use",
    trig_cat="Acquired brain lesion", trig="Left thalamic haemorrhage", intent="Injury or illness",
    resolution="Complete", down=1,
    summary="After a thalamic bleed a woman stopped smoking abruptly, without craving, and developed an aversion to alcohol.",
    tags=["lesion", "thalamus", "smoking", "alcohol"], tier="B", collections=["round2"], found_via="PubMed")

rec("yuan-2025", authors="Yuan M, Xu R.", title="Reduced nicotine dependence following traumatic brain injury in an elderly patient: a case report and literature review.",
    journal="Front Hum Neurosci", year=2025, vol="19", pages="1619775", doi="10.3389/fnhum.2025.1619775", pmid="40746908", pmcid="PMC12310724",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Heavy nicotine dependence (about 60 pack-years)", chronic=True,
    trig_cat="Traumatic brain injury", trig="Severe head injury with subdural and subarachnoid haemorrhage", intent="Injury or illness",
    resolution="Complete", follow_up="6 months", down=1,
    summary="An 87-year-old lost all nicotine craving after a severe head injury and was still abstinent at six months.",
    tags=["tbi", "smoking"], tier="B", collections=["round2"], found_via="PubMed")

rec("valadez-cuen-2024", authors="Valadez-Cuen K, Kozorosky E, Farahnik F, Garcia O.", title="An Unexpected Outcome of an Ischemic Stroke on the Reward Pathways in the Human Brain.",
    journal="HCA Healthc J Med", year=2024, vol="5", issue="6", pages="721-725", doi="10.36518/2689-0216.1707", pmid="39790695", pmcid="PMC11708937",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Extensive smoking history", chronic=True,
    trig_cat="Acquired brain lesion", trig="Left basal ganglia stroke including caudate and nucleus accumbens", intent="Injury or illness",
    resolution="Complete", down=1,
    summary="A 63-year-old smoker stopped after a stroke involving the caudate and nucleus accumbens.",
    tags=["lesion", "nucleus-accumbens", "basal-ganglia", "smoking"], tier="B", collections=["round2"], found_via="Consensus")

rec("pantoni-1997", authors="Pantoni L, Poggesi L, Repice A, Inzitari D.", title="Disappearance of motor tics after Wernicke's encephalopathy in a patient with Tourette's syndrome.",
    journal="Neurology", year=1997, vol="48", issue="2", pages="381-383", doi="10.1212/wnl.48.2.381", pmid="9040726",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Tourette syndrome", chronic=True,
    trig_cat="Acquired brain lesion", trig="Wernicke encephalopathy with a dorsal midbrain lesion", intent="Injury or illness",
    resolution="Complete", down=0,
    summary="A 48-year-old's motor tics disappeared after a dorsal midbrain lesion from thiamine deficiency.",
    tags=["lesion", "midbrain", "wernicke", "tourette", "tics"], tier="B", collections=["round2"], found_via="PubMed")

rec("kosel-2007", authors="Kosel M, Sturm V, Frick C, et al.", title="Mood improvement after deep brain stimulation of the internal globus pallidus for tardive dyskinesia in a patient suffering from major depression.",
    journal="J Psychiatr Res", year=2007, vol="41", issue="9", pages="801-803", doi="10.1016/j.jpsychires.2006.07.010", pmid="16962613",
    design="Case report", n=1, syn_cat=["Mood"], syn="Treatment-refractory major depressive episode", tr=True,
    trig_cat="Brain stimulation", trig="Internal globus pallidus DBS for tardive dyskinesia", intent="Treatment for another condition",
    resolution="Partial", follow_up="18 months", down=0,
    summary="Pallidal stimulation for tardive dyskinesia also substantially improved a refractory depression.",
    tags=["dbs", "globus-pallidus", "depression"], tier="B", collections=["round2"], found_via="PubMed")

rec("sciortino-2021", authors="Sciortino D, Schiena G, Cantù F, Maggioni E, Brambilla P.", title="Case Report: Repeated Transcranial Magnetic Stimulation Improves Comorbid Binge Eating Disorder in Two Female Patients With Treatment-Resistant Bipolar Depression.",
    journal="Front Psychiatry", year=2021, vol="12", pages="732066", doi="10.3389/fpsyt.2021.732066", pmid="34955908", pmcid="PMC8695790",
    design="Case series", n=2, syn_cat=["Eating"], syn="Binge eating disorder (comorbid bipolar II depression)",
    trig_cat="Brain stimulation", trig="Accelerated iTBS to left dorsolateral prefrontal cortex for bipolar depression", intent="Treatment for another condition",
    resolution="Partial", down=0,
    summary="Binge eating improved in two women given accelerated theta-burst stimulation for bipolar depression.",
    tags=["rtms", "itbs", "binge-eating", "eating"], tier="B", collections=["round2"], found_via="PubMed")

rec("rammouz-2024", authors="Rammouz I, El Oumary O, Aalouane R, Souirti Z, Boujraf S.", title="Unexpected improvement in nicotine consumption after low-frequency repetitive magnetic stimulation.",
    journal="Int J Psychiatry Clin Pract", year=2024, vol="28", issue="2", pages="142-144", doi="10.1080/13651501.2024.2417651", pmid="39417536",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Tobacco use",
    trig_cat="Brain stimulation", trig="1 Hz rTMS for depression and OCD", intent="Treatment for another condition",
    resolution="Partial", down=0,
    summary="Cigarette consumption fell unexpectedly in a man receiving low-frequency rTMS for depression and OCD.",
    tags=["rtms", "smoking"], tier="B", collections=["round2"], found_via="PubMed")

rec("barbieri-2005", authors="Barbieri V, Lo Russo G, Francione S, Scarone S, Gambini O.", title="Association of temporal lobe epilepsy and obsessive-compulsive disorder in a patient successfully treated with right temporal lobectomy.",
    journal="Epilepsy Behav", year=2005, vol="6", issue="4", pages="617-619", doi="10.1016/j.yebeh.2005.02.010", pmid="15907757",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Obsessive-compulsive disorder beginning with temporal lobe epilepsy",
    trig_cat="Neurosurgery", trig="Right temporal lobectomy for epilepsy", intent="Treatment for another condition",
    resolution="Complete", follow_up="1 year", down=0,
    summary="OCD that began with temporal lobe epilepsy went into near-complete remission after epilepsy surgery.",
    tags=["neurosurgery", "epilepsy", "temporal-lobe", "ocd"], tier="B", collections=["round2"], found_via="PubMed")

rec("meilinger-2026", authors="Meilinger A, Campbell MA, Reynolds HM, Chavez AS.", title="The Role of Glucagon-Like Peptide-1 Receptor Agonists in Prompting a Meaningful Improvement in Alcohol Use Disorder.",
    journal="J Prim Care Community Health", year=2026, vol="17", pages="21501319261437615", doi="10.1177/21501319261437615", pmid="41914511", pmcid="PMC13039557",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="High-risk alcohol use",
    trig_cat="Medication for another condition", trig="Semaglutide for obesity", intent="Treatment for another condition",
    resolution="Partial", follow_up="10 months", down=1,
    summary="A man prescribed semaglutide for obesity cut his drinking substantially over 10 months.",
    tags=["glp1", "semaglutide", "alcohol", "replication"], tier="B", collections=["round2"], found_via="PubMed")

rec("hill-2025", authors="Hill O, Hughes S, Singh A, Ang-Rabanes M, Mogallapu R.", title="The role of dulaglutide in the treatment of alcohol use disorder: a case report.",
    journal="Front Psychiatry", year=2025, vol="16", pages="1420316", doi="10.3389/fpsyt.2025.1420316", pmid="40375882", pmcid="PMC12078295",
    design="Case report", n=1, syn_cat=["Substance & addictive"], syn="Alcohol use disorder (about 90 beers a month)",
    trig_cat="Medication for another condition", trig="Dulaglutide for weight loss", intent="Treatment for another condition",
    resolution="Partial", down=1,
    summary="Drinking fell in a man started on dulaglutide for weight loss.",
    tags=["glp1", "dulaglutide", "alcohol", "replication"], tier="B", collections=["round2"], found_via="PubMed")

rec("takizawa-2026", authors="Takizawa H, Tsuda A, Suriki H, Amagane H.", title="Tirzepatide reduced alcohol use in three patients with alcohol-associated liver disease, type 2 diabetes, and obesity.",
    journal="Endocrinol Diabetes Metab Case Rep", year=2026, issue="2", pages="EDM260002", doi="10.1530/edm-26-0002", pmid="41925328", pmcid="PMC13052794",
    design="Case series", n=3, syn_cat=["Substance & addictive"], syn="Alcohol use (one with alcohol use disorder)",
    trig_cat="Medication for another condition", trig="Tirzepatide for type 2 diabetes and obesity", intent="Treatment for another condition",
    resolution="Partial", down=1,
    summary="Three patients with alcohol-related liver disease drank less after starting tirzepatide.",
    tags=["glp1", "tirzepatide", "alcohol", "replication"], tier="B", collections=["round2"], found_via="PubMed")

rec("guerdjikova-2026", authors="Guerdjikova AI, Walter LL, McElroy SL.", title="Improvement of Compulsive Shopping on Tirzepatide: A Case Report.",
    journal="J Clin Psychopharmacol", year=2026, vol="46", issue="3", pages="338-339", doi="10.1097/jcp.0000000000002135", pmid="41632102",
    design="Case report", n=1, syn_cat=["Impulse-control"], syn="Compulsive buying",
    trig_cat="Medication for another condition", trig="Tirzepatide", intent="Treatment for another condition",
    resolution="Partial", down=0,
    summary="Compulsive shopping improved on tirzepatide.",
    tags=["glp1", "tirzepatide", "compulsive-buying"], tier="B", collections=["round2"], found_via="PubMed",
    caveat="No abstract; indication for tirzepatide not confirmed.")

rec("kelly-2026", authors="Kelly H, Davis T.", title="Incidental Resolution of Dopamine Agonist Induced Impulse Control Disorder with GLP-1 Receptor Agonist.",
    journal="Mov Disord Clin Pract", year=2026, doi="10.1002/mdc3.70704", pmid="42260955", pmcid="PMC13338974",
    design="Case report", n=1, syn_cat=["Impulse-control"], syn="Dopamine agonist-induced impulse control disorder",
    trig_cat="Medication for another condition", trig="GLP-1 receptor agonist", intent="Treatment for another condition",
    resolution="Complete", down=0,
    summary="An impulse control disorder caused by a dopamine agonist resolved incidentally on a GLP-1 receptor agonist.",
    tags=["glp1", "impulse-control", "dopamine-agonist"], tier="B", collections=["round2"], found_via="Europe PMC full text",
    caveat="No abstract; details from title only.")

rec("lugo-radillo-2021", authors="Lugo-Radillo A, Cortes-Lopez JL.", title="Long-term Amelioration of OCD Symptoms in a Patient with Chronic Consumption of Psilocybin-containing Mushrooms.",
    journal="J Psychoactive Drugs", year=2021, vol="53", issue="2", pages="146-148", doi="10.1080/02791072.2020.1849879", pmid="33225874",
    design="Case report", n=1, syn_cat=["Obsessive-compulsive & tic"], syn="Obsessive-compulsive disorder",
    trig_cat="Recreational substance", trig="Chronic psilocybin mushroom use", intent="Self-administered",
    resolution="Partial", down=0,
    summary="A man's OCD improved meaningfully and lastingly with chronic consumption of psilocybin mushrooms.",
    tags=["psychedelic", "psilocybin", "ocd", "replication"], tier="B", collections=["round2"], found_via="PubMed")

rec("jansson-1984", authors="Jansson B, Kristjánsson E, Nilsson L.", title="[Schizophrenic psychosis disappearing after patient is given gluten-free diet].",
    journal="Lakartidningen", year=1984, vol="81", issue="6", pages="448-449", pmid="6700311",
    design="Case report", n=1, syn_cat=["Psychotic"], syn="Schizophrenic psychosis",
    trig_cat="Diet", trig="Gluten-free diet", intent="Treatment for another condition",
    resolution="Complete", down=1,
    summary="Swedish report of schizophrenic psychosis disappearing on a gluten-free diet, 13 years before De Santis.",
    tags=["diet", "gluten", "psychosis", "historical", "non-english"], tier="B", collections=["round2"], status="Provisional", found_via="PubMed",
    caveat="Swedish, no abstract: reason for the diet unconfirmed.")

# ---------------- Context (not counted as cases) ----------------
rec("joutsa-2022", authors="Joutsa J, Moussawi K, Siddiqi SH, et al.", title="Brain lesions disrupting addiction map to a common human brain circuit.",
    journal="Nat Med", year=2022, vol="28", issue="6", pages="1249-1255", doi="10.1038/s41591-022-01834-y", pmid="35697842", pmcid="PMC9205767",
    design="Pooled analysis", n=129, syn_cat=["Substance & addictive"], syn="Smoking addiction (two lesion cohorts) with alcohol risk validation",
    trig_cat="Acquired brain lesion", trig="Focal brain lesions", intent="Injury or illness",
    resolution="Unclear", down=2,
    summary="Lesions that ended smoking addiction sat in many places but mapped to one connected circuit, now a neuromodulation target.",
    tags=["pooled-analysis", "lesion", "network-mapping", "addiction"], record_type="context", collections=["round2"], found_via="Web search")

rec("ekstrom-2022", authors="Ekström LD, Pahnke S, Larfors G, et al.", title="No evidence for transmission of psychosis, bipolar or depressive disorder via hematopoietic stem cell transplantation: A Swedish registry study.",
    journal="Psychiatry Clin Neurosci", year=2022, vol="76", issue="10", pages="526-527", doi="10.1111/pcn.13448", pmid="35796307", pmcid="PMC9804901",
    design="Registry study", syn_cat=["Psychotic", "Mood"], syn="Psychosis, bipolar and depressive disorders",
    trig_cat="Immune reset", trig="Haematopoietic stem cell transplant", intent="Treatment for another condition",
    resolution="Unclear", down=0,
    summary="A national registry found no donor-to-recipient transmission of psychiatric disorders, weakening the immune-transfer reading of Miyaoka 2017.",
    tags=["registry", "transplant", "counterpoint"], record_type="context", collections=["round2"], found_via="Consensus")

rec("romer-2024", authors="Rømer TB, Sengeløv H, Christensen RHB, Benros ME.", title="Associations Between Mental Disorders in Donors and Matched Recipients of Hematopoietic Stem Cell Transplants: A Population-Based Cohort Study.",
    journal="Biol Psychiatry Glob Open Sci", year=2024, vol="4", issue="6", pages="100389", doi="10.1016/j.bpsgos.2024.100389", pmid="39416658", pmcid="PMC11480220",
    design="Registry study", n=464, syn_cat=["Psychotic", "Mood"], syn="Mental disorders in donor-recipient pairs",
    trig_cat="Immune reset", trig="Haematopoietic stem cell transplant", intent="Treatment for another condition",
    resolution="Unclear", down=0,
    summary="Danish cohort of 464 related donor-recipient pairs testing whether transplants transmit mental disorders.",
    tags=["registry", "transplant", "counterpoint"], record_type="context", collections=["round2"], found_via="Consensus",
    caveat="n counts donor-recipient pairs, not patients.")

rec("wagemaker-cade-1977", authors="Wagemaker H, Cade R.", title="The use of hemodialysis in chronic schizophrenia.",
    journal="Am J Psychiatry", year=1977, vol="134", issue="6", pages="684-685", doi="10.1176/ajp.134.6.684", pmid="869035",
    design="Case series", syn_cat=["Psychotic"], syn="Chronic drug-resistant schizophrenia",
    trig_cat="Immune reset", trig="Haemodialysis", intent="Treatment for another condition",
    resolution="Unclear", down=3, down_note="Failed under sham-controlled testing",
    down_links=[{"label": "Dialysis of schizophrenic patients: a double-blind study, Am J Psychiatry 1980", "doi": "10.1176/ajp.137.10.1220"}],
    summary="Uncontrolled remissions on dialysis set off a treatment wave that collapsed in sham-controlled trials: the cautionary tale.",
    tags=["cautionary", "haemodialysis", "psychosis", "failed-replication"], record_type="context", collections=["round1"], found_via="Web search",
    caveat="Deliberate treatment, not an accident; kept as the counterexample.")

out = {
    "library": "Serendipity Case Library",
    "schema_version": "1.0",
    "updated": ADDED,
    "unit_of_record": "One published study (a paper). n_patients counts patients within it.",
    "inclusion_criteria": [
        "A serious psychiatric syndrome resolved or substantially improved.",
        "The resolution was incidental: the triggering event or treatment was aimed at something else, or not aimed at all.",
        "Individual patients or small series; lesion series allowed when built on individual cases."],
    "vocabularies": VOCAB,
    "records": R,
}
os.makedirs("/home/claude/serendipity/library/data", exist_ok=True)
with open("/home/claude/serendipity/library/data/cases.json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

# sanity checks
ids = [r["id"] for r in R]
assert len(ids) == len(set(ids)), "duplicate ids"
for r in R:
    for c in r["syndrome"]["categories"]:
        assert c in VOCAB["syndrome_category"], (r["id"], c)
    assert r["trigger"]["category"] in VOCAB["trigger_category"], r["id"]
    assert r["trigger"]["intent"] in VOCAB["trigger_intent"], r["id"]
    assert r["outcome"]["resolution"] in VOCAB["resolution"], r["id"]
    assert r["outcome"]["reversal"] in VOCAB["reversal"], r["id"]
    assert r["design"] in VOCAB["design"], r["id"]
    assert r["links"]["full_text"] or r["links"]["abstract"], r["id"]
cases = [r for r in R if r["record_type"] == "case"]
print("records", len(R), "cases", len(cases), "free", sum(1 for r in cases if r["links"]["full_text"]),
      "patients", sum(r["n_patients"] or 0 for r in cases))
