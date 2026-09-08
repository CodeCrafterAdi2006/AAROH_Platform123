# AAROH — Master Idea & Engineering Specification
*Hybrid Clinical Intelligence Platform — Classical XGBoost & Variational Quantum Classifier (VQC) with Deterministic Agentic Orchestration and SHAP Explainability.*

---

## 1. Executive Summary & Pitch Baseline

**AAROH** is a hybrid clinical benchmarking and diagnostic intelligence platform that bridges classical machine learning (XGBoost) and quantum machine learning (Variational Quantum Classifier / VQC) with an agentic narration layer and SHAP-based clinical explainability.

Designed for breast cancer fine-needle aspiration (FNA) biopsy evaluation on the standardized Wisconsin Breast Cancer Diagnostic (WBCD) dataset (569 samples, 30 morphological features), AAROH processes high-dimensional clinical data, maps key PCA biomarker components into a 4-qubit quantum Hilbert space, computes exact SHAP feature attributions, and synthesizes a structured clinical consultation memo in real time via Server-Sent Events (SSE).

### The Evaluation Pitch
> *"AAROH is a hybrid clinical benchmarking platform that orchestrates classical XGBoost and a trained Variational Quantum Classifier through an agentic pipeline, producing SHAP-explainable predictions and a clinical consultation memo — with the honest result that at 569 rows, we validate quantum encoding viability, not quantum superiority."*

### Core Philosophy & Auditability
- **Real Computation**: Zero hardcoded arrays, zero mocked latency delays, zero fabricated SHAP values.
- **Traceable Agentic Narration**: 4-stage deterministic pipeline where every streamed status line is anchored to an actual computed tensor or metric.
- **Transparent Benchmarking**: Explicitly disclosing evaluation methodology (5-Fold Stratified CV on classical vs. held-out test split on quantum).

---

## 2. System Architecture & Proven Reference Foundations

AAROH leverages battle-tested, standard reference architectures across all tiers to ensure maximum reliability and speed of delivery:

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    AAROH PLATFORM                      │
                               └────────────────────────────────────────────────────────┘
                                                           │
                      ┌────────────────────────────────────┴────────────────────────────────────┐
                      ▼                                                                         ▼
     ┌─────────────────────────────────┐                                       ┌─────────────────────────────────┐
     │      REACT 18 CLINICAL UI       │                                       │     FASTAPI BACKEND ENGINE      │
     │     Port 5173 (Vite / React)    │                                       │      Port 8000 (Python 3.12)    │
     └─────────────────────────────────┘                                       └─────────────────────────────────┘
                      │                                                                         │
    • Glassmorphic Clinical Dark Theme                                         • `/api/predict/stream` (SSE)
    • Patient Preset Selector (Benign /                                        • `/api/metrics` (CV vs Split)
      Malignant / Borderline / Custom)                                         • `/api/explain` (SHAP Forces)
    • Real-time Agent Stream Terminal                                          • Model Registry & Cache
    • Dual Model Gauge (XGBoost vs VQC)                                                         │
    • SHAP Interactive Waterfall Chart                                         ┌────────────────┴────────────────┐
    • Printable Clinical Memo Export                                           │   DETERMINISTIC ORCHESTRATOR    │
                                                                               └────────────────┬────────────────┘
                                                                                                │
                                                       ┌────────────────────────┬───────────────┴───────────────┬────────────────────────┐
                                                       ▼                        ▼                               ▼                        ▼
                                            [Stage 1: Ingestion]    [Stage 2: Classical ML]          [Stage 3: Quantum VQC]   [Stage 4: Explain & Memo]
                                            • WBCD loader           • XGBoost Classifier             • 4-Qubit ZZFeatureMap   • TreeExplainer SHAP
                                            • StandardScaler        • 5-Fold Stratified CV           • RealAmplitudes Ansatz  • Consensus Logic
                                            • PCA 4-comp mapping    • Prob: 0.994 ROC-AUC            • COBYLA Optimization    • Clinical Memo Builder
                                                                                                     • NumPy Replay Fallback
