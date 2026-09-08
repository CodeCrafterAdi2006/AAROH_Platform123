"""
AAROH Quantum Machine Learning Pipeline: Variational Quantum Classifier (VQC)
- Dataset: Wisconsin Breast Cancer Diagnostic (WBCD), n=569
- Dimensionality: 30 features -> StandardScaler -> PCA (4 components, ~80% variance) -> MinMaxScaler([0, pi])
- Encoding: 4-qubit Second-Order Pauli Expansion (ZZFeatureMap, reps=1)
- Ansatz: 4-qubit Alternating Rotations & Entanglement (RealAmplitudes, reps=1, 8 parameters)
- Observable: Pauli-Z on Qubit 0 (SparsePauliOp IIIZ)
- Optimization: COBYLA (50-60 iterations, Binary Cross-Entropy Loss)
- Evaluation: Held-out 80/20 Stratified Split (reproducible seed=42)
- Artifacts: vqc_params_pretrained.npy, quantum_metrics.json, pca.joblib, quantum_scaler.joblib
"""

import os
import time
import json
import numpy as np
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
)
from scipy.optimize import minimize

import qiskit
from qiskit.circuit.library import zz_feature_map, real_amplitudes
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

# Guard for Windows threading
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_PATH = os.path.join(MODELS_DIR, "vqc_params_pretrained.npy")
METRICS_PATH = os.path.join(MODELS_DIR, "quantum_metrics.json")
PCA_PATH = os.path.join(MODELS_DIR, "pca.joblib")
Q_SCALER_PATH = os.path.join(MODELS_DIR, "quantum_scaler.joblib")
CLASSICAL_SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")

NUM_QUBITS = 4
FEATURE_REPS = 1
ANSATZ_REPS = 1


def build_vqc_circuit():
    """
    Constructs the 4-qubit VQC composed circuit:
    ZZFeatureMap (feature encoding) + RealAmplitudes (variational ansatz).
    """
    feature_map = zz_feature_map(NUM_QUBITS, reps=FEATURE_REPS)
    ansatz = real_amplitudes(NUM_QUBITS, reps=ANSATZ_REPS)
    circuit = feature_map.compose(ansatz)
    return circuit, feature_map, ansatz


def load_and_preprocess_data(random_state=42):
    """
    Loads WBCD, applies Stratified 80/20 split, fits StandardScaler + PCA(4) + MinMaxScaler([0, pi]).
    Clinical target convention: 1 = Malignant, 0 = Benign.
    """
    raw_data = load_breast_cancer()
    X = raw_data.data
    # 0 in sklearn is malignant, 1 is benign. Convert: 1 = Malignant, 0 = Benign
    y = (raw_data.target == 0).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=random_state
    )

    # Standard scale using the classical scaler if present, else fit new
    if os.path.exists(CLASSICAL_SCALER_PATH):
        std_scaler = joblib.load(CLASSICAL_SCALER_PATH)
        X_train_scaled = std_scaler.transform(X_train)
        X_test_scaled = std_scaler.transform(X_test)
    else:
        std_scaler = StandardScaler()
        X_train_scaled = std_scaler.fit_transform(X_train)
        X_test_scaled = std_scaler.transform(X_test)
        joblib.dump(std_scaler, CLASSICAL_SCALER_PATH)

    # Fit PCA with 4 components
    pca = PCA(n_components=NUM_QUBITS, random_state=random_state)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    joblib.dump(pca, PCA_PATH)

    # MinMax scale to [0, pi] for quantum angle rotation
    q_scaler = MinMaxScaler(feature_range=(0, np.pi))
    X_train_q = q_scaler.fit_transform(X_train_pca)
    X_test_q = q_scaler.transform(X_test_pca)
    joblib.dump(q_scaler, Q_SCALER_PATH)

    var_ratio = pca.explained_variance_ratio_.tolist()
    total_var = float(np.sum(pca.explained_variance_ratio_))

    return {
        "X_train_q": X_train_q,
        "X_test_q": X_test_q,
        "y_train": y_train,
        "y_test": y_test,
        "pca_variance_ratio": var_ratio,
        "pca_total_variance": total_var,
    }


