# AAROH — Project Progress & Engineering Master Plan (v2.0 Parkinson's Edition)

> **System Status**: `ALL PHASES COMPLETED (All 4 Validation Gates Passed — 24/24 Audits Verified)`  
> **Last Updated**: 2026-09-23 01:06 IST  
> **Project Goal**: Multimodal Hybrid Classical–Quantum Early Parkinson's Screening Platform with SHAP Explainability & Longitudinal Monitoring.

---

## 1. Executive Summary & Pitch Baseline

- **The Pitch**: *"AAROH is a multimodal hybrid classical–quantum clinical decision-support platform that analyzes Parkinson's-associated acoustic and motor biomarkers through an explainable AI pipeline, providing doctors with an interpretable screening signal, dual-model comparison, and longitudinal monitoring."*
- **Primary Dataset**: UCI Parkinson's Voice Telemonitoring Dataset (195 recordings, 32 subjects, 22 acoustic features).
- **Secondary Alignment**: GP2 Release 12 Clinical Data Schema & MDS-UPDRS Part III motor feature mapping.

---

## 2. Phase-by-Phase Roadmap

```
[Phase 1: Data & Classical ML] ──► [Phase 2: Quantum ML Pipeline] ──► [Phase 3: Hybrid Fusion Layer] ──► [Phase 4: FastAPI & SSE Agents] ──► [Phase 5: React 19 UI Dashboard] ──► [Phase 6: Persistence & History] ──► [Phase 7: Hardening & Demo]
```

---

## 3. Phase Details & Status Tracker

### 🔵 PHASE 1: Data Foundation & Classical ML Pipeline
*Goal: Load, explore, preprocess, and train verified classical baseline models with cross-validation and SHAP explainability.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **1.1** | UCI Parkinson's Voice dataset retrieval and data integrity validation | `data/parkinsons.csv` | ✅ Completed |
| **1.2** | Exploratory Data Analysis & subject/recording balance audit (195 samples, 32 subjects) | `backend/models/classical.py` | ✅ Completed |
| **1.3** | Full preprocessing pipeline (StandardScaler fitted on train splits only, zero data leakage) | `backend/models/scaler.joblib` | ✅ Completed |
| **1.4** | Benchmark classical baseline models (Logistic Regression, SVM RBF, Random Forest, XGBoost) | `backend/models/classical_metrics.json` | ✅ Completed |
| **1.5** | Primary 5-Fold Stratified Cross-Validation on XGBoost | 0.9622 ROC-AUC, 91.28% Acc, 96.60% Sens | ✅ Completed |
| **1.6** | Production XGBoost model training & artifact serialization | `backend/models/xgboost_model.json`, `feature_names.json` | ✅ Completed |
| **1.7** | Exact TreeSHAP Explainability Engine (per-patient waterfall + cohort biomarker ranking) | `backend/models/explainability.py`, `global_feature_importance.json` | ✅ Completed |
| **1.8** | Automated Validation Gate 1 Test Suite | `backend/models/test_gate1.py` | ✅ Completed |

---

### 🔵 PHASE 2: Quantum ML Pipeline
*Goal: Build, train, and validate the 4-Qubit Variational Quantum Classifier (VQC) with a resilient zero-fail NumPy fallback.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **2.1** | Dimensionality reduction via PCA (4 components explaining 85.09% variance) + MinMaxScaler([0, π]) | `backend/models/pca.joblib`, `quantum_scaler.joblib` | ✅ Completed |
| **2.2** | 4-Qubit VQC circuit design: `ZZFeatureMap` (reps=1) + `RealAmplitudes` (8 parameters) + Pauli-Z observable (`IIIZ`) | `backend/models/quantum.py` | ✅ Completed |
| **2.3** | Quantum training via COBYLA optimizer (50 iterations, BCE loss descent from 0.6734 ➔ 0.6314) | `backend/models/vqc_params_pretrained.npy` | ✅ Completed |
| **2.4** | Quantum metrics benchmark on held-out 80/20 test split (0.6966 ROC-AUC, 81.25% Precision) | `backend/models/quantum_metrics.json` | ✅ Completed |
| **2.5** | Pure NumPy matrix statevector simulation engine (`fallback_sim.py`) with exact 0.0-delta parity to Qiskit | `backend/models/fallback_sim.py` | ✅ Completed |
| **2.6** | Resilient transparent routing wrapper (Primary Qiskit ➔ NumPy fallback auto-switch) | `backend/models/fallback_sim.py` | ✅ Completed |

