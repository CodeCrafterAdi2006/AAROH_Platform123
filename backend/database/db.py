"""
AAROH Database Connection & Session Management
- SQLite persistent storage for longitudinal patient screening assessments.
- Seeds initial longitudinal visit trajectories for demo patients.
"""

import os
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, Assessment

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "aaroh_patients.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_demo_history_if_needed():
    """Seeds historical assessment visits for demo patients (P-001 through P-004)."""
    db = SessionLocal()
    try:
        count = db.query(Assessment).count()
        if count > 0:
            return

        now = datetime.utcnow()
        demo_records = [
            # P-001: Progressive Elevated PD Trajectory (3 visits over 6 months)
            Assessment(
                patient_id="P-001",
                assessed_at=now - timedelta(days=180),
                classical_score=0.74,
                quantum_score=0.55,
                hybrid_score=0.61,
                risk_tier="MODERATE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0052, "HNR": 21.4}),
                shap_json=json.dumps([{"feature": "PPE", "shap": 0.42}]),
                clinical_memo_json=json.dumps({"summary": "Initial baseline visit. Mild acoustic perturbation."}),
            ),
            Assessment(
                patient_id="P-001",
                assessed_at=now - timedelta(days=90),
                classical_score=0.86,
                quantum_score=0.61,
                hybrid_score=0.69,
                risk_tier="MODERATE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0071, "HNR": 18.2}),
                shap_json=json.dumps([{"feature": "PPE", "shap": 0.58}]),
                clinical_memo_json=json.dumps({"summary": "Follow-up visit 2. Increased shimmer and vocal tremor."}),
            ),
            Assessment(
                patient_id="P-001",
                assessed_at=now - timedelta(days=10),
                classical_score=0.99,
                quantum_score=0.56,
                hybrid_score=0.70,
                risk_tier="ELEVATED",
                consensus_status="DISCORDANT_REVIEW",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0089, "HNR": 16.8}),
                shap_json=json.dumps([{"feature": "PPE", "shap": 0.72}]),
                clinical_memo_json=json.dumps({"summary": "Recent visit. Significant dysphonia and high risk signal."}),
            ),

            # P-002: Moderate / Borderline Stable Case
            Assessment(
                patient_id="P-002",
                assessed_at=now - timedelta(days=120),
                classical_score=0.58,
                quantum_score=0.52,
                hybrid_score=0.54,
                risk_tier="MODERATE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0045, "HNR": 22.0}),
                shap_json=json.dumps([{"feature": "spread2", "shap": 0.31}]),
                clinical_memo_json=json.dumps({"summary": "Moderate baseline."}),
            ),
            Assessment(
                patient_id="P-002",
                assessed_at=now - timedelta(days=30),
                classical_score=0.62,
                quantum_score=0.54,
                hybrid_score=0.56,
                risk_tier="MODERATE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0048, "HNR": 21.5}),
                shap_json=json.dumps([{"feature": "spread2", "shap": 0.35}]),
                clinical_memo_json=json.dumps({"summary": "Stable moderate pattern."}),
            ),

            # P-003: Post-Therapy Improvement (Levodopa Response)
            Assessment(
                patient_id="P-003",
                assessed_at=now - timedelta(days=150),
                classical_score=0.88,
                quantum_score=0.64,
                hybrid_score=0.71,
                risk_tier="ELEVATED",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0082, "HNR": 17.1}),
                shap_json=json.dumps([{"feature": "PPE", "shap": 0.65}]),
                clinical_memo_json=json.dumps({"summary": "Pre-treatment baseline."}),
            ),
            Assessment(
                patient_id="P-003",
                assessed_at=now - timedelta(days=75),
                classical_score=0.68,
                quantum_score=0.58,
                hybrid_score=0.61,
                risk_tier="MODERATE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0055, "HNR": 20.4}),
                shap_json=json.dumps([{"feature": "PPE", "shap": 0.41}]),
                clinical_memo_json=json.dumps({"summary": "Mid-therapy check. Phonation improving."}),
            ),
            Assessment(
                patient_id="P-003",
                assessed_at=now - timedelta(days=5),
                classical_score=0.45,
                quantum_score=0.51,
                hybrid_score=0.49,
                risk_tier="BASELINE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0038, "HNR": 24.2}),
                shap_json=json.dumps([{"feature": "HNR", "shap": -0.38}]),
                clinical_memo_json=json.dumps({"summary": "Positive response to therapy."}),
            ),

            # P-004: Healthy Control Baseline
            Assessment(
                patient_id="P-004",
                assessed_at=now - timedelta(days=100),
                classical_score=0.04,
                quantum_score=0.48,
                hybrid_score=0.34,
                risk_tier="BASELINE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0021, "HNR": 28.5}),
                shap_json=json.dumps([{"feature": "HNR", "shap": -0.52}]),
                clinical_memo_json=json.dumps({"summary": "Normal acoustic phonation."}),
            ),
            Assessment(
                patient_id="P-004",
                assessed_at=now - timedelta(days=15),
                classical_score=0.05,
                quantum_score=0.50,
                hybrid_score=0.36,
                risk_tier="BASELINE",
                consensus_status="CONCORDANT",
                feature_json=json.dumps({"MDVP:Jitter(%)": 0.0023, "HNR": 27.9}),
                shap_json=json.dumps([{"feature": "HNR", "shap": -0.49}]),
                clinical_memo_json=json.dumps({"summary": "Healthy control stable."}),
            ),
        ]

        db.add_all(demo_records)
        db.commit()
    finally:
        db.close()


def init_db():
    """Initializes the database and seeds demonstration patient histories if empty."""
    Base.metadata.create_all(bind=engine)
    seed_demo_history_if_needed()


# Auto-initialize database tables on import
init_db()


def get_db():
    """Dependency generator for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
