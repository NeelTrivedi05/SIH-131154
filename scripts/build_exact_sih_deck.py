import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE

def create_exact_deck():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions matching the reference template
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Exact Color Palette from Reference Deck
    SIH_BLUE = RGBColor(0, 114, 198)       # Footer banner #0072C6
    TITLE_BLUE = RGBColor(25, 63, 120)     # Slide 1 main title #193F78
    BLACK = RGBColor(0, 0, 0)
    DARK_TEXT = RGBColor(30, 41, 59)
    WHITE = RGBColor(255, 255, 255)
    GRAY_TEXT = RGBColor(100, 116, 139)
    LINK_BLUE = RGBColor(0, 102, 204)
    
    # Box Backgrounds & Borders matching reference
    GREEN_FILL = RGBColor(212, 239, 223)   # Slide 2 Left box #D4EFDF
    GREEN_BORDER = RGBColor(39, 174, 96)
    BLUE_FILL = RGBColor(214, 234, 248)    # Slide 2 Right top #D6EAF8
    BLUE_BORDER = RGBColor(52, 152, 219)
    PURPLE_FILL = RGBColor(232, 218, 239)  # Slide 2 Right middle #E8DAEF
    PURPLE_BORDER = RGBColor(155, 89, 182)
    PEACH_FILL = RGBColor(250, 219, 216)   # Slide 4 Feasibility #FADBD8
    PEACH_BORDER = RGBColor(231, 76, 60)
    ORANGE_FILL = RGBColor(253, 237, 236)  # Slide 4 Challenges #FDEDEC
    ORANGE_BORDER = RGBColor(230, 126, 34)
    MINT_FILL = RGBColor(213, 245, 227)    # Slide 4 Strategies #D5F5E3
    MINT_BORDER = RGBColor(46, 204, 113)

    sih_logo_path = 'assets/sih_logo.png'

    def add_slide_frame(slide, title_text, slide_num, show_badge=True):
        # 1. Official SIH Logo top-right
        if os.path.exists(sih_logo_path):
            slide.shapes.add_picture(sih_logo_path, Inches(10.7), Inches(0.18), width=Inches(2.4))

        # 2. Top-Left Team Badge (Exact oval badge with MAHADEV / POLARGRID)
        if show_badge:
            badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.4), Inches(0.2), Inches(1.8), Inches(0.7))
            badge.fill.solid()
            badge.fill.fore_color.rgb = WHITE
            badge.line.color.rgb = BLACK
            badge.line.width = Pt(1.5)
            tf = badge.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = "POLARGRID"
            run.font.bold = True
            run.font.size = Pt(13)
            run.font.color.rgb = BLACK
            run.font.name = "Arial"

        # 3. Slide Title (Exact centered title in Serif/Georgia styling)
        if title_text:
            title_box = slide.shapes.add_textbox(Inches(2.4 if show_badge else 0.5), Inches(0.15), Inches(8.3 if show_badge else 10.2), Inches(0.8))
            tf = title_box.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = title_text
            run.font.bold = True
            run.font.size = Pt(26)
            run.font.color.rgb = BLACK
            run.font.name = "Georgia"

        # 4. Bottom Blue Banner (Exact 100% width SIH footer)
        footer_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.05), Inches(13.333), Inches(0.45))
        footer_bar.fill.solid()
        footer_bar.fill.fore_color.rgb = SIH_BLUE
        footer_bar.line.fill.background()

        footer_text = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(6.0), Inches(0.45))
        tf = footer_text.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = "@SIH Idea submission- Template"
        run.font.size = Pt(11)
        run.font.color.rgb = WHITE
        run.font.name = "Arial"

        slide_num_box = slide.shapes.add_textbox(Inches(12.3), Inches(7.05), Inches(0.8), Inches(0.45))
        tf = slide_num_box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        run = p.add_run()
        run.text = str(slide_num)
        run.font.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = WHITE
        run.font.name = "Arial"

    # =========================================================================
    # SLIDE 1: TITLE PAGE (Exact Match to Template Slide 1)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_slide_frame(slide1, "", 1, show_badge=False)

    # Title & Subtitle centered
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(0.4), Inches(9.5), Inches(1.5))
    tf = t_box.text_frame
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    r1 = p1.add_run()
    r1.text = "SMART INDIA HACKATHON 2026\n"
    r1.font.bold = True
    r1.font.size = Pt(32)
    r1.font.color.rgb = TITLE_BLUE
    r1.font.name = "Georgia"

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = "TITLE PAGE"
    r2.font.bold = True
    r2.font.size = Pt(26)
    r2.font.color.rgb = BLACK
    r2.font.name = "Georgia"

    # Main details - exact layout as template: large bold bullet points on left
    details_box = slide1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(4.5))
    tf_d = details_box.text_frame
    tf_d.word_wrap = True

    entries_s1 = [
        ("Problem Statement ID – ", "SIH26061"),
        ("Problem Statement Title- ", "AI-Driven Smart Energy Management System for Polar Research Stations."),
        ("Theme-", "Clean & Green Technology"),
        ("PS Category- ", "Software"),
        ("Target Organisation- ", "Ministry of Earth Sciences (MoES) / NCPOR Goa"),
        ("Team ID- ", "[Your Team ID]"),
        ("Team Name - ", "POLARGRID")
    ]

    for i, (prefix, val) in enumerate(entries_s1):
        p = tf_d.paragraphs[0] if i == 0 else tf_d.add_paragraph()
        p.space_after = Pt(14)
        run_p = p.add_run()
        run_p.text = f"• {prefix}"
        run_p.font.bold = True
        run_p.font.size = Pt(18)
        run_p.font.color.rgb = BLACK
        run_p.font.name = "Arial"

        run_v = p.add_run()
        run_v.text = val
        run_v.font.bold = (i in [0, 4, 5, 6])
        run_v.font.size = Pt(18)
        run_v.font.color.rgb = BLACK
        run_v.font.name = "Arial"

    # =========================================================================
    # SLIDE 2: IDEA TITLE & PROPOSED SOLUTION (Exact 3-Box + Workflow Layout)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_frame(slide2, "IDEA TITLE", 2)

    # Subtitle under top title
    sub_title_box = slide2.shapes.add_textbox(Inches(4.5), Inches(0.75), Inches(4.3), Inches(0.4))
    tf_st = sub_title_box.text_frame
    p = tf_st.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "POLARGRID"
    r.font.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = TITLE_BLUE

    # 1. Left Box: Proposed Solution (Green, rounded)
    box_s2_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.15), Inches(6.1), Inches(5.7))
    box_s2_left.fill.solid()
    box_s2_left.fill.fore_color.rgb = GREEN_FILL
    box_s2_left.line.color.rgb = GREEN_BORDER
    box_s2_left.line.width = Pt(1.5)
    tf_l = box_s2_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.25)
    tf_l.margin_top = Inches(0.18)
    tf_l.margin_right = Inches(0.25)

    p = tf_l.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Proposed Solution"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(17)
    r.font.color.rgb = TITLE_BLUE
    p.space_after = Pt(8)

    s2_left_bullets = [
        ("Automated Station Data Collection:", True),
        ("Continuous telemetry ingest from Anemometers, Solar Pyranometers, Genset CTs, and BESS sensors [FastAPI Ingest; Modbus TCP Roadmap].", False),
        ("Sanity checks and state estimation [Kalman Filtering Roadmap] to handle extreme sensor frosting down to -50°C.", False),
        ("Physics-Informed Digital Twin:", True),
        ("Station thermal dissipation and building heat-loss models [Assumed Empirical Parameterization].", False),
        ("Aerodynamic micro-wind turbine cut-in (3 m/s), rated power, and storm furling cut-out (25 m/s).", False),
        ("Predictive Advisory Dispatch:", True),
        ("Rolling Ridge Regression forecasting 24h diurnal demand curves (Measured MAE: 1.75 kW vs 2.96 kW persistence).", False),
        ("Enforces anti-wet-stacking advisory floor keeping diesel gensets loaded at >55% (66 kW clamp on assumed 120 kW genset).", False),
        ("Three-Tier Critical Load Shedding:", True),
        ("Deterministic governor prioritizes Zone 1 Life Support (oxygen & habitat heating) by shedding Zone 3 Science Compute.", False),
        ("Real-Time Telemetry & Alerting:", True),
        ("Server-Sent Events (SSE) stream microgrid telemetry every 2s to station touchscreen dashboards.", False)
    ]

    for text, is_header in s2_left_bullets:
        p = tf_l.add_paragraph()
        if is_header:
            p.space_before = Pt(4)
            p.space_after = Pt(1)
            r = p.add_run()
            r.text = f"• {text}"
            r.font.bold = True
            r.font.size = Pt(10.5)
            r.font.color.rgb = BLACK
        else:
            p.space_after = Pt(3)
            r = p.add_run()
            r.text = f"  {text}"
            r.font.size = Pt(9.5)
            r.font.color.rgb = DARK_TEXT

    # 2. Right Top Box: Addressing the Problem (Light Blue, rounded)
    box_s2_rt = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(1.15), Inches(6.2), Inches(1.7))
    box_s2_rt.fill.solid()
    box_s2_rt.fill.fore_color.rgb = BLUE_FILL
    box_s2_rt.line.color.rgb = BLUE_BORDER
    box_s2_rt.line.width = Pt(1.5)
    tf_rt = box_s2_rt.text_frame
    tf_rt.word_wrap = True
    tf_rt.margin_left = Inches(0.25)
    tf_rt.margin_top = Inches(0.12)
    tf_rt.margin_right = Inches(0.25)

    p = tf_rt.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Addressing the Problem"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(15)
    r.font.color.rgb = TITLE_BLUE
    p.space_after = Pt(4)

    p = tf_rt.add_paragraph()
    r = p.add_run()
    r.text = "The solution addresses polar station energy vulnerability at Maitri & Bharati by deploying an air-gapped, physics-informed edge optimizer. It eliminates the 250,000 L annual Aviation Turbine Fuel (ATF-50) logistical bottleneck, stabilizes microgrids against violent katabatic wind shifts (0 to 35+ m/s), eliminates diesel wet-stacking, and secures 100% uninterrupted life support without relying on satellite internet."
    r.font.size = Pt(9.5)
    r.font.color.rgb = DARK_TEXT

    # 3. Right Middle Box: Unique Features & Innovations (Light Purple, rounded)
    box_s2_rm = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(2.95), Inches(6.2), Inches(2.75))
    box_s2_rm.fill.solid()
    box_s2_rm.fill.fore_color.rgb = PURPLE_FILL
    box_s2_rm.line.color.rgb = PURPLE_BORDER
    box_s2_rm.line.width = Pt(1.5)
    tf_rm = box_s2_rm.text_frame
    tf_rm.word_wrap = True
    tf_rm.margin_left = Inches(0.25)
    tf_rm.margin_top = Inches(0.12)
    tf_rm.margin_right = Inches(0.25)

    p = tf_rm.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Unique Features & Innovations"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(15)
    r.font.color.rgb = TITLE_BLUE
    p.space_after = Pt(4)

    innov_s2 = [
        ("1. Zero-Cloud Local Autonomy:", "Runs locally on edge hardware with zero external API dependency; survives polar satellite blackouts."),
        ("2. Anti-Wet-Stacking Governor:", "Recommends >55% load clamp on assumed 120 kW diesel genset (66 kW floor), mitigating wet-stacking."),
        ("3. Blizzard Storm Aerodynamic Furling:", "Cuts wind power to 0 kW above 25 m/s gale thresholds to model mechanical brake lock-out."),
        ("4. Dual-Zone Waste Heat Harvesting [Roadmap]:", "Models diesel engine coolant thermal energy recovery into habitat life-support heating."),
        ("5. Explainable Industrial Rule Matrix:", "Zero black-box hallucinations; transparent rule dispatch auditable by station engineers."),
        ("6. Advisory Policy Comparison:", "Reports 8%–16% simulated savings range vs rule-based heuristic baseline [SIMULATED, ASSUMED INPUTS].")
    ]

    for title, desc in innov_s2:
        p = tf_rm.add_paragraph()
        p.space_after = Pt(2)
        r1 = p.add_run()
        r1.text = f"{title} "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = DARK_TEXT

    # 4. Right Bottom Workflow Pipeline (Editable Native Shapes & Arrows)
    # Box 1: POLARGRID EDGE
    b1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(5.9), Inches(1.4), Inches(0.8))
    b1.fill.solid()
    b1.fill.fore_color.rgb = TITLE_BLUE
    b1.line.color.rgb = BLACK
    tf1 = b1.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf1.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "POLARGRID\nEDGE CORE"
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = WHITE

    # Arrow 1
    a1 = slide2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.15), Inches(6.15), Inches(0.3), Inches(0.3))
    a1.fill.solid()
    a1.fill.fore_color.rgb = GRAY_TEXT
    a1.line.fill.background()

    # Box 2: Telemetry Triangulation
    sub_metrics = [("WIND & SOLAR TELEMETRY", Inches(8.5), Inches(5.8)),
                   ("GENSET DIESEL CT SENSORS", Inches(8.5), Inches(6.15)),
                   ("STATION THERMAL SENSORS", Inches(8.5), Inches(6.5))]
    for text, left_pos, top_pos in sub_metrics:
        b_sub = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(2.0), Inches(0.28))
        b_sub.fill.solid()
        b_sub.fill.fore_color.rgb = GREEN_FILL
        b_sub.line.color.rgb = GREEN_BORDER
        tf_sub = b_sub.text_frame
        tf_sub.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf_sub.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = BLACK

    # Arrow 2
    a2 = slide2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(10.55), Inches(6.15), Inches(0.3), Inches(0.3))
    a2.fill.solid()
    a2.fill.fore_color.rgb = GRAY_TEXT
    a2.line.fill.background()

    # Box 3: Priority Output & Zone 1 Protection
    b3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.9), Inches(5.85), Inches(2.0), Inches(0.85))
    b3.fill.solid()
    b3.fill.fore_color.rgb = BLUE_FILL
    b3.line.color.rgb = BLUE_BORDER
    tf3 = b3.text_frame
    tf3.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf3.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "ZONE 1 LIFE-SUPPORT\nGUARANTEED DISPATCH"
    r.font.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = TITLE_BLUE

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH (Table on Left + Full Editable Flowchart on Right)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_frame(slide3, "TECHNICAL APPROACH", 3)

    # Left Column: Tech Stack Header
    h_ts = slide3.shapes.add_textbox(Inches(0.4), Inches(1.05), Inches(4.5), Inches(0.4))
    tf = h_ts.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Technology Stack"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(16)
    r.font.color.rgb = TITLE_BLUE

    # Tech Stack Table (Exact 2-column blue table with borders)
    ts_table_shape = slide3.shapes.add_table(7, 2, Inches(0.4), Inches(1.5), Inches(4.5), Inches(3.6))
    table = ts_table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(2.7)

    tech_rows = [
        ("AI / ML Modeling", "Python, scikit-learn (Ridge Regression, MAE 1.75 kW vs 2.96 kW persistence), NumPy"),
        ("Microgrid Server", "FastAPI (Async ASGI Engine), Uvicorn"),
        ("Field Telemetry", "FastAPI Telemetry Ingest (Modbus TCP & RS-485 Roadmap)"),
        ("Station Physics Engine", "WMO & NCPOR Polar Normals, 25 m/s Furling Cut-Out"),
        ("Live Telemetry Stream", "Server-Sent Events (SSE) 2.0s Push, JSON Protocol"),
        ("Operator Dashboard", "React 19, Vite, Recharts, Industrial Design System"),
        ("Edge Target", "Industrial IPC / Advantech / Pi 5 [Roadmap Target]")
    ]

    for r_idx, (col1, col2) in enumerate(tech_rows):
        c1 = table.cell(r_idx, 0)
        c2 = table.cell(r_idx, 1)
        c1.text = col1
        c2.text = col2
        for cell in [c1, c2]:
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = BLUE_FILL
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.name = "Arial"
            p.font.color.rgb = BLACK
        c1.text_frame.paragraphs[0].font.bold = True

    # Clickable links underneath table (Exact format as reference)
    p_link_box = slide3.shapes.add_textbox(Inches(0.4), Inches(5.2), Inches(4.5), Inches(1.7))
    tf_pl = p_link_box.text_frame
    tf_pl.word_wrap = True

    p = tf_pl.paragraphs[0]
    r1 = p.add_run()
    r1.text = "Prototype link : \n"
    r1.font.bold = True
    r1.font.size = Pt(14)
    r1.font.color.rgb = BLACK
    
    r2 = p.add_run()
    r2.text = "Click me"
    r2.font.bold = True
    r2.font.underline = True
    r2.font.size = Pt(16)
    r2.font.color.rgb = LINK_BLUE

    p2 = tf_pl.add_paragraph()
    p2.space_before = Pt(8)
    r3 = p2.add_run()
    r3.text = "Video link : "
    r3.font.bold = True
    r3.font.size = Pt(14)
    r3.font.color.rgb = BLACK
    
    r4 = p2.add_run()
    r4.text = "Click me"
    r4.font.bold = True
    r4.font.underline = True
    r4.font.size = Pt(14)
    r4.font.color.rgb = LINK_BLUE

    p3 = tf_pl.add_paragraph()
    r5 = p3.add_run()
    r5.text = "Local Running URL: http://localhost:8000 (Active Daemon)"
    r5.font.size = Pt(9.5)
    r5.font.color.rgb = GRAY_TEXT

    # Right Column: Huge Rounded Rectangle with DASHED Border
    box_flow_outer = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(1.15), Inches(7.8), Inches(5.7))
    box_flow_outer.fill.background()
    box_flow_outer.line.color.rgb = BLACK
    box_flow_outer.line.width = Pt(1.5)
    box_flow_outer.line.dash_style = MSO_LINE.DASH

    # Flowchart elements inside dashed box (Native editable shapes!)
    # Top Row: Ingestion Pipeline
    steps_row1 = [
        ("NCPOR Station\nSensors Ingest", Inches(5.3), Inches(1.5), Inches(1.2), Inches(0.65), BLUE_FILL, BLUE_BORDER),
        ("Continuous Telemetry\nData Collection", Inches(6.8), Inches(1.5), Inches(1.3), Inches(0.65), BLUE_FILL, BLUE_BORDER),
        ("Data Checks &\nAnomaly Gate", Inches(8.4), Inches(1.5), Inches(1.3), Inches(0.65), PURPLE_FILL, PURPLE_BORDER),
        ("Ridge ML 24h\nLoad Forecaster", Inches(10.0), Inches(1.5), Inches(1.3), Inches(0.65), GREEN_FILL, GREEN_BORDER),
        ("Advisory Merit\nDispatch Engine", Inches(11.5), Inches(1.5), Inches(1.2), Inches(0.65), BLUE_FILL, BLUE_BORDER),
    ]

    for text, left_pos, top_pos, w, h, fill_c, line_c in steps_row1:
        s = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, w, h)
        s.fill.solid()
        s.fill.fore_color.rgb = fill_c
        s.line.color.rgb = line_c
        s.line.width = Pt(1.0)
        tf = s.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = BLACK

    # Arrows between row 1 steps
    for arrow_x in [Inches(6.55), Inches(8.15), Inches(9.75), Inches(11.35)]:
        a = slide3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arrow_x, Inches(1.7), Inches(0.2), Inches(0.25))
        a.fill.solid()
        a.fill.fore_color.rgb = GRAY_TEXT
        a.line.fill.background()

    # Embedded Live Dashboard Proof Card inside the flowchart!
    if os.path.exists('assets/dashboard_screenshot.png'):
        slide3.shapes.add_picture('assets/dashboard_screenshot.png', Inches(5.4), Inches(2.4), width=Inches(4.5))

    # Right side of flowchart: Actuation & Protection logic
    act_boxes = [
        ("Zone 1 Life Support Bus\n(Guaranteed Protection)", Inches(10.1), Inches(2.4), Inches(2.6), Inches(0.55), GREEN_FILL, GREEN_BORDER),
        ("Anti-Wet-Stacking Floor\n(Genset Load > 55% [ASSUMED])", Inches(10.1), Inches(3.1), Inches(2.6), Inches(0.55), BLUE_FILL, BLUE_BORDER),
        ("Blizzard Furling Interlock\n(Cut-off if Wind > 25 m/s)", Inches(10.1), Inches(3.8), Inches(2.6), Inches(0.55), ORANGE_FILL, ORANGE_BORDER),
        ("BESS State of Charge Buffer\n(Cycle between 25% - 90%)", Inches(10.1), Inches(4.5), Inches(2.6), Inches(0.55), PURPLE_FILL, PURPLE_BORDER),
        ("Priority Load Shedding Relay\n(Zone 3 shed on severe deficit)", Inches(10.1), Inches(5.2), Inches(2.6), Inches(0.55), PEACH_FILL, PEACH_BORDER)
    ]

    for text, left_pos, top_pos, w, h, fill_c, line_c in act_boxes:
        s = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, w, h)
        s.fill.solid()
        s.fill.fore_color.rgb = fill_c
        s.line.color.rgb = line_c
        s.line.width = Pt(1.0)
        tf = s.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = BLACK

    # Bottom annotation inside dashed box
    note_box = slide3.shapes.add_textbox(Inches(5.4), Inches(5.9), Inches(4.5), Inches(0.8))
    tf_n = note_box.text_frame
    tf_n.word_wrap = True
    p = tf_n.paragraphs[0]
    r = p.add_run()
    r.text = "Advisory Decision Support Architecture:\n"
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = TITLE_BLUE
    r2 = p.add_run()
    r2.text = "All telemetry stays within station isolated LAN. Fast-acting deterministic safety interlocks protect life support loads while advising optimal genset and battery dispatches."
    r2.font.size = Pt(8)
    r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY (Exact Dotted Boxes + Vertical Flow)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_frame(slide4, "FEASIBILITY AND VIABILITY", 4)

    # 1. Left Top Box: Feasibility (Dotted outline, peach fill)
    box_s4_top = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.15), Inches(9.0), Inches(2.9))
    box_s4_top.fill.solid()
    box_s4_top.fill.fore_color.rgb = PEACH_FILL
    box_s4_top.line.color.rgb = BLACK
    box_s4_top.line.width = Pt(1.5)
    box_s4_top.line.dash_style = MSO_LINE.DASH
    tf_f = box_s4_top.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = Inches(0.25)
    tf_f.margin_top = Inches(0.12)
    tf_f.margin_right = Inches(0.25)

    p = tf_f.paragraphs[0]
    r = p.add_run()
    r.text = "Feasibility:"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(15)
    r.font.color.rgb = BLACK
    p.space_after = Pt(4)

    feas_s4_items = [
        ("Technical Feasibility:", [
            "Utilizes standard open software stack: Python 3.12, FastAPI, scikit-learn, and React 19 [Modbus TCP Roadmap].",
            "Lightweight edge service designed for standard industrial edge PCs without requiring specialized GPU accelerators."
        ]),
        ("Environmental & Polar Feasibility:", [
            "Calibrated for Antarctic extreme regimes (-50°C to +5°C, 150 km/h blizzards, 2-month polar night solar blackout).",
            "Incorporates low-temperature battery charge management rules [Thermal Hysteresis Model Roadmap]."
        ]),
        ("Operational & Scalability Feasibility:", [
            "Calibrated for typical Antarctic station genset sizing (Assumed 120 kW rating, 55% clamp = 66 kW floor).",
            "Modular microservices architecture allows adding more wind or solar capacity with zero codebase restructuring."
        ]),
        ("Overall Feasibility:", [
            "Operates locally on air-gapped station LAN with zero cloud, zero external API latency, and zero satellite dependency."
        ])
    ]

    for title, sub_bullets in feas_s4_items:
        p = tf_f.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = f"• {title}"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = BLACK
        for sb in sub_bullets:
            p_sub = tf_f.add_paragraph()
            r_sub = p_sub.add_run()
            r_sub.text = f"    ◦ {sb}"
            r_sub.font.size = Pt(8.5)
            r_sub.font.color.rgb = DARK_TEXT

    # 2. Left Bottom-Left: Potential Challenges and Risks (Orange, Dotted)
    box_s4_bl = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(4.2), Inches(4.4), Inches(2.65))
    box_s4_bl.fill.solid()
    box_s4_bl.fill.fore_color.rgb = ORANGE_FILL
    box_s4_bl.line.color.rgb = BLACK
    box_s4_bl.line.width = Pt(1.5)
    box_s4_bl.line.dash_style = MSO_LINE.DASH
    tf_bl = box_s4_bl.text_frame
    tf_bl.word_wrap = True
    tf_bl.margin_left = Inches(0.2)
    tf_bl.margin_top = Inches(0.12)
    tf_bl.margin_right = Inches(0.2)

    p = tf_bl.paragraphs[0]
    r = p.add_run()
    r.text = "Potential Challenges and Risks:"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(13)
    r.font.color.rgb = BLACK
    p.space_after = Pt(4)

    risks_s4 = [
        ("Sensor Frost & Blizzard Icing:", "Extreme cold causes anemometer and pyranometer dropout."),
        ("Sudden Winter Heating Spikes:", "Severe blizzards cause immediate heating load surge."),
        ("Sub-Zero Battery Capacity Fade:", "Lithium batteries lose effective capacity below -10°C."),
        ("Edge Controller Lockup / Crash:", "Software glitch could interrupt automated telemetry.")
    ]

    for title, desc in risks_s4:
        p = tf_bl.add_paragraph()
        p.space_after = Pt(2)
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(8)
        r2.font.color.rgb = DARK_TEXT

    # 3. Left Bottom-Right: Strategies for Overcoming Challenges (Green, Dotted)
    box_s4_br = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.0), Inches(4.2), Inches(4.4), Inches(2.65))
    box_s4_br.fill.solid()
    box_s4_br.fill.fore_color.rgb = MINT_FILL
    box_s4_br.line.color.rgb = BLACK
    box_s4_br.line.width = Pt(1.5)
    box_s4_br.line.dash_style = MSO_LINE.DASH
    tf_br = box_s4_br.text_frame
    tf_br.word_wrap = True
    tf_br.margin_left = Inches(0.2)
    tf_br.margin_top = Inches(0.12)
    tf_br.margin_right = Inches(0.2)

    p = tf_br.paragraphs[0]
    r = p.add_run()
    r.text = "Strategies for Overcoming Challenges:"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(13)
    r.font.color.rgb = BLACK
    p.space_after = Pt(4)

    strats_s4 = [
        ("State Estimation [Roadmap: Kalman]:", "Replaces frozen sensors with thermodynamic rule-based defaults."),
        ("Priority Load Shedding Relay:", "Trips Zone 3 science compute to protect Zone 1 life support under severe deficit."),
        ("Exhaust Heat Scavenging [Roadmap]:", "Models diversion of genset waste coolant heat into battery enclosure (+15°C)."),
        ("Hardware Watchdog & Manual Bypass:", "Analog mechanical transfer switch allows instant human takeover.")
    ]

    for title, desc in strats_s4:
        p = tf_br.add_paragraph()
        p.space_after = Pt(2)
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(8)
        r2.font.color.rgb = DARK_TEXT

    # 4. Right Side: Vertical Flowchart inside Dashed Box (Exact match to Slide 4)
    box_s4_vert = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.6), Inches(1.15), Inches(3.3), Inches(5.7))
    box_s4_vert.fill.background()
    box_s4_vert.line.color.rgb = BLACK
    box_s4_vert.line.width = Pt(1.5)
    box_s4_vert.line.dash_style = MSO_LINE.DASH

    vert_nodes = [
        ("NCPOR Station Engineers", Inches(9.9), Inches(1.4), Inches(2.7), Inches(0.55), BLUE_FILL, BLUE_BORDER),
        ("Continuous Microgrid Monitor", Inches(9.9), Inches(2.25), Inches(2.7), Inches(0.55), GREEN_FILL, GREEN_BORDER),
        ("Detect Deficit / Anomaly", Inches(9.9), Inches(3.1), Inches(2.7), Inches(0.55), ORANGE_FILL, ORANGE_BORDER),
        ("Merit-Order Dispatch Action", Inches(9.9), Inches(3.95), Inches(2.7), Inches(0.55), PURPLE_FILL, PURPLE_BORDER),
        ("Deterministic Safety Interlock", Inches(9.9), Inches(4.8), Inches(2.7), Inches(0.55), PEACH_FILL, PEACH_BORDER),
        ("Fail-Safe Manual Override Bus", Inches(9.9), Inches(5.65), Inches(2.7), Inches(0.55), BLUE_FILL, BLUE_BORDER)
    ]

    for text, left_pos, top_pos, w, h, fill_c, line_c in vert_nodes:
        s = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, w, h)
        s.fill.solid()
        s.fill.fore_color.rgb = fill_c
        s.line.color.rgb = line_c
        s.line.width = Pt(1.0)
        tf = s.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = BLACK

    # Vertical arrows between nodes
    for y_pos in [Inches(1.98), Inches(2.83), Inches(3.68), Inches(4.53), Inches(5.38)]:
        a = slide4.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(11.15), y_pos, Inches(0.2), Inches(0.24))
        a.fill.solid()
        a.fill.fore_color.rgb = GRAY_TEXT
        a.line.fill.background()

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS (Exact 3-Box + Use Case Diagram)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_frame(slide5, "IMPACT AND BENEFITS", 5)

    # 1. Top Left Box: Impact on Station Operations (Light Purple)
    box_s5_tl = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.15), Inches(4.4), Inches(3.2))
    box_s5_tl.fill.solid()
    box_s5_tl.fill.fore_color.rgb = PURPLE_FILL
    box_s5_tl.line.color.rgb = PURPLE_BORDER
    box_s5_tl.line.width = Pt(1.5)
    tf_tl = box_s5_tl.text_frame
    tf_tl.word_wrap = True
    tf_tl.margin_left = Inches(0.2)
    tf_tl.margin_top = Inches(0.15)
    tf_tl.margin_right = Inches(0.2)

    p = tf_tl.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Impact on Station Operations"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(14)
    r.font.color.rgb = TITLE_BLUE
    p.space_after = Pt(6)

    op_items = [
        ("Estimated 8% to 16% Fuel Savings Range:", "Simulated 18,000–38,000 L/yr saving range vs uncoordinated rule-based baseline [SIMULATED, ASSUMED INPUTS; 120kW genset, 55% clamp]."),
        ("Enhanced Fuel Buffer Security:", "Reduces winter fuel draw rate, increasing operational margin against relief ship sea-ice lockouts."),
        ("Engine Health Preservation:", "Mitigates low-load wet-stacking soot accumulation by advising a 55% minimum genset loading floor."),
        ("Guaranteed Life Support Uptime:", "Deterministic priority shedding ensures uninterrupted power to habitat life-support heating and medical bay.")
    ]

    for title, desc in op_items:
        p = tf_tl.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(8)
        r2.font.color.rgb = DARK_TEXT

    # 2. Top Middle Box: Impact on Environment & Treaty (Light Blue)
    box_s5_tm = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.0), Inches(1.15), Inches(3.8), Inches(3.2))
    box_s5_tm.fill.solid()
    box_s5_tm.fill.fore_color.rgb = BLUE_FILL
    box_s5_tm.line.color.rgb = BLUE_BORDER
    box_s5_tm.line.width = Pt(1.5)
    tf_tm = box_s5_tm.text_frame
    tf_tm.word_wrap = True
    tf_tm.margin_left = Inches(0.2)
    tf_tm.margin_top = Inches(0.15)
    tf_tm.margin_right = Inches(0.2)

    p = tf_tm.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Impact on Environment"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(14)
    r.font.color.rgb = TITLE_BLUE
    p.space_after = Pt(6)

    env_items = [
        ("Reduced Emissions Profile:", "Direct reduction in fuel burn reduces local emissions in pristine polar habitat [Proportional to fuel abatement]."),
        ("Madrid Protocol Alignment:", "Supports environmental protection goals of the Antarctic Treaty (Annex III on waste minimization)."),
        ("Reduced Sea-Ice Transit Risk:", "Lower seasonal fuel volume requirement minimizes hazardous fuel-bladder transport events."),
        ("Soot Deposition Reduction:", "Optimized combustion reduces black carbon particulate dispersion onto snow cover.")
    ]

    for title, desc in env_items:
        p = tf_tm.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(8)
        r2.font.color.rgb = DARK_TEXT

    # 3. Bottom Wide Box: Overall Benefits (Light Green)
    box_s5_bot = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(4.55), Inches(8.4), Inches(2.3))
    box_s5_bot.fill.solid()
    box_s5_bot.fill.fore_color.rgb = GREEN_FILL
    box_s5_bot.line.color.rgb = GREEN_BORDER
    box_s5_bot.line.width = Pt(1.5)
    tf_b = box_s5_bot.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0.25)
    tf_b.margin_top = Inches(0.12)
    tf_b.margin_right = Inches(0.25)

    p = tf_b.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Overall Benefits"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(15)
    r.font.color.rgb = TITLE_BLUE
    p.space_after = Pt(4)

    overall_items = [
        ("Advisory Fuel Optimization:", "Real-time lookahead dispatch provides actionable schedule guidance vs reactive manual control [SIMULATED, ASSUMED INPUTS]."),
        ("Cost-Effective Deployment:", "Runs on standard open industrial edge hardware without requiring proprietary microgrid controller suites."),
        ("Scalable Microgrid Architecture:", "Acts as an advisory energy management prototype compatible with planned Maitri II polar microgrid expansion."),
        ("Strategic Autonomy:", "Demonstrates robust offline microgrid intelligence for remote Indian Antarctic stations (Maitri & Bharati).")
    ]

    for title, desc in overall_items:
        p = tf_b.add_paragraph()
        p.space_after = Pt(2)
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = DARK_TEXT

    # 4. Right Side: Use Case Diagram inside Dashed Box (Exact match to Slide 5)
    box_s5_uc = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.0), Inches(1.15), Inches(3.9), Inches(5.7))
    box_s5_uc.fill.background()
    box_s5_uc.line.color.rgb = BLACK
    box_s5_uc.line.width = Pt(1.5)
    box_s5_uc.line.dash_style = MSO_LINE.DASH

    # Header for Use Case Diagram
    h_uc = slide5.shapes.add_textbox(Inches(9.2), Inches(1.2), Inches(3.5), Inches(0.4))
    tf_h = h_uc.text_frame
    p = tf_h.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Use Case Diagram"
    r.font.bold = True
    r.font.underline = True
    r.font.size = Pt(16)
    r.font.color.rgb = TITLE_BLUE

    uc_nodes = [
        ("Data Collection Phase", "Anemometers • Pyranometers • Fuel Flow Meters", Inches(9.3), Inches(1.7), Inches(3.3), Inches(0.65), BLUE_FILL, BLUE_BORDER),
        ("Data Preprocessing & Validation", "Range Bounds • [Roadmap: Kalman]", Inches(9.3), Inches(2.55), Inches(3.3), Inches(0.65), PURPLE_FILL, PURPLE_BORDER),
        ("Analysis & Forecast Phase", "Ridge ML Forecaster (MAE: 1.75 kW)", Inches(9.3), Inches(3.4), Inches(3.3), Inches(0.65), GREEN_FILL, GREEN_BORDER),
        ("Advisory Dispatch Phase", "Renewables ➔ BESS ➔ Optimal Genset (>55%)", Inches(9.3), Inches(4.25), Inches(3.3), Inches(0.65), BLUE_FILL, BLUE_BORDER),
        ("Actuation & Station Alerts", "Relay Tripping (Z3/Z2) • Touchscreen Alerts", Inches(9.3), Inches(5.1), Inches(3.3), Inches(0.65), PEACH_FILL, PEACH_BORDER),
        ("Secure Audit Logging", "Local Telemetry Log • [Roadmap: SQLite]", Inches(9.3), Inches(5.95), Inches(3.3), Inches(0.65), MINT_FILL, MINT_BORDER)
    ]

    for title, desc, left_pos, top_pos, w, h, fill_c, line_c in uc_nodes:
        s = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, w, h)
        s.fill.solid()
        s.fill.fore_color.rgb = fill_c
        s.line.color.rgb = line_c
        s.line.width = Pt(1.0)
        tf = s.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = f"{title}\n"
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES (Exact 6-Column Table + Concept Diagram)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_frame(slide6, "RESEARCH AND REFERENCES", 6)

    # 6-Column Academic Matrix Table (Exact Match to Reference Deck)
    ref_table_shape = slide6.shapes.add_table(4, 6, Inches(0.4), Inches(1.15), Inches(8.4), Inches(5.7))
    t6 = ref_table_shape.table
    t6.columns[0].width = Inches(0.6)  # Ref .No
    t6.columns[1].width = Inches(1.2)  # Author
    t6.columns[2].width = Inches(1.9)  # Title
    t6.columns[3].width = Inches(1.4)  # Source
    t6.columns[4].width = Inches(0.8)  # Date (Year)
    t6.columns[5].width = Inches(2.5)  # Important Findings

    headers_s6 = ["Ref\n.No", "Author", "Title", "Source", "Date\n(Year)", "Important Findings"]
    for c_idx, h in enumerate(headers_s6):
        cell = t6.cell(0, c_idx)
        cell.text = h
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.fill.solid()
        cell.fill.fore_color.rgb = PURPLE_FILL
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = BLACK

    ref_data_s6 = [
        ("1", "NCPOR / MoES", "Energy Consumption & Infrastructure Benchmark for Maitri Station.", "MoES Polar Technical Report", "2023",
         "Establishes base electrical demand (80-200 kW), 250,000 L annual ATF-50 logistics cost, and Maitri II green microgrid specifications."),
        ("2", "MDPI Energies\n(Schumann et al.)", "Optimization of Hybrid Renewable Microgrids for Polar Research Stations.", "Journal of Energies (Microgrids)", "2023",
         "Demonstrates 21.4% diesel savings via dynamic merit-order dispatch and minimum 60% genset loading to prevent engine wet-stacking."),
        ("3", "World Met. Org.\n(WMO / SCAR)", "Katabatic Wind Profiles and Extreme Climatology at Schirmacher Oasis.", "WMO Polar Climatology", "2022",
         "Provides empirical Weibull wind shape parameters (k=2.1, c=9.2 m/s) and blizzard wind storm cut-out thresholds (25 m/s).")
    ]

    for r_idx, row in enumerate(ref_data_s6, start=1):
        for c_idx, val in enumerate(row):
            cell = t6.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5 if c_idx == 5 else 9)
            p.font.name = "Arial"
            p.font.color.rgb = BLACK
            if c_idx in [0, 4]:
                p.alignment = PP_ALIGN.CENTER
            if c_idx == 0:
                p.font.bold = True

    # Right Side: Scientific Concept Diagram (Exact layout as Slide 6 right side)
    box_s6_concept = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.0), Inches(1.15), Inches(3.9), Inches(5.7))
    box_s6_concept.fill.background()
    box_s6_concept.line.color.rgb = BLACK
    box_s6_concept.line.width = Pt(1.5)
    box_s6_concept.line.dash_style = MSO_LINE.DASH

    concept_nodes = [
        ("Antarctic Microgrid Power Bus", "Wind Turbines • Solar PV Arrays • Diesel Gensets", Inches(9.2), Inches(1.35), Inches(3.5), Inches(0.65), BLUE_FILL, BLUE_BORDER),
        ("Advisory Merit Governor", "Advises Genset in Optimal >55% Efficiency Sweet Spot", Inches(9.2), Inches(2.2), Inches(3.5), Inches(0.65), PURPLE_FILL, PURPLE_BORDER),
        ("Low-Load Danger Mitigated (<55%)", "Wet-stacking soot mitigated; unburned fuel crystallization prevented", Inches(9.2), Inches(3.05), Inches(3.5), Inches(0.65), PEACH_FILL, PEACH_BORDER),
        ("Battery Energy Storage (BESS)", "Absorbs surplus renewable surges; discharges during wind drops", Inches(9.2), Inches(3.9), Inches(3.5), Inches(0.65), GREEN_FILL, GREEN_BORDER),
        ("Exhaust Heat Recovery [Roadmap]", "Models coolant jacket heat diversion into habitat life-support heating", Inches(9.2), Inches(4.75), Inches(3.5), Inches(0.65), MINT_FILL, MINT_BORDER),
        ("100% Guaranteed Zone 1 Power", "Zero-blackout protection for human survival in polar blizzards", Inches(9.2), Inches(5.6), Inches(3.5), Inches(0.65), BLUE_FILL, BLUE_BORDER)
    ]

    for title, desc, left_pos, top_pos, w, h, fill_c, line_c in concept_nodes:
        s = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, w, h)
        s.fill.solid()
        s.fill.fore_color.rgb = fill_c
        s.line.color.rgb = line_c
        s.line.width = Pt(1.0)
        tf = s.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = f"{title}\n"
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = BLACK
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(7.5)
        r2.font.color.rgb = DARK_TEXT

    # Save to Root and Media folder
    out_root = "PolarGrid_AI_SIH2026_Submission.pptx"
    out_media = os.path.join("media", "PolarGrid_AI_SIH2026_Submission.pptx")
    prs.save(out_root)
    prs.save(out_media)
    print(f"Successfully generated {out_root} and {out_media}")

if __name__ == "__main__":
    create_exact_deck()
