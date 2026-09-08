# AAROH — Project Progress & Engineering Master Plan

> **System Status**: `PHASE 3 COMPLETED (Validation Gate 3 Passed)`  
> **Last Updated**: 2026-09-08 22:00 IST  
> **Project Goal**: Hybrid Clinical Intelligence Platform orchestrating Classical XGBoost & Variational Quantum Classifier (VQC) via deterministic agentic pipeline with SHAP explainability and clinical consultation memo generation.

---

## 1. Executive Summary & Pitch Baseline

- **The Pitch**: *"AAROH is a hybrid clinical benchmarking platform that orchestrates classical XGBoost and a trained Variational Quantum Classifier through an agentic pipeline, producing SHAP-explainable predictions and a clinical consultation memo — with the honest result that at 569 rows, we validate quantum encoding viability, not quantum superiority."*
- **Target Dataset**: Wisconsin Breast Cancer Diagnostic (WBCD) — 569 cases, 30 features reduced to 4 primary PCA/Biomarker components for 4-qubit encoding.
- **Architectural Philosophy**: Real computation under the hood. No fake values, no hardcoded SHAP arrays, no black-box hallucinations. Full clinical auditability.

---

## 2. Phase-by-Phase Roadmap

```
[Phase 1: ML & Quantum Foundation] ──► [Phase 2: FastAPI Orchestrator & SSE] ──► [Phase 3: High-Impact UI] ──► [Phase 4: Multi-Model Validation] ──► [Phase 5: Pitch & Demo Hardening]
```

---

## 3. Phase Details & Status Tracker

### 🔵 PHASE 1: Machine Learning & Quantum Foundation
*Goal: Implement and validate real classical and quantum models with reproducible evaluation metrics.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **1.1** | Setup Python virtual environment & dependency matrix (`fastapi`, `uvicorn`, `xgboost`, `scikit-learn`, `shap`, `qiskit`, `qiskit-aer`, `numpy`, `pandas`) | `backend/requirements.txt` | ✅ Completed |
| **1.2** | Classical ML pipeline: WBCD loader, standard scaler, XGBoost classifier with 5-Fold Stratified CV | `backend/models/classical.py` | ✅ Completed |
| **1.3** | Quantum VQC pipeline: 4-qubit Angle/ZZFeatureMap encoding + RealAmplitudes ansatz trained via COBYLA optimizer (50 iterations) | `backend/models/quantum.py` | ✅ Completed |
| **1.4** | Fallback parameter generator: Pre-train and save stable parameters to `vqc_params_pretrained.npy` and pure numpy circuit replay fallback | `backend/models/fallback_sim.py` | ✅ Completed |
| **1.5** | SHAP feature attribution calculator (TreeExplainer on top clinical features) | `backend/models/explainability.py` | ✅ Completed |

**Validation Gate 1**: `✅ PASSED` — Automated test suite (`backend/models/test_gate1.py`) verified all 9 artifacts, XGBoost & VQC probabilities in `[0.0, 1.0]`, exact SHAP additive property (`delta < 1e-6`), and zero-delta NumPy fallback parity.

---

### 🔵 PHASE 2: Agentic Orchestration & FastAPI Backend
*Goal: Create an SSE-streamed deterministic agent pipeline narrating actual computations.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **2.1** | FastAPI server initialization with CORS, healthcheck, and model cache at startup | `backend/main.py` | ✅ Completed |
| **2.2** | Model evaluation endpoint `/api/metrics` reporting 5-fold CV for XGBoost vs single 80/20 test split for VQC | `GET /api/metrics` | ✅ Completed |
| **2.3** | Agent Orchestrator: Deterministic 4-stage pipeline (Data Ingestion Agent ➔ Quantum Feature Agent ➔ Ensemble Consensus Agent ➔ Clinical Synthesis Agent) | `backend/agents/orchestrator.py` | ✅ Completed |
| **2.4** | Server-Sent Events (SSE) streaming endpoint `/api/predict/stream` providing live stage execution & real metrics | `POST /api/predict/stream` | ✅ Completed |
| **2.5** | Clinical Consultation Memo generator creating structured, printable diagnostic summary with clinical disclaimer | `backend/reports/memo_gen.py` | ✅ Completed |

**Validation Gate 2**: `✅ PASSED` — Automated integration test suite (`backend/tests/test_gate2.py`) verified `GET /api/health`, dual-metric comparison (`/api/metrics`), 3 authentic WBCD reference patient presets (`/api/reference-patients`), synchronous prediction (`/api/predict`), full 4-stage SSE streaming (`/api/predict/stream`, 9 events received in ~200ms), and input validation guardrails.

