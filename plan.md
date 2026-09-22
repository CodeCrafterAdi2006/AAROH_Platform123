# AAROH — Hybrid Classical-Quantum Early Parkinson's Screening Platform
## Master Implementation Plan v2.0

> **Version**: 2.0 (Parkinson's Edition)
> **Status**: Planning
> **Domain**: Parkinson's Disease Screening & Longitudinal Monitoring
> **Dataset**: UCI Parkinson's Voice Dataset + GP2 Release 12 Clinical Schema Alignment

---

## 1. One-Line Pitch

> *A multimodal hybrid classical-quantum clinical decision-support platform that analyzes Parkinson's-associated voice and motor features through an explainable AI pipeline to provide doctors with an interpretable screening signal, dual-model comparison, and longitudinal patient monitoring.*

---

## 2. Problem Statement

Parkinson's Disease (PD) affects **10 million people worldwide** and is the fastest-growing neurological disorder.

- **60-80% of dopaminergic neurons** are already lost before motor symptoms become clinically obvious.
- Early-stage voice and motor biomarkers (jitter, shimmer, tremor frequency, rigidity) are measurable but require systematic computational analysis.
- Most current AI tools are black-boxes — doctors cannot trust a probability without knowing *why* the model flagged a patient.
- Clinical time constraints mean longitudinal pattern tracking across visits is rarely done manually.

**Core Research Question**: Can a hybrid classical-quantum system provide clinicians with a reliable, interpretable, and consistent early screening signal from multimodal voice and motor data?

---

## 3. System Architecture Overview

```
+----------------------------------------------------------------------+
|                        AAROH PLATFORM v2                             |
+----------------------------------------------------------------------+
                               |
          +--------------------+--------------------+
          v                                         v
   React 19 Frontend                         FastAPI Backend
   (Clinical Dashboard)                      (Agentic Pipeline)
          |                                         |
          |                         +---------------+---------------+
          |                         |     REST API + SSE Streaming  |
          |                         +---------------+---------------+
          |                                         |
          |              +----------+----------+----+----+----------+
          |              v          v          v         v          v
          |          Stage 1    Stage 2    Stage 3   Stage 4   Stage 5-6
          |          Data QC  Classical   Quantum    Fusion    Explain +
          |          Agent    XGBoost     4-Qubit    Layer     Memo
          |                   + SHAP      VQC
          |                      |          |
          |                      +----+-----+
          |                           v
          |                   Hybrid Score + Clinical Memo
          |                           |
          +---------------------------+
               Live SSE stream updates UI in real-time
```

---

## 4. Datasets Strategy

### Primary Dataset: UCI Parkinson's Voice Dataset
- **Source**: UCI Machine Learning Repository (Max Little, University of Oxford, 2007)
- **Samples**: 197 voice recordings from 31 patients (23 with PD, 8 healthy controls)
- **Features**: 22 acoustic features (MDVP-based: Jitter, Shimmer, HNR, NHR, RPDE, DFA, PPE, D2)
- **Target**: Binary — `status`: 1 = Parkinson's, 0 = Healthy
- **Why**: Fully public, no institutional DUA required, clean tabular format, perfect for MVP

### Secondary Reference: Oxford PD Detection Dataset
- **Samples**: 195 voice measurements, 48 subjects (36 PD, 12 healthy)
- **Use**: Cross-validation benchmarking and model robustness testing

### Clinical Schema Alignment: GP2 Release 12
- Feature naming and clinical interpretation aligned with the GP2 data dictionary
- MDS-UPDRS Part III sub-scores referenced for motor feature clinical mapping
- Ensures medical credibility for evaluator pitch and future research plans

### Simulated Motor / Clinical Features (for Demo Dashboard)
- Realistic synthetic MDS-UPDRS subscores and MoCA values
- Drawn from GP2 R12 population-level clinical statistics
- Motor variables: tremor frequency (Hz), bradykinesia index, postural instability score

---

## 5. Feature Engineering

### Voice / Acoustic Feature Vector (22 UCI Features)

| Feature | Symbol | Clinical Meaning |
|:--------|:-------|:----------------|
| Avg. fundamental frequency | MDVP:Fo(Hz) | Baseline pitch, reduced in PD |
| Max fundamental frequency | MDVP:Fhi(Hz) | Pitch ceiling |
| Min fundamental frequency | MDVP:Flo(Hz) | Pitch floor |
| Jitter (absolute) | MDVP:Jitter(Abs) | Cycle-to-cycle F0 variation |
| Jitter (percentage) | MDVP:Jitter(%) | % variation from mean pitch |
| Jitter:RAP | MDVP:RAP | Relative average perturbation |
| Jitter:PPQ5 | MDVP:PPQ | 5-point period perturbation |
| Shimmer (amplitude) | MDVP:Shimmer | Cycle-to-cycle amplitude variation |
| Shimmer (dB) | Shimmer:dB | Amplitude variation in decibels |
| Shimmer:APQ3/APQ5/APQ11 | MDVP:APQ | Amplitude perturbation quotients |
| Harmonics-to-noise ratio | HNR | Voice periodicity vs noise |
| Noise-to-harmonics ratio | NHR | Turbulent noise presence |
| Recurrence period entropy | RPDE | Signal complexity |
| Detrended fluctuation analysis | DFA | Fractal scaling of vocal signal |
| Pitch period entropy | PPE | Irregularity of fundamental period |
| Correlation dimension | D2 | Nonlinear dynamical complexity |

### Motor / Clinical Feature Vector (Simulated for Demo)

| Feature | Clinical Meaning |
|:--------|:----------------|
| Tremor frequency (Hz) | 3-7 Hz resting tremor characteristic |
| Bradykinesia score | Slowness-of-movement index |
| Postural instability | Balance and gait irregularity |
| MoCA score (0-30) | Montreal Cognitive Assessment |
| Symptom duration (months) | Time since first noticeable symptom |
| Age | Demographic risk factor |
| Sex | Sex-stratified PD incidence differences |

### Preprocessing Pipeline

```
Raw Features
    -> Missing value imputation (median)
    -> Outlier capping (IQR-based, 1.5x IQR)
    -> StandardScaler (fitted on train ONLY)
    -> PCA 4 components (for Quantum branch, retaining ~80% variance)
    -> MinMaxScaler [0, pi] (for quantum angle encoding)
```

**Critical rule**: All preprocessors fitted on training data only. Zero leakage.

### Train/Test Split Strategy
- **Patient-level split** — no patient's recordings split across train/test sets
- 80/20 patient-level stratified split
- 5-fold stratified cross-validation on classical branch only

---

## 6. Phase-by-Phase Development Plan

---

### PHASE 1 — Data Foundation & Classical ML Pipeline
*Goal: Load, explore, preprocess, and train verified classical baselines*

**Tasks**:
- [x] 1.1 Download UCI Parkinson's dataset to `data/parkinsons.csv`
- [x] 1.2 EDA: class distribution, correlation heatmap, feature distributions
- [x] 1.3 Implement patient-level stratified train/test split
- [x] 1.4 Build full preprocessing pipeline (impute -> clip -> scale)
- [x] 1.5 Train baseline models: Logistic Regression, SVM (RBF), Random Forest, XGBoost
- [x] 1.6 Run 5-fold stratified CV on XGBoost — report Accuracy, Sensitivity, Specificity, F1, ROC-AUC
- [x] 1.7 Save artifacts: `xgboost_model.json`, `scaler.joblib`, `feature_names.json`, `classical_metrics.json`
- [x] 1.8 Implement SHAP TreeExplainer for per-patient feature attribution
- [x] 1.9 Write `test_gate1.py` — validate all artifacts, model output range, SHAP additivity

**Exit Criterion**: XGBoost achieves >85% ROC-AUC with verified 5-fold CV. All test_gate1 assertions pass. [PASSED: 0.9622 ROC-AUC, 91.28% Acc, 96.60% Sens]

---

### PHASE 2 — Quantum ML Pipeline
*Goal: Build, train, and validate the Variational Quantum Classifier*

**Tasks**:
- [x] 2.1 Implement PCA (4 components) + MinMaxScaler for quantum preprocessing
- [x] 2.2 Build 4-qubit VQC circuit (Qiskit):
  - Encoding: ZZFeatureMap (reps=1)
  - Ansatz: RealAmplitudes (reps=1, 8 trainable parameters)
  - Observable: Pauli-Z on qubit 0 (IIIZ)
- [x] 2.3 Implement QuantumVQC class with predict_proba() via expectation value -> probability mapping
- [x] 2.4 Train with COBYLA optimizer (50 iterations) on Binary Cross-Entropy loss
- [x] 2.5 Save artifacts: `vqc_params_pretrained.npy`, `pca.joblib`, `quantum_scaler.joblib`, `quantum_metrics.json`
- [x] 2.6 Implement pure NumPy matrix statevector fallback (`fallback_sim.py`)
- [x] 2.7 Compare VQC vs Classical on identical held-out test set

**Exit Criterion**: VQC outputs valid probabilities in [0.0, 1.0]. NumPy fallback matches Qiskit output within tolerance. test_gate1 quantum assertions pass. [PASSED: 0.6966 ROC-AUC, Exact Parity with NumPy Delta=0.0]

---

### PHASE 3 — Hybrid Fusion Layer
*Goal: Design and validate the optimal fusion of classical and quantum outputs*

**Tasks**:
- [x] 3.1 Implement validation-tuned late fusion: `Hybrid = a*P_classical + b*P_quantum` where `a + b = 1`
- [x] 3.2 Grid-search optimal (a, b) on validation set (NOT test set — no leakage)
- [x] 3.3 Implement meta-classifier (Logistic Regression on [P_classical, P_quantum])
- [x] 3.4 Benchmark three experiments:
  - Experiment A: Classical XGBoost only
  - Experiment B: Quantum VQC only
  - Experiment C: Hybrid Fusion (best of late fusion and meta-classifier)
- [x] 3.5 Generate full comparison table (Accuracy, Sensitivity, Specificity, F1, ROC-AUC)
- [x] 3.6 Save `fusion_weights.json` with optimal alpha/beta

**Exit Criterion**: All three experiments benchmarked with honest results. Fusion weights saved. [PASSED: alpha=0.31, beta=0.69, Hybrid ROC-AUC 0.9966, Meta ROC-AUC 1.000]

---

### PHASE 4 — FastAPI Backend & 6-Stage Agentic Pipeline
*Goal: Build the SSE-streaming deterministic agent orchestrator*

**API Endpoints**:
```
GET  /api/health
GET  /api/metrics                        (full model comparison table)
GET  /api/demo-patients                  (4 pre-built demo patient presets)
POST /api/screen/stream                  (SSE — live 6-stage pipeline)
POST /api/screen/sync                    (synchronous for testing)
GET  /api/patient/{id}/history           (longitudinal assessment history)
POST /api/patient/{id}/save-assessment   (save assessment to DB)
```

**6-Stage Agent Pipeline** (`agents/orchestrator.py`):
- **Stage 1**: Data Ingestion & QC Agent — validate inputs, clip outliers, normalize
- **Stage 2**: Classical Inference Agent — XGBoost predict + SHAP attribution
- **Stage 3**: Quantum Encoding Agent — PCA + VQC statevector computation
- **Stage 4**: Hybrid Fusion Agent — apply optimal (a, b) weights
- **Stage 5**: Explainability Synthesis Agent — rank voice vs motor contributions
- **Stage 6**: Clinical Memo Agent — screening signal, risk tier, ICD-10, clinical narrative

**Tasks**:
- [x] 4.1 FastAPI app init with CORS, lifespan model cache, healthcheck
- [x] 4.2 Pydantic request/response models
- [x] 4.3 Build all 6 agent stages in orchestrator.py
- [x] 4.4 Implement SSE streaming endpoint
- [x] 4.5 Build all REST endpoints
- [x] 4.6 SQLAlchemy SQLite integration (db.py + models.py)
- [x] 4.7 Write test_gate2.py — integration tests for all endpoints

**Exit Criterion**: All endpoints functional. SSE emits 6+ events per request in <500ms. [PASSED: 13 events in 265.9ms, 8/8 Audits Passed]

---

### PHASE 5 — Frontend Dashboard (React 19 + Vite 6 + Tailwind)
*Goal: Build a premium clinical UI matching the reference design system*

#### Design System

```
Background Canvas:  #F8FAFC (Slate 50 — clean clinical white)
Cards:              #FFFFFF with border #E2E8F0, rounded-2xl corners
Primary Accent:     #0D9488 (Teal 600)
Hover Accent:       #14B8A6 (Teal 500)
Dark Engine Block:  #0F172A (Slate 900 — quantum telemetry card)
Success Badge:      #10B981 (Emerald 500)
Warning Badge:      #F59E0B (Amber 500)
Danger Badge:       #EF4444 (Red 500)
Typography:         Inter (body text), Outfit (headings)
```

#### Components List

**`Navbar.jsx`**
- AAROH wordmark + tagline
- Patient ID selector pill
- [Analyze] teal button + [Framework] ghost button
- Backend online/offline status dot

**`VoiceModalityCard.jsx`**
- Animated waveform bar visualizer (teal bars, breathing animation)
- File metadata: filename, duration, sample rate
- Acoustic metric pills: Jitter %, Shimmer %, HNR, NHR, RPDE, PPE
- [Use Demo Sample] button

**`MotorModalityCard.jsx`**
- Tremor waveform chart (Recharts LineChart)
- Motor metric chips: Tremor Freq, Bradykinesia, Postural Instability
- "Accelerometer simulated" framing for demo

**`ClinicalPhenotypeCard.jsx`**
- MoCA Score input (slider 0-30)
- Age, Sex, Symptom Duration fields
- [Use Demo Patient] preset buttons (P-001 through P-004)

**`QuantumEngineCard.jsx`** (Dark card — like "Physiological Sensors" block)
- Background #0F172A with teal glow border
- 4 animated qubit state orbs (pulsing when active)
- Classical / Quantum / Hybrid score badges
- Telemetry line: ZZFeatureMap | RealAmplitudes | 4 Qubits | <10ms
- Fusion weight display: a=0.65, b=0.35

**`AgentStream.jsx`**
- Real-time SSE terminal log
- 6 stage steps with icons, status (Queued / Running / Done)
- Latency badges per stage

**`ScreeningResult.jsx`**
- Large hybrid screening signal score
- Signal category badge: ELEVATED / MODERATE / BASELINE
- All three scores side-by-side: Classical | Quantum | Hybrid
- Recommended clinical action narrative

**`ShapExplainability.jsx`**
- Horizontal Recharts bar chart
- Grouped by modality: Voice vs Motor vs Clinical
- Red = PD-associated, Green = Protective
- Feature labels with directional arrows (Jitter: up Elevated)

**`LongitudinalHistory.jsx`**
- Recharts LineChart across sequential assessments
- X-axis: visit dates / assessment numbers
- Per-visit tooltip: Classical | Quantum | Hybrid breakdown
- "No history yet" placeholder for new patients

**`ClinicalMemo.jsx`**
- Printable A4 clinical consultation memo
- Patient ID, Date, Scores, Risk Tier, ICD-10 code
- Top 4 SHAP feature drivers
- Disclaimer + pathologist signature block
- [Print / Export] with @media print CSS

**`MetricsModal.jsx`**
- Full model comparison table (all 6 models)
- ROC-AUC curve chart (Recharts AreaChart)
- Confusion matrix per model
- Evaluation methodology disclosure banner

**Tasks**:
- [x] 5.1 Initialize Vite + React 19 app with Tailwind CSS and Inter/Outfit typography
- [x] 5.2 Build Navbar with live backend status, preset patient switcher, and analysis trigger
- [x] 5.3 Build Modality Input Deck (`VoiceModalityCard.jsx`, `MotorModalityCard.jsx`, `ClinicalPhenotypeCard.jsx`)
- [x] 5.4 Build Dark-themed Quantum Circuit & State Monitor (`QuantumEngineCard.jsx`) with 4 orbital qubit angles
- [x] 5.5 Build Real-time SSE Agent Stream Visualizer (`AgentStream.jsx`) with 6 stage cards and millisecond latencies
- [x] 5.6 Build Screening Result Card (`ScreeningResult.jsx`) with dual-score comparison and clinical narrative
- [x] 5.7 Build TreeSHAP Waterfall & Cohort Importance Charts (`ShapExplainability.jsx`)
- [x] 5.8 Build Multi-visit Longitudinal Progression Chart (`LongitudinalHistory.jsx`)
- [x] 5.9 Build Printable A4 Clinical Consultation Memo (`ClinicalMemo.jsx`) with `@media print`
- [x] 5.10 Build Master Metrics & Benchmark Modal (`MetricsModal.jsx`) with ROC curves and CV disclosure
- [x] 5.11 Verify production Vite bundle build (`npm run build` completed with 0 errors)

**Exit Criterion**: All 11 UI components rendered, interactive, responsive, with successful Vite production build. [PASSED: 2415 modules transformed, 0 build errors]

---

### PHASE 6 — Data Persistence & Longitudinal History
*Goal: Enable multi-visit patient tracking*

**SQLite Schema**:
```sql
CREATE TABLE assessments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id      TEXT NOT NULL,
    assessed_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    classical_score REAL,
    quantum_score   REAL,
    hybrid_score    REAL,
    risk_tier       TEXT,
    feature_json    TEXT,
    shap_json       TEXT
);
```

**Tasks**:
- [x] 6.1 Set up SQLAlchemy with SQLite (`database/db.py`)
- [x] 6.2 Define Assessment ORM model (`database/models.py`)
- [x] 6.3 Wire `POST /api/patient/{id}/save-assessment` to DB write
- [x] 6.4 Wire `GET /api/patient/{id}/history` to DB read
- [x] 6.5 Seed demo patient histories (3+ visits per demo patient)
- [x] 6.6 `LongitudinalHistory.jsx` fetches and renders history on patient select
- [x] 6.7 Automated Validation Gate 3 Test Suite (`backend/tests/test_gate3.py` passed 5/5 audits)

**Exit Criterion**: SQLite persistence verified, demo trajectories seeded, save and retrieve API endpoints tested with 100% parity. [PASSED: 5/5 Gate 3 Audits Verified]

**V2 Upgrade Path**: PostgreSQL + patient authentication

---

### PHASE 7 — Hardening, Testing & Demo Preparation
*Goal: Zero-failure live demo for SIH evaluation*

**Tasks**:
- [x] 7.1 End-to-end test all 4 demo patient presets through full pipeline (`test_gate4_e2e.py`)
- [x] 7.2 Resilience test: verify pure NumPy fallback simulator auto-activates with zero external dependencies
- [x] 7.3 Stress test: concurrent multi-user load test (5 simultaneous screening requests with 200 OK)
- [x] 7.4 Populate `MetricsModal.jsx` with real benchmark numbers across all 4 experiments
- [x] 7.5 Build 4 authentic clinical demo presets (P-001 High, P-002 Moderate, P-003 Recovery, P-004 Control)
- [x] 7.6 Update `README.md` with complete setup, architecture, pitch scripts, and demo instructions
- [x] 7.7 Update `progress.md` with phase-by-phase completion status and master metrics
- [x] 7.8 Run full Gate 1–4 validation audit suites (24/24 individual automated audits verified)

**Exit Criterion**: Zero-failure live demo readiness, complete test suite green, documentation fully updated for SIH 2026. [PASSED: 24/24 Audits Verified across Gates 1, 2, 3, and 4]

---

## 7. Complete File/Directory Structure

```
SIH_Project2026/
|
+-- backend/
|   +-- main.py                        <- FastAPI app + all API routes
|   +-- requirements.txt
|   +-- agents/
|   |   +-- orchestrator.py            <- 6-Stage SSE pipeline
|   +-- models/
|   |   +-- classical.py               <- XGBoost train + 5-fold CV
|   |   +-- quantum.py                 <- VQC train + Qiskit
|   |   +-- fusion.py                  <- Hybrid late fusion + meta-classifier
|   |   +-- explainability.py          <- SHAP TreeExplainer
|   |   +-- fallback_sim.py            <- Pure NumPy statevector simulator
|   |   +-- xgboost_model.json
|   |   +-- scaler.joblib
|   |   +-- pca.joblib
|   |   +-- quantum_scaler.joblib
|   |   +-- vqc_params_pretrained.npy
|   |   +-- fusion_weights.json
|   |   +-- classical_metrics.json
|   |   +-- quantum_metrics.json
|   |   +-- feature_names.json
|   +-- reports/
|   |   +-- memo_gen.py                <- Clinical Memo generator
|   +-- database/
|   |   +-- db.py                      <- SQLAlchemy SQLite setup
|   |   +-- models.py                  <- Assessment ORM table
|   +-- tests/
|       +-- test_gate1.py              <- ML artifact validation tests
|       +-- test_gate2.py              <- API integration tests
|
+-- aaroh-app/                         <- React 19 + Vite 6 + Tailwind
|   +-- src/
|       +-- App.jsx
|       +-- index.css
|       +-- components/
|           +-- Navbar.jsx
|           +-- VoiceModalityCard.jsx
|           +-- MotorModalityCard.jsx
|           +-- ClinicalPhenotypeCard.jsx
|           +-- QuantumEngineCard.jsx
|           +-- AgentStream.jsx
|           +-- ScreeningResult.jsx
|           +-- ShapExplainability.jsx
|           +-- LongitudinalHistory.jsx
|           +-- ClinicalMemo.jsx
|           +-- MetricsModal.jsx
|
+-- data/
|   +-- parkinsons.csv                 <- UCI Parkinson's dataset
|
+-- idea.md
+-- plan.md                            <- This file
+-- progress.md
+-- README.md
```

---

## 8. Scientific Honesty Protocol

1. Never say "AI detected Parkinson's" — always say "Elevated Parkinson's-associated screening signal"
2. Never merge 5-fold CV and single-split metrics — label methodology explicitly on UI
3. Honestly report if hybrid does NOT improve over classical — explain why scientifically
4. Clearly distinguish clinical screening support from autonomous diagnosis
5. Every SHAP value is computed dynamically — no hardcoded arrays
6. All model weights loaded from saved artifacts — no re-training at demo time

---

## 9. Evaluator Q&A Defense Points

| Evaluator Question | Our Answer |
|:-------------------|:-----------|
| Why Parkinson's? | PD is the world's fastest-growing neurological disorder. Early detection prevents irreversible dopaminergic neuron loss. |
| Why voice features? | Voice changes (jitter, shimmer, HNR) are among the earliest measurable PD biomarkers — detectable before major motor symptoms. |
| Why hybrid? | Classical models miss non-linear quantum feature interactions. The hybrid provides complementary uncertainty quantification. |
| Why 4 qubits? | Barren plateau theorem: shallow circuits on 4 qubits avoid exponential gradient vanishing. Validated on AerSimulator. |
| What if quantum doesn't outperform? | We honestly report it. The scientific contribution is the hybrid benchmarking framework and clinical explainability pipeline. |
| How does a doctor use this? | Input voice features, see hybrid screening score, inspect SHAP attribution per biomarker, track patient trajectory over visits. |
| Is this a diagnosis tool? | No. It is a Clinical Decision Support System (CDSS). All outputs require pathologist sign-off. |

---

## 10. Technology Stack

| Layer | Technology | Version |
|:------|:-----------|:--------|
| Frontend | React + Vite + Tailwind CSS | React 19, Vite 6, Tailwind 3 |
| Backend | Python + FastAPI + Uvicorn | Python 3.12 |
| Classical ML | XGBoost + scikit-learn | XGBoost 3.4, sklearn 1.9 |
| Quantum ML | Qiskit + Qiskit Aer | Qiskit 2.5, Aer 0.17 |
| Quantum Fallback | Pure NumPy Simulator | NumPy 2.x |
| Explainability | SHAP (TreeExplainer) | shap 0.52 |
| Streaming | Server-Sent Events (SSE) | FastAPI StreamingResponse |
| Database | SQLite via SQLAlchemy | SQLAlchemy 2.x |
| Charts | Recharts | 2.x |
| Icons | Lucide React | Latest |

---

## 11. Phase Completion Checklist

| Phase | Description | Status |
|:------|:------------|:-------|
| 1 | Data Foundation & Classical ML | Completed (0.962 ROC-AUC) |
| 2 | Quantum ML Pipeline | Completed (0.697 ROC-AUC) |
| 3 | Hybrid Fusion Layer | Completed (0.997 ROC-AUC) |
| 4 | FastAPI Backend & SSE Agents | Completed (6 Stages, SQLite) |
| 5 | Frontend Dashboard | Not Started |
| 6 | Data Persistence & History | Not Started |
| 7 | Hardening, Testing & Demo Prep | Not Started |