class QuantumVQC:
    """
    Variational Quantum Classifier wrapping Qiskit StatevectorEstimator.
    Evaluates Pauli-Z expectation values and provides probability predictions.
    """

    def __init__(self, weights=None):
        self.circuit, self.feature_map, self.ansatz = build_vqc_circuit()
        self.observable = SparsePauliOp.from_list([("IIIZ", 1.0)])
        self.estimator = StatevectorEstimator()
        self.weights = weights

    def evaluate_evs(self, X_q, weights=None):
        """
        Computes the expectation values <IIIZ> for a batch of quantum features.
        """
        if weights is None:
            weights = self.weights
        if weights is None:
            raise ValueError("No weights provided for VQC inference.")

        N = len(X_q)
        param_array = np.hstack([X_q, np.tile(weights, (N, 1))])
        pub = (self.circuit, self.observable, param_array)
        job = self.estimator.run([pub])
        result = job.result()
        return result[0].data.evs

    def predict_proba(self, X_q, weights=None):
        """
        Maps raw expectation value <Z> in [-1.0, 1.0] to probability P(Malignant) in [0.0, 1.0].
        """
        evs = self.evaluate_evs(X_q, weights=weights)
        # Quantum state mapping: evs in [-1, 1] -> (1 - ev)/2
        probs = (1.0 - evs) / 2.0
        return np.clip(probs, 1e-6, 1.0 - 1e-6)

    def predict(self, X_q, threshold=0.5):
        probs = self.predict_proba(X_q)
        return (probs >= threshold).astype(int)


def train_vqc(maxiter=50, random_state=42):
    """
    Executes VQC training on the WBCD training set using COBYLA optimizer.
    Logs loss descent and computes held-out test split generalization metrics.
    """
    print("=" * 65)
    print("AAROH QUANTUM ML PIPELINE: VARIATIONAL QUANTUM CLASSIFIER (VQC)")
    print("=" * 65)

    data = load_and_preprocess_data(random_state=random_state)
    X_train_q = data["X_train_q"]
    X_test_q = data["X_test_q"]
    y_train = data["y_train"]
    y_test = data["y_test"]

    print(f"Data Split: {len(y_train)} train samples, {len(y_test)} held-out test samples")
    print(f"PCA Total Variance Explained (4 components): {data['pca_total_variance']*100:.2f}%")

    vqc = QuantumVQC()
    num_params = vqc.ansatz.num_parameters
    print(f"Circuit Setup: {NUM_QUBITS} qubits, {num_params} variational parameters")
    print(f"Optimizer: COBYLA (maxiter={maxiter})")

    loss_history = []
    iter_counter = [0]

    def loss_objective(weights):
        probs = vqc.predict_proba(X_train_q, weights=weights)
        # Binary Cross-Entropy Loss
        bce = -np.mean(y_train * np.log(probs) + (1 - y_train) * np.log(1 - probs))
        iter_counter[0] += 1
        current_iter = iter_counter[0]
        loss_history.append({"iteration": current_iter, "loss": float(bce)})
        if current_iter % 10 == 0 or current_iter == 1:
            print(f"  [Iter {current_iter:02d}/{maxiter}] BCE Loss: {bce:.4f}")
        return bce

    np.random.seed(random_state)
    initial_weights = np.random.uniform(-0.5, 0.5, size=num_params)

    print("\n[Step 1/2] Initiating COBYLA Optimization...")
    start_time = time.time()
    res = minimize(
        loss_objective,
        initial_weights,
        method="COBYLA",
        options={"maxiter": maxiter, "disp": False},
    )
    train_duration = time.time() - start_time
    opt_weights = res.x
    vqc.weights = opt_weights
    print(f"  -> Optimization completed in {train_duration:.2f}s across {res.nfev} evaluations.")
    print(f"  -> Final Convergence Loss: {res.fun:.4f}")

    print("\n[Step 2/2] Evaluating on Held-Out Test Split (n=114)...")
    test_probs = vqc.predict_proba(X_test_q)
    test_preds = (test_probs >= 0.5).astype(int)

    test_auc = float(roc_auc_score(y_test, test_probs))
    test_acc = float(accuracy_score(y_test, test_preds))
    test_sens = float(recall_score(y_test, test_preds))
    test_prec = float(precision_score(y_test, test_preds))
    test_f1 = float(f1_score(y_test, test_preds))

    print(f"  -> Test ROC-AUC:     {test_auc:.4f}")
    print(f"  -> Test Accuracy:    {test_acc:.4f} ({test_acc*100:.1f}%)")
    print(f"  -> Test Sensitivity: {test_sens:.4f}")
    print(f"  -> Test Precision:   {test_prec:.4f}")
    print(f"  -> Test F1-Score:    {test_f1:.4f}")

    # Save trained parameter vector
    np.save(PARAMS_PATH, opt_weights)
    print(f"  [OK] Saved optimal parameters to {PARAMS_PATH}")

    # Construct complete metrics payload
    metrics_payload = {
        "model": "Variational Quantum Classifier (VQC)",
        "framework": f"Qiskit {qiskit.__version__} (Aer/Statevector)",
        "circuit_specification": {
            "num_qubits": NUM_QUBITS,
            "feature_map": f"ZZFeatureMap (reps={FEATURE_REPS})",
            "ansatz": f"RealAmplitudes (reps={ANSATZ_REPS})",
            "num_parameters": int(num_params),
            "observable": "Pauli-Z on Qubit 0 (IIIZ)",
            "encoding_range": "[0, pi]",
            "pca_components": 4,
            "pca_variance_explained": data["pca_total_variance"],
        },
        "training_details": {
            "optimizer": "COBYLA",
            "maxiter": maxiter,
            "total_evaluations": int(res.nfev),
            "training_duration_seconds": round(train_duration, 2),
            "final_loss": float(res.fun),
            "loss_history": loss_history,
        },
        "evaluation_protocol": {
            "method": "Single Held-Out Stratified 80/20 Split",
            "sample_size": len(y_test),
            "random_state": random_state,
            "honest_methodology_note": (
                "Evaluated on a single 80/20 test split (n=114, seed=42). "
                "Classical XGBoost is validated via 5-Fold Stratified Cross-Validation. "
                "Direct comparison carries methodology asymmetry and should be viewed directionally."
            ),
        },
        "metrics": {
            "roc_auc": round(test_auc, 4),
            "accuracy": round(test_acc, 4),
            "sensitivity": round(test_sens, 4),
            "precision": round(test_prec, 4),
            "f1": round(test_f1, 4),
        },
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"  [OK] Saved quantum metrics summary to {METRICS_PATH}")

    print("\n" + "=" * 65)
    print("VQC SUMMARY FOR PITCH & API:")
    print(f"VQC Test Metric: {test_auc:.3f} ROC-AUC (single split, 80/20, seed=42)")
    print("=" * 65)
    return metrics_payload


