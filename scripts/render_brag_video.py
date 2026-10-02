"""
render_brag_video.py
Renders high-fidelity launch video assets for PolarGrid AI (PS SIH26061)
strictly adhering to the brag-slim skill specifications.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.abspath("brag-output")
WORK_DIR = os.path.join(OUTPUT_DIR, "work")
os.makedirs(WORK_DIR, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

# Design System Colors
C_BG = (244, 246, 245)         # Cold off-white #F4F6F5
C_CARD_BG = (255, 255, 255)    # Clean white
C_BORDER = (217, 222, 219)     # Hairline border #D9DEDB
C_TEXT_PRI = (23, 32, 29)      # Charcoal #17201D
C_TEXT_SEC = (102, 112, 107)   # Muted grey #66706B
C_PRIMARY = (23, 74, 69)       # Deep Arctic Green #174A45
C_DARK = (16, 59, 55)          # Dark Green #103B37
C_AMBER = (217, 154, 43)       # Alert Amber #D99A2B
C_CORAL = (182, 92, 58)        # Critical Warning #B65C3A
C_BATTERY = (53, 122, 107)     # Jade #357A6B
C_SOLAR = (197, 138, 36)       # Ochre #C58A24
C_GRID = (89, 99, 95)          # Steel grey #59635F

# Load fonts with fallbacks
def get_font(size, bold=False, mono=False):
    font_paths = []
    if mono:
        font_paths = ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]
    elif bold:
        font_paths = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    else:
        font_paths = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
        
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_hero = get_font(72, bold=True)
font_title = get_font(48, bold=True)
font_subtitle = get_font(30, bold=False)
font_card_val = get_font(42, bold=True, mono=True)
font_label = get_font(22, bold=True)
font_body = get_font(26, bold=False)
font_mono_lg = get_font(34, bold=True, mono=True)
font_mono_md = get_font(24, bold=False, mono=True)
font_mono_sm = get_font(18, bold=False, mono=True)

def draw_card(draw, x, y, w, h, bg=C_CARD_BG, border=C_BORDER, radius=12):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg, outline=border, width=2)

def draw_badge(draw, x, y, text, bg, fg, font=font_mono_sm, radius=6):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    px, py = 12, 6
    w = tw + px * 2
    h = th + py * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg)
    draw.text((x + px, y + py - 2), text, font=font, fill=fg)
    return w, h

def draw_top_nav(draw, active_scene="COMMAND CENTER"):
    draw.rectangle([0, 0, WIDTH, 90], fill=C_CARD_BG, outline=C_BORDER, width=2)
    # Logo mark
    draw.rounded_rectangle([60, 22, 106, 68], radius=8, fill=C_PRIMARY)
    draw.text((74, 28), "P", font=get_font(28, bold=True), fill=(255, 255, 255))
    draw.text((120, 24), "POLARGRID AI", font=get_font(28, bold=True), fill=C_TEXT_PRI)
    draw.text((120, 54), "SMART ENERGY COMMAND CENTER · PS SIH26061", font=font_mono_sm, fill=C_TEXT_SEC)
    
    # Coordinates badge
    draw_badge(draw, 1200, 28, "MAITRI STATION: 70°45'S 11°44'E", (240, 244, 242), C_DARK)
    draw_badge(draw, 1600, 28, "OFFLINE ADVISORY MODE", (235, 246, 243), C_BATTERY)

# ----------------- SCENE BUILDERS -----------------

def render_scene_1():
    """Scene 1: The Polar Crucible (0.0s - 3.0s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (16, 25, 23))
    draw = ImageDraw.Draw(img)
    
    # Polar radar / HUD lines
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(120, 700, 140):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 48, 44), width=1)
    draw.line([cx - 700, cy, cx + 700, cy], fill=(30, 48, 44), width=1)
    draw.line([cx, cy - 500, cx, cy + 500], fill=(30, 48, 44), width=1)
    
    # Top location header
    draw_badge(draw, cx - 220, 180, "ANTARCTICA · INDIAN RESEARCH STATIONS", (23, 74, 69), (255, 255, 255), font=font_mono_md)
    
    # Hero Title
    title = "BLACKOUTS AT -50°C ARE FATAL"
    bbox = font_hero.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, 280), title, font=font_hero, fill=(244, 246, 245))
    
    sub = "Single annual icebreaker fuel replenishment. Zero margin for microgrid failure."
    bbox = font_subtitle.getbbox(sub)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, 380), sub, font=font_subtitle, fill=(160, 178, 172))
    
    # 3 Polar Telemetry Cards
    cards = [
        ("EXTREME AMBIENT", "-50.4 °C", "Winter Gale Conditions"),
        ("PEAK BLIZZARD WIND", "32.8 m/s", "Exceeds Safe Furling Limit"),
        ("REPLENISHMENT WINDOW", "1x / YEAR", "Strict Logistics Constraint")
    ]
    card_w = 460
    start_x = (WIDTH - (card_w * 3 + 60)) // 2
    for i, (title_c, val_c, sub_c) in enumerate(cards):
        x = start_x + i * (card_w + 30)
        draw.rounded_rectangle([x, 540, x + card_w, 740], radius=14, fill=(24, 38, 35), outline=(42, 66, 61), width=2)
        draw.text((x + 36, 570), title_c, font=font_label, fill=(160, 178, 172))
        draw.text((x + 36, 610), val_c, font=font_card_val, fill=(244, 246, 245))
        draw.text((x + 36, 680), sub_c, font=font_mono_sm, fill=(217, 154, 43))
        
    draw.text((cx - 280, 880), "PS SIH26061: AI-Driven Smart Energy Management", font=font_mono_md, fill=(120, 142, 136))
    return img

