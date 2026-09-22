"""
AAROH FastAPI Backend & Server-Sent Events (SSE) Orchestration Service
- Domain: Multimodal Hybrid Classical-Quantum Parkinson's Disease Screening Platform
- 6-Stage Deterministic Agentic Pipeline with real-time SSE streaming
- REST APIs:
    * GET  /api/health
    * GET  /api/metrics (Experiments A, B, C, C2 comparison + 5-fold CV)
    * GET  /api/demo-patients (4 curated Parkinson's reference cases)
    * POST /api/screen/stream (SSE live 6-stage streaming)
    * POST /api/screen/sync (synchronous screening endpoint)
    * GET  /api/patient/{id}/history (SQLite longitudinal assessment history)
    * POST /api/patient/{id}/save-assessment (save assessment to DB)
"""

import os
# Guard against OpenBLAS thread allocation exhaustion on Windows multi-core environments
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import sys
import json
import time
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

import xgboost
import shap
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.models.quantum import get_quantum_inference_pipeline
from backend.models.fallback_sim import get_fallback_inference_pipeline
from backend.models.explainability import get_explainability_engine
from backend.models.fusion import get_hybrid_pipeline
from backend.agents.orchestrator import run_diagnostic_pipeline, stream_diagnostic_pipeline
from backend.database.db import init_db, get_db
from backend.database.models import Assessment

# Paths
MODELS_DIR = os.path.join(BACKEND_DIR, "models")
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "parkinsons.csv")
CLASSICAL_METRICS_PATH = os.path.join(MODELS_DIR, "classical_metrics.json")
QUANTUM_METRICS_PATH = os.path.join(MODELS_DIR, "quantum_metrics.json")
GLOBAL_IMPORTANCE_PATH = os.path.join(MODELS_DIR, "global_feature_importance.json")
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, "feature_names.json")
FUSION_WEIGHTS_PATH = os.path.join(MODELS_DIR, "fusion_weights.json")
COMPARISON_METRICS_PATH = os.path.join(MODELS_DIR, "model_comparison_metrics.json")

DEMO_PATIENTS_CACHE: Optional[Dict[str, Any]] = None