---

### 🔵 PHASE 3: Hybrid Fusion Layer & Model Comparison Benchmark
*Goal: Design, calibrate, and validate the optimal late fusion layer and meta-classifier.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **3.1** | 5-Fold Cross Validation grid-search on training splits for optimal $(\alpha, \beta)$ fusion weights | `backend/models/fusion_weights.json` ($\alpha=0.31, \beta=0.69$) | ✅ Completed |
| **3.2** | Stacking Meta-Classifier (Logistic Regression on $[P_{\text{classical}}, P_{\text{quantum}}]$) | `backend/models/meta_classifier.joblib` | ✅ Completed |
| **3.3** | Multi-experiment benchmarking (Experiments A, B, C, C2 on identical held-out test split) | `backend/models/model_comparison_metrics.json` | ✅ Completed |
| **3.4** | Discordance detection & clinical consensus flagging ($|P_c - P_q| \ge 0.30$) | `backend/models/fusion.py` | ✅ Completed |
| **3.5** | Comprehensive Validation Gate 1 Test Suite Update | `backend/models/test_gate1.py` (6/6 Audits Passed) | ✅ Completed |

---

### 🔵 PHASE 4: FastAPI Backend & 6-Stage Agentic Pipeline
*Goal: Create an SSE-streamed deterministic 6-stage agent orchestrator with SQLite persistence.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **4.1** | FastAPI app initialization with CORS, lifespan startup cache, and healthcheck | `backend/main.py` (`GET /api/health`) | ✅ Completed |
| **4.2** | Multi-experiment metrics endpoint exposing dual-model benchmark & honest disclosure | `GET /api/metrics` | ✅ Completed |
| **4.3** | Authentic Parkinson's Demo Preset cases (P-001 High, P-002 Moderate, P-003 Recovery, P-004 Control) | `GET /api/demo-patients` | ✅ Completed |
| **4.4** | Deterministic 6-Stage Agent Pipeline (`orchestrator.py`): Data Ingestion ➔ Classical ➔ Quantum ➔ Hybrid Fusion ➔ TreeSHAP ➔ Clinical Memo | `backend/agents/orchestrator.py` | ✅ Completed |
| **4.5** | Live Server-Sent Events (SSE) streaming endpoint delivering 13 real-time events in 265ms | `POST /api/screen/stream` | ✅ Completed |
| **4.6** | Structured Parkinson's Clinical Consultation Memo generator with ICD-10 (`G20`/`R47.81`) | `backend/reports/memo_gen.py` | ✅ Completed |
| **4.7** | SQLite database with SQLAlchemy ORM + longitudinal assessment history seeding | `backend/database/db.py`, `models.py` | ✅ Completed |
| **4.8** | Automated Validation Gate 2 Test Suite | `backend/tests/test_gate2.py` (8/8 Audits Passed) | ✅ Completed |

---

## 4. Benchmark Summary Across All Experiments (Held-Out Test Set, n=39)

| Experiment | Model Architecture | ROC-AUC | Accuracy | Sensitivity | Specificity | F1 Score |
|:-----------|:-------------------|:--------|:---------|:------------|:------------|:---------|
| **Experiment A** | Classical XGBoost (22 Features) | **1.0000** | 100.0% | 100.0% | 100.0% | 1.0000 |
| **Experiment B** | Quantum VQC (4 Qubits, 8 Params) | **0.6966** | 51.28% | 44.83% | 70.00% | 0.5778 |
| **Experiment C** | Hybrid Late Fusion ($0.31 P_c + 0.69 P_q$) | **0.9966** | **97.44%** | **96.55%** | **100.0%** | **0.9825** |
| **Experiment C2**| Stacking Meta-Classifier (Logistic Regression) | **1.0000** | 100.0% | 100.0% | 100.0% | 1.0000 |

