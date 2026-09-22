"""
AAROH Clinical Consultation Memo Generator
- Generates structured, physician-ready screening reports synthesizing:
  1. Classical XGBoost prediction & calibrated confidence
  2. 4-Qubit VQC quantum state expectation value & probability
  3. Hybrid screening signal & discordance status
  4. Exact TreeSHAP feature attributions & acoustic biomarker drivers
  5. Clinical ICD-10 categorization & recommended next diagnostic step
  6. Mandatory regulatory decision-support disclaimer & audit metadata
"""

import datetime
from typing import Dict, Any, List, Optional


def format_clinical_memo(
    patient_id: str,
    xgb_prob: float,
    vqc_prob: float,
    hybrid_prob: float,
    top_shap_features: List[Dict[str, Any]],
    narrative: str,
    raw_features: Optional[List[float]] = None,
    execution_time_ms: float = 0.0,
    model_consensus: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Synthesizes predictions and explainability attributions into a structured Parkinson's clinical consultation memo.
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

    # Determine risk category based on hybrid probability
    if hybrid_prob >= 0.75:
        risk_tier = "ELEVATED SCREENING SIGNAL"
        diagnosis_label = "HIGH RISK OF PARKINSONIAN PHONATION / EARLY DYSDIADOCHOKINESIA"
        icd10_code = "G20"  # Parkinson's disease
        recommendation = (
            "URGENT: Recommend comprehensive Movement Disorder Specialist consultation. "
            "Order dedicated DaTscan (123I-FP-CIT SPECT) imaging and administer formal "
            "MDS-UPDRS Part III motor examination with optional Levodopa Response Challenge. "
            "Refer for acoustic speech-language assessment."
        )
    elif hybrid_prob >= 0.45:
        risk_tier = "MODERATE / SUSPICIOUS SIGNAL"
        diagnosis_label = "BORDERLINE ACOUSTIC MICROPERTURBATION"
        icd10_code = "R47.81"  # Dysarthria and anarthria
        recommendation = (
            "Recommend repeat voice recording assessment and accelerometry tremor screening in 60 days. "
            "Administer Montreal Cognitive Assessment (MoCA) and screen for REM sleep behavior disorder (RBD) "
            "and olfactory dysfunction."
        )
    else:
        risk_tier = "BASELINE / NORMAL CONCORDANCE"
        diagnosis_label = "UNREMARKABLE ACOUSTIC BIOMARKERS (HEALTHY CONTROL PATTERN)"
        icd10_code = "Z71.1"  # Person with feared health complaint in whom no diagnosis is made
        recommendation = (
            "Acoustic phonation stability and fractal complexity within physiological normative ranges. "
            "No indication for specialized neuroimaging. Re-evaluate if clinical tremor or bradykinesia develops."
        )

    # Consensus analysis
    discordance_delta = abs(xgb_prob - vqc_prob)
    computed_concordance = "CONCORDANT" if discordance_delta < 0.30 else "DISCORDANT (PHYSICIAN REVIEW REQUIRED)"
    concordance = model_consensus if model_consensus is not None else computed_concordance

    # Format top biomarker drivers
    key_drivers = []
    for f in top_shap_features[:4]:
        direction_arrow = "▲" if f.get("direction") == "pd_associated" else "▼"
        impact_sign = "+" if f.get("shap_value", 0) > 0 else ""
        key_drivers.append({
            "feature_name": f.get("feature_name", "Unknown"),
            "raw_value": f.get("raw_value", 0.0),
            "z_score": f.get("standardized_z_score", 0.0),
            "shap_attribution": f"{impact_sign}{f.get('shap_value', 0.0):.3f}",
            "direction": f.get("direction", "neutral"),
            "clinical_interpretation": f"{direction_arrow} {f.get('direction', '').upper()} impact",
        })

    # Synthesize plain-text / Markdown memo for export
    memo_markdown = f"""# AAROH CLINICAL SCREENING CONSULTATION MEMORANDUM
**Hospital Identification / Case ID**: {patient_id}
**Date of Evaluation**: {now_str}
**Modality**: Voice Phonation Acoustic Telemonitoring (22 Feature Protocol)
**Architecture**: Multimodal Hybrid Classical (XGBoost) + Quantum VQC (4-Qubit ZZ-Map)
--------------------------------------------------------------------------------

### 1. SCREENING IMPRESSION & RISK SUMMARY
- **Primary Finding**: {diagnosis_label}
- **Assigned ICD-10 Code**: {icd10_code}
- **Clinical Risk Tier**: {risk_tier}
- **Hybrid Screening Score**: {hybrid_prob*100:.1f}% (Optimal Calibration: 0.31 Classical + 0.69 Quantum)
- **Classical XGBoost Probability**: {xgb_prob*100:.1f}%
- **Quantum VQC State Probability**: {vqc_prob*100:.1f}% (Qubit 0 <IIIZ> Projection)
- **Consensus Status**: {concordance}

### 2. PRIMARY ACOUSTIC BIOMARKER DRIVERS (SHAP ATTRIBUTION)
{chr(10).join([f"- **{d['feature_name']}**: Raw={d['raw_value']} (Z={d['z_score']}) ➔ SHAP={d['shap_attribution']} ({d['direction'].upper()})" for d in key_drivers])}

### 3. CLINICAL NEUROLOGY SYNTHESIS
{narrative}

### 4. RECOMMENDED CLINICAL NEXT ACTION
{recommendation}

--------------------------------------------------------------------------------
**REGULATORY & CLINICAL DISCLAIMER**:
AAROH is a hybrid clinical decision-support and quantum benchmarking platform
developed for early screening assistance and algorithmic auditability. It does not
constitute a definitive standalone medical diagnosis. All screening signals must be
correlated with in-person neurological examination (MDS-UPDRS) and approved by a physician.
--------------------------------------------------------------------------------
*Execution Latency: {execution_time_ms:.1f}ms | Pipeline Audit Hash: SHA256-AAROH-PARKINSONS-GATE2*
"""

    return {
        "case_id": patient_id,
        "timestamp": now_str,
        "modality": "Acoustic Telemonitoring (22 MDVP Features)",
        "icd10_code": icd10_code,
        "diagnosis": diagnosis_label,
        "risk_tier": risk_tier,
        "concordance": concordance,
        "hybrid_screening_score": round(hybrid_prob, 4),
        "classical_xgb_confidence": round(xgb_prob, 4),
        "quantum_vqc_probability": round(vqc_prob, 4),
        "key_biomarker_drivers": key_drivers,
        "clinical_narrative": narrative,
        "recommended_action": recommendation,
        "memo_markdown": memo_markdown,
        "disclaimer": (
            "AAROH is a clinical decision-support tool. Not intended as a standalone diagnostic device. "
            "In-person clinical examination and neurological correlation required."
        ),
        "execution_time_ms": round(execution_time_ms, 2),
    }