---

### 🔵 PHASE 3: Frontend Interface & Interactive Clinical Dashboard
*Goal: Build a high-density, polished UI with real-time SSE stream consumption, SHAP visualizations, and quantum state indicators.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **3.1** | Design system & modern UI layout (Dark mode, glassmorphism, responsive grid) | `aaroh-app/src/index.css` | ✅ Completed |
| **3.2** | Patient input & preset selector (Benign reference, Malignant reference, Borderline case, Custom sliders) | `aaroh-app/src/components/PatientInput.jsx` | ✅ Completed |
| **3.3** | Live Agentic Stream visualizer (Terminal-like stage timeline with active status pulses) | `aaroh-app/src/components/AgentStream.jsx` | ✅ Completed |
| **3.4** | Dual Model Comparison Panel (XGBoost Confidence vs VQC State Probability + Quantum Circuit Diagram preview) | `aaroh-app/src/components/ModelComparison.jsx` | ✅ Completed |
| **3.5** | Interactive SHAP Waterfall/Bar Chart (Visualizing exact positive & negative force contributors) | `aaroh-app/src/components/ShapViewer.jsx` | ✅ Completed |
| **3.6** | Formatted Clinical Consultation Memo modal with one-click PDF/Print export | `aaroh-app/src/components/ClinicalMemo.jsx` | ✅ Completed |

**Validation Gate 3**: `✅ PASSED` — Clean Vite production build (`✓ built in 2.34s`, 257 kB bundle). Full end-to-end integration verified with live FastAPI backend: reference preset switching, real-time SSE streaming of all 4 agent stages, side-by-side XGBoost vs 4-Qubit VQC comparison, exact TreeSHAP force vectors, and printable hospital clinical memorandum.

---

### 🔵 PHASE 4: Robustness, Benchmark Metrics & Fallback Testing
*Goal: Guarantee zero-fail resilience under live presentation constraints.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **4.1** | Fallback trigger check (Live Qiskit ➔ PennyLane ➔ Pre-trained NumPy replay) | `backend/tests/test_fallback.py` | ⏳ Pending |
| **4.2** | Hard timeout guardrails (Any circuit inference exceeding 3s automatically routes to precomputed numpy simulator) | `backend/models/quantum.py` | ⏳ Pending |
| **4.3** | Metric panel audit: Separate model-level cross-validation metrics panel from per-patient inference confidence | `aaroh-app/src/components/MetricsOverview.jsx` | ⏳ Pending |

**Validation Gate 4**: Simulate backend environment without Qiskit/GPU and ensure seamless automatic fallback with identical API interface.

---

### 🔵 PHASE 5: Presentation Polish, Pitch Prep & Demo Video Recording
*Goal: Lock in presentation assets and foolproof demo materials.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **5.1** | Record crisp 1080p fallback demo video demonstrating full end-to-end flow with voiceover/captions | `artifacts/aaroh_demo.mp4` | ⏳ Pending |
| **5.2** | Pitch deck slide integration according to `SIH2025-IDEA-Presentation-Format.pdf` | Slide Deck sync | ⏳ Pending |
| **5.3** | Rehearse 3 pre-written judge responses (VQC Wins / VQC Matches / VQC Underperforms) | Team Q&A Sheet | ⏳ Pending |

---

## 4. Phase Execution Log & Changelog

