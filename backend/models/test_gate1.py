"""
AAROH Validation Gate 1 Test Suite
Verifies:
1. Classical XGBoost inference & probability sanity ([0.0, 1.0])
2. Quantum VQC (Qiskit + NumPy fallback) inference & probability sanity ([0.0, 1.0])
3. SHAP TreeExplainer additive property: sum(shap) + base_value == output_margin
4. All artifacts exist and are non-empty
"""

import os
import sys
import json
import numpy as np
from sklearn.datasets import load_breast_cancer

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(MODELS_DIR, "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from backend.models.quantum import predict_single_patient as predict_qiskit
from backend.models.fallback_sim import predict_single_patient_numpy, predict_quantum_with_resilient_fallback
from backend.models.explainability import explain_patient

def run_validation_gate_1():
    print("=" * 65)
    print("AAROH VALIDATION GATE 1: ML & QUANTUM FOUNDATION AUDIT")
    print("=" * 65)

    # 1. Check Artifacts
    required_artifacts = [
        "xgboost_model.json",
        "scaler.joblib",
        "classical_metrics.json",
        "feature_names.json",
        "vqc_params_pretrained.npy",
        "quantum_metrics.json",
        "pca.joblib",
        "quantum_scaler.joblib",
        "global_feature_importance.json",
    ]
    print("\n[Audit 1/4] Checking required artifacts...")
    for artifact in required_artifacts:
        path = os.path.join(MODELS_DIR, artifact)
        assert os.path.exists(path), f"Missing artifact: {artifact}"
        assert os.path.getsize(path) > 0, f"Empty artifact: {artifact}"
        print(f"  [OK] Found {artifact:<30} ({os.path.getsize(path):>7} bytes)")

    # 2. Test Samples
    raw = load_breast_cancer()
    sample_mal = raw.data[raw.target == 0][0]
    sample_ben = raw.data[raw.target == 1][0]

    # 3. Test Classical + SHAP
    print("\n[Audit 2/4] Verifying Classical XGBoost & SHAP Additive Invariant...")
    for label, sample in [("Malignant", sample_mal), ("Benign", sample_ben)]:
        exp = explain_patient(sample)
        prob = exp["probability_malignant"]
        assert 0.0 <= prob <= 1.0, f"Probability out of bounds: {prob}"
        delta = exp["margin_additive_delta"]
        assert delta < 1e-4, f"SHAP additive property failed for {label}: delta={delta}"
        print(f"  [PASS] {label:<9} -> Prob: {prob*100:.2f}%, Margin: {exp['output_margin']:+.4f}, SHAP Delta: {delta:.2e}")

    # 4. Test Quantum Primary (Qiskit)
    print("\n[Audit 3/4] Verifying Quantum VQC (Qiskit Primary Engine)...")
    res_q_mal = predict_qiskit(sample_mal)
    res_q_ben = predict_qiskit(sample_ben)
    for label, res in [("Malignant", res_q_mal), ("Benign", res_q_ben)]:
        prob = res["vqc_probability"]
        assert 0.0 <= prob <= 1.0, f"VQC probability out of bounds: {prob}"
        print(f"  [PASS] {label:<9} -> VQC Prob: {prob*100:.2f}%, Ev: {res['expectation_value']:+.4f}, Latency: {res['execution_time_ms']:.2f}ms")

    # 5. Test NumPy Fallback & Cross-Match
    print("\n[Audit 4/4] Verifying NumPy Fallback Engine & Routing...")
    res_np_mal = predict_single_patient_numpy(sample_mal)
    res_np_ben = predict_single_patient_numpy(sample_ben)
    assert abs(res_np_mal["expectation_value"] - res_q_mal["expectation_value"]) < 1e-4
    assert abs(res_np_ben["expectation_value"] - res_q_ben["expectation_value"]) < 1e-4
    print("  [PASS] NumPy expectation values match Qiskit Aer exactly (delta < 1e-4)!")

    # Test transparent routing
    routed = predict_quantum_with_resilient_fallback(sample_mal, force_fallback=False)
    assert routed["routing"] == "Primary Qiskit Engine"
    routed_fb = predict_quantum_with_resilient_fallback(sample_mal, force_fallback=True)
    assert routed_fb["routing"] == "Forced NumPy Fallback"
    print("  [PASS] Resilient routing switches seamlessly between Qiskit and NumPy fallback!")

    print("\n" + "=" * 65)
    print("ALL VALIDATION GATE 1 TESTS PASSED CLEANLY!")
    print("Phase 1 (Machine Learning & Quantum Foundation) is 100% COMPLETE.")
    print("=" * 65)
    return True

if __name__ == "__main__":
    run_validation_gate_1()
