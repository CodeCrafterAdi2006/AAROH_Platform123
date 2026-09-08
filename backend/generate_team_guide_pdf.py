"""
AAROH — Teammate & Contributor Comprehensive Master PDF Guide Generator
Generates a publication-grade, beautifully formatted PDF guide for the entire team.
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Define Palette
COLOR_PRIMARY = colors.HexColor("#0f172a")     # Deep Slate / Navy
COLOR_SECONDARY = colors.HexColor("#0284c7")   # Medical Cyan / Blue
COLOR_ACCENT = colors.HexColor("#0d9488")      # Teal Accent
COLOR_ROSE = colors.HexColor("#e11d48")        # Warning / Malignant Rose
COLOR_BG_LIGHT = colors.HexColor("#f8fafc")    # Light Card Surface
COLOR_BORDER = colors.HexColor("#cbd5e1")      # Border Grey
COLOR_TEXT = colors.HexColor("#1e293b")        # Dark Charcoal Text
COLOR_MUTED = colors.HexColor("#64748b")       # Secondary Slate Text
COLOR_WHITE = colors.HexColor("#ffffff")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' 
    and a top header rule on all pages after the cover.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_decorations(self, total_pages):
        self.saveState()
        page_num = self._pageNumber

        if page_num > 1:
            # Top Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(COLOR_MUTED)
            self.drawString(36, 11 * inch - 26, "AAROH — HYBRID CLINICAL INTELLIGENCE PLATFORM")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * inch - 36, 11 * inch - 26, "TEAMMATE & CONTRIBUTOR GUIDE")
            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.5)
            self.line(36, 11 * inch - 30, 8.5 * inch - 36, 11 * inch - 30)

        # Bottom Running Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)
        self.drawString(36, 22, "Smart India Hackathon (SIH 2026) | Healthcare AI & Quantum Benchmarking")
        page_str = f"Page {page_num} of {total_pages}"
        self.drawRightString(8.5 * inch - 36, 22, page_str)
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(36, 32, 8.5 * inch - 36, 32)

        self.restoreState()


def create_callout_box(title, text, bg_color=COLOR_BG_LIGHT, border_color=COLOR_SECONDARY):
    """Generates a styled callout box table."""
    styles = getSampleStyleSheet()
    t_style = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=border_color,
        spaceAfter=3
    )
    b_style = ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=COLOR_TEXT
    )

    content = [
        Paragraph(f"<b>{title}</b>", t_style),
        Paragraph(text, b_style)
    ]

    t = Table([[content]], colWidths=[7.4 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 1.2, border_color),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def build_pdf(filename="AAROH_Teammate_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Custom Typographic Hierarchy
    style_main_title = ParagraphStyle(
        'MainTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=COLOR_PRIMARY,
        spaceAfter=3
    )

    style_main_sub = ParagraphStyle(
        'MainSub',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=COLOR_SECONDARY,
        spaceAfter=10
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=COLOR_TEXT,
        spaceAfter=5
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        parent=style_body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=COLOR_TEXT
    )

    style_table_head = ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=COLOR_WHITE
    )

    story = []

    # =========================================================================
    # COVER / HEADER HERO SECTION
    # =========================================================================
    story.append(Paragraph("AAROH (आरोह)", style_main_title))
    story.append(Paragraph("Hybrid Classical-Quantum Clinical Benchmarking & Intelligence Platform", style_main_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=8))

    # Meta Tag Strip
    meta_table_data = [[
        Paragraph("<b>Domain:</b> Healthcare AI / Oncology", style_table_cell),
        Paragraph("<b>Dataset:</b> WBCD (569 Biopsies, 30 Features)", style_table_cell),
        Paragraph("<b>Stack:</b> Qiskit Aer, XGBoost, TreeSHAP, FastAPI, React 19", style_table_cell)
    ]]
    meta_table = Table(meta_table_data, colWidths=[2.3 * inch, 2.7 * inch, 2.4 * inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Executive Summary Callout
    exec_summary = (
        "<b>What is AAROH in simple words?</b><br/>"
        "AAROH is a medical decision-support platform for breast cancer biopsy diagnosis. It runs <b>BOTH</b> a production classical "
        "model (XGBoost) and a 4-qubit Quantum Classifier (Qiskit VQC) through an auditable, real-time agent pipeline. It explains "
        "every decision with exact TreeSHAP attribution forces and generates an official printable hospital pathology memo."
    )
    story.append(create_callout_box("EXECUTIVE SUMMARY (THE 60-SECOND TL;DR)", exec_summary, bg_color=colors.HexColor("#f0fdf4"), border_color=COLOR_ACCENT))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 1: THE CORE PITCH & WHY THIS EXISTS
    # =========================================================================
    story.append(Paragraph("1. The Core Pitch & The 'Honest Numbers' Strategy", style_h1))
    story.append(Paragraph(
        "Many hackathon teams lose credibility by making fake '99.9% Quantum Advantage' claims. AAROH takes the winning scientific path:", style_body
    ))

    pitch_quote = (
        "<i>'AAROH is a hybrid clinical benchmarking platform that orchestrates classical XGBoost and a trained "
        "Variational Quantum Classifier through an agentic pipeline, producing SHAP-explainable predictions and a clinical "
        "consultation memo — with the honest result that at 569 rows, we validate quantum encoding viability, not quantum superiority.'</i>"
    )
    story.append(create_callout_box("THE OFFICIAL ELEVATOR PITCH (MEMORIZE FOR FACULTY & JUDGES)", pitch_quote, bg_color=colors.HexColor("#f8fafc"), border_color=COLOR_PRIMARY))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Three Foundational Pillars to Remember:</b>", style_body))
    story.append(Paragraph("• <b>Real Computation Under the Hood:</b> Zero hardcoded metric arrays, zero mocked latency timers, zero hallucinated SHAP values. Every tensor is computed live.", style_bullet))
    story.append(Paragraph("• <b>The Honest Numbers Protocol:</b> On 569 tabular rows, classical XGBoost is mathematically optimal (0.994 ROC-AUC). Our 4-qubit VQC achieves 0.748 ROC-AUC on a held-out test split, validating non-linear Hilbert space encoding viability under NISQ quantum constraints.", style_bullet))
    story.append(Paragraph("• <b>Deterministic Agentic Telemetry:</b> Instead of unpredictable LLMs that can hallucinate medical dosages, our 4-stage pipeline is 100% deterministic, auditable, and streamed live via Server-Sent Events (SSE).", style_bullet))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: THE 3-TIER ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. System Architecture & Component Roles", style_h1))

    arch_data = [
        [Paragraph("Subsystem", style_table_head), Paragraph("Tech Stack", style_table_head), Paragraph("Role & Key Responsibilities", style_table_head)],
        [
            Paragraph("<b>Backend API</b><br/>(Port 8000)", style_table_cell),
            Paragraph("Python 3.12, FastAPI, Uvicorn", style_table_cell),
            Paragraph("Serves REST & SSE endpoints. Manages lifespan model pre-warming so inferences respond in sub-70 milliseconds.", style_table_cell)
        ],
        [
            Paragraph("<b>Hybrid ML & Quantum Core</b>", style_table_cell),
            Paragraph("Qiskit Aer, XGBoost, TreeSHAP, NumPy", style_table_cell),
            Paragraph("Executes 5-Fold CV XGBoost, 4-qubit ZZFeatureMap + RealAmplitudes VQC, zero-leakage TreeSHAP, and zero-fail NumPy fallback matrix simulator.", style_table_cell)
        ],
        [
            Paragraph("<b>Deterministic Orchestrator</b>", style_table_cell),
            Paragraph("Python Generators, Server-Sent Events", style_table_cell),
            Paragraph("Streams stage execution telemetry in real-time packets (Stage 1 ➔ Stage 2 ➔ Stage 3 ➔ Stage 4 ➔ Final Result).", style_table_cell)
        ],
        [
            Paragraph("<b>Clinical Frontend UI</b><br/>(Port 5173)", style_table_cell),
            Paragraph("React 19, Vite, Tailwind CSS, Lucide, Recharts", style_table_cell),
            Paragraph("Glassmorphic clinical dark theme, WBCD presets, live agent stream terminal, interactive SHAP force bars, and 1-click printable hospital memo.", style_table_cell)
        ]
    ]
    t_arch = Table(arch_data, colWidths=[1.4 * inch, 1.8 * inch, 4.2 * inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_LIGHT]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: STEP-BY-STEP DIAGNOSTIC PIPELINE (THE 4 AGENTS)
    # =========================================================================
    story.append(Paragraph("3. Step-by-Step Diagnostic Pipeline (The 4 Agent Stages)", style_h1))
    story.append(Paragraph(
        "When a user clicks <b>'Run Hybrid Diagnostic Pipeline'</b>, here is the exact 4-stage sequence streamed live via SSE:", style_body
    ))

    stages_data = [
        [Paragraph("Stage", style_table_head), Paragraph("Agent Name", style_table_head), Paragraph("Exact Computation Performed", style_table_head)],
        [
            Paragraph("<b>Stage 1</b>", style_table_cell),
            Paragraph("<b>Data Ingestion & QC Agent</b>", style_table_cell),
            Paragraph("Validates patient vector has exactly 30 positive measurements. Checks bounds, zero-NaN verification, and logs nuclear morphology baseline (Radius, Perimeter, Area).", style_table_cell)
        ],
        [
            Paragraph("<b>Stage 2</b>", style_table_cell),
            Paragraph("<b>Quantum Encoding Agent</b>", style_table_cell),
            Paragraph("Compresses 30 features to 4 PCA components, maps to [-π, +π] angles, encodes into 4 qubits via <code>ZZFeatureMap</code> (reps=1), applies <code>RealAmplitudes</code> ansatz (8 parameters), and measures &lt;IIIZ&gt; to calculate quantum probability.", style_table_cell)
        ],
        [
            Paragraph("<b>Stage 3</b>", style_table_cell),
            Paragraph("<b>Classical Explainability Agent</b>", style_table_cell),
            Paragraph("Executes XGBoost inference for calibrated confidence and log-odds margin f(x). Runs exact <code>TreeExplainer</code> feature attributions, verifying additive invariant: f(x) = E[f(x)] + Σφ_i with zero margin leakage (delta &lt; 1e-6).", style_table_cell)
        ],
        [
            Paragraph("<b>Stage 4</b>", style_table_cell),
            Paragraph("<b>Clinical Synthesis & Memo Agent</b>", style_table_cell),
            Paragraph("Cross-checks dual-model concordance. Assigns ICD-10 coding (<b>C50.919</b> malignant carcinoma or <b>N60.99</b> benign dysplasia). Assigns risk tier and synthesizes a printable hospital consultation memo with clinical recommendations.", style_table_cell)
        ]
    ]
    t_stages = Table(stages_data, colWidths=[0.7 * inch, 1.9 * inch, 4.8 * inch])
    t_stages.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECONDARY),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_LIGHT]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_stages)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 4: THE NUMBERS & BENCHMARK DEFENSE
    # =========================================================================
    story.append(KeepTogether([
        Paragraph("4. Benchmark Metrics & Faculty / Judge Defense Sheet", style_h1),
        Paragraph("Memorize these exact empirical numbers and defense scripts for presentations:", style_body)
    ]))

    bench_data = [
        [Paragraph("Metric", style_table_head), Paragraph("Classical XGBoost (5-Fold CV)", style_table_head), Paragraph("4-Qubit VQC (80/20 Test Split)", style_table_head), Paragraph("Clinical Interpretation", style_table_head)],
        [
            Paragraph("<b>ROC-AUC</b>", style_table_cell),
            Paragraph("<b>0.994 ± 0.004</b>", style_table_cell),
            Paragraph("<b>0.748</b>", style_table_cell),
            Paragraph("Separation power between malignant and benign cases.", style_table_cell)
        ],
        [
            Paragraph("<b>Accuracy</b>", style_table_cell),
            Paragraph("96.0% ± 1.6%", style_table_cell),
            Paragraph("68.4%", style_table_cell),
            Paragraph("Overall correct classification rate across test samples.", style_table_cell)
        ],
        [
            Paragraph("<b>Sensitivity (Recall)</b>", style_table_cell),
            Paragraph("93.4% ± 3.3%", style_table_cell),
            Paragraph("69.1%", style_table_cell),
            Paragraph("Critical in oncology: Percentage of actual cancers caught.", style_table_cell)
        ],
        [
            Paragraph("<b>Specificity</b>", style_table_cell),
            Paragraph("97.5% ± 1.3%", style_table_cell),
            Paragraph("68.1%", style_table_cell),
            Paragraph("Percentage of benign cases correctly ruled out.", style_table_cell)
        ],
        [
            Paragraph("<b>Sample Size</b>", style_table_cell),
            Paragraph("n = 569 (All cases)", style_table_cell),
            Paragraph("n = 114 (Held-out test split)", style_table_cell),
            Paragraph("Evaluation asymmetry disclosed via Honest Protocol.", style_table_cell)
        ]
    ]
    t_bench = Table(bench_data, colWidths=[1.3 * inch, 2.0 * inch, 1.8 * inch, 2.3 * inch])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_LIGHT]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 8))

    # Pre-written Judge Q&A Box
    qa_text = (
        "<b>Q1: 'Why use Quantum ML when XGBoost already gets 99% ROC-AUC?'</b><br/>"
        "<i>Answer: 'At 569 tabular rows, classical ML is mathematically optimal. AAROH does not claim quantum supremacy "
        "today; it is a benchmarking platform designed to validate non-linear quantum Hilbert space feature encoding viability "
        "and provide clinical auditability as quantum processors scale toward fault tolerance.'</i><br/><br/>"
        "<b>Q2: 'How are quantum states represented and measured?'</b><br/>"
        "<i>Answer: 'Features are mapped to 4 qubits via a second-order Pauli expansion (ZZFeatureMap), parameterized by an "
        "entangling RealAmplitudes ansatz (8 parameters), and measured through the Z-basis expectation value &lt;IIIZ&gt; on qubit 0.'</i><br/><br/>"
        "<b>Q3: 'What if Qiskit fails or simulator crashes during live evaluation?'</b><br/>"
        "<i>Answer: 'AAROH implements a zero-fail multi-tier fallback: Level 0 runs live Qiskit Aer; Level 1 automatically "
        "routes to our pre-computed pure NumPy statevector matrix simulator (0.000000 delta parity in &lt;4ms); Level 2 defaults "
        "to full classical XGBoost with honest diagnostic disclaimer.'</i>"
    )
    story.append(create_callout_box("THE 3 PRE-WRITTEN FACULTY / JUDGE RESPONSES", qa_text, bg_color=colors.HexColor("#fff1f2"), border_color=COLOR_ROSE))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: EXPLAINABILITY & CLINICAL MEMO
    # =========================================================================
    story.append(Paragraph("5. Explainable AI (XAI) & The Doctor's Trust Layer", style_h1))
    story.append(Paragraph(
        "Doctors reject black-box AI. AAROH makes every prediction 100% transparent using exact <b>TreeSHAP</b>:", style_body
    ))
    story.append(Paragraph("• <b>Base Value E[f(x)] = -0.5699:</b> The baseline probability of cancer across the general cohort.", style_bullet))
    story.append(Paragraph("• <b>Attribution Forces:</b> Each of the 30 cell nucleus measurements pushes the score either toward cancer (Positive / Red force) or toward benign (Negative / Green force).", style_bullet))
    story.append(Paragraph("• <b>#1 Clinical Cancer Driver:</b> <i>Worst Concave Points</i> (severe indentation of cell nucleus margins, a hallmark sign of carcinoma).", style_bullet))
    story.append(Paragraph("• <b>Formal Pathology Memorandum:</b> Generates ICD-10 diagnostic codes (<code>C50.919</code> / <code>N60.99</code>) and recommended next clinical steps (e.g. Core Needle Biopsy with IHC profiling ER/PR/HER2). Clicking 'Print' renders a clean black-and-white hospital sheet ready for clinical records.", style_bullet))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: CODEBASE DIRECTORY TOUR (FOR CONTRIBUTORS)
    # =========================================================================
    story.append(Paragraph("6. Codebase Tour — Where Everything Lives", style_h1))

    tree_text = (
        "<b>backend/main.py:</b> FastAPI entrypoint, CORS, lifespan model cache, /api/predict/stream.<br/>"
        "<b>backend/agents/orchestrator.py:</b> 4-stage deterministic SSE generator & input validator.<br/>"
        "<b>backend/models/classical.py:</b> XGBoost trainer with 5-Fold Stratified CV.<br/>"
        "<b>backend/models/quantum.py:</b> 4-Qubit VQC circuit (ZZFeatureMap + RealAmplitudes).<br/>"
        "<b>backend/models/fallback_sim.py:</b> Pure NumPy matrix simulator with zero dependencies.<br/>"
        "<b>backend/models/explainability.py:</b> TreeSHAP feature attributions & narrative builder.<br/>"
        "<b>backend/reports/memo_gen.py:</b> ICD-10 pathology memorandum synthesizer.<br/>"
        "<b>aaroh-app/src/App.jsx:</b> Master React dashboard handling live SSE streams.<br/>"
        "<b>aaroh-app/src/components/:</b> Modular UI components (PatientInput, AgentStream, ModelComparison, ShapViewer, ClinicalMemo, MetricsModal).<br/>"
        "<b>idea.md & progress.md:</b> Full pitch scripts, Q&A defenses, and master engineering logs."
    )
    story.append(create_callout_box("REPOSITORY MAP", tree_text, bg_color=COLOR_BG_LIGHT, border_color=COLOR_MUTED))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: HOW TO RUN LOCALLY
    # =========================================================================
    story.append(Paragraph("7. How to Run AAROH Locally (Quickstart for the Team)", style_h1))

    run_text = (
        "<b>Terminal 1 — Backend Service (Port 8000):</b><br/>"
        "<code>cd SIH_Project2026</code><br/>"
        "<code>backend\\.venv\\Scripts\\activate</code> (or <code>source backend/.venv/bin/activate</code>)<br/>"
        "<code>pip install -r backend/requirements.txt</code><br/>"
        "<code>python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload</code><br/><br/>"
        "<b>Terminal 2 — Frontend UI (Port 5173):</b><br/>"
        "<code>cd aaroh-app</code><br/>"
        "<code>npm install</code><br/>"
        "<code>npm run dev</code><br/><br/>"
        "Open browser at <b>http://localhost:5173/</b>. Select 'Malignant' or 'Benign' preset and click 'Run Hybrid Diagnostic Pipeline'."
    )
    story.append(create_callout_box("LOCAL SETUP COMMANDS", run_text, bg_color=COLOR_BG_LIGHT, border_color=COLOR_SECONDARY))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 8: FUTURE ROADMAP & HOW WE CAN IMPROVE (FOR TEAMMATES)
    # =========================================================================
    story.append(KeepTogether([
        Paragraph("8. Future Roadmap: How We Can Elevate This Further", style_h1),
        Paragraph("High-impact directions the team can take to make AAROH even more impressive:", style_body)
    ]))

    roadmap_data = [
        [Paragraph("Enhancement Area", style_table_head), Paragraph("Specific Technical Task", style_table_head), Paragraph("Expected Impact on Judges", style_table_head)],
        [
            Paragraph("<b>1. Frontend 'De-AI-fying' & Clinical Polish</b>", style_table_cell),
            Paragraph("• Refine UI to look like an authentic hospital pathology workstation (Cerner/Epic EHR style).<br/>• Add interactive SVG cell cytology diagrams showing cell margin irregularity.<br/>• Add dark/light mode hospital toggle.", style_table_cell),
            Paragraph("Removes any 'generic template' feel. Proves deep domain empathy for how pathologists actually review tissue biopsies.", style_table_cell)
        ],
        [
            Paragraph("<b>2. Multi-Modal Histology Imaging</b>", style_table_cell),
            Paragraph("• Integrate Whole Slide Images (WSI) alongside numerical FNA tables.<br/>• Train a lightweight Vision Transformer (ViT) or ResNet feature extractor and concatenate image embeddings with 30D morphometry.", style_table_cell),
            Paragraph("Elevates project from purely tabular data into cutting-edge multi-modal AI, a top criteria in SIH healthcare tracks.", style_table_cell)
        ],
        [
            Paragraph("<b>3. Scaling to Real IBM Quantum Hardware (QPU)</b>", style_table_cell),
            Paragraph("• Connect backend to IBM Quantum Runtime API (via free IBM Cloud API token).<br/>• Execute circuits on real superconducting 127-qubit processors (Eagle/Heron) with readout error mitigation (M3/TREX).", style_table_cell),
            Paragraph("Demonstrates real physical quantum execution rather than just simulation, validating true NISQ capability.", style_table_cell)
        ],
        [
            Paragraph("<b>4. Privacy-Preserving Federated Learning</b>", style_table_cell),
            Paragraph("• Simulate 3 distinct hospital nodes (e.g. AIIMS, Tata Memorial, Apollo).<br/>• Train models using federated averaging (FedAvg) with differential privacy so patient data never leaves hospital servers.", style_table_cell),
            Paragraph("Addresses major real-world regulatory hurdles (HIPAA / GDPR / DISHA compliance) for hospital AI adoption.", style_table_cell)
        ],
        [
            Paragraph("<b>5. Multi-Cancer Generalization</b>", style_table_cell),
            Paragraph("• Adapt pipeline to other cytology datasets: Thyroid FNA (Bethesda), Lung adenocarcinoma, or Melanoma dermoscopy.", style_table_cell),
            Paragraph("Proves AAROH is a universal clinical orchestration engine, not just a one-dataset demo.", style_table_cell)
        ]
    ]
    t_road = Table(roadmap_data, colWidths=[1.8 * inch, 3.4 * inch, 2.2 * inch])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACCENT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_LIGHT]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 9: PRESENTATION DAY CHEAT SHEET
    # =========================================================================
    story.append(Paragraph("9. Presentation Day Cheat Sheet (Key Terms Decoded)", style_h1))
    story.append(Paragraph("• <b>FNA (Fine Needle Aspiration):</b> A quick biopsy technique where a thin needle extracts cell clusters from a breast lump.", style_bullet))
    story.append(Paragraph("• <b>Ansatz:</b> A parameterized quantum circuit with adjustable rotation gates (like weights in a neural network).", style_bullet))
    story.append(Paragraph("• <b>ZZFeatureMap:</b> A quantum mapping technique that entangles pairs of qubits to encode non-linear feature correlations.", style_bullet))
    story.append(Paragraph("• <b>Observable &lt;IIIZ&gt;:</b> Measuring the Pauli-Z operator on qubit 0 to get an expectation value between -1.0 and +1.0.", style_bullet))
    story.append(Paragraph("• <b>TreeSHAP:</b> An exact algorithm by Scott Lundberg that computes the mathematical contribution of each feature to the tree margin.", style_bullet))
    story.append(Paragraph("• <b>ICD-10 C50.919:</b> Official International Classification of Diseases code for malignant breast neoplasm.", style_bullet))
    story.append(Spacer(1, 10))

    # Closing Signature Strip
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER, spaceBefore=2, spaceAfter=6))
    closing_text = (
        "<b>Repository Link:</b> https://github.com/CodeCrafterAdi2006/AAROH_Platform123<br/>"
        "<b>Prepared for:</b> AAROH Engineering Team & Evaluators | Smart India Hackathon (SIH 2026)"
    )
    story.append(Paragraph(closing_text, style_body))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated master PDF guide: {filename}")


if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "AAROH_Teammate_Guide.pdf")
    build_pdf(out_pdf)
