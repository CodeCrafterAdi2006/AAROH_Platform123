# AAROH — Hybrid Classical-Quantum Clinical Intelligence Platform

> **A deterministic multi-agent benchmarking and diagnostic intelligence platform that bridges classical machine learning (XGBoost) and a trained 4-qubit Variational Quantum Classifier (VQC) with exact TreeSHAP explainability and printable pathology consultation memos.**

---

## 📌 Executive Pitch & Core Philosophy

> *"AAROH is a hybrid clinical benchmarking platform that orchestrates classical XGBoost and a trained Variational Quantum Classifier through an agentic pipeline, producing SHAP-explainable predictions and a clinical consultation memo — with the honest result that at 569 rows, we validate quantum encoding viability, not quantum superiority."*

- **Clinical Problem**: Fine-needle aspiration (FNA) breast biopsy diagnosis on the standardized Wisconsin Breast Cancer Diagnostic (WBCD) dataset (569 patient cases, 30 nuclear morphology features).
- **Architectural Philosophy**: **100% Real Computation**. Zero hardcoded metric arrays, zero mocked latency delays, zero fabricated SHAP values. Every streamed status is mathematically anchored to an actual computed tensor.

---

## 🔬 System Architecture

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    AAROH PLATFORM                      │
                               └────────────────────────────────────────────────────────┘
                                                            │
                       ┌────────────────────────────────────┴────────────────────────────────────┐
                       ▼                                                                         ▼
      ┌─────────────────────────────────┐                                       ┌─────────────────────────────────┐
      │      REACT 19 CLINICAL UI       │                                       │     FASTAPI BACKEND ENGINE      │
      │     Port 5173 (Vite / React)    │                                       │      Port 8000 (Python 3.12)    │
      └─────────────────────────────────┘                                       └─────────────────────────────────┘
                       │                                                                         │
     • Glassmorphic Clinical Dark Theme                                         • `/api/predict/stream` (SSE)
     • Patient Preset Selector (Benign /                                        • `/api/metrics` (CV vs Split)
       Malignant / Borderline / Custom)                                         • `/api/reference-patients`
     • Real-time Agent Stream Terminal                                          • Model Registry & Lifespan Cache
     • Dual Model Gauge (XGBoost vs VQC)                                                         │
     • SHAP Interactive Force Visualizer                                        ┌────────────────┴────────────────┐
     • Printable Clinical Memo Export                                           │   DETERMINISTIC ORCHESTRATOR    │
                                                                                └────────────────┬────────────────┘
                                                                                                 │
                                                        ┌────────────────────────┬───────────────┴───────────────┬────────────────────────┐
                                                        ▼                        ▼                               ▼                        ▼
                                             [Stage 1: Ingestion]    [Stage 2: Quantum VQC]          [Stage 3: Classical ML]  [Stage 4: Explain & Memo]
                                             • 30D Biopsy Vector     • 30D ➔ 4D PCA Mapping          • XGBoost Inference      • TreeExplainer Forces
                                             • StandardScaler check  • 4-Qubit ZZFeatureMap          • Margin f(x) Calib.     • Concordance Logic
                                             • Quality Bounds Audit  • RealAmplitudes Ansatz         • 5-Fold Stratified CV   • ICD-10 Coding
                                                                     • Observable <IIIZ>             • 0.994 ROC-AUC          • Pathology Synthesis
                                                                     • NumPy Fallback Engine                                  • Printable Memo PDF
