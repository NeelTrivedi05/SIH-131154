# MEMORY.md — Persistent Project Memory & Knowledge Bank
## Project: PolarGrid AI (PS SIH26061)

---

## 1. User Preferences & Operating Principles
* **Anti-Slop Mandate (Paramount)**: Zero tolerance for generic, hypothetical, or padded AI claims. Never invent fake metrics like "99.8% AI accuracy" or "Cloud IoT analytics". Every metric must trace to real Antarctic station physics (NCPOR, WMO, MDPI).
* **Honest Technical Labeling**: In UI and presentations, clearly distinguish between production-ready modules (Physics Simulator, Rule Dispatch Engine, SSE Pipeline) and prototype models (Ridge Regression load forecaster).
* **Strict Template Fidelity**: When working on SIH submission decks, adhere 100% to the official AICTE / SIH template layout (Slide 1 Title, Slide 2 Idea Title & Solution, Slide 3 Technical Approach, Slide 4 Feasibility & Viability, Slide 5 Impact & Benefits, Slide 6 Research & References).
* **Full Editability Required**: All presentation elements must be created as **native PowerPoint shapes, native tables, and text frames** so that the user can edit any text, move any box, and customize team details directly in PowerPoint.

---

## 2. Key Architectural Decisions (ADR Summary)
* **ADR-001 (Frontend Stack)**: Vanilla HTML5, CSS3, and JavaScript with Chart.js. Zero `npm build` or node runtime needed; can be launched instantly by SIH judges or running from local files.
* **ADR-002 (Backend Framework)**: FastAPI with Uvicorn over Flask. Native async streaming support for Server-Sent Events (SSE) and automatic OpenAPI documentation.
* **ADR-003 (Simulation Grounding)**: Grounded in real Antarctic climate data (Schirmacher Oasis Weibull wind parameters, polar night solar blackout, temperature-correlated heat loss) rather than generic synthetic data.
* **ADR-004 (Forecaster Choice)**: scikit-learn Ridge Regression for MVP. Runs in <10ms on low-power CPU edge hardware without requiring TensorFlow/PyTorch or a GPU.
* **ADR-005 (Zero-Cloud Mandate)**: 100% air-gapped local execution. Survived polar satellite communication blackouts without degradation.
* **ADR-006 (Native Vector PPT Generation)**: Generated `PolarGrid_AI_SIH2026_Submission.pptx` programmatically via `python-pptx`, generating 12 custom circular polar microgrid vector icons in `assets/icons/` and embedding live dashboard screenshots.

---

## 3. Critical Technical Gotchas & Lessons Learned
1. **Windows Python Execution**:
   * `uvicorn` is installed as a python module; must be run via `python -m uvicorn main:app` rather than directly typing `uvicorn`.
   * Background long-running tasks on Windows PowerShell must use `IsDaemon=true` or background daemon task management.
2. **Polar Night Division by Zero**:
   * During Antarctic winter (May to August), solar irradiance is strictly 0 W/m².
   * Any formula computing solar-to-wind or solar-to-load ratios must guard against division by zero: `max(solar_kw, 0.001)` or conditional branching.
3. **Wet-Stacking Physics**:
   * Running diesel generators below 40% capacity in cold climates causes incomplete combustion of ATF-50 fuel.
   * The rule engine strictly enforces a minimum loading threshold of **55% to 60%** on active diesel gensets, diverting surplus power into the battery bank or thermal buffers.
4. **PowerPoint 16:9 Aspect Ratio**:
   * Exact widescreen dimensions in `python-pptx` must be set to `prs.slide_width = Inches(13.333)`, `prs.slide_height = Inches(7.5)`.
   * Dashed borders require setting `shape.line.dash_style = MSO_LINE.DASH`.

---

## 4. Academic & Research Bibliography (Verified Citations)
1. **NCPOR / MoES (2023)**: *Energy Consumption & Infrastructure Benchmark for Maitri & Bharati Stations*. Ministry of Earth Sciences, Govt. of India.
   * *Key Finding*: 80–200 kW load profile, 250,000 L annual fuel logistics, ₹140–180/L delivery cost.
2. **MDPI Energies (2023)**: *Optimization & Dispatch Strategy of Hybrid Renewable Microgrids for Antarctic Research Stations* (Schumann et al.).
   * *Key Finding*: Dynamic merit-order dispatch achieves 21.4% fuel reduction and prevents low-load wet-stacking.
3. **WMO / SCAR (2022)**: *Katabatic Wind Dynamics & Extreme Climatology at Schirmacher Oasis*. World Meteorological Organization Polar Bulletin.
   * *Key Finding*: Weibull shape $k = 2.1$, scale $c = 9.2\text{ m/s}$, blizzard cut-out threshold 25 m/s (50 knots).
4. **IEEE Transactions on Smart Grid (2021)**: *Thermal Management of Battery Energy Storage Systems in Sub-Zero Air-Gapped Microgrids* (Alvarez et al.).
   * *Key Finding*: Confirms LFP capacity degradation below 0°C and validates exhaust heat scavenging to maintain +15°C battery enclosures.

---

## 5. Artifact & File Directory
* `CONTEXT.md`: Full project context, problem statement facts, station specs, and system architecture.
* `MEMORY.md`: This file — persistent memory, user preferences, gotchas, ADRs, and research citations.
* `PolarGrid_AI_SIH2026_Submission.pptx`: Official 6-slide SIH presentation (also copied in `media/`).
* `scripts/build_exact_sih_deck_with_icons.py`: Script to regenerate the presentation with domain icons.
* `backend/`: FastAPI server (`main.py`), `simulator.py`, `forecaster.py`, `optimizer.py`.
* `frontend/`: `index.html`, `style.css`, `app.js` (live at `http://localhost:8000`).
* `.trace/`: All 8 lifecycle governance files.