class QuantumInferencePipeline:
    """
    Cached, pre-loaded inference engine holding transformers and QuantumVQC instance
    in memory to avoid disk I/O and circuit rebuild on every request.
    """

    def __init__(self):
        if not os.path.exists(PARAMS_PATH):
            raise FileNotFoundError(f"VQC pre-trained parameters not found at {PARAMS_PATH}. Run training first.")
        if not os.path.exists(CLASSICAL_SCALER_PATH):
            raise FileNotFoundError(f"Classical scaler not found at {CLASSICAL_SCALER_PATH}.")
        if not os.path.exists(PCA_PATH):
            raise FileNotFoundError(f"PCA artifact not found at {PCA_PATH}.")
        if not os.path.exists(Q_SCALER_PATH):
            raise FileNotFoundError(f"Quantum scaler not found at {Q_SCALER_PATH}.")

        self.weights = np.load(PARAMS_PATH)
        self.std_scaler = joblib.load(CLASSICAL_SCALER_PATH)
        self.pca = joblib.load(PCA_PATH)
        self.q_scaler = joblib.load(Q_SCALER_PATH)
        self.vqc = QuantumVQC(weights=self.weights)

    def predict(self, raw_features_30):
        t0 = time.perf_counter()

        x_arr = np.array(raw_features_30, dtype=float).reshape(1, -1)
        x_scaled = self.std_scaler.transform(x_arr)
        x_pca = self.pca.transform(x_scaled)
        x_q = self.q_scaler.transform(x_pca)

        ev = float(self.vqc.evaluate_evs(x_q)[0])
        prob = float(np.clip((1.0 - ev) / 2.0, 1e-6, 1.0 - 1e-6))

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "vqc_probability": round(prob, 4),
            "vqc_prediction": 1 if prob >= 0.5 else 0,
            "expectation_value": round(ev, 4),
            "execution_time_ms": round(elapsed_ms, 2),
            "pca_features": [round(float(v), 4) for v in x_pca[0]],
            "quantum_angles_rad": [round(float(v), 4) for v in x_q[0]],
        }


# Module-level singleton cache
_cached_quantum_pipeline = None


def get_quantum_inference_pipeline():
    """Returns the cached QuantumInferencePipeline instance, initializing it lazily on first call."""
    global _cached_quantum_pipeline
    if _cached_quantum_pipeline is None:
        _cached_quantum_pipeline = QuantumInferencePipeline()
    return _cached_quantum_pipeline


def predict_single_patient(raw_features_30):
    """
    End-to-end inference for a single patient vector (30 features):
    1. StandardScaler normalization (cached in memory)
    2. PCA projection to 4 components (cached in memory)
    3. MinMaxScaler to [0, pi] (cached in memory)
    4. VQC forward pass using pre-warmed circuit and pre-trained weights
    Returns: dict with probability, raw expectation value, and execution duration ms.
    """
    pipeline = get_quantum_inference_pipeline()
    return pipeline.predict(raw_features_30)


if __name__ == "__main__":
    train_vqc(maxiter=50, random_state=42)