```

---

## 📊 The Honest Numbers Protocol

In healthcare machine learning, scientific integrity is paramount. AAROH explicitly discloses the evaluation asymmetry between classical and quantum algorithms:

| Dimension | Classical XGBoost Baseline | Quantum VQC Core |
| :--- | :--- | :--- |
| **Model Architecture** | Gradient Boosted Decision Trees (`XGBClassifier`) | 4-Qubit `ZZFeatureMap` (reps=1) + `RealAmplitudes` (reps=1) |
| **Evaluation Method** | **5-Fold Stratified Cross-Validation** (mean ± std) | **Held-out 80/20 Test Split** (n=114, seed=42) |
| **Sample Coverage** | Full cohort ($n=569$) | Train: $n=455$, Test: $n=114$ |
| **ROC-AUC Score** | **`0.994 ± 0.004`** | **`0.748`** |
| **Classification Accuracy** | **`96.0% ± 1.6%`** | **`68.4%`** |
| **Sensitivity (Recall)** | **`93.4% ± 3.3%`** | **`69.1%`** |
| **Specificity** | **`97.5% ± 1.3%`** | **`68.1%`** |
| **F1-Score** | **`94.6% ± 2.2%`** | **`61.7%`** |
| **Scientific Finding** | Optimal operational model for tabular diagnostic scale ($n=569$). | Validates non-linear Hilbert space encoding viability under NISQ constraints. |

---

## 🛡️ Multi-Tier Fallback Chain (Guaranteed Live Execution)

To eliminate any risk of failure during live demonstrations or evaluation:

1. **Level 0 (Primary Engine)**: Live Qiskit Aer `StatevectorEstimator` simulation executing the parameterized quantum circuit in ~8–20ms.
2. **Level 1 (Zero-Dependency Fallback)**: Pure NumPy statevector matrix simulator (`backend/models/fallback_sim.py`) executing exact unitary tensor contractions with **zero external quantum package dependencies** at **exact 0.000000e+00 delta parity** in sub-4ms.
3. **Level 2 (Classical Operational Tier)**: Full classical XGBoost decision margin + TreeSHAP feature attributions + hospital consultation memorandum.

---

## 📁 Repository Structure

```
SIH_Project2026/
├── README.md                           # Master repository documentation
├── idea.md                             # Complete idea specification, pitch scripts & Q&A defense
├── progress.md                         # Engineering roadmap, subphase tracker & changelog
├── SIH2025-IDEA-Presentation-Format.pdf# SIH presentation guidelines
│
├── backend/                            # FastAPI Python Backend Service (Port 8000)
│   ├── requirements.txt                # Frozen Python dependency matrix
│   ├── main.py                         # FastAPI app, CORS, lifespan warmup, REST & SSE endpoints
│   ├── agents/
│   │   ├── __init__.py
│   │   └── orchestrator.py             # Deterministic 4-stage SSE pipeline & validator
│   ├── models/
│   │   ├── classical.py                # 5-Fold Stratified CV trainer for XGBoost & Scaler
│   │   ├── quantum.py                  # 4-Qubit VQC (ZZFeatureMap + RealAmplitudes + COBYLA)
│   │   ├── fallback_sim.py             # Pure NumPy matrix simulator & resilient fallback router
│   │   ├── explainability.py           # Exact TreeSHAP calculator & clinical narrative generator
│   │   ├── test_gate1.py               # Validation Gate 1 test suite (ML & Quantum parity)
│   │   ├── xgboost_model.json          # Serialized production XGBoost model
│   │   ├── scaler.joblib               # Serialized 30-feature StandardScaler
│   │   ├── pca.joblib                  # Serialized 30D -> 4D PCA transformer
│   │   ├── quantum_scaler.joblib       # Serialized MinMaxScaler for [-pi, pi] angles
│   │   ├── vqc_params_pretrained.npy   # Pre-trained 8-parameter variational vector
│   │   ├── classical_metrics.json      # 5-Fold CV metrics summary
│   │   ├── quantum_metrics.json        # 80/20 test split metrics summary
│   │   ├── global_feature_importance.json # Cohort-wide TreeSHAP rankings
│   │   └── feature_names.json          # Canonical 30 WBCD feature labels
│   ├── reports/
│   │   ├── __init__.py
│   │   └── memo_gen.py                 # Structured pathology consultation memo builder & ICD-10
│   └── tests/
│       ├── __init__.py
│       └── test_gate2.py               # Validation Gate 2 test suite (FastAPI, SSE, Presets, Memo)
│
└── aaroh-app/                          # React 19 + Vite Frontend Application (Port 5173)
    ├── package.json                    # Dependencies (React 19, Lucide, Recharts, Tailwind)
    ├── vite.config.js                  # Vite configuration
    ├── tailwind.config.js              # Custom clinical & quantum theme tokens
    ├── index.html                      # HTML entrypoint
    └── src/
        ├── index.css                   # Glassmorphic dark styling & @media print rules
        ├── main.jsx                    # React root mounting
        ├── App.jsx                     # Master dashboard orchestrating state & live SSE streams
        └── components/
            ├── Header.jsx              # Status badges, connectivity indicator & modal triggers
            ├── PatientInput.jsx        # WBCD preset selector, 30D inspector & fallback toggle
            ├── AgentStream.jsx         # Real-time SSE stage timeline & computed telemetry
            ├── ModelComparison.jsx     # Side-by-side XGBoost vs VQC, circuit wire & honest notice
            ├── ShapViewer.jsx          # Bidirectional TreeSHAP horizontal force bar chart
            ├── ClinicalMemo.jsx        # Printable hospital consultation memo modal (1-click PDF)
            └── MetricsModal.jsx        # Empirical benchmark comparisons & global rankings
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** (Recommended: Python 3.12)
- **Node.js 18+** & **npm**

