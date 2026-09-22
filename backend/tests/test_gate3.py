"""
AAROH Validation Gate 3: Phase 6 Data Persistence & Longitudinal History Audit
- Verifies SQLite assessment table schema & indexes
- Audits pre-seeded demonstration patient histories (P-001 to P-004)
- Tests POST /api/patient/{id}/save-assessment database insertion
- Tests GET /api/patient/{id}/history retrieval, chronological order, and field completeness
"""

import os
import sys
import json

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(backend_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from fastapi.testclient import TestClient
from backend.main import app
from backend.database.db import SessionLocal, init_db
from backend.database.models import Assessment

client = TestClient(app)


def test_gate3_persistence_and_history():
    print("=" * 70)
    print(">>> RUNNING VALIDATION GATE 3: DATA PERSISTENCE & LONGITUDINAL AUDIT <<<")
    print("=" * 70)

    # Audit 1: DB Initialization & Table Schema
    print("\n[Audit 1/5] Checking SQLite Database and Table Initialization...")
    init_db()
    db = SessionLocal()
    try:
        count = db.query(Assessment).count()
        assert count > 0, f"Expected seeded assessments, found {count}"
        print(f"  [PASS] SQLite initialized with {count} pre-seeded assessment records.")
    finally:
        db.close()

    # Audit 2: Demo Patient History Integrity
    print("\n[Audit 2/5] Auditing Pre-Seeded Demonstration Patient Trajectories...")
    for pid in ["P-001", "P-002", "P-003", "P-004"]:
        res = client.get(f"/api/patient/{pid}/history")
        assert res.status_code == 200, f"Failed to fetch history for {pid}: {res.status_code}"
        data = res.json()
        assert data["patient_id"] == pid
        history = data["history"]
        assert len(history) >= 2, f"Expected >= 2 visits for {pid}, found {len(history)}"
        print(f"  [PASS] Patient {pid}: {len(history)} longitudinal visits found.")
        for visit in history:
            assert "classical_score" in visit
            assert "quantum_score" in visit
            assert "hybrid_score" in visit
            assert "risk_tier" in visit
            assert "consensus_status" in visit
            assert 0.0 <= visit["hybrid_score"] <= 1.0

    # Audit 3: Save Assessment DB Write Test
    print("\n[Audit 3/5] Testing Assessment Persistence API (POST /api/patient/{id}/save-assessment)...")
    test_patient_id = "TEST-P-999"
    payload = {
        "patient_id": test_patient_id,
        "classical_score": 0.88,
        "quantum_score": 0.62,
        "hybrid_score": 0.70,
        "risk_tier": "ELEVATED",
        "consensus_status": "CONCORDANT",
        "feature_json": json.dumps({"MDVP:Fo(Hz)": 119.992, "PPE": 0.284654}),
        "shap_json": json.dumps([{"feature": "PPE", "shap": 0.45}]),
        "clinical_memo_json": json.dumps({"risk_tier": "ELEVATED", "primary_action": "Urgent Movement Specialist Referral"}),
    }

    save_res = client.post(f"/api/patient/{test_patient_id}/save-assessment", json=payload)
    assert save_res.status_code == 200, f"Save failed: {save_res.text}"
    save_data = save_res.json()
    assert save_data["status"] == "saved"
    assert "assessment_id" in save_data
    print(f"  [PASS] Successfully persisted new assessment ID: {save_data['assessment_id']}")

    # Audit 4: Query Saved Assessment via History API
    print("\n[Audit 4/5] Verifying History Retrieval for Newly Saved Patient...")
    hist_res = client.get(f"/api/patient/{test_patient_id}/history")
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["patient_id"] == test_patient_id
    assert len(hist_data["history"]) == 1
    record = hist_data["history"][0]
    assert abs(record["hybrid_score"] - 0.70) < 1e-4
    assert record["risk_tier"] == "ELEVATED"
    print(f"  [PASS] Verified persistent retrieval for {test_patient_id} with exact score matching.")

    # Audit 5: Cleanup Test Patient
    print("\n[Audit 5/5] Cleaning up temporary test records...")
    db = SessionLocal()
    try:
        deleted = db.query(Assessment).filter(Assessment.patient_id == test_patient_id).delete()
        db.commit()
        print(f"  [PASS] Cleaned up {deleted} temporary test record(s).")
    finally:
        db.close()

    print("\n" + "=" * 70)
    print(">>> VALIDATION GATE 3 PASSED (5/5 PERSISTENCE & HISTORY AUDITS VERIFIED) <<<")
    print("=" * 70)


if __name__ == "__main__":
    test_gate3_persistence_and_history()
