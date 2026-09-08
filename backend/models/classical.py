"""
AAROH Classical ML Pipeline: XGBoost on Wisconsin Breast Cancer Diagnostic (WBCD)
- 5-Fold Stratified Cross-Validation (reproducible seed=42)
- Trains final deployed model
- Saves model, scaler, feature metadata, and cross-validation metrics
"""
import os
import json
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
import xgboost as xgb
import joblib

# Guard for Windows threading
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(MODELS_DIR, "classical_metrics.json")
MODEL_PATH = os.path.join(MODELS_DIR, "xgboost_model.json")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")


def load_wbcd_data():
    """
    Loads WBCD dataset.
    Note on labels: sklearn assigns 0 = Malignant, 1 = Benign.
    We convert this to standard clinical convention:
    1 = Malignant (positive class), 0 = Benign (negative class).
    """
    raw_data = load_breast_cancer()
    feature_names = list(raw_data.feature_names)
    X = raw_data.data
    # 0 in sklearn is malignant, 1 is benign. Convert: 1 = Malignant, 0 = Benign
    y = (raw_data.target == 0).astype(int)
    return X, y, feature_names


def evaluate_5fold_cv(X, y, random_state=42):
    """
    Performs rigorous 5-fold Stratified Cross-Validation to evaluate generalization.
    Returns mean and std for all key clinical metrics.
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    fold_metrics = {
        "roc_auc": [],
        "accuracy": [],
        "sensitivity": [],  # Recall for malignant class
        "precision": [],
        "f1": [],
    }

    for fold_idx, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)

        clf = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=random_state + fold_idx,
        )
        clf.fit(X_train_scaled, y_train)

        y_prob = clf.predict_proba(X_val_scaled)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)

        fold_metrics["roc_auc"].append(roc_auc_score(y_val, y_prob))
        fold_metrics["accuracy"].append(accuracy_score(y_val, y_pred))
        fold_metrics["sensitivity"].append(recall_score(y_val, y_pred))
        fold_metrics["precision"].append(precision_score(y_val, y_pred))
        fold_metrics["f1"].append(f1_score(y_val, y_pred))

    summary = {
        "validation_method": "5-Fold Stratified Cross-Validation",
        "sample_size": len(y),
        "random_state": random_state,
        "metrics": {
            "roc_auc": {
                "mean": float(np.mean(fold_metrics["roc_auc"])),
                "std": float(np.std(fold_metrics["roc_auc"])),
                "folds": [float(v) for v in fold_metrics["roc_auc"]],
            },
            "accuracy": {
                "mean": float(np.mean(fold_metrics["accuracy"])),
                "std": float(np.std(fold_metrics["accuracy"])),
            },
            "sensitivity": {
                "mean": float(np.mean(fold_metrics["sensitivity"])),
                "std": float(np.std(fold_metrics["sensitivity"])),
            },
            "precision": {
                "mean": float(np.mean(fold_metrics["precision"])),
                "std": float(np.std(fold_metrics["precision"])),
            },
            "f1": {
                "mean": float(np.mean(fold_metrics["f1"])),
                "std": float(np.std(fold_metrics["f1"])),
            },
        },
    }
    return summary


def train_and_save_production_model(X, y, feature_names, random_state=42):
    """
    Fits scaler and XGBoost model on full dataset for maximum inference quality.
    Saves artifacts for the API server.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=random_state,
    )
    model.fit(X_scaled, y)

    # Save scaler and XGBoost model
    joblib.dump(scaler, SCALER_PATH)
    model.save_model(MODEL_PATH)

    # Save feature names list
    feature_meta_path = os.path.join(MODELS_DIR, "feature_names.json")
    with open(feature_meta_path, "w") as f:
        json.dump(feature_names, f, indent=2)

    return model, scaler


def run_pipeline():
    print("=" * 65)
    print("AAROH CLASSICAL ML PIPELINE (XGBoost + 5-Fold Stratified CV)")
    print("=" * 65)

    X, y, feature_names = load_wbcd_data()
    n_malignant = int(np.sum(y == 1))
    n_benign = int(np.sum(y == 0))
    print(f"Dataset Loaded: {len(y)} samples, {X.shape[1]} features")
    print(f"Class Distribution: {n_malignant} Malignant (1), {n_benign} Benign (0)")

    print("\n[Step 1/2] Running 5-Fold Stratified Cross-Validation...")
    cv_results = evaluate_5fold_cv(X, y, random_state=42)

    auc_mean = cv_results["metrics"]["roc_auc"]["mean"]
    auc_std = cv_results["metrics"]["roc_auc"]["std"]
    acc_mean = cv_results["metrics"]["accuracy"]["mean"]
    acc_std = cv_results["metrics"]["accuracy"]["std"]
    sens_mean = cv_results["metrics"]["sensitivity"]["mean"]
    sens_std = cv_results["metrics"]["sensitivity"]["std"]

    print(f"  -> ROC-AUC:      {auc_mean:.4f} +/- {auc_std:.4f}")
    print(f"  -> Accuracy:     {acc_mean:.4f} +/- {acc_std:.4f}")
    print(f"  -> Sensitivity:  {sens_mean:.4f} +/- {sens_std:.4f}")

    # Write metrics to JSON
    with open(METRICS_PATH, "w") as f:
        json.dump(cv_results, f, indent=2)
    print(f"  [OK] Saved CV metrics to {METRICS_PATH}")

    print("\n[Step 2/2] Training Deployed Production Model on Full Dataset...")
    train_and_save_production_model(X, y, feature_names, random_state=42)
    print(f"  [OK] Saved XGBoost model to {MODEL_PATH}")
    print(f"  [OK] Saved StandardScaler to {SCALER_PATH}")

    print("\n" + "=" * 65)
    print(f"SUMMARY FOR PITCH / API:")
    print(f"XGBoost Baseline: {auc_mean:.3f} +/- {auc_std:.3f} ROC-AUC (5-fold CV, n=569, seed=42)")
    print("=" * 65)
    return cv_results


if __name__ == "__main__":
    run_pipeline()
