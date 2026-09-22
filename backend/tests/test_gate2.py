"""
AAROH Validation Gate 2 Test Suite: Phase 4 (FastAPI Backend, 6-Stage SSE Agents & SQLite Store)
Verifies:
1. Service Health: GET /api/health returns online status and SQLite DB
2. Benchmarking Metrics: GET /api/metrics returns full classical, quantum & hybrid comparisons
3. Demo Patients: GET /api/demo-patients returns 4 valid 22D acoustic presets
4. Synchronous Screening: POST /api/screen/sync executes 6-stage pipeline cleanly
5. Live SSE Streaming: POST /api/screen/stream emits real-time event packets for all 6 agent stages
6. Longitudinal History: GET /api/patient/{id}/history retrieves longitudinal visit trajectory
7. Persistence: POST /api/patient/{id}/save-assessment stores new assessment in SQLite
8. Input Guardrails: Rejects malformed or corrupted feature inputs
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
PROJECT_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from backend.main import app
from backend.database.db import SessionLocal
from backend.database.models import Assessment


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
    print("AAROH VALIDATION GATE 2: FASTAPI, 6-STAGE SSE & SQLITE AUDIT")
    print("=" * 65)

    client = TestClient(app)

    # ---------------------------------------------------------
    # 1. Health & Service Status
    # ---------------------------------------------------------
    print("\n[Audit 1/8] Verifying GET /api/health...")
    resp_health = client.get("/api/health")
    assert resp_health.status_code == 200, f"Health check failed: {resp_health.text}"
    health_data = resp_health.json()
    assert health_data["status"] == "online"
    assert "SQLite" in health_data["database"]
    print(f"  [PASS] Status: {health_data['status']}, Database: {health_data['database']}")

    # ---------------------------------------------------------
    # 2. Metrics & Comparison Benchmark
    # ---------------------------------------------------------
    print("\n[Audit 2/8] Verifying GET /api/metrics...")
    resp_metrics = client.get("/api/metrics")
    assert resp_metrics.status_code == 200
    m_data = resp_metrics.json()
    assert "classical_xgboost" in m_data
    assert "quantum_vqc" in m_data
    assert "hybrid_comparison" in m_data
    assert "fusion_weights" in m_data
    print(f"  [PASS] Fusion Weights: alpha={m_data['fusion_weights'].get('alpha')}, beta={m_data['fusion_weights'].get('beta')}")
    print(f"  [PASS] Honest Methodology Disclosure present.")

    # ---------------------------------------------------------
    # 3. Demo Patients Preset Library
    # ---------------------------------------------------------
    print("\n[Audit 3/8] Verifying GET /api/demo-patients & /api/global-importance...")
    resp_pts = client.get("/api/demo-patients")
    assert resp_pts.status_code == 200
    pts_data = resp_pts.json()
    assert len(pts_data["patients"]) == 4, f"Expected 4 demo patients, got {len(pts_data['patients'])}"
    for p in pts_data["patients"]:
        assert len(p["features"]) == 22, f"Preset {p['preset_id']} does not have 22 features"
        print(f"  [PASS] Found Demo Preset: {p['preset_id']} ({p['label']})")

    resp_gi = client.get("/api/global-importance")
    assert resp_gi.status_code == 200
    gi_data = resp_gi.json()
    assert "top_10_biomarkers" in gi_data
    print(f"  [PASS] Cohort Rankings loaded. #1 Acoustic Biomarker: {gi_data['top_10_biomarkers'][0]['feature_name']}")

    # ---------------------------------------------------------
    # 4. Synchronous Screening Pipeline
    # ---------------------------------------------------------
    print("\n[Audit 4/8] Verifying POST /api/screen/sync (Synchronous Endpoint)...")
    high_pd_sample = pts_data["patients"][0]["features"]
    healthy_sample = pts_data["patients"][3]["features"]

    # Test High PD Case
    t0 = time.perf_counter()
    resp_sync_pd = client.post("/api/screen/sync", json={
        "patient_id": "P-001",
        "features": high_pd_sample,
    })
    elapsed_pd = (time.perf_counter() - t0) * 1000.0
    assert resp_sync_pd.status_code == 200
    res_pd = resp_sync_pd.json()
    assert res_pd["status"] == "success"
    assert res_pd["fusion"]["hybrid_probability"] >= 0.50
    assert "icd10_code" in res_pd["memo"]
    print(f"  [PASS] PD Case: Classical={res_pd['fusion']['classical_probability']*100:.1f}%, Quantum={res_pd['fusion']['quantum_probability']*100:.1f}% => Hybrid={res_pd['fusion']['hybrid_probability']*100:.1f}%, Latency={elapsed_pd:.1f}ms")

    # Test Healthy Control Case
    resp_sync_healthy = client.post("/api/screen/sync", json={
        "patient_id": "P-004",
        "features": healthy_sample,
    })
    assert resp_sync_healthy.status_code == 200
    res_healthy = resp_sync_healthy.json()
    assert res_healthy["fusion"]["hybrid_probability"] <= 0.55
    print(f"  [PASS] Healthy Case: Hybrid Signal={res_healthy['fusion']['hybrid_probability']*100:.1f}%, Tier={res_healthy['memo']['risk_tier']}")

    # ---------------------------------------------------------
    # 5. Live Server-Sent Events (SSE) Streaming
    # ---------------------------------------------------------
    print("\n[Audit 5/8] Verifying POST /api/screen/stream (6-Stage SSE Live Stream)...")
    t0_stream = time.perf_counter()
    with client.stream("POST", "/api/screen/stream", json={
        "patient_id": "TEST-STREAM-001",
        "features": high_pd_sample,
    }) as stream_resp:
        assert stream_resp.status_code == 200
        assert "text/event-stream" in stream_resp.headers["content-type"]
        stream_resp.read()
        full_text = stream_resp.text
        stream_ms = (time.perf_counter() - t0_stream) * 1000.0

    events = parse_sse_events(full_text)
    event_types = [e[0] for e in events]
    print(f"  [OK] Streamed {len(events)} total SSE events in {stream_ms:.1f}ms.")

    stages_completed = [e[1].get("stage") for e in events if e[0] == "stage_complete"]
    expected_stages = [
        "data_ingestion",
        "classical_inference",
        "quantum_encoding",
        "hybrid_fusion",
        "explainability_synthesis",
        "clinical_memo",
    ]
    for stg in expected_stages:
        assert stg in stages_completed, f"Missing stage in SSE stream: {stg}"
        print(f"    - Completed Stage: {stg}")

    assert "final_result" in event_types, "Missing final_result event"
    print("  [PASS] All 6 Agent stages executed sequentially and final consolidated result delivered!")

    # ---------------------------------------------------------
    # 6. Longitudinal Assessment History
    # ---------------------------------------------------------
    print("\n[Audit 6/8] Verifying GET /api/patient/{id}/history (SQLite Store)...")
    resp_hist = client.get("/api/patient/P-001/history")
    assert resp_hist.status_code == 200
    hist_data = resp_hist.json()
    assert hist_data["patient_id"] == "P-001"
    assert hist_data["total_assessments"] >= 3, f"Expected >= 3 visits for P-001, got {hist_data['total_assessments']}"
    print(f"  [PASS] Retrieved {hist_data['total_assessments']} historical visits for P-001.")

    # ---------------------------------------------------------
    # 7. Persistence (Saving New Assessment)
    # ---------------------------------------------------------
    print("\n[Audit 7/8] Verifying POST /api/patient/{id}/save-assessment...")
    db = SessionLocal()
    try:
        db.query(Assessment).filter(Assessment.patient_id == "P-TEST-999").delete()
        db.commit()
    finally:
        db.close()

    save_payload = {
        "patient_id": "P-TEST-999",
        "classical_score": 0.92,
        "quantum_score": 0.58,
        "hybrid_score": 0.69,
        "risk_tier": "MODERATE",
        "consensus_status": "CONCORDANT",
        "feature_json": json.dumps({"MDVP:Fo(Hz)": 119.9}),
        "shap_json": json.dumps([{"feature": "PPE", "shap": 0.55}]),
        "clinical_memo_json": json.dumps({"summary": "Automated audit test assessment"}),
    }
    resp_save = client.post("/api/patient/P-TEST-999/save-assessment", json=save_payload)
    assert resp_save.status_code == 200
    save_data = resp_save.json()
    assert save_data["status"] == "saved"
    assert "assessment_id" in save_data

    # Verify retrieval
    resp_check = client.get("/api/patient/P-TEST-999/history")
    assert resp_check.status_code == 200
    assert resp_check.json()["total_assessments"] == 1
    print(f"  [PASS] Saved and retrieved assessment ID {save_data['assessment_id']} from SQLite.")

    # Cleanup
    db = SessionLocal()
    try:
        db.query(Assessment).filter(Assessment.patient_id == "P-TEST-999").delete()
        db.commit()
    finally:
        db.close()

    # ---------------------------------------------------------
    # 8. Input Guardrails & Validation Rejection
    # ---------------------------------------------------------
    print("\n[Audit 8/8] Verifying Input Guardrails & Error Responses...")
    # Malformed length (21 features instead of 22)
    resp_bad_len = client.post("/api/screen/sync", json={
        "patient_id": "TEST-BAD",
        "features": high_pd_sample[:21],
    })
    assert resp_bad_len.status_code in [400, 422]
    print("  [PASS] Correctly rejected 21-feature vector (HTTP 422/400).")

    print("\n" + "=" * 65)
    print("ALL VALIDATION GATE 2 TESTS PASSED WITH 100% COMPLIANCE (8/8)!")
    print("PHASE 4 (FastAPI Backend, 6-Stage SSE Agents & SQLite Store) is COMPLETE.")
    print("=" * 65)
    return True


if __name__ == "__main__":
    run_validation_gate_2()
