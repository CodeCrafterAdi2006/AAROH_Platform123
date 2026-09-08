"""
AAROH Environment & Quantum Sanity Check
Tests:
1. Python version and core math (numpy)
2. Qiskit import, circuit building, and Qiskit-Aer simulation
3. Classical ML imports (XGBoost, scikit-learn, shap)
"""
import os
import sys
import time

# Guard for Windows OpenBLAS threading
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

def run_checks():
    print("=" * 60)
    print("AAROH ENVIRONMENT SANITY CHECK")
    print("=" * 60)
    print(f"Python Version: {sys.version}")

    # 1. Classical ML Stack Check
    print("\n[1/3] Testing Classical ML Stack...")
    try:
        import numpy as np
        import pandas as pd
        import sklearn
        import xgboost
        import shap
        print(f"  [OK] NumPy: {np.__version__}")
        print(f"  [OK] Pandas: {pd.__version__}")
        print(f"  [OK] Scikit-Learn: {sklearn.__version__}")
        print(f"  [OK] XGBoost: {xgboost.__version__}")
        print(f"  [OK] SHAP: {shap.__version__}")
    except Exception as e:
        print(f"  [FAIL] Classical ML check failed: {e}")
        return False

    # 2. Web & API Framework Check
    print("\n[2/3] Testing API Framework...")
    try:
        import fastapi
        import uvicorn
        print(f"  [OK] FastAPI: {fastapi.__version__}")
        print(f"  [OK] Uvicorn: {uvicorn.__version__}")
    except Exception as e:
        print(f"  [FAIL] API check failed: {e}")
        return False

    # 3. Quantum Simulation Check (Qiskit + Aer)
    print("\n[3/3] Testing Quantum Simulator (Qiskit + Aer)...")
    t0 = time.time()
    try:
        import qiskit
        print(f"  [OK] Qiskit Core: {qiskit.__version__}")
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator

        # Create 2-qubit Bell State: |psi> = (|00> + |11>) / sqrt(2)
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()

        simulator = AerSimulator()
        job = simulator.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts()
        elapsed = time.time() - t0

        print(f"  [OK] AerSimulator execution successful in {elapsed:.3f}s")
        print(f"  [OK] Measurement Counts (1000 shots): {counts}")
        
        # Verify valid Bell state outcomes (dominated by '00' and '11')
        p00 = counts.get('00', 0) / 1000
        p11 = counts.get('11', 0) / 1000
        assert p00 > 0.4 and p11 > 0.4, f"Unexpected counts distribution: {counts}"
        print(f"  [OK] Bell state entanglement verified (P(00)={p00:.3f}, P(11)={p11:.3f})")
    except Exception as e:
        print(f"  [FAIL] Qiskit execution failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("ALL CHECKS PASSED: Environment is verified and ready for AAROH.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
