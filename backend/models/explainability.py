"""
AAROH Explainability Engine: SHAP TreeExplainer for Classical XGBoost
- Dataset: Wisconsin Breast Cancer Diagnostic (WBCD)
- Method: Exact TreeSHAP (Lundberg & Lee, Nature Machine Intelligence 2020)
- Computes additive feature attributions for both per-patient inference and global cohort ranking.
- Additive Property: sum(phi_i) + base_value == model_output_margin
- Provides structured payload for frontend Waterfall charts and clinical consultation memos.
"""

import os
import sys
import json
import time
import numpy as np
import joblib
import xgboost as xgb
import shap
from sklearn.datasets import load_breast_cancer

# Guard for Windows threading
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(MODELS_DIR, "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

MODEL_PATH = os.path.join(MODELS_DIR, "xgboost_model.json")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, "feature_names.json")
GLOBAL_IMPORTANCE_PATH = os.path.join(MODELS_DIR, "global_feature_importance.json")


def _sigmoid(x):
    """Logistic sigmoid function to map log-odds margin to probability."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50.0, 50.0)))


class ShapExplainabilityEngine:
    """
    Cached SHAP TreeExplainer engine for rapid per-patient clinical attribution.
    """

    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"XGBoost model not found at {MODEL_PATH}. Run classical.py first.")
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Scaler not found at {SCALER_PATH}. Run classical.py first.")
        if not os.path.exists(FEATURE_NAMES_PATH):
            raise FileNotFoundError(f"Feature names not found at {FEATURE_NAMES_PATH}.")

        self.clf = xgb.XGBClassifier()
        self.clf.load_model(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

        with open(FEATURE_NAMES_PATH, "r") as f:
            self.feature_names = json.load(f)

        self.explainer = shap.TreeExplainer(self.clf)
        ev = self.explainer.expected_value
        self.base_value = float(np.array(ev).ravel()[0])
        self.base_probability = float(_sigmoid(self.base_value))

    def explain_patient(self, raw_features_30, top_k=10):
        """
        Computes exact SHAP attributions for a 30-feature patient biopsy vector.
        Returns:
          - base_value & base_probability
          - output_margin & output_probability
          - top_features: list formatted for interactive Waterfall chart
          - top_malignant_drivers: features increasing cancer risk
          - top_benign_drivers: features decreasing cancer risk
          - clinical_narrative: auto-synthesized explanation for physician memo
        """
        t0 = time.perf_counter()
        x_raw = np.array(raw_features_30, dtype=float).reshape(1, -1)
        x_scaled = self.scaler.transform(x_raw)

        # Compute SHAP values using modern Explanation API
        exp_obj = self.explainer(x_scaled)
        shap_vals = exp_obj.values[0]
        base_val = float(exp_obj.base_values[0])
        base_prob = float(_sigmoid(base_val))

        output_margin = float(self.clf.predict(x_scaled, output_margin=True)[0])
        prob_malignant = float(self.clf.predict_proba(x_scaled)[0, 1])

        # Verify additive property: sum(shap) + base_value == output_margin
        reconstructed_margin = float(np.sum(shap_vals) + base_val)
        margin_delta = abs(reconstructed_margin - output_margin)

        # Build feature attribution records
        all_features = []
        for i, name in enumerate(self.feature_names):
            phi = float(shap_vals[i])
            val = float(x_raw[0, i])
            scaled_val = float(x_scaled[0, i])
            all_features.append({
                "feature_index": i,
                "feature_name": name,
                "raw_value": round(val, 4),
                "standardized_z_score": round(scaled_val, 3),
                "shap_value": round(phi, 4),
                "abs_shap": abs(phi),
                "direction": "malignant" if phi > 0 else "benign",
            })

        # Sort by absolute SHAP magnitude
        sorted_features = sorted(all_features, key=lambda f: f["abs_shap"], reverse=True)
        top_features = sorted_features[:top_k]

        # Calculate cumulative waterfall sequence
        running_margin = base_val
        waterfall_steps = [{
            "step": "Baseline Prior",
            "delta": 0.0,
            "cumulative_margin": round(base_val, 4),
            "cumulative_probability": round(base_prob, 4),
        }]
        for feat in top_features:
            running_margin += feat["shap_value"]
            waterfall_steps.append({
                "feature_name": feat["feature_name"],
                "delta": feat["shap_value"],
                "direction": feat["direction"],
                "cumulative_margin": round(running_margin, 4),
                "cumulative_probability": round(float(_sigmoid(running_margin)), 4),
            })

        # Drivers
        malignant_drivers = [f for f in sorted_features if f["shap_value"] > 0][:5]
        benign_drivers = [f for f in sorted_features if f["shap_value"] < 0][:5]

        # Generate narrative for physician consultation memo
        if prob_malignant >= 0.5:
            top_names = [f["feature_name"] for f in malignant_drivers[:2]]
            narrative = (
                f"Prediction of Malignancy ({prob_malignant*100:.1f}%) is predominantly driven by "
                f"elevated nuclear morphometry in '{top_names[0]}' (+{malignant_drivers[0]['shap_value']:.2f}) "
                f"and '{top_names[1]}' (+{malignant_drivers[1]['shap_value']:.2f}), "
                f"indicating significant structural atypia characteristic of carcinoma."
            )
        else:
            top_names = [f["feature_name"] for f in benign_drivers[:2]]
            narrative = (
                f"Prediction of Benign Pathology ({(1.0 - prob_malignant)*100:.1f}% confidence) is supported by "
                f"favorable nuclear metrics in '{top_names[0]}' ({benign_drivers[0]['shap_value']:.2f}) "
                f"and '{top_names[1]}' ({benign_drivers[1]['shap_value']:.2f}), "
                f"demonstrating regular cell perimeter and uniform chromatin architecture."
            )

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "prediction": 1 if prob_malignant >= 0.5 else 0,
            "probability_malignant": round(prob_malignant, 4),
            "base_value": round(base_val, 4),
            "base_probability": round(base_prob, 4),
            "output_margin": round(output_margin, 4),
            "margin_additive_delta": round(margin_delta, 8),
            "top_features": top_features,
            "waterfall_steps": waterfall_steps,
            "top_malignant_drivers": malignant_drivers,
            "top_benign_drivers": benign_drivers,
            "clinical_narrative": narrative,
            "execution_time_ms": round(elapsed_ms, 2),
        }


def compute_and_save_global_importance():
    """
    Computes global cohort-level SHAP rankings across all 569 samples in WBCD.
    Saves to global_feature_importance.json.
    """
    print("=" * 65)
    print("AAROH EXPLAINABILITY ENGINE: GLOBAL SHAP COHORT BENCHMARK")
    print("=" * 65)

    engine = ShapExplainabilityEngine()
    raw = load_breast_cancer()
    X_scaled = engine.scaler.transform(raw.data)

    print(f"Computing exact TreeSHAP values for all {len(raw.data)} WBCD samples...")
    t0 = time.time()
    all_shap = engine.explainer.shap_values(X_scaled)
    duration = time.time() - t0
    print(f"SHAP matrix calculated in {duration:.2f}s!")

    mean_abs_shap = np.mean(np.abs(all_shap), axis=0)
    sorted_indices = np.argsort(mean_abs_shap)[::-1]

    global_rankings = []
    for rank, idx in enumerate(sorted_indices, 1):
        global_rankings.append({
            "rank": rank,
            "feature_name": engine.feature_names[idx],
            "mean_abs_shap": round(float(mean_abs_shap[idx]), 4),
            "feature_index": int(idx),
        })

    payload = {
        "cohort_size": len(raw.data),
        "total_features": len(engine.feature_names),
        "method": "Mean Absolute TreeSHAP Attribution (cohort-wide)",
        "base_value": round(engine.base_value, 4),
        "top_10_biomarkers": global_rankings[:10],
        "all_rankings": global_rankings,
    }

    with open(GLOBAL_IMPORTANCE_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"[OK] Saved global feature importance to {GLOBAL_IMPORTANCE_PATH}")
    print("\nTop 5 Clinical Biomarkers:")
    for b in global_rankings[:5]:
        print(f"  #{b['rank']} {b['feature_name']:<25} | Mean |SHAP|: {b['mean_abs_shap']:.4f}")
    print("=" * 65)
    return payload


# Singleton instance for fast reuse
_cached_engine = None


def get_explainability_engine():
    global _cached_engine
    if _cached_engine is None:
        _cached_engine = ShapExplainabilityEngine()
    return _cached_engine


def explain_patient(raw_features_30, top_k=10):
    engine = get_explainability_engine()
    return engine.explain_patient(raw_features_30, top_k=top_k)


if __name__ == "__main__":
    compute_and_save_global_importance()
    # Self-test on reference samples
    raw_data = load_breast_cancer()
    sample_mal = raw_data.data[raw_data.target == 0][0]
    sample_ben = raw_data.data[raw_data.target == 1][0]

    print("\n[Self-Test: Malignant Reference Patient]")
    res_m = explain_patient(sample_mal)
    print(f"  Probability: {res_m['probability_malignant']*100:.1f}% (Margin: {res_m['output_margin']})")
    print(f"  Narrative: {res_m['clinical_narrative']}")
    print(f"  Top 3 Drivers:")
    for f in res_m["top_features"][:3]:
        print(f"    - {f['feature_name']}: {f['shap_value']:+.4f} (Raw: {f['raw_value']})")

    print("\n[Self-Test: Benign Reference Patient]")
    res_b = explain_patient(sample_ben)
    print(f"  Probability: {res_b['probability_malignant']*100:.1f}% (Margin: {res_b['output_margin']})")
    print(f"  Narrative: {res_b['clinical_narrative']}")
    print(f"  Top 3 Drivers:")
    for f in res_b["top_features"][:3]:
        print(f"    - {f['feature_name']}: {f['shap_value']:+.4f} (Raw: {f['raw_value']})")