---

### 🔵 PHASE 5: Frontend Dashboard (React 19 + Vite 6 + Tailwind CSS)
*Goal: Build a high-performance, clinical-grade decision-support UI matching the GP2-inspired aesthetic (Slate-50 `#F8FAFC`, Teal accents `#0D9488`, Dark Engine `#0F172A`).*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **5.1** | Global styling tokens, typography (Inter, Outfit, JetBrains Mono), custom print CSS, and Tailwind configuration | `aaroh-app/tailwind.config.js`, `src/index.css` | ✅ Completed |
| **5.2** | Navigation header with live backend status indicator, Benchmark modal trigger, and one-click SSE analysis CTA | `aaroh-app/src/components/Navbar.jsx` | ✅ Completed |
| **5.3** | Modality Input Deck: 22 MDVP acoustic micro-sliders with wave animation, kinematics & 3-7Hz tremor PSD chart, clinical phenotype card | `VoiceModalityCard.jsx`, `MotorModalityCard.jsx`, `ClinicalPhenotypeCard.jsx` | ✅ Completed |
| **5.4** | Dark-themed Quantum Circuit & State Monitor (`#0F172A`) showing 4 orbital qubit angles, runtime telemetry, and discordance alerts | `aaroh-app/src/components/QuantumEngineCard.jsx` | ✅ Completed |
| **5.5** | Real-time 6-Stage Agentic SSE Stream visualizer with step progress bars and sub-second execution timestamps | `aaroh-app/src/components/AgentStream.jsx` | ✅ Completed |
| **5.6** | Multi-tier Risk Assessment Display with circular progress gauge, confidence intervals, and ICD-10 clinical recommendations | `aaroh-app/src/components/ScreeningResult.jsx` | ✅ Completed |
| **5.7** | TreeSHAP Explainability View featuring interactive Recharts horizontal bar chart, base value delta, and cohort importance ranking | `aaroh-app/src/components/ShapExplainability.jsx` | ✅ Completed |
| **5.8** | Longitudinal Progression Tracker with multi-visit Recharts area/line chart and audit-logged visit history | `aaroh-app/src/components/LongitudinalHistory.jsx` | ✅ Completed |
| **5.9** | A4 Printable Clinical Consultation Memo with physician signature block, discordance flags, and `@media print` support | `aaroh-app/src/components/ClinicalMemo.jsx` | ✅ Completed |
| **5.10** | Comprehensive Benchmark & Metrics Modal with dual-model ROC curves and transparent CV disclosures | `aaroh-app/src/components/MetricsModal.jsx` | ✅ Completed |
| **5.11** | Production Build Verification with zero Vite/React compilation warnings | `aaroh-app/dist/` (2415 modules transformed, 0 errors) | ✅ Completed |

---

## 4. Benchmark Summary Across All Experiments (Held-Out Test Set, n=39)

| Experiment | Model Architecture | ROC-AUC | Accuracy | Sensitivity | Specificity | F1 Score |
|:-----------|:-------------------|:--------|:---------|:------------|:------------|:---------|
| **Experiment A** | Classical XGBoost (22 Features) | **1.0000** | 100.0% | 100.0% | 100.0% | 1.0000 |
| **Experiment B** | Quantum VQC (4 Qubits, 8 Params) | **0.6966** | 51.28% | 44.83% | 70.00% | 0.5778 |
| **Experiment C** | Hybrid Late Fusion ($0.31 P_c + 0.69 P_q$) | **0.9966** | **97.44%** | **96.55%** | **100.0%** | **0.9825** |
| **Experiment C2**| Stacking Meta-Classifier (Logistic Regression) | **1.0000** | 100.0% | 100.0% | 100.0% | 1.0000 |

---