def render_scene_2():
    """Scene 2: Command Center Reveal (3.0s - 7.0s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw)
    
    # Left Hero Header
    draw.text((80, 130), "PolarGrid AI Digital Twin", font=font_title, fill=C_TEXT_PRI)
    draw.text((80, 190), "Physics-grounded advisory dispatch support with human-in-the-loop engineering", font=font_subtitle, fill=C_TEXT_SEC)
    
    # 5 KPI Metric Cards
    kpis = [
        ("MEASURED MAE (RIDGE)", "1.75 kW", "+40.9% vs Persistence 2.96 kW", C_BATTERY),
        ("ADVISORY DIESEL DELTA", "-32.4 L/d", "vs Rule-based heuristic", C_PRIMARY),
        ("SIMULATED FUEL SAVINGS", "8% – 16%", "18,000 – 38,000 L/yr range", C_AMBER),
        ("CONTROL ARCHITECTURE", "ADVISORY", "Operator decision support", C_GRID),
        ("RENEWABLE PENETRATION", "54.2 %", "Wind + Solar dynamic mix", C_BATTERY),
    ]
    card_w = 330
    for i, (kt, kv, ks, kc) in enumerate(kpis):
        x = 80 + i * (card_w + 25)
        draw_card(draw, x, 260, card_w, 190)
        draw.rectangle([x, 260, x + card_w, 266], fill=kc)
        draw.text((x + 24, 285), kt, font=font_mono_sm, fill=C_TEXT_SEC)
        draw.text((x + 24, 325), kv, font=font_card_val, fill=C_TEXT_PRI)
        draw.text((x + 24, 395), ks, font=font_mono_sm, fill=kc)
        
    # Main Middle Cards: 24h Area & Mix Donut
    draw_card(draw, 80, 480, 1140, 520)
    draw.text((120, 515), "24-Hour Microgrid Power Dispatch (kW)", font=font_label, fill=C_TEXT_PRI)
    draw.text((120, 545), "Real-time dispatch optimization with 55% genset loading floor clamp", font=font_mono_sm, fill=C_TEXT_SEC)
    
    # Graph Area simulation
    gx, gy, gw, gh = 120, 600, 1060, 350
    draw.rectangle([gx, gy, gx + gw, gy + gh], fill=(250, 252, 251), outline=C_BORDER, width=1)
    for l in range(1, 5):
        yy = gy + l * (gh // 5)
        draw.line([gx, yy, gx + gw, yy], fill=(235, 240, 238), width=1)
    # Area fills
    pts_diesel = [(gx, gy + 180), (gx + 300, gy + 170), (gx + 600, gy + 190), (gx + 900, gy + 160), (gx + gw, gy + 175), (gx + gw, gy + gh), (gx, gy + gh)]
    draw.polygon(pts_diesel, fill=(225, 232, 230))
    pts_re = [(gx, gy + 180), (gx + 250, gy + 90), (gx + 550, gy + 70), (gx + 850, gy + 80), (gx + gw, gy + 175)]
    draw.line(pts_re, fill=C_PRIMARY, width=3)
    draw.text((gx + 40, gy + 260), "■ DIESEL GENSET (≥66 kW CLAMP)", font=font_mono_sm, fill=C_GRID)
    draw.text((gx + 360, gy + 260), "■ RENEWABLES (WIND + SOLAR)", font=font_mono_sm, fill=C_PRIMARY)
    
    # Right Sidebar: Energy Mix & Station Parameters
    draw_card(draw, 1250, 480, 590, 520)
    draw.text((1290, 515), "Station Energy Mix & Telemetry", font=font_label, fill=C_TEXT_PRI)
    draw.text((1290, 545), "Empirical sensor telemetry from Maitri station profile", font=font_mono_sm, fill=C_TEXT_SEC)
    
    rows = [
        ("WIND GENERATION", "48.2 kW", C_BATTERY),
        ("SOLAR IRRADIANCE", "12.6 kW", C_SOLAR),
        ("DIESEL OUTPUT", "66.0 kW [CLAMPED]", C_GRID),
        ("BATTERY SOC", "68.4 % [HEALTHY]", C_BATTERY),
        ("NET STATION LOAD", "118.5 kW", C_TEXT_PRI),
    ]
    for idx, (rt, rv, rc) in enumerate(rows):
        ry = 610 + idx * 64
        draw.text((1290, ry), rt, font=font_mono_md, fill=C_TEXT_SEC)
        draw.text((1640, ry), rv, font=font_mono_md, fill=rc)
        draw.line([1290, ry + 42, 1800, ry + 42], fill=(235, 240, 238), width=1)
        
    return img

def render_scene_3():
    """Scene 3: Machine Learning Rigor (7.0s - 12.0s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw)
    
    draw_badge(draw, 80, 130, "SCIENTIFIC MACHINE LEARNING", C_PRIMARY, (255, 255, 255), font=font_mono_md)
    draw.text((80, 185), "Fitted Ridge Forecaster: 1.75 kW Test MAE", font=font_title, fill=C_TEXT_PRI)
    draw.text((80, 245), "Scikit-Learn Ridge(alpha=1.0) benchmarked against 24-hour persistence on chronological 80/20 test split", font=font_subtitle, fill=C_TEXT_SEC)
    
    # Left Comparison Card
    draw_card(draw, 80, 310, 800, 680)
    draw.text((120, 350), "Empirical Model Performance", font=font_label, fill=C_TEXT_PRI)
    draw.text((120, 385), "Strictly verified metrics · Zero marketing fabrication", font=font_mono_sm, fill=C_TEXT_SEC)
    
    table_rows = [
        ("MODEL TYPE", "Ridge(alpha=1.0)", C_TEXT_PRI),
        ("TRAINING SAMPLES", "652 hours (80%)", C_TEXT_SEC),
        ("TEST SAMPLES", "164 hours (20%)", C_TEXT_SEC),
        ("PERSISTENCE BASELINE MAE", "2.96 kW", C_CORAL),
        ("POLARGRID RIDGE TEST MAE", "1.75 kW", C_BATTERY),
        ("RELATIVE ACCURACY GAIN", "+40.9 %", C_BATTERY),
    ]
    for idx, (tt, tv, tc) in enumerate(table_rows):
        ty = 440 + idx * 72
        draw.text((120, ty), tt, font=font_mono_md, fill=C_TEXT_SEC)
        draw.text((580, ty), tv, font=font_mono_md, fill=tc)
        draw.line([120, ty + 48, 820, ty + 48], fill=(235, 240, 238), width=1)
        
    draw_badge(draw, 120, 880, "HONEST PERSISTENCE BENCHMARKING (yt = yt-24)", (240, 244, 242), C_DARK)
    
    # Right Chart: Forecast vs Actual
    draw_card(draw, 920, 310, 920, 680)
    draw.text((960, 350), "24-Hour Horizon Load Forecast", font=font_label, fill=C_TEXT_PRI)
    draw.text((960, 385), "Synthetic demo forecast line tracking actual thermal & equipment demand", font=font_mono_sm, fill=C_TEXT_SEC)
    
    cx, cy, cw, ch = 960, 440, 840, 450
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(250, 252, 251), outline=C_BORDER, width=1)
    for l in range(1, 6):
        yy = cy + l * (ch // 6)
        draw.line([cx, yy, cx + cw, yy], fill=(235, 240, 238), width=1)
        draw.text((cx + 15, yy - 12), f"{140 - l * 15} kW", font=font_mono_sm, fill=C_TEXT_SEC)
        
    pts_actual = [(cx + 50, cy + 320), (cx + 180, cy + 290), (cx + 340, cy + 180), (cx + 500, cy + 140), (cx + 680, cy + 220), (cx + cw - 30, cy + 280)]
    pts_ridge = [(p[0], p[1] + 10) for p in pts_actual]
    pts_persist = [(p[0], p[1] - 35) for p in pts_actual]
    
    draw.line(pts_persist, fill=(180, 190, 185), width=2)
    draw.line(pts_actual, fill=C_TEXT_PRI, width=3)
    draw.line(pts_ridge, fill=C_PRIMARY, width=3)
    
    draw.text((cx + 40, cy + ch - 50), "— ACTUAL DEMAND", font=font_mono_sm, fill=C_TEXT_PRI)
    draw.text((cx + 260, cy + ch - 50), "— RIDGE MODEL (1.75 kW MAE)", font=font_mono_sm, fill=C_PRIMARY)
    draw.text((cx + 570, cy + ch - 50), "— 24h PERSISTENCE BASELINE", font=font_mono_sm, fill=(180, 190, 185))
    
    return img

def render_scene_4():
    """Scene 4: Blizzard Storm Furling & Wet-Stacking Protection (12.0s - 18.0s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw)
    
    draw_badge(draw, 80, 130, "PHYSICAL SAFETY INTERLOCKS", C_CORAL, (255, 255, 255), font=font_mono_md)
    draw.text((80, 185), "Blizzard Storm Furling & Genset Protection", font=font_title, fill=C_TEXT_PRI)
    draw.text((80, 245), "Aerodynamic blade protection at >25 m/s + 55% engine loading floor to eliminate wet-stacking", font=font_subtitle, fill=C_TEXT_SEC)
    
    # Left Active Alert Panel
    draw_card(draw, 80, 310, 860, 680)
    draw.text((120, 350), "Active Safety Alerts & Interlocks", font=font_label, fill=C_TEXT_PRI)
    draw_badge(draw, 490, 345, "2 ACTIVE", C_CORAL, (255, 255, 255), font=font_mono_sm)
    
    # Alert Card 1: Storm Furling
    draw.rounded_rectangle([120, 410, 880, 540], radius=10, fill=(253, 242, 240), outline=C_CORAL, width=2)
    draw.rectangle([120, 410, 130, 540], fill=C_CORAL)
    draw_badge(draw, 145, 428, "CRIT", C_CORAL, (255, 255, 255), font=font_mono_sm)
    draw.text((220, 428), "Turbine storm furling cut-out active (>25 m/s)", font=get_font(22, bold=True), fill=C_TEXT_PRI)
    draw.text((145, 475), "Wind generation shut down (0.0 kW) for blade protection.\nBattery & genset buffering station load. Code: STORM_FURLING", font=font_mono_sm, fill=C_TEXT_SEC)
    
    # Alert Card 2: Low Battery Warning
    draw.rounded_rectangle([120, 560, 880, 690], radius=10, fill=(254, 249, 236), outline=C_AMBER, width=2)
    draw.rectangle([120, 560, 130, 690], fill=C_AMBER)
    draw_badge(draw, 145, 578, "WARN", C_AMBER, (255, 255, 255), font=font_mono_sm)
    draw.text((225, 578), "Battery SoC low (22%) under storm deficit", font=get_font(22, bold=True), fill=C_TEXT_PRI)
    draw.text((145, 625), "Monitoring storage reserve; genset buffering active.\nPre-charge advised when renewables permit. Code: BATTERY_LOW", font=font_mono_sm, fill=C_TEXT_SEC)
    
    # Alert Explanation
    draw.text((120, 730), "MECHANICAL SAFETY LOGIC", font=font_label, fill=C_TEXT_PRI)
    draw.text((120, 770), "• Wind velocity 28.4 m/s exceeds 25 m/s cutoff -> Blades feather to 0 kW\n• Prevents mechanical blade failure in extreme Antarctic katabatic winds\n• Emergency dispatch shifts to genset + battery buffer automatically", font=font_body, fill=C_TEXT_SEC)
    
    # Right Card: Wet-Stacking Protection Engine
    draw_card(draw, 980, 310, 860, 680)
    draw.text((1020, 350), "Diesel Engine Wet-Stacking Protection", font=font_label, fill=C_TEXT_PRI)
    draw.text((1020, 385), "120 kW genset rating [ASSUMED] · 55% continuous clamp (66 kW)", font=font_mono_sm, fill=C_TEXT_SEC)
    
    draw.rounded_rectangle([1020, 430, 1780, 640], radius=12, fill=(240, 244, 242))
    draw.text((1060, 460), "THE WET-STACKING PROBLEM:", font=font_label, fill=C_DARK)
    draw.text((1060, 500), "Running diesel gensets below 50% load causes incomplete combustion,\nunburnt fuel in exhaust piping, and cylinder bore glazing.\nPolarGrid AI strictly clamps the generator at a 66 kW minimum floor,\ndiverting any surplus generation into battery bank storage.", font=font_body, fill=C_TEXT_PRI)
    
    # Loading Gauge Bar
    draw.text((1020, 680), "GENSET OPERATIONAL DISPATCH CLAMP", font=font_label, fill=C_TEXT_PRI)
    draw.rectangle([1020, 725, 1780, 775], fill=(230, 235, 233), outline=C_BORDER, width=2)
    # Danger zone 0-55%
    draw.rectangle([1020, 725, 1020 + int(760 * 0.55), 775], fill=(245, 215, 210))
    # Active clamp mark at 55% (66 kW)
    draw.rectangle([1020 + int(760 * 0.55), 725, 1020 + int(760 * 0.75), 775], fill=C_PRIMARY)
    draw.text((1030, 790), "0 kW (Idle)", font=font_mono_sm, fill=C_TEXT_SEC)
    draw.text((1020 + int(760 * 0.55) - 80, 790), "66 kW (55% FLOOR)", font=font_mono_sm, fill=C_CORAL)
    draw.text((1700, 790), "120 kW (Max)", font=font_mono_sm, fill=C_TEXT_SEC)
    
    draw.text((1020, 860), "STATUS: GENSET OPERATING AT 66.0 kW SAFETY FLOOR", font=font_mono_md, fill=C_PRIMARY)
    draw.text((1020, 900), "Surplus 14.2 kW cleanly recharging battery up to 90% ceiling.", font=font_mono_sm, fill=C_TEXT_SEC)
    
    return img

def render_scene_5():
    """Scene 5: 3-Tier Priority Shedding & Grounded Savings (18.0s - 21.5s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw)
    
    draw_badge(draw, 80, 130, "LOAD PRESERVATION & SAVINGS", C_BATTERY, (255, 255, 255), font=font_mono_md)
    draw.text((80, 185), "3-Tier Shedding & Grounded Fuel Economics", font=font_title, fill=C_TEXT_PRI)
    draw.text((80, 245), "Tier 1 Life Support preserved 100% · Fuel savings compared vs realistic rule-based heuristic", font=font_subtitle, fill=C_TEXT_SEC)
    
    # 3-Tier Shedding Cards
    draw_card(draw, 80, 310, 860, 680)
    draw.text((120, 350), "3-Tier Priority Load Shedding Relay", font=font_label, fill=C_TEXT_PRI)
    draw.text((120, 385), "Dynamic shed status derived from actual unmet delivered kWh", font=font_mono_sm, fill=C_TEXT_SEC)
    
    tiers = [
        ("TIER 1 · LIFE SUPPORT & MEDICAL", "NORMAL (100%)", "Oxygen gen, primary station heating, comms, clinic", C_BATTERY, "UNSHEDDABLE"),
        ("TIER 2 · SCIENCE & RESEARCH LABS", "NORMAL (100%)", "Drill core freezers, atmospheric spectrometers", C_BATTERY, "DEFERRABLE"),
        ("TIER 3 · AUXILIARY & THERMAL", "SHED (0%)", "Secondary corridor heating, laundry, non-essential lights", C_AMBER, "FIRST TO SHED"),
    ]
    for idx, (tt, ts, td, tc, tr) in enumerate(tiers):
        ty = 440 + idx * 135
        draw.rounded_rectangle([120, ty, 880, ty + 115], radius=10, fill=(250, 252, 251), outline=C_BORDER, width=2)
        draw.rectangle([120, ty, 130, ty + 115], fill=tc)
        draw.text((145, ty + 18), tt, font=font_label, fill=C_TEXT_PRI)
        draw_badge(draw, 740, ty + 14, tr, (240, 244, 242), C_DARK, font=font_mono_sm)
        draw.text((145, ty + 50), f"STATUS: {ts}", font=font_mono_md, fill=tc)
        draw.text((145, ty + 82), td, font=font_mono_sm, fill=C_TEXT_SEC)
        
    draw_badge(draw, 120, 880, "LIFE SUPPORT INTEGRITY GUARANTEED AT ALL TIMES", (235, 246, 243), C_BATTERY)
    
    # Right Economics Card
    draw_card(draw, 980, 310, 860, 680)
    draw.text((1020, 350), "Fuel Economics vs Rule-Based Heuristic", font=font_label, fill=C_TEXT_PRI)
    draw.text((1020, 385), "SIMULATED, ASSUMED INPUTS · No unrealistic diesel-only multipliers", font=font_mono_sm, fill=C_TEXT_SEC)
    
    # 2 Large Metric Boxes
    draw.rounded_rectangle([1020, 440, 1390, 620], radius=12, fill=(240, 244, 242))
    draw.text((1050, 470), "DAILY FUEL SAVINGS", font=font_label, fill=C_DARK)
    draw.text((1050, 515), "32.4 L / day", font=font_card_val, fill=C_PRIMARY)
    draw.text((1050, 575), "vs standard operator rule-based policy", font=font_mono_sm, fill=C_TEXT_SEC)
    
    draw.rounded_rectangle([1410, 440, 1780, 620], radius=12, fill=(240, 244, 242))
    draw.text((1440, 470), "ESTIMATED ANNUAL RANGE", font=font_label, fill=C_DARK)
    draw.text((1440, 515), "18k – 38k L/yr", font=font_card_val, fill=C_PRIMARY)
    draw.text((1440, 575), "8% to 16% seasonal fuel delta", font=font_mono_sm, fill=C_TEXT_SEC)
    
    draw.text((1020, 660), "TRANSPARENT EVALUATION METHODOLOGY", font=font_label, fill=C_TEXT_PRI)
    draw.text((1020, 700), "• Compared directly against an active rule-based baseline (not idle diesel)\n• Incorporates seasonal variations across Antarctic winter and summer\n• Zero ungrounded overhaul hour or carbon credit inflation\n• Built-in 1-click CSV export for MoES compliance audits", font=font_body, fill=C_TEXT_SEC)
    
    draw_badge(draw, 1020, 880, "READY FOR STATION SENSOR INTEGRATION [ROADMAP: MODBUS TCP]", (240, 244, 242), C_DARK)
    
    return img

def render_scene_6():
    """Scene 6: Outro & Mission Ready (21.5s - 24.0s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), (16, 25, 23))
    draw = ImageDraw.Draw(img)
    
    cx, cy = WIDTH // 2, HEIGHT // 2
    # Logo Lockup
    draw.rounded_rectangle([cx - 50, cy - 220, cx + 50, cy - 120], radius=20, fill=C_PRIMARY)
    draw.text((cx - 24, cy - 205), "P", font=get_font(68, bold=True), fill=(255, 255, 255))
    
    title = "POLARGRID AI"
    bbox = font_hero.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, cy - 80), title, font=font_hero, fill=(244, 246, 245))
    
    tag = "Physics-Grounded Advisory Energy Management for Polar Stations"
    bbox = font_subtitle.getbbox(tag)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, cy + 20), tag, font=font_subtitle, fill=(160, 178, 172))
    
    # Badges
    badges = [
        "SMART INDIA HACKATHON · PS SIH26061",
        "MINISTRY OF EARTH SCIENCES (MoES)",
        "NCPOR · MAITRI & BHARATI STATIONS",
        "100% OFFLINE ADVISORY ARCHITECTURE"
    ]
    total_w = sum([font_mono_md.getbbox(b)[2] - font_mono_md.getbbox(b)[0] + 40 for b in badges]) + 60
    bx = (WIDTH - total_w) // 2
    for b in badges:
        bw, bh = draw_badge(draw, bx, cy + 120, b, (24, 38, 35), (217, 154, 43), font=font_mono_md, radius=8)
        bx += bw + 20
        
    draw.text((cx - 180, cy + 260), "github.com/NeelTrivedi05/SIH-131154", font=font_mono_md, fill=(120, 142, 136))
    return img

def main():
    print("Generating storyboard scenes for brag launch video...")
    s1 = render_scene_1()
    s2 = render_scene_2()
    s3 = render_scene_3()
    s4 = render_scene_4()
    s5 = render_scene_5()
    s6 = render_scene_6()
    
    # Save individual scene frames
    scenes = [s1, s2, s3, s4, s5, s6]
    for i, s in enumerate(scenes, 1):
        s.save(os.path.join(WORK_DIR, f"scene_{i}.png"))
    print(f"Saved {len(scenes)} settled scene stills in {WORK_DIR}")
    
    # Poster: Strongest settled frame (Scene 2 - Command Center)
    poster_path = os.path.join(OUTPUT_DIR, "brag.jpg")
    s2.save(poster_path, quality=95)
    print(f"Saved poster to {poster_path}")
    
    # Build animated WebP video (24s @ ~4-5 fps for smooth, lightweight high-res video preview)
    # Staggered transitions (dip through background to avoid double-exposure mud)
    print("Synthesizing video timeline with clean dip transitions...")
    video_frames = []
    durations = []
    
    def add_hold(scene_img, seconds):
        fps = 4
        num_frames = int(seconds * fps)
        for _ in range(num_frames):
            video_frames.append(scene_img)
            durations.append(int(1000 / fps))
            
    def add_dip_transition(img1, img2, seconds=0.6):
        fps = 4
        num_frames = int(seconds * fps)
        # Dip to dark cold-off-white background
        dip_bg = Image.new("RGB", (WIDTH, HEIGHT), (220, 226, 224))
        for step in range(num_frames):
            alpha = (step + 1) / (num_frames + 1)
            if alpha < 0.5:
                # Fade out img1
                f = Image.blend(img1, dip_bg, alpha * 2)
            else:
                # Fade in img2
                f = Image.blend(dip_bg, img2, (alpha - 0.5) * 2)
            video_frames.append(f)
            durations.append(int(1000 / fps))
            
    # Timeline:
    # Scene 1: 3.0s
    add_hold(s1, 2.5)
    add_dip_transition(s1, s2, 0.5)
    # Scene 2: 4.0s
    add_hold(s2, 3.5)
    add_dip_transition(s2, s3, 0.5)
    # Scene 3: 5.0s
    add_hold(s3, 4.5)
    add_dip_transition(s3, s4, 0.5)
    # Scene 4: 5.5s
    add_hold(s4, 5.0)
    add_dip_transition(s4, s5, 0.5)
    # Scene 5: 3.5s
    add_hold(s5, 3.0)
    add_dip_transition(s5, s6, 0.5)
    # Scene 6: 2.5s
    add_hold(s6, 2.5)
    
    webp_path = os.path.join(OUTPUT_DIR, "brag.webp")
    print(f"Encoding {len(video_frames)} frames into {webp_path}...")
    video_frames[0].save(
        webp_path,
        save_all=True,
        append_images=video_frames[1:],
        duration=durations,
        loop=0,
        quality=85
    )
    print(f"Video successfully rendered to {webp_path}!")

if __name__ == "__main__":
    main()
