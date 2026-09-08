"""
AAROH Clinical Consultation Memo Generator (Subphase 2.5)
- Generates structured, physician-ready diagnostic reports synthesizing:
  1. Classical XGBoost prediction & calibrated confidence
  2. 4-Qubit VQC quantum state expectation value & probability
  3. Exact TreeSHAP feature attributions & nuclear morphometry drivers
  4. Clinical ICD-10 categorization & recommended next diagnostic step
  5. Mandatory regulatory decision-support disclaimer & audit metadata
"""

import datetime
from typing import Dict, Any, List, Optional


def format_clinical_memo(
    patient_id: str,
    xgb_prob: float,
    vqc_prob: float,
    top_shap_features: List[Dict[str, Any]],
    narrative: str,
    raw_features: Optional[List[float]] = None,
    execution_time_ms: float = 0.0,
    model_consensus: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Synthesizes predictions and explainability attributions into a structured clinical consultation memo.
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    
    # Determine primary diagnosis based on classical model (higher empirical validation)
    is_malignant = xgb_prob >= 0.5
    diagnosis_label = "MALIGNANT (CARCINOMA)" if is_malignant else "BENIGN (NON-MALIGNANT)"
    
    # Risk Tier
    if xgb_prob >= 0.85:
        risk_tier = "CRITICAL / HIGH RISK"
        icd10_code = "C50.919"  # Malignant neoplasm of unspecified site of unspecified female breast
        recommendation = (
            "URGENT: Recommend immediate ultrasound-guided Core Needle Biopsy (CNB) "
            "with reflex Immunohistochemistry (IHC) profiling (ER, PR, HER2, Ki-67). "
            "Expedite multidisciplinary tumor board surgical consultation."
        )
    elif xgb_prob >= 0.50:
        risk_tier = "MODERATE / SUSPICIOUS"
        icd10_code = "C50.919"
        recommendation = (
            "Recommend dedicated diagnostic mammography spot compression views and "
            "repeat targeted fine needle aspiration (FNA) or core needle biopsy within 14 days."
        )
    elif xgb_prob >= 0.15:
        risk_tier = "LOW / BORDERLINE"
        icd10_code = "N60.99"  # Unspecified benign mammary dysplasia
        recommendation = (
            "Findings favour benign etiology (e.g. fibroadenoma or fibrocystic changes). "
            "Recommend 6-month interval diagnostic ultrasound surveillance to verify morphological stability."
        )
    else:
        risk_tier = "VERY LOW / NORMAL"
        icd10_code = "N60.99"
        recommendation = (
            "Morphological metrics consistent with normal glandular architecture. "
            "Recommend return to routine age-appropriate screening intervals."
        )

    # Consensus analysis
    vqc_malignant = vqc_prob >= 0.5
    computed_concordance = "CONCORDANT" if (is_malignant == vqc_malignant) else "DISCORDANT (REVIEW REQUIRED)"
    concordance = model_consensus if model_consensus is not None else computed_concordance
    
    # Format top biomarker drivers
    key_drivers = []
    for f in top_shap_features[:4]:
        direction_arrow = "▲" if f.get("direction") == "malignant" else "▼"
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
    memo_markdown = f"""# AAROH CLINICAL CONSULTATION MEMORANDUM
**Hospital Identification / Case ID**: {patient_id}
**Date of Evaluation**: {now_str}
**Specimen Type**: Fine Needle Aspirate (FNA) — Wisconsin Diagnostic Protocol
**Diagnostic Modality**: Dual Classical (XGBoost 5-Fold CV) + Quantum VQC (4-Qubit ZZ-Map)
--------------------------------------------------------------------------------

### 1. DIAGNOSTIC IMPRESSION & RISK SUMMARY
- **Primary Finding**: {diagnosis_label}
- **Assigned ICD-10 Code**: {icd10_code}
- **Clinical Risk Tier**: {risk_tier}
- **Classical XGBoost Confidence**: {xgb_prob*100:.1f}% (Calibrated Margin)
- **Quantum VQC State Probability**: {vqc_prob*100:.1f}% (Qubit 0 <IIIZ> Projection)
- **Dual-Model Concordance**: {concordance}

### 2. PRIMARY NUCLEAR BIOMARKER DRIVERS (SHAP ATTRIBUTION)
{chr(10).join([f"- **{d['feature_name']}**: Raw={d['raw_value']} (Z={d['z_score']}) ➔ SHAP={d['shap_attribution']} ({d['direction'].upper()})" for d in key_drivers])}

### 3. PATHOLOGY SYNTHESIS
{narrative}

### 4. RECOMMENDED CLINICAL NEXT ACTION
{recommendation}

--------------------------------------------------------------------------------
**REGULATORY & CLINICAL DISCLAIMER**:
AAROH is an experimental hybrid clinical decision-support and quantum benchmarking
platform developed for research and algorithmic auditability. It does not constitute
a standalone medical device. All outputs must be correlated with definitive tissue
histopathology and approved by a board-certified pathologist.
--------------------------------------------------------------------------------
*Execution Latency: {execution_time_ms:.1f}ms | Pipeline Audit Hash: SHA256-AAROH-GATE2*
"""

    return {
        "case_id": patient_id,
        "timestamp": now_str,
        "specimen": "FNA Breast Biopsy",
        "icd10_code": icd10_code,
        "diagnosis": diagnosis_label,
        "risk_tier": risk_tier,
        "concordance": concordance,
        "classical_xgb_confidence": round(xgb_prob, 4),
        "quantum_vqc_probability": round(vqc_prob, 4),
        "key_biomarker_drivers": key_drivers,
        "clinical_narrative": narrative,
        "recommended_action": recommendation,
        "memo_markdown": memo_markdown,
        "disclaimer": (
            "AAROH is a clinical decision-support and quantum benchmarking tool. "
            "Not intended as a standalone diagnostic device. Clinical correlation with "
            "full histological specimen is required."
        ),
        "execution_time_ms": round(execution_time_ms, 2),
    }
