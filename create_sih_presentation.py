import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # blank layout

    # Colors
    NAVY = RGBColor(15, 32, 67)         # #0F2043
    DEEP_BLUE = RGBColor(10, 25, 47)    # #0A192F
    ACCENT_BLUE = RGBColor(14, 116, 144)# #0E7490
    CYAN = RGBColor(14, 165, 233)       # #0EA5E9
    DARK_TEXT = RGBColor(30, 41, 59)    # #1E293B
    MUTED_TEXT = RGBColor(100, 116, 139)# #64748B
    LIGHT_BG = RGBColor(248, 250, 252)  # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)   # #FFFFFF
    BORDER_COLOR = RGBColor(226, 232, 240) # #E2E8F0
    ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981
    ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B
    WHITE = RGBColor(255, 255, 255)

    sih_logo_path = "extracted_ppt_assets/slide_1_img_1_Image6.png"
    sih_banner_path = "extracted_ppt_assets/slide_1_img_0_Image3.png"
    arch_flow_path = "extracted_ppt_assets/slide_3_img_1_Image12.png"
    tech_stack_path = "extracted_ppt_assets/slide_3_img_2_Image13.png"

    def add_header(slide, title_text, category_tag="SMART INDIA HACKATHON 2025"):
        # Top banner bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = DEEP_BLUE
        top_bar.line.fill.background()

        # Category / Subtitle tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(9.0), Inches(0.3))
        tf_tag = tb_tag.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN

        # Main slide title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.40), Inches(9.5), Inches(0.65))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # SIH Logo on top right
        if os.path.exists(sih_logo_path):
            slide.shapes.add_picture(sih_logo_path, Inches(11.2), Inches(0.18), width=Inches(1.5))

        # Bottom subtle footer
        foot_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.15), Inches(13.333), Inches(0.35))
        foot_bar.fill.solid()
        foot_bar.fill.fore_color.rgb = LIGHT_BG
        foot_bar.line.color.rgb = BORDER_COLOR

        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.18), Inches(11.7), Inches(0.3))
        tf_foot = tb_foot.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Team AAROH  |  Problem Statement ID: 26139  |  Hybrid Quantum Machine Learning for Early Disease Detection"
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 1: TITLE PAGE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)

    # Background
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DEEP_BLUE
    bg1.line.fill.background()

    # SIH Banner
    if os.path.exists(sih_banner_path):
        slide1.shapes.add_picture(sih_banner_path, Inches(0.8), Inches(0.5), width=Inches(4.2))

    # Hackathon Subtitle
    tb1_sub = slide1.shapes.add_textbox(Inches(0.8), Inches(2.4), Inches(11.7), Inches(0.5))
    tf1_sub = tb1_sub.text_frame
    p1_sub = tf1_sub.paragraphs[0]
    p1_sub.text = "SMART INDIA HACKATHON 2025 / 2026 — IDEA PRESENTATION"
    p1_sub.font.size = Pt(14)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = CYAN

    # Project Title
    tb1_t = slide1.shapes.add_textbox(Inches(0.8), Inches(2.85), Inches(11.7), Inches(1.2))
    tf1_t = tb1_t.text_frame
    tf1_t.word_wrap = True
    p1_t = tf1_t.paragraphs[0]
    p1_t.text = "AAROH: Hybrid Quantum Machine Learning for Early Disease Detection"
    p1_t.font.size = Pt(28)
    p1_t.font.bold = True
    p1_t.font.color.rgb = WHITE

    # Desc
    tb1_d = slide1.shapes.add_textbox(Inches(0.8), Inches(4.0), Inches(11.7), Inches(0.6))
    tf1_d = tb1_d.text_frame
    p1_d = tf1_d.paragraphs[0]
    p1_d.text = "An Explainable Hybrid Classical-Quantum Clinical Intelligence Platform for Oncology Triage"
    p1_d.font.size = Pt(15)
    p1_d.font.color.rgb = RGBColor(203, 213, 225)

    # 4 Metadata Cards
    meta_items = [
        ("Problem Statement ID", "26139", CYAN),
        ("Theme", "Quantum and AI in Healthcare", ACCENT_GREEN),
        ("PS Category", "Software", ACCENT_AMBER),
        ("Team Name & ID", "AAROH  (SIH25XXXX)", WHITE)
    ]
    card_w = Inches(2.7)
    card_gap = Inches(0.3)
    start_x = Inches(0.8)
    for i, (label, val, col) in enumerate(meta_items):
        cx = start_x + i * (card_w + card_gap)
        c_shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(4.9), card_w, Inches(1.8))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = RGBColor(22, 43, 77)
        c_shape.line.color.rgb = RGBColor(40, 70, 115)

        tb_c = slide1.shapes.add_textbox(cx + Inches(0.15), Inches(5.1), card_w - Inches(0.3), Inches(1.4))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        p_l = tf_c.paragraphs[0]
        p_l.text = label.upper()
        p_l.font.size = Pt(11)
        p_l.font.bold = True
        p_l.font.color.rgb = MUTED_TEXT

        p_v = tf_c.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(14)
        p_v.font.bold = True
        p_v.font.color.rgb = col
        p_v.space_before = Pt(8)

    # =========================================================================
    # SLIDE 2: PROPOSED SOLUTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "PROPOSED SOLUTION", "AAROH Hybrid Clinical Intelligence Platform")

    # Left Column: Core Solution Architecture
    box_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.5))
    box_left.fill.solid()
    box_left.fill.fore_color.rgb = CARD_BG
    box_left.line.color.rgb = BORDER_COLOR

    tb_l = slide2.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(5.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Unified Hybrid Classical-Quantum Architecture"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    points_l = [
        ("Clinical Biomedical Ingestion: ", "Standardized ingestion of 30 fine-needle aspiration (FNA) nuclear morphometry features from the Wisconsin Breast Cancer Dataset (WBCD, 569 cases)."),
        ("Intelligent Dimensional Compression: ", "StandardScaler normalization and Principal Component Analysis (PCA) mapping 30 clinical metrics to top 4 principal components preserving ~85% clinical variance."),
        ("Dual-Engine Classification: ", "Orchestrates Classical XGBoost (0.994 ROC-AUC) alongside a 4-Qubit Variational Quantum Classifier (VQC) with ZZFeatureMap & RealAmplitudes ansatz."),
        ("Deterministic Agentic Orchestration: ", "4-stage verifiable pipeline narrating real execution telemetry via Server-Sent Events (SSE) — 100% real computation, zero hardcoded values."),
        ("Local Explainability: ", "Exact TreeSHAP additive feature attribution showing patient-specific morphological risk drivers."),
        ("Clinical Decision Support (CDSS): ", "Produces an auditable Clinical Consultation Memo with human-in-the-loop oversight and discordant consensus alerts.")
    ]

    for title, desc in points_l:
        p = tf_l.add_paragraph()
        p.space_before = Pt(8)
        run_t = p.add_run()
        run_t.text = "● " + title
        run_t.font.bold = True
        run_t.font.size = Pt(11.5)
        run_t.font.color.rgb = DARK_TEXT

        run_d = p.add_run()
        run_d.text = desc
        run_d.font.size = Pt(11)
        run_d.font.color.rgb = RGBColor(71, 85, 105)

    # Right Column: 3 Key Innovation Highlights
    right_items = [
        ("Dual-Model Consensus Engine", "Combines Classical XGBoost & Quantum VQC predictions. Concordant consensus validates high diagnostic confidence; discordant divergence flags borderline lesions for confirmatory immunohistochemistry (IHC) biopsy.", ACCENT_BLUE),
        ("Pure NumPy Zero-Dependency Fallback", "To guarantee zero-fail live resilience, AAROH includes a native NumPy matrix simulator that computes Kronecker statevector evolution in <10ms if quantum C++ drivers encounter environment constraints.", ACCENT_GREEN),
        ("Scientifically Honest Benchmarking", "Explicitly reports 5-Fold Stratified CV on classical ML vs held-out 80/20 test split on quantum VQC. Validates quantum encoding feasibility at small scale rather than claiming premature supremacy.", ACCENT_AMBER)
    ]

    for i, (title, desc, col) in enumerate(right_items):
        ry = Inches(1.4) + i * Inches(1.88)
        box_r = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), ry, Inches(5.7), Inches(1.72))
        box_r.fill.solid()
        box_r.fill.fore_color.rgb = CARD_BG
        box_r.line.color.rgb = BORDER_COLOR

        # Left accent stripe
        stripe = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), ry, Inches(0.15), Inches(1.72))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = col
        stripe.line.fill.background()

        tb_r = slide2.shapes.add_textbox(Inches(7.1), ry + Inches(0.1), Inches(5.2), Inches(1.5))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True

        p_rt = tf_r.paragraphs[0]
        p_rt.text = title
        p_rt.font.size = Pt(13)
        p_rt.font.bold = True
        p_rt.font.color.rgb = NAVY

        p_rd = tf_r.add_paragraph()
        p_rd.text = desc
        p_rd.font.size = Pt(11)
        p_rd.font.color.rgb = RGBColor(71, 85, 105)
        p_rd.space_before = Pt(4)

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "TECHNICAL APPROACH & ARCHITECTURE", "End-to-End Pipeline & System Stack")

    # Left: Embed Architecture Diagram
    if os.path.exists(arch_flow_path):
        slide3.shapes.add_picture(arch_flow_path, Inches(0.8), Inches(1.35), height=Inches(5.6))
    else:
        # Fallback box
        b = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(4.8), Inches(5.6))
        b.fill.solid()
        b.fill.fore_color.rgb = CARD_BG

    # Right: Technology Stack Table & Description
    tb_tst = slide3.shapes.add_textbox(Inches(5.7), Inches(1.35), Inches(6.8), Inches(0.4))
    tf_tst = tb_tst.text_frame
    p = tf_tst.paragraphs[0]
    p.text = "Engineered Technology Stack (Implemented & Verified)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Add Tech Stack Table
    table_shape = slide3.shapes.add_table(9, 3, Inches(5.7), Inches(1.85), Inches(6.8), Inches(5.1))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.8)

    headers = ["LAYER", "FRAMEWORK", "ROLE / SPECIFICATION"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(10.5)
            p.font.color.rgb = WHITE

    rows_data = [
        ("Frontend UI", "React 19 + Tailwind CSS", "Dark clinical theme, sliders, memo print"),
        ("Backend Server", "Python 3.12 + FastAPI", "High-throughput asynchronous REST & SSE"),
        ("Classical ML", "XGBoost + scikit-learn", "5-Fold Stratified CV (0.994 ROC-AUC)"),
        ("Quantum ML", "Qiskit 2.5 + Aer 0.17", "4-Qubit ZZFeatureMap + RealAmplitudes VQC"),
        ("Quantum Fallback", "Pure NumPy Simulator", "Matrix statevector replay (<10ms latency)"),
        ("Explainability", "shap 0.52 (TreeExplainer)", "Exact local additive Shapley attribution"),
        ("Streaming Protocol", "Server-Sent Events (SSE)", "Unidirectional stage telemetry pipeline"),
        ("Clinical Reporting", "HTML5 / CSS3 Print", "1-Click Pathology Consultation Memo export")
    ]

    for row_idx, r in enumerate(rows_data):
        for col_idx, text in enumerate(r):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 0 else LIGHT_BG
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.color.rgb = DARK_TEXT
                if col_idx == 0:
                    p.font.bold = True

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "FEASIBILITY AND VIABILITY", "Deployment Readiness & Technical Mitigations")

    # 3 Columns / Cards
    # Column 1: Why Feasible?
    b1 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.5))
    b1.fill.solid()
    b1.fill.fore_color.rgb = CARD_BG
    b1.line.color.rgb = BORDER_COLOR

    tb = slide4.shapes.add_textbox(Inches(0.95), Inches(1.55), Inches(3.4), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Why Feasible Today?"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    f_points = [
        ("Simulator-First Deployment: ", "Zero dependence on active cloud quantum queues. Runs on local Qiskit Aer statevector backend with sub-second execution."),
        ("NISQ-Era Ready: ", "Circuit depth is restricted to D=2 on 4 qubits, safely operating below the theoretical Barren Plateau threshold (McClean et al.)."),
        ("Hybrid Efficiency: ", "Heavy ingestion, scaling, and feature extraction run on classical CPU; quantum circuits handle non-linear Hilbert space kernel mapping."),
        ("Modular Medical Extensibility: ", "Architecture readily extends from breast FNA biopsies to lung CT radiomics and multi-omic gene profiles.")
    ]
    for t, d in f_points:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "● " + t
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = DARK_TEXT
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = RGBColor(71, 85, 105)

    # Column 2: Challenges -> Proven Solutions
    b2 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.4), Inches(4.0), Inches(5.5))
    b2.fill.solid()
    b2.fill.fore_color.rgb = CARD_BG
    b2.line.color.rgb = BORDER_COLOR

    tb = slide4.shapes.add_textbox(Inches(4.95), Inches(1.55), Inches(3.7), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Challenges & Mitigations"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    c_points = [
        ("High Dimensionality (30 features):", "PCA dimensional reduction maps 30 correlated features to 4 orthogonal principal components preserving ~85% variance."),
        ("Limited Qubit Count & Noise:", "Angle Encoding (Ry) and 2-repetition RealAmplitudes minimize gate depth and error accumulation."),
        ("Quantum Driver/Environment Glitches:", "Zero-dependency pure NumPy linear algebra simulator reproduces exact matrix statevectors in <10ms."),
        ("Clinical Adoption Barriers:", "Exact TreeSHAP feature attributions and printable pathology consultation memos provide full physician auditability.")
    ]
    for t, d in c_points:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = "⚡ " + t + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_AMBER
        r2 = p.add_run()
        r2.text = "➔ Solution: " + d
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = DARK_TEXT

    # Column 3: Roadmap
    b3 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.1), Inches(1.4), Inches(3.4), Inches(5.5))
    b3.fill.solid()
    b3.fill.fore_color.rgb = CARD_BG
    b3.line.color.rgb = BORDER_COLOR

    tb = slide4.shapes.add_textbox(Inches(9.25), Inches(1.55), Inches(3.1), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Execution Roadmap"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    roadmap = [
        ("PHASE 1: Foundation (Completed)", "Classical XGBoost (5-Fold CV: 0.994 ROC-AUC), 4-Qubit VQC, SHAP TreeExplainer, and NumPy fallback simulator."),
        ("PHASE 2: Backend (Completed)", "FastAPI deterministic 4-stage agent orchestrator with Server-Sent Events (SSE) live streaming."),
        ("PHASE 3: UI & Memos (Completed)", "React 19 clinical dashboard, dual-model comparison, real-time SHAP waterfall, and printable pathology memo."),
        ("PHASE 4: Hardware & Hospital Pilot", "IBM Quantum Eagle/Falcon processor deployment via Qiskit Runtime; multi-center clinical observational study.")
    ]
    for t, d in roadmap:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = t + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_BLUE
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "IMPACT AND CLINICAL BENEFITS", "Measurable Healthcare Outcomes & Value Proposition")

    # 4 Cards in 2x2 Grid
    cards_data = [
        ("Earlier & Accurate Oncology Detection",
         "Dramatically reduces false negatives in breast fine-needle aspiration (FNA) biopsies. Demonstrates 93.4% sensitivity and 0.994 ROC-AUC on baseline clinical data, enabling timely intervention before malignant metastasis.",
         ACCENT_BLUE),
        ("High-Dimensional Non-Linear Mapping",
         "Translates multi-parameter cellular morphology into a 2^4 = 16-dimensional quantum Hilbert space, capturing complex non-linear feature correlations that traditional linear boundaries miss.",
         ACCENT_GREEN),
        ("Clinical Explainability & Trust",
         "Eliminates black-box diagnosis. TreeSHAP feature attributions calculate the exact quantitative impact of each biomarker (concavity, perimeter, radius) for every patient, building physician confidence.",
         ACCENT_AMBER),
        ("Dual-Model Consensus & Triage Safety",
         "Concordance analysis verifies whether classical and quantum engines agree. Flags discordant borderline cases to prompt confirmatory core biopsy, minimizing diagnostic blind spots.",
         RGBColor(239, 68, 68)),
    ]

    card_gw = Inches(5.6)
    card_gh = Inches(2.2)
    positions = [
        (Inches(0.8), Inches(1.4)),
        (Inches(6.8), Inches(1.4)),
        (Inches(0.8), Inches(3.9)),
        (Inches(6.8), Inches(3.9))
    ]

    for idx, (title, desc, col) in enumerate(cards_data):
        x, y = positions[idx]
        b = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_gw, card_gh)
        b.fill.solid()
        b.fill.fore_color.rgb = CARD_BG
        b.line.color.rgb = BORDER_COLOR

        st = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.15), card_gh)
        st.fill.solid()
        st.fill.fore_color.rgb = col
        st.line.fill.background()

        tb = slide5.shapes.add_textbox(x + Inches(0.3), y + Inches(0.15), card_gw - Inches(0.5), card_gh - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_TEXT
        p2.space_before = Pt(6)

    # Bottom summary tag
    sum_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.3), Inches(11.6), Inches(0.7))
    sum_box.fill.solid()
    sum_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    sum_box.line.color.rgb = RGBColor(199, 210, 254)

    tb = slide5.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.2), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "★ Quantum-Ready Extensibility: Establishes the clinical data pipelining and benchmarking framework today, ready to transition to quantum advantage as multi-omic genomic sequencing and fault-tolerant quantum hardware expand."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(49, 46, 129)

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "RESEARCH AND REFERENCES", "Scientific Foundations & Empirical Benchmarks")

    # Left Box: Theoretical Foundations & Papers
    b_l = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
    b_l.fill.solid()
    b_l.fill.fore_color.rgb = CARD_BG
    b_l.line.color.rgb = BORDER_COLOR

    tb = slide6.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.2), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Theoretical Foundations & Literature"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    lit = [
        ("Schuld & Petruccione (2018): ", "Supervised Learning with Quantum Computers. Foundational theory for quantum kernels and Hilbert space embeddings."),
        ("Havlíček et al. (Nature 2019): ", "Supervised learning with quantum-enhanced feature spaces. Establishes the ZZFeatureMap second-order Pauli expansion used in AAROH."),
        ("Cerezo et al. (Nature Reviews 2021): ", "Variational Quantum Algorithms. Methodological basis for parameterized ansatzes (RealAmplitudes) and gradient-free optimization."),
        ("McClean et al. (Nature Comm 2018): ", "Barren plateaus in quantum neural network training landscapes. Direct theoretical rationale for restricting AAROH to 4 shallow qubits."),
        ("Lundberg & Lee (NeurIPS 2017): ", "A Unified Approach to Interpreting Model Predictions. Algorithmic foundation for exact TreeSHAP local additive feature attributions.")
    ]

    for t, d in lit:
        p = tf.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "● " + t
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = DARK_TEXT
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = RGBColor(71, 85, 105)

    # Right Box: Concrete Empirical Benchmark Results
    b_r = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5))
    b_r.fill.solid()
    b_r.fill.fore_color.rgb = CARD_BG
    b_r.line.color.rgb = BORDER_COLOR

    tb_r = slide6.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.3), Inches(5.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Empirical Validation Protocol (Honest Numbers)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_sub = tf_r.add_paragraph()
    p_sub.text = "Dataset: Wisconsin Breast Cancer Diagnostic (WBCD) — n=569 cases, 30 features"
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = MUTED_TEXT
    p_sub.space_before = Pt(2)

    # Mini Table for Metrics
    bm_table_shape = slide6.shapes.add_table(4, 3, Inches(7.0), Inches(2.35), Inches(5.3), Inches(1.9))
    bm_table = bm_table_shape.table
    bm_table.columns[0].width = Inches(1.9)
    bm_table.columns[1].width = Inches(1.7)
    bm_table.columns[2].width = Inches(1.7)

    bm_headers = ["METRIC", "CLASSICAL XGBOOST", "QUANTUM VQC"]
    for c_idx, h in enumerate(bm_headers):
        cell = bm_table.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(10)
            p.font.color.rgb = WHITE

    bm_data = [
        ("Validation Method", "5-Fold Stratified CV", "Held-out 80/20 Test Split"),
        ("ROC-AUC Score", "0.994 ± 0.004", "0.748 (seed=42)"),
        ("Accuracy", "96.0% ± 1.6%", "68.4% (F1: 61.7%)")
    ]
    for r_idx, row in enumerate(bm_data):
        for c_idx, val in enumerate(row):
            cell = bm_table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 0 else LIGHT_BG
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 1:
                    p.font.bold = True
                    p.font.color.rgb = ACCENT_BLUE

    # Evaluation Pitch Note Box
    tb_bot = slide6.shapes.add_textbox(Inches(7.0), Inches(4.45), Inches(5.3), Inches(2.3))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True

    p = tf_bot.paragraphs[0]
    p.text = "The Evaluation Pitch Baseline:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_bot.add_paragraph()
    p.text = "\"AAROH is a hybrid clinical benchmarking platform that orchestrates classical XGBoost and a trained Variational Quantum Classifier through an agentic pipeline, producing SHAP-explainable predictions and a clinical consultation memo — with the honest result that at 569 rows, we validate quantum encoding viability, not quantum superiority.\""
    p.font.size = Pt(10.5)
    p.font.italic = True
    p.font.color.rgb = RGBColor(30, 58, 138)
    p.space_before = Pt(4)

    p = tf_bot.add_paragraph()
    p.text = "Core Stack: Qiskit Aer 0.17 | XGBoost 3.4 | Scikit-Learn 1.9 | SHAP 0.52 | FastAPI | React 19"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = MUTED_TEXT
    p.space_before = Pt(6)

    # Save presentation
    output_pptx = "AAROH_SIH2025_Presentation.pptx"
    prs.save(output_pptx)
    print(f"Presentation saved successfully to: {output_pptx}")

if __name__ == "__main__":
    create_presentation()