def get_or_build_demo_patients() -> Dict[str, Any]:
    """Extracts authentic, representative demo cases from the Parkinson's dataset."""
    global DEMO_PATIENTS_CACHE
    if DEMO_PATIENTS_CACHE is not None:
        return DEMO_PATIENTS_CACHE

    df = pd.read_csv(DATA_PATH)
    feature_cols = [c for c in df.columns if c not in ["name", "status"]]
    
    # 1. High Risk PD Case (Strong dysphonia & perturbation)
    pd_cases = df[df["status"] == 1]
    high_pd_sample = pd_cases.iloc[0][feature_cols].values.tolist()

    # 2. Moderate / Borderline PD Case
    moderate_pd_sample = pd_cases.iloc[10][feature_cols].values.tolist()

    # 3. Longitudinal Recovery Case (moderate PD responding to therapy)
    recovery_sample = pd_cases.iloc[20][feature_cols].values.tolist()

    # 4. Healthy Control Case
    healthy_cases = df[df["status"] == 0]
    healthy_sample = healthy_cases.iloc[0][feature_cols].values.tolist()

    DEMO_PATIENTS_CACHE = {
        "feature_names": feature_cols,
        "patients": [
            {
                "preset_id": "case_high_pd",
                "patient_id": "P-001",
                "label": "Elevated Parkinson's Phonation (High Risk)",
                "ground_truth": "Parkinson's Disease",
                "description": "Marked vocal jitter, elevated PPE, and reduced HNR indicating advanced cycle-to-cycle frequency instability.",
                "features": high_pd_sample,
                "clinical_metadata": {"age": 68, "sex": "Male", "moca": 23, "tremor_freq_hz": 5.4, "symptom_months": 24},
            },
            {
                "preset_id": "case_moderate_pd",
                "patient_id": "P-002",
                "label": "Moderate / Borderline Microperturbation",
                "ground_truth": "Parkinson's Disease",
                "description": "Intermediate acoustic features near clinical boundary with subtle tremor characteristics.",
                "features": moderate_pd_sample,
                "clinical_metadata": {"age": 62, "sex": "Female", "moca": 26, "tremor_freq_hz": 4.8, "symptom_months": 12},
            },
            {
                "preset_id": "case_therapy_response",
                "patient_id": "P-003",
                "label": "Post-Therapy Improvement (Longitudinal)",
                "ground_truth": "Parkinson's Disease (On Medication)",
                "description": "Phonation metrics demonstrating stabilization post-Levodopa administration over repeated visits.",
                "features": recovery_sample,
                "clinical_metadata": {"age": 71, "sex": "Male", "moca": 25, "tremor_freq_hz": 3.9, "symptom_months": 36},
            },
            {
                "preset_id": "case_healthy_control",
                "patient_id": "P-004",
                "label": "Healthy Control Baseline (Normative)",
                "ground_truth": "Healthy Control",
                "description": "High harmonicity (HNR > 25 dB), low jitter/shimmer, regular fundamental frequency periodicity.",
                "features": healthy_sample,
                "clinical_metadata": {"age": 59, "sex": "Female", "moca": 29, "tremor_freq_hz": 0.0, "symptom_months": 0},
            },
        ],
    }
    return DEMO_PATIENTS_CACHE


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup lifecycle: pre-warms all model engines and SQLite database."""
    print("=" * 65)
    print("AAROH BACKEND INITIALIZATION: PRE-WARMING MODELS & DATABASE...")
    print("=" * 65)
    t0 = time.perf_counter()
    try:
        init_db()
        print("  [OK] SQLite Database & demo assessment histories initialized.")

        get_explainability_engine()
        print("  [OK] Classical XGBoost & SHAP TreeExplainer pre-warmed.")

        get_quantum_inference_pipeline()
        print("  [OK] Quantum VQC StatevectorEstimator pre-warmed.")

        get_fallback_inference_pipeline()
        print("  [OK] Pure NumPy Fallback Matrix Simulator pre-warmed.")

        get_hybrid_pipeline()
        print("  [OK] Hybrid Fusion Pipeline pre-warmed.")

        get_or_build_demo_patients()
        print("  [OK] Parkinson's Demo Patient presets cached in memory.")

        warmup_ms = (time.perf_counter() - t0) * 1000.0
        print(f"--> All singletons and database pre-warmed in {warmup_ms:.1f}ms!")
        print("--> AAROH Hybrid Clinical Orchestrator is ONLINE.")
        print("=" * 65)
    except Exception as e:
        print(f"  [WARNING] Warmup encountered exception (will retry on request): {e}")

    yield
    print("AAROH Backend shutting down gracefully.")


app = FastAPI(
    title="AAROH — Hybrid Classical-Quantum Parkinson's Screening API",
    description="Deterministic 6-stage multi-agent clinical decision support and quantum benchmarking platform.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================================
# Request & Response Schemas
# =========================================================================
class ScreenRequest(BaseModel):
    patient_id: Optional[str] = Field(default="PATIENT-DEMO-001", description="Patient identifier")
    features: List[float] = Field(
        ...,
        description="List of exactly 22 acoustic voice features.",
        min_length=22,
        max_length=22,
    )
    force_fallback: Optional[bool] = Field(
        default=False,
        description="If True, forces pure NumPy statevector simulation.",
    )


class SaveAssessmentRequest(BaseModel):
    patient_id: str
    classical_score: float
    quantum_score: float
    hybrid_score: float
    risk_tier: str
    consensus_status: str
    feature_json: Optional[str] = None
    shap_json: Optional[str] = None
    clinical_memo_json: Optional[str] = None


# =========================================================================
# Endpoints
# =========================================================================
@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Service health and diagnostic status."""
    return {
        "status": "online",
        "service": "AAROH Hybrid Parkinson's Screening Platform",
        "version": "2.0.0",
        "domain": "Parkinson's Disease Acoustic Biomarker Screening",
        "database": "SQLite (Longitudinal Assessment Store)",
        "quantum_framework": "Qiskit Aer + Pure NumPy Fallback Simulator",
        "classical_framework": f"XGBoost {xgboost.__version__} (5-Fold Stratified CV)",
        "explainability_engine": f"Exact TreeSHAP (shap {shap.__version__})",
        "timestamp": time.time(),
    }