| Date / Time | Phase / Subphase | Changes Made | Key Decision / Outcome |
| :--- | :--- | :--- | :--- |
| **2026-09-08 19:25** | **Phase 0** | Created `progress.md` master engineering tracker and initialized task checklist. | Project scope locked; 5 distinct building phases defined. |
| **2026-09-08 20:01** | **Subphase 1.1** | Created isolated `backend/.venv`, installed all requirements (`qiskit 2.5.2`, `qiskit-aer 0.17.2`, `xgboost 3.4.1`, `shap 0.52.0`, `scikit-learn 1.9.0`, `fastapi 0.141.1`), and verified Qiskit Bell-state Aer simulation. | Environment check passed cleanly in 2.1s without needing abort/PennyLane fallback. |
| **2026-09-08 20:29** | **Subphase 1.2** | Implemented `backend/models/classical.py` with 5-Fold Stratified CV on 569 WBCD samples. Trained and serialized production XGBoost model and StandardScaler. | Baseline established: `0.994 ± 0.004 ROC-AUC` (Accuracy: `96.0% ± 1.6%`, Sensitivity: `93.4% ± 3.3%`). |
| **2026-09-08 20:43** | **Specification Sync** | Updated `idea.md` and `progress.md` with open-source reference matrix (IBM Qiskit ML VQC, FastAPI SSE, React clinical UI), locked pitch scripts, and Q&A defenses. | Subphases 1.3 and 1.4 initiated. |
| **2026-09-08 20:56** | **Subphase 1.3** | Built and executed `backend/models/quantum.py`: 4-qubit `ZZFeatureMap` + `RealAmplitudes` ansatz + `StatevectorEstimator` trained via COBYLA optimizer (50 iterations, BCE loss) on 80/20 held-out split. Serialized `vqc_params_pretrained.npy`, `pca.joblib`, `quantum_scaler.joblib`, and `quantum_metrics.json`. | VQC test generalization achieved: `0.748 ROC-AUC`, `68.4% Accuracy`, `69.1% Sensitivity`. Per-patient forward pass takes ~12-25ms. |
| **2026-09-08 21:09** | **Subphase 1.4** | Implemented `backend/models/fallback_sim.py` pure NumPy statevector matrix simulator (tensordot unitary gate propagation, 16-amplitude complex statevector, <IIIZ> observable). Verified against Qiskit Aer statevector output. Added resilient transparent routing (`predict_quantum_with_resilient_fallback`). | Exact numerical match with Qiskit Aer (`delta = 0.000000e+00`). Sub-4ms fallback latency with zero external quantum dependencies at runtime. |
| **2026-09-08 21:22** | **Subphase 1.5** | Built `backend/models/explainability.py`: exact `TreeExplainer` attribution, per-patient Waterfall step generator, clinical memo synthesis, and cohort-wide global rankings (`global_feature_importance.json`). Executed and passed `test_gate1.py` audit suite. | Additive property verified (`delta = 2.4e-07`). Phase 1 (ML & Quantum Foundation) officially 100% complete. |
| **2026-09-08 21:35** | **Phase 2 (All Subphases)** | Implemented `backend/reports/memo_gen.py`, `backend/agents/orchestrator.py`, `backend/main.py`, and `backend/tests/test_gate2.py`. Pre-warmed model singletons in FastAPI lifespan. Built live Server-Sent Events (SSE) streaming endpoint (`/api/predict/stream`), dual metrics comparison (`/api/metrics`), 3 WBCD reference patient presets (`/api/reference-patients`), and input validation. | Validation Gate 2 100% passed. Full 4-agent SSE diagnostic loop executes in ~200ms with zero errors. Phase 2 complete. |
| **2026-09-08 21:49** | **Phase 2 Hardening** | Senior dev audit addressed: 1) Cached static WBCD presets at startup in `REFERENCE_PATIENTS_CACHE` (eliminated repeated sklearn dataset I/O), 2) Purged dead imports (`Request`, `JSONResponse`), 3) Refactored SSE stage delays into configurable `DEFAULT_STAGE_STREAM_DELAY_SEC`, 4) Fixed `memo_gen.py` `model_consensus` override logic, 5) Dynamic version discovery in `/api/health`, 6) Set OpenBLAS thread guards for Windows stability. | Validation Gate 2 re-verified at 100% compliance. Synchronous diagnostic latency reduced to 69.5ms. |
| **2026-09-08 21:55** | **Phase 3 (All Subphases)** | Replaced old mock UI with production-grade clinical dashboard: built `Header.jsx`, `PatientInput.jsx` (WBCD presets + 30D inspector + fallback toggle), `AgentStream.jsx` (live SSE telemetry), `ModelComparison.jsx` (XGBoost vs VQC + circuit wire + Honest Asymmetry protocol), `ShapViewer.jsx` (bidirectional force bars), `ClinicalMemo.jsx` (printable hospital memo with `@media print`), and `MetricsModal.jsx` (empirical benchmarks & global rankings). | Validation Gate 3 passed. Clean Vite production build in 2.34s. Both backend (:8000) and frontend (:5173) operational. |

---

## 5. Live Rules for Updating this File

1. **Before starting a subphase**: Mark status as `🔄 In Progress`.
2. **Upon completing a subphase**:
   - Run verification test.
   - Mark status as `✅ Completed`.
   - Add entry to the **Phase Execution Log** with exact timestamp and architectural changes.
3. **If a pivot occurs**: Record the reason in the log and update affected subphases.