### 🔵 PHASE 6: Data Persistence & Longitudinal History
*Goal: Persistent SQLite assessment recording with multi-visit trajectory tracking, progression delta calculation, and audit history.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **6.1** | SQLite Database setup with SQLAlchemy ORM and session connection pooling | `backend/database/db.py` | ✅ Completed |
| **6.2** | Assessment ORM Model with scores, risk tier, consensus status, and JSON dumps | `backend/database/models.py` | ✅ Completed |
| **6.3** | Assessment saving endpoint with JSON payload parsing and autoincrement ID generation | `POST /api/patient/{id}/save-assessment` | ✅ Completed |
| **6.4** | Patient history retrieval endpoint sorted chronologically | `GET /api/patient/{id}/history` | ✅ Completed |
| **6.5** | Pre-seeded multi-visit clinical trajectories for all demo patients (P-001 through P-004) | `seed_demo_history_if_needed()` | ✅ Completed |
| **6.6** | Frontend Longitudinal Tracker integration with dynamic disease delta calculation (+/- %) and Recharts trajectory | `aaroh-app/src/components/LongitudinalHistory.jsx` | ✅ Completed |
| **6.7** | Automated Validation Gate 3 Test Suite | `backend/tests/test_gate3.py` (5/5 Audits Passed) | ✅ Completed |

---

### 🔵 PHASE 7: Hardening, Testing & SIH Demo Preparation
*Goal: Zero-failure live demo readiness, end-to-end stress testing, quantum fallback resilience, and SIH pitch documentation.*

| Subphase | Task Description | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **7.1** | End-to-end verification of all 4 clinical demo presets across the full 6-stage deterministic pipeline | `test_gate4_e2e.py` | ✅ Completed |
| **7.2** | Quantum Fallback zero-fail resilience test (pure NumPy statevector matrix simulation) | `backend/models/fallback_sim.py` | ✅ Completed |
| **7.3** | Concurrent multi-user load & stress test (5 simultaneous screening requests with 200 OK) | `test_gate4_e2e.py` | ✅ Completed |
| **7.4** | Master benchmarking API verification with honest CV vs single-split disclosure | `GET /api/metrics` | ✅ Completed |
| **7.5** | Real-time SSE streaming sequence audit (13 events emitted in exact 6-stage sequence) | `test_gate4_e2e.py` | ✅ Completed |
| **7.6** | Comprehensive master documentation with pitch scripts, clinical defense, and architecture | `README.md` | ✅ Completed |
| **7.7** | Automated Validation Gate 4 Test Suite | `backend/tests/test_gate4_e2e.py` (5/5 Audits Passed) | ✅ Completed |

---

## 4. Benchmark Summary Across All Experiments (Held-Out Test Set, n=39)

| Experiment | Model Architecture | ROC-AUC | Accuracy | Sensitivity | Specificity | F1 Score |
|:-----------|:-------------------|:--------|:---------|:------------|:------------|:---------|
| **Experiment A** | Classical XGBoost (22 Features) | **1.0000** | 100.0% | 100.0% | 100.0% | 1.0000 |
| **Experiment B** | Quantum VQC (4 Qubits, 8 Params) | **0.6966** | 51.28% | 44.83% | 70.00% | 0.5778 |
| **Experiment C** | Hybrid Late Fusion ($0.31 P_c + 0.69 P_q$) | **0.9966** | **97.44%** | **96.55%** | **100.0%** | **0.9825** |
| **Experiment C2**| Stacking Meta-Classifier (Logistic Regression) | **1.0000** | 100.0% | 100.0% | 100.0% | 1.0000 |

---

## 5. Master System Status & Summary

> **All 7 Phases Successfully Completed & Production Ready.**  
> - **Classical Baseline**: 0.9622 5-Fold ROC-AUC (XGBoost)  
> - **Quantum Classifier**: 4-Qubit VQC with zero-fail NumPy fallback  
> - **Hybrid Late Fusion**: $\alpha=0.31, \beta=0.69$ (0.9966 ROC-AUC)  
> - **Real-time Pipeline**: 6-Stage SSE Agent Orchestrator streaming 13 events in ~265ms  
> - **Clinical UI**: React 19 + Vite 6 + Tailwind CSS with TreeSHAP waterfall & longitudinal charts  
> - **Database Persistence**: SQLite SQLAlchemy 2.0 with pre-seeded demo trajectories  
> - **Quality Assurance**: 4/4 Validation Gates Passed (24/24 individual automated audits)
