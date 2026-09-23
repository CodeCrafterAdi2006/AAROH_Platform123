# AAROH — Plain-English Glossary & Judge Defense Cheat Sheet

> **Simple, non-technical definitions, 1-line layman analogies, and quick verbal answers for every medical, AI, quantum, and software term used in the AAROH platform.**

---

## 📑 Quick Navigation
1. [Medical & Voice Acoustic Terms](#1-medical--voice-acoustic-biomarkers)
2. [AI, Machine Learning & Explainability Terms](#2-ai-machine-learning--explainability)
3. [Quantum Computing Terms](#3-quantum-computing-terms)
4. [Software & Engineering Terms](#4-software--web-architecture-terms)
5. [Rapid 1-Line "Layman Analogies" (Memorize for Judges)](#5-rapid-1-line-layman-analogies-memorize-for-judges)

---

## 1. Medical & Voice Acoustic Biomarkers

### 1. **Dysphonia / Phonation**
- **Meaning**: Phonation is the physical production of sound by vocal cords. Dysphonia means a voice disorder or abnormal vocal sound.
- **Layman Analogy**: Like a guitar string that is vibrating erratically instead of producing a clean note.

### 2. **Jitter (Frequency Perturbation)**
- **Meaning**: The micro-fluctuation in pitch (vocal frequency) from one vibration cycle to the next.
- **Layman Analogy**: Imagine singing a steady note, but your pitch wavers slightly up and down every millisecond because your vocal muscles are trembling.

### 3. **Shimmer (Amplitude Perturbation)**
- **Meaning**: The micro-fluctuation in loudness (vocal volume) from one vibration cycle to the next.
- **Layman Analogy**: Like a lightbulb whose brightness flickers subtly because the power flow is unstable.

### 4. **HNR (Harmonics-to-Noise Ratio)**
- **Meaning**: The ratio between the clear musical sound (harmonics) and unwanted breathy/raspy air noise.
- **Layman Analogy**: Tuning a radio into a clean song station (high HNR) versus hearing static hiss over the music (low HNR).

### 5. **PPE (Pitch Period Entropy)**
- **Meaning**: A measure of how irregularly and chaotically the pitch jumps during steady speech.
- **Layman Analogy**: Like a car engine running with irregular stuttering rather than a smooth, predictable hum.

### 6. **RPDE (Recurrence Period Density Entropy)**
- **Meaning**: Measures whether vocal vibration patterns repeat in an orderly or disordered cycle over time.

### 7. **MoCA Score (Montreal Cognitive Assessment)**
- **Meaning**: A standard 30-point clinical quiz used by doctors to measure memory and cognitive alertness (26–30 is normal).

### 8. **MDS-UPDRS**
- **Meaning**: The gold-standard rating scale used by neurologists worldwide to grade Parkinson's motor severity (tremor, stiffness, walking).

### 9. **ICD-10 Code (`G20`, `R47.81`)**
- **Meaning**: The official global hospital billing and diagnosis code standard. `G20` means Parkinson's Disease; `R47.81` means vocal speech disturbance.

---

## 2. AI, Machine Learning & Explainability

### 1. **XGBoost (Extreme Gradient Boosting)**
- **Meaning**: An advanced AI algorithm made of hundreds of small "decision trees" that vote together to make an accurate diagnosis.
- **Layman Analogy**: Like asking a council of 100 experienced doctors who each look at a different clue, then averaging their expert opinions.

### 2. **5-Fold Stratified Cross-Validation**
- **Meaning**: Testing the AI 5 separate times on 5 different slices of data to prove it didn't just "memorize" the answers.
- **Layman Analogy**: Giving a student 5 completely different exam papers to guarantee they actually understand the subject.

### 3. **TreeSHAP (Explainable AI)**
- **Meaning**: A mathematical tool that breaks down the final AI score and tells the doctor exactly which biomarker caused what percentage of the risk.
- **Layman Analogy**: Like an itemized grocery receipt showing exactly how many rupees each item added to the total bill.

### 4. **Additive Invariant ($\sum \phi_i + \phi_0 = f(x)$)**
- **Meaning**: Mathematical proof that the SHAP explanation adds up 100% perfectly with zero missing or fabricated numbers.

### 5. **Late Fusion**
- **Meaning**: Running two separate AI models (Classical + Quantum) and combining their final probabilities using tuned weights ($\alpha=0.31, \beta=0.69$).
- **Layman Analogy**: Getting a second opinion from another specialist doctor, then weighting both opinions together.

### 6. **Discordance Gate ($|P_c - P_q| \ge 0.30$)**
- **Meaning**: An automated safety alarm that triggers if the classical model and quantum model strongly disagree on a borderline case.
- **Layman Analogy**: If two doctors give contradictory diagnoses, the system stops and orders a human specialist to review it manually.

### 7. **ROC-AUC Score**
- **Meaning**: A score from 0.0 to 1.0 measuring how well the AI distinguishes between sick patients and healthy people (1.0 is a perfect score; our XGBoost achieves **0.9622**).

### 8. **Sensitivity vs Specificity**
- **Sensitivity (Recall)**: Ability to correctly catch sick patients (avoiding false negatives).
- **Specificity**: Ability to correctly identify healthy people (avoiding false alarms).

---

## 3. Quantum Computing Terms

### 1. **Qubit**
- **Meaning**: The quantum equivalent of a standard computer bit. While a normal bit is strictly 0 or 1, a qubit can exist in a superposition of both simultaneously.

### 2. **Hilbert Space**
- **Meaning**: The vast multi-dimensional mathematical realm where quantum states live ($2^4 = 16$ dimensions for 4 qubits).
- **Layman Analogy**: Looking at a flat 2D shadow vs looking at the full 3D object in space. High dimensions make hidden patterns easy to separate.

### 3. **ZZFeatureMap (Quantum Embedding)**
- **Meaning**: The quantum circuit that encodes human voice numbers into rotation angles and entangles qubits together.
- **Layman Analogy**: Translating English text into musical notes so that complex harmonies can be analyzed.

### 4. **RealAmplitudes (Ansatz)**
- **Meaning**: The customizable quantum circuit whose knob angles ($\theta$) are adjusted during training to learn the boundary between sick and healthy voice patterns.

### 5. **Expectation Value ($\langle \text{IIIZ} \rangle$)**
- **Meaning**: The final measurement readout from the quantum circuit, which we convert into a probability percentage from 0% to 100%.

### 6. **COBYLA Optimizer**
- **Meaning**: A classical optimization algorithm that tunes the quantum circuit's rotation parameters step-by-step.

### 7. **NumPy Statevector Fallback Simulator**
- **Meaning**: A lightweight built-in simulator that replicates the exact quantum circuit using pure basic math in 0.2 milliseconds, ensuring the website never crashes even without quantum hardware.

---

## 4. Software & Web Architecture Terms

### 1. **CDSS (Clinical Decision-Support System)**
- **Meaning**: Software designed to assist and advise human doctors, not replace them.

### 2. **FastAPI**
- **Meaning**: A high-speed, modern Python framework used to build our backend calculation engine.

### 3. **Server-Sent Events (SSE)**
- **Meaning**: A web technology that lets the backend push step-by-step calculation progress to the doctor's browser in real-time without reloading the page.

### 4. **Longitudinal Monitoring**
- **Meaning**: Tracking the same patient across multiple visits over months or years to see if their disease is getting worse ($+\Delta\%$) or improving ($-\Delta\%$).

### 5. **ORM (SQLAlchemy)**
- **Meaning**: The bridge that translates Python data objects directly into database rows inside our SQLite database.

---

## 5. Rapid 1-Line "Layman Analogies" (Memorize for Judges)

| If the Judge Asks: | Give this Instant 1-Sentence Answer: |
| :--- | :--- |
| **"What is Jitter and Shimmer?"** | *"Jitter is the microscopic wavering in voice pitch, while Shimmer is the microscopic flickering in voice loudness."* |
| **"What does HNR mean?"** | *"HNR measures how clear and musical a voice is compared to breathy background static noise."* |
| **"Why do you need Quantum if Classical ML is already good?"** | *"Classical trees look at scalar thresholds, while Quantum circuits map multi-feature entanglements in a 16-dimensional space, giving doctors a dual-model consensus and an automated safety alarm whenever models disagree."* |
| **"What is TreeSHAP?"** | *"TreeSHAP is like an itemized grocery bill for AI—it tells the doctor exactly which biomarker added how many percentage points to the patient's risk."* |
| **"What happens if a hospital doesn't have a quantum computer?"** | *"Our platform includes a sub-millisecond NumPy matrix simulator that matches Qiskit to zero delta and runs on any standard laptop or hospital PC."* |
| **"Is this diagnosing the patient autonomously?"** | *"No, AAROH is strictly a Decision-Support System (CDSS) that flags early warning signals and generates an official ICD-10 memo for the neurologist to sign."* |
| **"What does the +14% / -12% on the history tab mean?"** | *"That is our Longitudinal Trajectory Delta—it shows whether the patient's vocal stability is deteriorating or improving after starting medication."* |
