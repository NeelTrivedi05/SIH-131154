# CONTEXT.md — Complete Project Context & Intelligence
## Project: PolarGrid AI (Problem Statement: SIH26061)

---

## 1. Executive Summary & Problem Classification
* **Problem Statement ID**: SIH26061
* **Title**: AI-Driven Smart Energy Management System for Polar Research Stations
* **Category**: Software (Industrial Edge Computing & Applied AI)
* **Theme**: Clean & Green Technology
* **Sponsoring Authority**: Ministry of Earth Sciences (MoES), Government of India
* **Implementing Organization**: National Centre for Polar and Ocean Research (NCPOR), Goa
* **Target Research Stations**:
  * **Maitri Station** (Established 1989, 70°45′58″S, 11°44′09″E, Schirmacher Oasis, Queen Maud Land, Antarctica)
  * **Bharati Station** (Established 2012, 69°24′29″S, 76°11′14″E, Larsemann Hills, Antarctica)
  * **Maitri II (Projected Base)**: Planned green research base scheduled for commissioning by January 2029, featuring hybrid solar PV and wind microgrid installations.

---

## 2. Real-World Grounded Constraints (Strict Anti-Slop Discipline)

### A. The Extreme Antarctic Operating Environment
* **Extreme Temperatures**: Ambient temperatures fluctuate between **-50°C in winter** and **+5°C in brief summer**.
* **Katabatic Wind Profile**: Sudden katabatic winds descending from the continental polar ice cap regularly surge from gentle breezes (3–5 m/s) to destructive gale forces (**>35 m/s or 125+ km/h**) within minutes.
* **Weibull Distribution Parameters**: Schirmacher Oasis climate data shows a Weibull shape parameter $k = 2.1$ and scale parameter $c = 9.2\text{ m/s}$.
* **Polar Night Solar Blackout**: From late May to mid-August (~60 to 75 days), solar irradiance is strictly **$0\text{ W/m}^2$** (total darkness). Peak summer solar irradiance reaches **350–420 W/m²**.

### B. The Station Electrical & Thermal Profile
* **Station Electrical Demand**: Base electrical load is **80 kW to 120 kW** in summer, spiking to **160 kW to 200 kW** during severe winter storms due to life-support habitat heating and trace-heating on water supply pipes (Lake Priyadarshini water delivery line).
* **Generation Infrastructure**:
  * Primary Power: Multi-unit diesel gensets (Caterpillar / Kirloskar 62.5 kVA & 125 kVA industrial engines).
  * Fuel Type: High-grade Aviation Turbine Fuel (**ATF-50 / Jet A-1 with anti-icing additives**), remaining fluid down to -50°C.
  * Station Annual Consumption: **~250,000 Litres of ATF-50 per year** at Maitri.
  * Renewable Assets: Micro-wind turbines (horizontal/vertical axis rated 3–25 m/s) and rooftop bifacial solar PV arrays.
  * Energy Storage: Battery Energy Storage System (BESS) — Lithium Iron Phosphate (LiFePO4) or specialized cold-climate Lead-Acid gel banks.

### C. The Two Fatal Engineering Problems
1. **Low-Load Engine Wet-Stacking (<40% Loading)**:
   * When renewable wind generation surges during low electrical demand, diesel gensets are forced to run at very light loads (<40% capacity).
   * In extreme cold, combustion cylinder temperatures drop below the fuel vaporization threshold.
   * Result: Unburned fuel and carbon black crystallize on turbocharger blades and exhaust manifolds ("wet-stacking"), causing soot fouling, engine stalling, emergency shutdowns, and up to **30% fuel wastage**.
2. **Logistical Supply Vulnerability & Cost**:
   * Fuel can only be delivered to Antarctica once a year during the narrow 60-day summer sea window (December–February) via chartered polar ice-strengthened cargo vessels (e.g., *Vasiliy Golovnin*).
   * Real landed cost of fuel in Antarctica is **₹140 to ₹180 per Litre** (including icebreaker charter, helicopter airlift, and tracked sledge convoys).
   * Delayed relief expeditions threaten station human survival if winter fuel runs out.

### D. Zero-Cloud / 100% Air-Gapped Mandate
* Polar research stations rely on high-latency, weather-vulnerable satellite uplinks (Iridium / Inmarsat / GSAT).
* Satellite communication experiences frequent blackout windows during ionospheric storms and blizzards.
* **Hard Rule**: The entire energy management system must run **100% offline** on local edge hardware. Zero external cloud APIs, zero SaaS dependencies, zero external database calls.

---

