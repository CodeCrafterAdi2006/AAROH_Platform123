"""
AAROH Classical ML Pipeline: XGBoost on UCI Parkinson's Voice Dataset
- Dataset: UCI Parkinson's Telemonitoring / Acoustic Biomarker Dataset (195 recordings, 22 features)
- 5-Fold Stratified Cross-Validation (reproducible seed=42)
- Trains final deployed model
- Saves model, scaler, feature metadata, and cross-validation metrics
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
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
PROJECT_ROOT = os.path.abspath(os.path.join(MODELS_DIR, "..", ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "parkinsons.csv")

METRICS_PATH = os.path.join(MODELS_DIR, "classical_metrics.json")
MODEL_PATH = os.path.join(MODELS_DIR, "xgboost_model.json")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, "feature_names.json")


def load_parkinsons_data(csv_path=DATA_PATH):
    """
    Loads UCI Parkinson's dataset from CSV.
    Features: 22 biomedical voice measurements (MDVP, Jitter, Shimmer, HNR, RPDE, DFA, PPE, etc.)
    Target: status (1 = Parkinson's, 0 = Healthy)
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Parkinson's dataset not found at {csv_path}. Please download it first.")

    df = pd.read_csv(csv_path)
    feature_cols = [c for c in df.columns if c not in ["name", "status"]]
    
    X = df[feature_cols].values.astype(np.float64)
    y = df["status"].values.astype(int)
    subject_ids = df["name"].apply(lambda x: x.rsplit("_", 1)[0]).values
    
    return X, y, feature_cols, subject_ids


def evaluate_baselines(X, y, groups=None, random_state=42):
    """
    Evaluates baseline classical models (Logistic Regression, SVM, Random Forest, XGBoost)
    using 5-Fold Stratified Cross-Validation.
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    
    model_defs = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=random_state),
        "SVM (RBF)": SVC(probability=True, kernel="rbf", C=1.0, random_state=random_state),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=4, random_state=random_state),
        "XGBoost": xgb.XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=random_state,
        ),
    }

    baseline_results = {}

    for model_name, clf in model_defs.items():
        fold_metrics = {"roc_auc": [], "accuracy": [], "sensitivity": [], "specificity": [], "precision": [], "f1": []}

        for fold_idx, (train_idx, val_idx) in enumerate(skf.split(X, y)):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_val_scaled = scaler.transform(X_val)

            clf.fit(X_train_scaled, y_train)
            y_prob = clf.predict_proba(X_val_scaled)[:, 1]
            y_pred = (y_prob >= 0.5).astype(int)

            fold_metrics["roc_auc"].append(roc_auc_score(y_val, y_prob))
            fold_metrics["accuracy"].append(accuracy_score(y_val, y_pred))
            fold_metrics["sensitivity"].append(recall_score(y_val, y_pred, zero_division=0))
            fold_metrics["specificity"].append(recall_score(y_val == 0, y_pred == 0, zero_division=0))
            fold_metrics["precision"].append(precision_score(y_val, y_pred, zero_division=0))
            fold_metrics["f1"].append(f1_score(y_val, y_pred, zero_division=0))

        baseline_results[model_name] = {
            "roc_auc": {"mean": float(np.mean(fold_metrics["roc_auc"])), "std": float(np.std(fold_metrics["roc_auc"]))},
            "accuracy": {"mean": float(np.mean(fold_metrics["accuracy"])), "std": float(np.std(fold_metrics["accuracy"]))},
            "sensitivity": {"mean": float(np.mean(fold_metrics["sensitivity"])), "std": float(np.std(fold_metrics["sensitivity"]))},
            "specificity": {"mean": float(np.mean(fold_metrics["specificity"])), "std": float(np.std(fold_metrics["specificity"]))},
            "precision": {"mean": float(np.mean(fold_metrics["precision"])), "std": float(np.std(fold_metrics["precision"]))},
            "f1": {"mean": float(np.mean(fold_metrics["f1"])), "std": float(np.std(fold_metrics["f1"]))},
        }

    return baseline_results


def evaluate_5fold_cv(X, y, random_state=42):
    """
    Performs 5-Fold Stratified Cross-Validation on the primary XGBoost model.
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    fold_metrics = {
        "roc_auc": [],
        "accuracy": [],
        "sensitivity": [],
        "specificity": [],
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
        fold_metrics["sensitivity"].append(recall_score(y_val, y_pred, zero_division=0))
        fold_metrics["specificity"].append(recall_score(y_val == 0, y_pred == 0, zero_division=0))
        fold_metrics["precision"].append(precision_score(y_val, y_pred, zero_division=0))
        fold_metrics["f1"].append(f1_score(y_val, y_pred, zero_division=0))

    summary = {
        "validation_method": "5-Fold Stratified Cross-Validation",
        "dataset": "UCI Parkinson's Voice Telemonitoring Dataset",
        "sample_size": len(y),
        "feature_count": X.shape[1],
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
            "specificity": {
                "mean": float(np.mean(fold_metrics["specificity"])),
                "std": float(np.std(fold_metrics["specificity"])),
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
    Fits StandardScaler and XGBoost model on full dataset for inference.
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
    with open(FEATURE_NAMES_PATH, "w") as f:
        json.dump(feature_names, f, indent=2)

    return model, scaler


def run_pipeline():
    print("=" * 65)
    print("AAROH CLASSICAL ML PIPELINE: PARKINSON'S DISEASE (XGBoost)")
    print("=" * 65)

    X, y, feature_names, subject_ids = load_parkinsons_data()
    n_pd = int(np.sum(y == 1))
    n_healthy = int(np.sum(y == 0))
    n_subjects = len(np.unique(subject_ids))
    print(f"Dataset Loaded: {len(y)} recordings from {n_subjects} subjects, {X.shape[1]} acoustic features")
    print(f"Class Distribution: {n_pd} Parkinson's (1), {n_healthy} Healthy Controls (0)")

    print("\n[Step 1/3] Benchmarking Baseline Classical Models (5-Fold Stratified CV)...")
    baselines = evaluate_baselines(X, y, groups=subject_ids, random_state=42)
    for model_name, m in baselines.items():
        print(f"  {model_name:<20} | AUC: {m['roc_auc']['mean']:.4f} +/- {m['roc_auc']['std']:.4f} | Acc: {m['accuracy']['mean']:.4f} | Sens: {m['sensitivity']['mean']:.4f} | Spec: {m['specificity']['mean']:.4f} | F1: {m['f1']['mean']:.4f}")

    print("\n[Step 2/3] Running Primary 5-Fold Stratified Cross-Validation on XGBoost...")
    cv_results = evaluate_5fold_cv(X, y, random_state=42)
    cv_results["baselines"] = baselines

    auc_mean = cv_results["metrics"]["roc_auc"]["mean"]
    auc_std = cv_results["metrics"]["roc_auc"]["std"]
    acc_mean = cv_results["metrics"]["accuracy"]["mean"]
    acc_std = cv_results["metrics"]["accuracy"]["std"]
    sens_mean = cv_results["metrics"]["sensitivity"]["mean"]
    sens_std = cv_results["metrics"]["sensitivity"]["std"]
    spec_mean = cv_results["metrics"]["specificity"]["mean"]
    spec_std = cv_results["metrics"]["specificity"]["std"]

    print(f"  -> ROC-AUC:      {auc_mean:.4f} +/- {auc_std:.4f}")
    print(f"  -> Accuracy:     {acc_mean:.4f} +/- {acc_std:.4f}")
    print(f"  -> Sensitivity:  {sens_mean:.4f} +/- {sens_std:.4f}")
    print(f"  -> Specificity:  {spec_mean:.4f} +/- {spec_std:.4f}")

    # Write metrics to JSON
    with open(METRICS_PATH, "w") as f:
        json.dump(cv_results, f, indent=2)
    print(f"  [OK] Saved CV & baseline metrics to {METRICS_PATH}")

    print("\n[Step 3/3] Training Production XGBoost Model on Full Dataset...")
    train_and_save_production_model(X, y, feature_names, random_state=42)
    print(f"  [OK] Saved XGBoost model to {MODEL_PATH}")
    print(f"  [OK] Saved StandardScaler to {SCALER_PATH}")
    print(f"  [OK] Saved feature names ({len(feature_names)}) to {FEATURE_NAMES_PATH}")

    print("\n" + "=" * 65)
    print("SUMMARY FOR EVALUATION & API:")
    print(f"XGBoost Primary: {auc_mean:.3f} +/- {auc_std:.3f} ROC-AUC (5-Fold Stratified CV, n={len(y)}, seed=42)")
    print("=" * 65)
    return cv_results


if __name__ == "__main__":
    run_pipeline()
