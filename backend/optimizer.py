"""
optimizer.py — Dispatch Optimizer & Alert Engine

Rule-based dispatch with physics-informed thresholds.
Logic based on published microgrid management strategies for isolated systems.

Priority order:
1. Safety: never let battery die completely (keep SoC > 10%)
2. Renewable first: maximize renewable fraction
3. Load flexibility: shed non-critical loads before overloading diesel
4. Efficiency: avoid diesel running at very low load (< 30% efficiency cliff)
"""


# Station capacity limits
STATION_MAX_KW = 200.0       # Generator hard ceiling
DIESEL_GEN_RATED_KW = 200.0  # Full-rated diesel output
BATTERY_CRITICAL_PCT = 15.0  # Below this: critical alert
BATTERY_LOW_PCT = 25.0       # Below this: warning
DIESEL_EFFICIENCY_FLOOR = 60.0  # Below this, diesel is thermally inefficient


def get_dispatch_decision(readings: dict, forecast: list[dict]) -> dict:
    """
    Determine optimal dispatch plan and generate alerts.
    
    Returns:
    - dispatch_plan: recommended source mix
    - alerts: list of current alerts with severity
    - renewable_fraction: 0-1 fraction of load covered by renewables
    - load_shed_recommended: bool + which zones to shed
    """
    gen = readings["generation"]
    load = readings["load_zones"]
    storage = readings["storage"]

    wind_kw = gen["wind_kw"]
    solar_kw = gen["solar_kw"]
    diesel_kw = gen["diesel_kw"]
    total_load = load["total_kw"]
    battery_soc = storage["battery_soc_percent"]

    total_renewable = wind_kw + solar_kw
    renewable_fraction = min(1.0, total_renewable / max(total_load, 1.0))

    # ── Dispatch Plan ──────────────────────────────────────────────────────
    # Determine what diesel actually needs to cover
    renewable_available = min(total_renewable, total_load)
    diesel_needed = max(0.0, total_load - renewable_available)

    # Check if diesel is running inefficiently (below 30% = 60 kW)
    diesel_low_efficiency = (0 < diesel_needed < DIESEL_EFFICIENCY_FLOOR)

    dispatch_plan = {
        "renewable_kw": round(renewable_available, 1),
        "diesel_kw": round(diesel_needed, 1),
        "battery_discharge": False,   # MVP: battery as buffer, not primary
        "diesel_efficiency_warning": diesel_low_efficiency,
    }

    # ── Alert Engine ───────────────────────────────────────────────────────
    alerts = []

    # CRITICAL: Battery critically low
    if battery_soc < BATTERY_CRITICAL_PCT:
        alerts.append({
            "severity": "critical",
            "code": "BATTERY_CRITICAL",
            "message": f"Battery SoC at {battery_soc}% — below safe minimum. Diesel must carry full load.",
            "action": "Disable non-essential loads immediately. Check battery health.",
        })

    # CRITICAL: Load approaching station capacity
    if total_load > STATION_MAX_KW * 0.92:
        alerts.append({
            "severity": "critical",
            "code": "OVERLOAD_RISK",
            "message": f"Total load {total_load:.0f} kW approaching station limit ({STATION_MAX_KW:.0f} kW).",
            "action": "Shed heating zone thermostat by 2°C. Defer lab batch processes.",
        })

    # WARNING: High diesel consumption
    if diesel_needed > 160.0:
        alerts.append({
            "severity": "warning",
            "code": "HIGH_DIESEL",
            "message": f"Diesel carrying {diesel_needed:.0f} kW. Fuel burn elevated.",
            "action": "Review if any non-critical loads can be deferred.",
        })

    # WARNING: Battery low (but not critical)
    if BATTERY_LOW_PCT <= battery_soc < BATTERY_CRITICAL_PCT + 10:
        alerts.append({
            "severity": "warning",
            "code": "BATTERY_LOW",
            "message": f"Battery SoC at {battery_soc}%. Monitor closely.",
            "action": "Reduce lab equipment standby loads.",
        })

    # WARNING: Forecast shows demand spike in next 4 hours
    if forecast:
        next_4h_peak = max(f["predicted_load_kw"] for f in forecast[:4])
        if next_4h_peak > total_load * 1.15:
            alerts.append({
                "severity": "warning",
                "code": "FORECAST_SPIKE",
                "message": f"Forecast shows demand spike to {next_4h_peak:.0f} kW within 4 hours.",
                "action": "Pre-charge battery if renewable headroom available.",
            })

    # POSITIVE INFO: Good renewable performance
    if renewable_fraction > 0.55:
        alerts.append({
            "severity": "info",
            "code": "HIGH_RENEWABLE",
            "message": f"Renewable fraction at {renewable_fraction * 100:.0f}%. Excellent energy mix.",
            "action": "Consider charging battery with surplus if SoC < 80%.",
        })

    # INFO: Diesel running in low efficiency zone
    if diesel_low_efficiency:
        alerts.append({
            "severity": "info",
            "code": "DIESEL_INEFFICIENT",
            "message": f"Diesel running at {diesel_needed:.0f} kW — below optimal efficiency threshold.",
            "action": "Use battery to pick up slack and let diesel run at rated point.",
        })

    # ── Load Shedding Recommendation ───────────────────────────────────────
    load_shed = {"recommended": False, "zones": []}
    if total_load > STATION_MAX_KW * 0.88 or battery_soc < BATTERY_CRITICAL_PCT:
        load_shed["recommended"] = True
        # Shed in priority order: quarters > lab batch > heating margin
        if load["quarters_kw"] > 15:
            load_shed["zones"].append("quarters")
        if load["laboratory_kw"] > 25:
            load_shed["zones"].append("laboratory_batch")
        # Never shed: communications, critical heating

    return {
        "dispatch_plan": dispatch_plan,
        "alerts": alerts,
        "renewable_fraction": round(renewable_fraction, 3),
        "load_shed": load_shed,
        "summary": {
            "total_load_kw": total_load,
            "total_renewable_kw": total_renewable,
            "diesel_required_kw": round(diesel_needed, 1),
            "alert_count": len(alerts),
            "highest_severity": _highest_severity(alerts),
        }
    }


def _highest_severity(alerts: list[dict]) -> str:
    """Return the highest severity level present in the alert list."""
    if not alerts:
        return "none"
    order = {"critical": 3, "warning": 2, "info": 1}
    return max(alerts, key=lambda a: order.get(a["severity"], 0))["severity"]