## 3. The PolarGrid AI System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   POLARGRID AI EDGE ARCHITECTURE                       │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   [ Station Telemetry Bus ] (RS-485 Modbus RTU / Modbus TCP)          │
│   ├── Anemometer & Wind Direction (0 - 45 m/s)                         │
│   ├── Pyranometer Solar Irradiance (0 - 450 W/m²)                     │
│   ├── Outdoor & Indoor Thermocouples (-50°C to +20°C)                 │
│   ├── Diesel Genset CT Power & SFOC Sensors (0 - 250 kW)               │
│   └── Battery BMS (State of Charge 0 - 100%, Cell Temp)               │
│                            │                                           │
│                            ▼                                           │
│   [ Edge Ingestion & Anomaly Validation Layer ]                        │
│   ├── Range Bounding & Physics Plausibility Filter                     │
│   └── Kalman-Filtered Virtual State Estimator (Sensor Icing Fallback) │
│                            │                                           │
│                            ▼                                           │
│   [ PolarGrid Edge Intelligence Core ] (Python / FastAPI)              │
│   ├── Physics Digital Twin (Thermal dissipation & heat loss curves)   │
│   ├── Rolling 24h Ridge ML Load Forecaster (Diurnal demand curve)     │
│   ├── Dynamic Merit-Order Dispatch Optimizer                           │
│   │   Priority: Renewables (1st) ➔ BESS Buffer (2nd) ➔ Genset (3rd)   │
│   └── Anti-Wet-Stacking Genset Governor (Keeps Genset Load >55-60%)   │
│                            │                                           │
│                            ▼                                           │
│   [ Deterministic 3-Tier Priority Load Shedding Relay ]               │
│   ├── Zone 1: Critical Life Support (Oxygen, Heating, Med) ➔ 100% SAFE │
│   ├── Zone 2: Secondary Utilities (Galley, Laundry, Lighting)         │
│   └── Zone 3: Non-Essential Science (Radar compute, snow pumps)       │
│                            │                                           │
│                            ▼                                           │
│   [ Real-Time Operator Interface ]                                    │
│   ├── Server-Sent Events (SSE) 2.0s Push Pipeline                      │
│   ├── High-Contrast Antarctic Night Dashboard (HTML5/CSS3/Chart.js)   │
│   └── Audio-Visual Alert Panel (6 Rule Interlocks)                    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Current Implementation Status

### A. Working Codebase
1. **`.trace/` Management System**:
   * All 8 standard files fully initialized and up-to-date: `ARCHITECTURE.md`, `CONSTRAINTS.md`, `DECISIONS.md`, `FEATURE.md`, `FLOW.md`, `HANDOVER.md`, `ROLLBACK.md`, `TEST_CHECKLIST.md`.
2. **Backend Engine (`backend/`)** — Single Unified Simulator:
   * `twin_simulator.py`: Single source-of-truth physics-grounded microgrid advisory dispatch engine — 120 kW genset [ASSUMED] with 55% anti-wet-stacking clamp (66 kW floor), 50 kW wind turbine with 25 m/s storm furling cut-out, dynamic 3-tier priority load shedding, rule-based heuristic baseline comparison.
   * `forecaster.py`: Real Scikit-Learn `Ridge(alpha=1.0)` model fitted on synthetic polar load series with chronological 80/20 train/test split. Measured test MAE: **1.75 kW** vs **2.96 kW** 24h persistence baseline (+40.9% improvement).
   * `main.py`: FastAPI server with REST (`/api/simulate`, `/api/status`, `/api/forecast`, `/api/model-metrics`) and SSE (`/api/stream`) endpoints, mounting `frontend/dist` as static files.
3. **Frontend Dashboard (`frontend/`)** — React 19 + Vite:
   * `App.jsx`: Main command center coordinator with dual-engine architecture (fast local `simulationEngine.js` for 60fps slider scrubbing + backend sync via `/api/simulate`).
   * CSS Modules with industrial scientific light theme (`#EBF0ED` background, `#174A45` primary green, `#D99A2B` energy accent, `#17201D` text).
   * Recharts-based visualizations: Load Forecast, Dispatch Stack, Battery SoC Trajectory, Energy Mix, Tier Shedding Relay, Alert Panel, and Hourly Schedule Table with CSV export.
   * All metrics labeled honestly: forecast = "Synthetic demo forecast", savings tagged `SIMULATED, ASSUMED INPUTS`, genset spec tagged `[ASSUMED]`.
4. **PowerPoint Presentation Deck**:
   * File: `PolarGrid_AI_SIH2026_Submission.pptx` (saved in root and `media/`).
   * All ungrounded claims (Kalman, Modbus, SQLite, thermal hysteresis, heat recovery, CPU/RAM benchmarks) labeled as `[Roadmap]`.
   * Reframed as Advisory Decision Support with human-in-the-loop engineering.

---

## 5. Measured & Estimated Impact Metrics [SIMULATED, ASSUMED INPUTS]

> **Note**: All savings below are computed dynamically by the simulator against a standard uncoordinated rule-based genset-following policy (not naive diesel-only). Values are estimated seasonal ranges based on synthetic scenarios.

* **Forecast Accuracy (Measured on Test Split)**: Ridge model MAE **1.75 kW** vs persistence baseline **2.96 kW** (40.9% improvement).
* **Fuel Savings Estimate**: Dynamic range depending on scenario — typically **8%–16%** vs rule-based policy, projected **18,000 – 38,000 L/yr** seasonal range.
* **Human Safety**: Zone 1 life-support loads protected via deterministic 3-tier priority shedding relay during blizzard scenarios.