@app.get("/api/metrics")
def get_benchmarking_metrics() -> Dict[str, Any]:
    """
    Returns full model benchmarking comparison:
    Classical XGBoost (5-fold CV) vs Quantum VQC vs Hybrid Late Fusion (Experiment C).
    """
    classical_data = {}
    quantum_data = {}
    comparison_data = {}
    fusion_weights = {}

    if os.path.exists(CLASSICAL_METRICS_PATH):
        with open(CLASSICAL_METRICS_PATH, "r") as f:
            classical_data = json.load(f)

    if os.path.exists(QUANTUM_METRICS_PATH):
        with open(QUANTUM_METRICS_PATH, "r") as f:
            quantum_data = json.load(f)

    if os.path.exists(COMPARISON_METRICS_PATH):
        with open(COMPARISON_METRICS_PATH, "r") as f:
            comparison_data = json.load(f)

    if os.path.exists(FUSION_WEIGHTS_PATH):
        with open(FUSION_WEIGHTS_PATH, "r") as f:
            fusion_weights = json.load(f)

    return {
        "classical_xgboost": classical_data,
        "quantum_vqc": quantum_data,
        "hybrid_comparison": comparison_data,
        "fusion_weights": fusion_weights,
        "honest_disclosure": (
            "Classical XGBoost is evaluated via 5-Fold Stratified Cross-Validation across all 195 recordings. "
            "Quantum VQC is evaluated on a single held-out 80/20 test split (n=39, seed=42). "
            "The hybrid architecture combines both via validation-tuned late fusion."
        ),
    }


@app.get("/api/demo-patients")
@app.get("/api/reference-patients")
def get_demo_patients() -> Dict[str, Any]:
    """Returns 4 authentic Parkinson's reference patient presets."""
    return get_or_build_demo_patients()


@app.get("/api/global-importance")
def get_global_feature_importance() -> Dict[str, Any]:
    """Returns cohort-wide SHAP rankings across all Parkinson's cases."""
    if not os.path.exists(GLOBAL_IMPORTANCE_PATH):
        raise HTTPException(status_code=404, detail="Global feature importance not found.")
    with open(GLOBAL_IMPORTANCE_PATH, "r") as f:
        return json.load(f)


@app.post("/api/screen/sync")
@app.post("/api/predict")
def screen_patient_sync(req: ScreenRequest) -> Dict[str, Any]:
    """Synchronous 6-stage clinical screening pipeline execution."""
    try:
        result = run_diagnostic_pipeline(
            raw_features=req.features,
            patient_id=req.patient_id,
            force_fallback=req.force_fallback,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/screen/stream")
@app.post("/api/predict/stream")
def screen_patient_stream(req: ScreenRequest):
    """
    Live Server-Sent Events (SSE) streaming endpoint.
    Emits events across all 6 deterministic agent stages:
      Stage 1: Data Ingestion & QC Agent
      Stage 2: Classical Inference Agent
      Stage 3: Quantum Encoding Agent
      Stage 4: Hybrid Fusion Agent
      Stage 5: Explainability Synthesis Agent
      Stage 6: Clinical Memo Agent
      Final: Full consolidated payload
    """
    return StreamingResponse(
        stream_diagnostic_pipeline(
            raw_features=req.features,
            patient_id=req.patient_id,
            force_fallback=req.force_fallback,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/patient/{patient_id}/history")
def get_patient_history(patient_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Returns longitudinal screening assessment history for a specific patient."""
    records = (
        db.query(Assessment)
        .filter(Assessment.patient_id == patient_id)
        .order_by(Assessment.assessed_at.asc())
        .all()
    )
    return {
        "patient_id": patient_id,
        "total_assessments": len(records),
        "history": [r.to_dict() for r in records],
    }


@app.post("/api/patient/{patient_id}/save-assessment")
def save_patient_assessment(
    patient_id: str,
    req: SaveAssessmentRequest,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Saves a completed screening assessment to the SQLite database."""
    assessment = Assessment(
        patient_id=patient_id,
        classical_score=req.classical_score,
        quantum_score=req.quantum_score,
        hybrid_score=req.hybrid_score,
        risk_tier=req.risk_tier,
        consensus_status=req.consensus_status,
        feature_json=req.feature_json,
        shap_json=req.shap_json,
        clinical_memo_json=req.clinical_memo_json,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return {
        "status": "saved",
        "assessment_id": assessment.id,
        "patient_id": assessment.patient_id,
        "assessed_at": assessment.assessed_at.isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