---

### Step 1: Backend Setup & Verification

```bash
# 1. Navigate to project root and create virtual environment
cd SIH_Project2026
python -m venv backend/.venv

# 2. Activate virtual environment
# Windows (PowerShell):
backend\.venv\Scripts\Activate.ps1
# Linux / macOS:
source backend/.venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Run automated test suites to verify ML models and API endpoints
python backend/models/test_gate1.py
python backend/tests/test_gate2.py

# 5. Launch FastAPI backend server (Port 8000)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend endpoints will be available at:
- **Health check**: `http://127.0.0.1:8000/api/health`
- **Interactive OpenAPI Docs**: `http://127.0.0.1:8000/docs`

---

### Step 2: Frontend Setup

In a new terminal window:

```bash
# 1. Navigate to frontend directory
cd aaroh-app

# 2. Install dependencies
npm install

# 3. Launch Vite development server (Port 5173)
npm run dev
```

Open your browser at **`http://localhost:5173/`** to interact with the live AAROH platform.

---

## 📡 API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service status, framework versions, and diagnostic metadata. |
| `GET` | `/api/metrics` | Dual-model evaluation comparison (5-Fold CV vs 80/20 test split). |
| `GET` | `/api/reference-patients` | Curated authentic WBCD presets (Malignant, Benign, Borderline). |
| `GET` | `/api/global-importance` | Cohort-wide TreeSHAP biomarker rankings across 569 cases. |
| `POST` | `/api/predict` | Synchronous JSON diagnostic execution returning full bundle. |
| `POST` | `/api/predict/stream` | **Server-Sent Events (SSE)** endpoint streaming live stage execution events. |

---

## 👥 Notes for Teammates & Collaborators

- **Idea & Pitch Guide**: Read [`idea.md`](idea.md) for pre-written judge responses, Q&A defense against faculty, and presentation scripts.
- **Progress Tracker**: Read [`progress.md`](progress.md) for historical milestone logs and architectural decisions.
- **Frontend Customization**: All UI components are neatly modularized under `aaroh-app/src/components/`. You can customize styles, typography, or layouts in `aaroh-app/src/index.css` and `aaroh-app/tailwind.config.js`.

---

## ⚖️ Clinical & Regulatory Disclaimer

*AAROH is an experimental hybrid clinical decision-support and quantum benchmarking platform developed for academic research and algorithmic auditability. It does not constitute a standalone medical device. All outputs must be correlated with definitive histological tissue specimens and approved by a board-certified pathologist.*
