"""
main.py — FastAPI Server for PolarGrid AI Dashboard
PS SIH26061 — AI-Driven Smart Energy Management System for Polar Research Stations

Endpoints:
  GET /              → Serves frontend (if frontend/ dir present)
  GET /api/status    → Single snapshot of current readings
  GET /api/forecast  → 24-hour load forecast
  GET /api/stream    → Server-Sent Events for live dashboard updates
  GET /health        → Health check
"""

import asyncio
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
import os

from twin_simulator import run_simulation
from forecaster import get_model_metrics
from pydantic import BaseModel
from typing import Optional

class SimulationRequest(BaseModel):
    station: Optional[str] = "maitri"
    preset: Optional[str] = "polar_night"
    forecast_horizon: Optional[int] = 24
    battery_kwh: Optional[float] = 300.0
    battery_kw: Optional[float] = 60.0
    fuel_rs_l: Optional[float] = 160.0
    wind_multiplier: Optional[float] = 1.0


app = FastAPI(
    title="PolarGrid AI",
    description="Smart Energy Management for Polar Research Stations — PS SIH26061",
    version="0.1.0-mvp",
)

# CORS: Allow frontend (may be opened from file:// in browser during demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_payload() -> dict:
    """Build the complete data payload from the single twin simulator."""
    return run_simulation(station="maitri", preset="polar_night")


@app.get("/health")
def health():
    return {"status": "ok", "service": "polargrid-ai-mvp"}


@app.get("/api/status")
def status():
    """Single snapshot — powered by the single twin simulator."""
    return JSONResponse(content=_build_payload())


@app.get("/api/forecast")
def forecast_only():
    """Load forecast from single twin simulator."""
    sim = _build_payload()
    return JSONResponse(content=sim["schedule"])


@app.get("/api/simulate")
def simulate_get(
    station: str = "maitri",
    preset: str = "polar_night",
    forecast_horizon: int = 24,
    battery_kwh: float = 300.0,
    battery_kw: float = 60.0,
    fuel_rs_l: float = 160.0,
    wind_multiplier: float = 1.0,
):
    """Run full microgrid scenario simulation (GET)."""
    result = run_simulation(
        station=station,
        preset=preset,
        forecast_horizon=forecast_horizon,
        battery_kwh=battery_kwh,
        battery_kw=battery_kw,
        fuel_rs_l=fuel_rs_l,
        wind_multiplier=wind_multiplier,
    )
    return JSONResponse(content=result)


@app.post("/api/simulate")
def simulate_post(req: SimulationRequest):
    """Run full microgrid scenario simulation (POST)."""
    result = run_simulation(
        station=req.station or "maitri",
        preset=req.preset or "polar_night",
        forecast_horizon=req.forecast_horizon or 24,
        battery_kwh=req.battery_kwh or 300.0,
        battery_kw=req.battery_kw or 60.0,
        fuel_rs_l=req.fuel_rs_l or 160.0,
        wind_multiplier=req.wind_multiplier or 1.0,
    )
    return JSONResponse(content=result)



async def _event_generator():
    """
    Async generator for Server-Sent Events.
    Emits a new data packet every 2 seconds.
    """
    while True:
        payload = _build_payload()
        # SSE format: data: <json>\n\n
        yield f"data: {json.dumps(payload)}\n\n"
        await asyncio.sleep(2)


@app.get("/api/stream")
async def stream():
    """SSE endpoint for live dashboard updates."""
    return StreamingResponse(
        _event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Prevents Nginx buffering SSE
        },
    )



@app.get("/api/model-metrics")
def model_metrics():
    """Return verified Scikit-Learn model metrics on test set."""
    return JSONResponse(content=get_model_metrics())


# Mount frontend/dist static files if built, fallback to frontend/
_dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
_frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.isdir(_dist_dir):
    app.mount("/", StaticFiles(directory=_dist_dir, html=True), name="frontend-dist")
elif os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    print("🧊 PolarGrid AI — Starting server...")
    print("📊 Dashboard: http://localhost:8000")
    print("📡 API Docs:  http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
