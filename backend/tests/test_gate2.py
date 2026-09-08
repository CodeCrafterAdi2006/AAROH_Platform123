"""
AAROH Validation Gate 2 Test Suite
Verifies Phase 2 (FastAPI Orchestrator, SSE Streaming & Clinical Synthesis):
1. Service Health: GET /api/health returns online status
2. Benchmarking Metrics: GET /api/metrics returns 5-Fold CV vs 80/20 VQC comparison
3. Reference Patients: GET /api/reference-patients returns 3 valid 30D cases
4. Global Feature Importance: GET /api/global-importance returns top biomarkers
5. Synchronous Diagnostic: POST /api/predict executes 4-stage pipeline cleanly
6. Live SSE Streaming: POST /api/predict/stream emits real-time event packets
7. Input Validation & Error Guardrails: Rejects malformed or corrupted inputs
"""

import os
# Guard against OpenBLAS thread allocation exhaustion on Windows
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys
import json
import time

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from fastapi.testclient import TestClient
from backend.main import app


def parse_sse_events(raw_text: str):
    """Parses raw text/event-stream into a list of (event_type, json_data) tuples."""
    events = []
    current_event = "message"
    current_data = []

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            if current_data:
                data_str = "\n".join(current_data)
                try:
                    events.append((current_event, json.loads(data_str)))
                except json.JSONDecodeError:
                    events.append((current_event, data_str))
                current_data = []
                current_event = "message"
            continue

        if line.startswith("event:"):
            current_event = line[len("event:"):].strip()
        elif line.startswith("data:"):
            current_data.append(line[len("data:"):].strip())

    if current_data:
        data_str = "\n".join(current_data)
        try:
            events.append((current_event, json.loads(data_str)))
        except json.JSONDecodeError:
            events.append((current_event, data_str))

    return events