```

### Component Reference Matrix

| Subsystem | Architecture / Foundation | Open-Source Reference | Implementation Details |
| :--- | :--- | :--- | :--- |
| **Quantum Core** | Variational Quantum Classifier (VQC) | Qiskit Machine Learning (`qiskit-aer`) | 4-qubit `ZZFeatureMap` (2 reps) + `RealAmplitudes` ansatz + COBYLA optimizer + Parity/Z measurement. |
| **Quantum Fallback** | Pure NumPy Unitary Simulator | Matrix Statevector Replay | Parameter vector loader (`vqc_params_pretrained.npy`) running exact matrix multiplication without Qiskit runtime overhead. |
| **Classical Engine** | Gradient Boosted Decision Trees | `xgboost.XGBClassifier` + `scikit-learn` | 5-Fold Stratified Cross-Validation on 569 samples with StandardScaler normalization. |
| **Explainability** | Additive Feature Attribution | `shap.TreeExplainer` | Per-patient SHAP values and base values for top 10 nuclear morphometry features. |
| **Orchestrator** | Asynchronous Event Streaming | FastAPI `StreamingResponse` / SSE | Deterministic 4-stage event loop emitting structured JSON events (`stage_start`, `classical_done`, `quantum_done`, `memo_ready`). |
| **Frontend UI** | High-Density Medical Dashboard | React 18 + Lucide + Tailwind/Vanilla CSS | Dark clinical theme, real-time event log, interactive patient sliders, SHAP force waterfall, and PDF/Print clinical report. |

---

## 3. The Honest Numbers Protocol

### 1. Classical XGBoost Validation (Baseline Established)
- **Method**: 5-Fold Stratified Cross-Validation on WBCD (n=569, `random_state=42`).
- **Empirical Results**:
  - **ROC-AUC**: `0.994 ± 0.004`
  - **Accuracy**: `96.0% ± 1.6%`
  - **Sensitivity (Recall)**: `93.4% ± 3.3%`
  - **Specificity**: `97.5% ± 1.3%`
- **Serving Model**: Deployed model trained on full 569 samples after CV validation to maximize diagnostic feature coverage.

### 2. Quantum VQC Validation
- **Method**: Held-out 80/20 Stratified Split (`random_state=42`, n_train=455, n_test=114).
- **Reported Metric**: `0.748 ROC-AUC (single split, 80/20, seed=42)`.
  - **Empirical Results**: `Accuracy: 68.4%`, `Sensitivity: 69.1%`, `Precision: 55.8%`, `F1-Score: 61.7%`.
- **Honest Framing**: Never falsely claim direct equivalence between a single 80/20 split and 5-fold CV. Label the methodology prominently on the UI.

### 3. The 3 Pre-Written Pitch Responses (Locked)

* **Scenario A (VQC achieves comparable/higher test ROC-AUC):**
  > *"Our trained VQC achieves strong classification accuracy on our held-out test split, demonstrating that non-linear quantum Hilbert space mapping preserves high feature fidelity. Note that classical XGBoost is validated via 5-fold CV while VQC is on a single test split — so we treat this as directional evidence of quantum encoding viability at small data scale."*

* **Scenario B (VQC is within ±0.03 of XGBoost):**
  > *"Both models achieve comparable diagnostic competence. Quantum encoding effectively preserves clinical feature separation without loss of discriminative power, validating the hybrid orchestration architecture for future scalable NISQ processors."*

* **Scenario C (VQC underperforms XGBoost):**
  > *"The VQC underperforms XGBoost on this data scale — which is completely aligned with established NISQ limitations on tabular data. Classical XGBoost is the operational winner at 569 rows. Our core technical innovation is the hybrid dual-engine pipeline, SHAP interpretability, and the deterministic benchmarking framework itself."*

---

## 4. Multi-Tier Fallback Chain (Guaranteed Live Execution)

To guarantee 100% zero-fail reliability during live faculty evaluation:

```
[Level 0: Full Qiskit Aer]
  │   Live simulator execution via qiskit-aer.
  ▼ (If execution time > 3.0s or library issue)
[Level 1: Pre-trained NumPy Matrix Simulator]
  │   Loads vqc_params_pretrained.npy, computes statevector via pure NumPy.
  ▼ (If quantum tensor execution fails)
[Level 2: Classical Tier & Hybrid Benchmarking Note]
      Full XGBoost inference + SHAP explanation + honest clinical fallback notice.
```

---

## 5. College Evaluation Q&A Defense

| Question from Faculty / Judge | Precise Technical Defense |
| :--- | :--- |
| **"Why use Quantum ML when XGBoost already gets 99% ROC-AUC?"** | *"In tabular diagnostic data at 569 samples, classical ML is mathematically optimal. AAROH is not claiming quantum supremacy today; it is a benchmarking and orchestration platform designed to validate quantum feature encoding viability and provide full clinical explainability as quantum hardware matures."* |
| **"How are quantum states represented and measured?"** | *"Features are mapped to 4 qubits using a second-order Pauli expansion (`ZZFeatureMap`), parameterized by two repetitions of a `RealAmplitudes` alternating rotation and entanglement layer, and measured via Z-basis expectation values."* |
| **"What makes your pipeline 'Agentic' rather than a standard script?"** | *"AAROH implements deterministic, auditable pipeline stages with real-time SSE telemetry. In healthcare AI, non-deterministic LLM autonomy is a regulatory liability; deterministic agent narration provides 100% auditability with live step-by-step clinical justification."* |
| **"How does the clinician interpret the output?"** | *"Via exact SHAP TreeExplainer attributions showing exactly how much each nuclear morphological feature (concavity, radius, texture) pushed the risk score toward Malignant or Benign, backed by a printable clinical consultation memo."* |