def run_validation_gate_2():
    print("=" * 65)
    print("AAROH VALIDATION GATE 2: FASTAPI & AGENTIC SSE STREAMING AUDIT")
    print("=" * 65)

    client = TestClient(app)

    # ---------------------------------------------------------
    # 1. Health & Service Status
    # ---------------------------------------------------------
    print("\n[Audit 1/6] Verifying GET /api/health...")
    resp_health = client.get("/api/health")
    assert resp_health.status_code == 200, f"Health check failed: {resp_health.text}"
    health_data = resp_health.json()
    assert health_data["status"] == "online"
    print(f"  [PASS] Status: {health_data['status']}, Quantum: {health_data['quantum_framework']}")

    # ---------------------------------------------------------
    # 2. Metrics & Methodology Disclaimer
    # ---------------------------------------------------------
    print("\n[Audit 2/6] Verifying GET /api/metrics...")
    resp_metrics = client.get("/api/metrics")
    assert resp_metrics.status_code == 200
    m_data = resp_metrics.json()
    assert "classical_xgboost" in m_data
    assert "quantum_vqc" in m_data
    assert "honest_comparison" in m_data
    cv_auc = m_data["honest_comparison"]["classical_cv_roc_auc"]
    vqc_auc = m_data["honest_comparison"]["quantum_test_roc_auc"]
    print(f"  [PASS] XGBoost 5-Fold CV AUC: {cv_auc:.3f} | VQC Single-Split AUC: {vqc_auc:.3f}")
    print(f"  [PASS] Honest Methodology Disclaimer present.")

    # ---------------------------------------------------------
    # 3. Reference Patients Preset Library
    # ---------------------------------------------------------
    print("\n[Audit 3/6] Verifying GET /api/reference-patients & /api/global-importance...")
    resp_pts = client.get("/api/reference-patients")
    assert resp_pts.status_code == 200
    pts_data = resp_pts.json()
    assert len(pts_data["patients"]) == 3
    for p in pts_data["patients"]:
        assert len(p["features"]) == 30, f"Preset {p['preset_id']} does not have 30 features"
        print(f"  [PASS] Found Preset: {p['preset_id']} ({p['label']})")

    # Verify caching: subsequent calls return identical data instantly
    resp_pts2 = client.get("/api/reference-patients")
    assert resp_pts2.status_code == 200
    assert resp_pts2.json() == pts_data
    print("  [PASS] Cached reference patients verified for consistency.")

    resp_gi = client.get("/api/global-importance")
    assert resp_gi.status_code == 200
    gi_data = resp_gi.json()
    assert "top_10_biomarkers" in gi_data
    print(f"  [PASS] Cohort Rankings loaded. #1 Biomarker: {gi_data['top_10_biomarkers'][0]['feature_name']}")

    # ---------------------------------------------------------
    # 4. Synchronous Diagnostic Pipeline
    # ---------------------------------------------------------
    print("\n[Audit 4/6] Verifying POST /api/predict (Synchronous Endpoint)...")
    mal_sample = pts_data["patients"][0]["features"]
    ben_sample = pts_data["patients"][1]["features"]

    # Test Malignant Case
    t0 = time.perf_counter()
    resp_pred_mal = client.post("/api/predict", json={
        "patient_id": "TEST-MAL-001",
        "features": mal_sample,
    })
    elapsed_sync_mal = (time.perf_counter() - t0) * 1000.0
    assert resp_pred_mal.status_code == 200
    res_m = resp_pred_mal.json()
    assert res_m["classical"]["probability_malignant"] >= 0.85
    assert res_m["memo"]["icd10_code"] == "C50.919"
    assert "CRITICAL" in res_m["memo"]["risk_tier"]
    print(f"  [PASS] Malignant: XGB Prob={res_m['classical']['probability_malignant']*100:.1f}%, VQC Prob={res_m['quantum']['vqc_probability']*100:.1f}%, Latency={elapsed_sync_mal:.1f}ms")

    # Test Benign Case
    resp_pred_ben = client.post("/api/predict", json={
        "patient_id": "TEST-BEN-001",
        "features": ben_sample,
    })
    assert resp_pred_ben.status_code == 200
    res_b = resp_pred_ben.json()
    assert res_b["classical"]["probability_malignant"] <= 0.15
    assert res_b["memo"]["icd10_code"] == "N60.99"
    print(f"  [PASS] Benign:    XGB Prob={res_b['classical']['probability_malignant']*100:.1f}%, VQC Prob={res_b['quantum']['vqc_probability']*100:.1f}%")

    # Verify memo generator consensus parameter
    from backend.reports.memo_gen import format_clinical_memo
    test_memo = format_clinical_memo(
        patient_id="TEST-OVERRIDE",
        xgb_prob=0.9,
        vqc_prob=0.9,
        top_shap_features=[],
        narrative="Test narrative",
        model_consensus="CUSTOM_OVERRIDE_CONSENSUS",
    )
    assert test_memo["concordance"] == "CUSTOM_OVERRIDE_CONSENSUS"
    print("  [PASS] format_clinical_memo respects explicit model_consensus.")

    # ---------------------------------------------------------
    # 5. Live Server-Sent Events (SSE) Streaming
    # ---------------------------------------------------------
    print("\n[Audit 5/6] Verifying POST /api/predict/stream (SSE Live Stream)...")
    t0_stream = time.perf_counter()
    with client.stream("POST", "/api/predict/stream", json={
        "patient_id": "TEST-STREAM-001",
        "features": mal_sample,
    }) as stream_resp:
        assert stream_resp.status_code == 200
        assert "text/event-stream" in stream_resp.headers["content-type"]
        
        stream_resp.read()
        full_text = stream_resp.text
        stream_ms = (time.perf_counter() - t0_stream) * 1000.0

    events = parse_sse_events(full_text)
    event_types = [e[0] for e in events]
    print(f"  [OK] Streamed {len(events)} total SSE events in {stream_ms:.1f}ms.")
    print(f"  [OK] Event sequence: {' -> '.join(event_types)}")

    # Verify stage progression
    stages_completed = [e[1].get("stage") for e in events if e[0] == "stage_complete"]
    assert "data_ingestion" in stages_completed
    assert "quantum_encoding" in stages_completed
    assert "classical_explainability" in stages_completed
    assert "clinical_synthesis" in stages_completed
    assert "final_result" in event_types
    print("  [PASS] All 4 Agent stages completed and final diagnostic bundle received!")

    # ---------------------------------------------------------
    # 6. Input Guardrails & Rejection Handling
    # ---------------------------------------------------------
    print("\n[Audit 6/6] Verifying Input Guardrails & Error Responses...")
    # Malformed length (29 features instead of 30)
    resp_bad_len = client.post("/api/predict", json={
        "patient_id": "TEST-BAD",
        "features": mal_sample[:29],
    })
    assert resp_bad_len.status_code in [400, 422]
    print("  [PASS] Correctly rejected 29-feature vector (HTTP 422/400).")

    # Negative invalid morphometry
    bad_features = mal_sample.copy()
    bad_features[0] = -99.9
    resp_bad_val = client.post("/api/predict", json={
        "patient_id": "TEST-BAD-VAL",
        "features": bad_features,
    })
    assert resp_bad_val.status_code in [400, 422]
    print("  [PASS] Correctly rejected negative morphological feature (HTTP 400).")

    print("\n" + "=" * 65)
    print("ALL VALIDATION GATE 2 TESTS PASSED WITH 100% COMPLIANCE!")
    print("Phase 2 (FastAPI Backend, Deterministic Agents & SSE) is COMPLETE.")
    print("=" * 65)
    return True


if __name__ == "__main__":
    run_validation_gate_2()
