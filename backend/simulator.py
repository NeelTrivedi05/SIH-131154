"""
simulator.py — Polar Station Sensor Data Simulator
Based on real Antarctic climate profiles: Maitri station, Schirmacher Oasis, Queen Maud Land
Sources: NCPOR reports, SCAR data, NASA ERA5 Antarctic profiles

Honest scope: This is a physics-grounded simulation, NOT real sensor data.
"""

import math
import random
import time
from datetime import datetime


def _solar_irradiance(month: int, hour: int) -> float:
    """
    Compute solar irradiance (W/m²) for Antarctic station.
    
    Based on actual Antarctic sun angle patterns:
    - Polar night (May-Aug): No sun at all for Maitri lat ~70°S
    - Shoulder seasons (Mar-Apr, Sep-Oct): Low angle sun, 0-200 W/m²
    - Summer (Nov-Feb): Up to 400 W/m² at solar noon (but overcast often)
    
    Maitri: 70°45'S, 11°44'E — approximate model.
    """
    # Months where there's usable solar (Southern Hemisphere summer)
    # 11=Nov, 12=Dec, 1=Jan, 2=Feb have good solar
    # 3=Mar, 10=Oct have marginal solar
    # 4-9 = effectively no solar at 70°S
    summer_months = {11, 12, 1, 2}
    marginal_months = {3, 10}

    if month in summer_months:
        peak = 380.0
    elif month in marginal_months:
        peak = 120.0
    else:
        return 0.0  # Polar night

    # Diurnal pattern — Antarctic summer has near-continuous daylight
    # but irradiance follows a broad curve; at polar summer, sun doesn't set
    # Use a broad sinusoid centered around noon
    angle = math.pi * (hour - 2) / 20.0  # broad peak
    solar = peak * max(0.0, math.sin(angle))

    # Add cloud cover randomness (overcast is common in Antarctic)
    cloud_factor = random.uniform(0.3, 1.0)
    return round(solar * cloud_factor, 1)


def _wind_speed(month: int) -> float:
    """
    Wind speed in m/s. Antarctic winds follow Weibull distribution.
    Maitri experiences strong katabatic winds; mean ~9 m/s, frequent gusts.
    Blizzards (> 30 m/s) more common in winter.
    """
    # Scale parameter varies by season
    if month in {6, 7, 8}:  # winter — stronger winds
        scale = 13.0
    elif month in {12, 1, 2}:  # summer — slightly calmer
        scale = 7.0
    else:
        scale = 10.0

    # Weibull shape k=2 approximated via: -scale * ln(random())^0.5
    wind = scale * math.sqrt(-math.log(max(random.random(), 1e-9)))
    wind = min(wind, 60.0)  # Physical cap: recorded max ~60 m/s
    return round(wind, 1)


def _ambient_temperature(month: int) -> float:
    """
    Ambient temperature in °C for Schirmacher Oasis (Maitri location).
    Data based on published NCPOR and WMO climatological normals.
    
    Monthly means (approximate):
    Jan: -2, Feb: -3, Mar: -9, Apr: -16, May: -21, Jun: -24,
    Jul: -26, Aug: -25, Sep: -20, Oct: -13, Nov: -7, Dec: -2
    """
    monthly_means = {
        1: -2, 2: -3, 3: -9, 4: -16, 5: -21,
        6: -24, 7: -26, 8: -25, 9: -20, 10: -13,
        11: -7, 12: -2
    }
    mean = monthly_means.get(month, -15.0)
    # Add realistic daily variability (±5°C)
    noise = random.gauss(0, 3.0)
    return round(max(-50.0, min(5.0, mean + noise)), 1)


def _wind_power(wind_ms: float, turbine_rated_kw: float = 50.0) -> float:
    """
    Wind turbine power output (kW).
    Assumes a small-medium turbine rated at 50kW (realistic for remote station).
    Cut-in: 3 m/s, rated: 12 m/s, cut-out: 25 m/s (turbine stops in storm to protect itself).
    """
    cut_in, rated_speed, cut_out = 3.0, 12.0, 25.0
    if wind_ms < cut_in or wind_ms > cut_out:
        return 0.0
    if wind_ms >= rated_speed:
        return turbine_rated_kw
    # Power curve: cubic between cut-in and rated
    power = turbine_rated_kw * ((wind_ms - cut_in) / (rated_speed - cut_in)) ** 3
    return round(power, 1)


def _solar_power(irradiance: float, panel_area_m2: float = 100.0, efficiency: float = 0.18) -> float:
    """
    Solar panel output (kW). 100 m² of 18% efficient panels = 18 kW peak.
    Realistic for a station supplement, not primary source.
    """
    power_w = irradiance * panel_area_m2 * efficiency
    return round(power_w / 1000.0, 1)  # Convert to kW


def get_current_readings() -> dict:
    """
    Generate a single snapshot of current station telemetry.
    All values are physically grounded to Antarctic operating reality.
    """
    now = datetime.utcnow()
    month = now.month
    hour = now.hour

    # Environmental readings
    temp_c = _ambient_temperature(month)
    wind_ms = _wind_speed(month)
    solar_irr = _solar_irradiance(month, hour)

    # Renewable generation
    wind_kw = _wind_power(wind_ms)
    solar_kw = _solar_power(solar_irr)
    total_renewable_kw = wind_kw + solar_kw

    # Load profile: typical Antarctic station uses 80-200 kW
    # Heating demand increases with lower temperature
    heating_factor = max(0.5, min(2.0, 1.0 + (abs(temp_c) - 15) / 30.0))

    zone_lab_kw = round(random.uniform(18, 30), 1)       # Scientific equipment
    zone_heating_kw = round(random.uniform(40, 80) * heating_factor, 1)  # Dominant load
    zone_comms_kw = round(random.uniform(8, 15), 1)      # Communications/satellite
    zone_quarters_kw = round(random.uniform(10, 20), 1)  # Living quarters

    total_load_kw = zone_lab_kw + zone_heating_kw + zone_comms_kw + zone_quarters_kw
    total_load_kw = round(min(total_load_kw, 200.0), 1)  # Station capacity cap

    # Battery storage (SoC oscillates; not modelled fully for MVP)
    # Use a slow random walk clamped between 10-95%
    battery_soc = round(random.uniform(25, 90), 1)

    # Diesel required = max(0, total_load - renewables)
    diesel_required_kw = round(max(0, total_load_kw - total_renewable_kw), 1)

    # Fuel savings vs. all-diesel baseline (in litres/hour)
    # Diesel generator: ~0.3 L/kWh (realistic for industrial gen at partial load)
    renewable_offset_kw = min(total_renewable_kw, total_load_kw)
    fuel_saved_lph = round(renewable_offset_kw * 0.3, 2)
    # Cost at ₹89/L (approximate Antarctic logistics cost — actual is much higher,
    # but using India domestic diesel price as conservative baseline)
    cost_saved_inr_per_hour = round(fuel_saved_lph * 89, 0)

    return {
        "timestamp": now.isoformat() + "Z",
        "month": month,
        "hour": hour,
        "environment": {
            "temperature_c": temp_c,
            "wind_speed_ms": wind_ms,
            "solar_irradiance_wm2": solar_irr,
        },
        "generation": {
            "wind_kw": wind_kw,
            "solar_kw": solar_kw,
            "diesel_kw": diesel_required_kw,
            "total_renewable_kw": total_renewable_kw,
        },
        "load_zones": {
            "laboratory_kw": zone_lab_kw,
            "heating_kw": zone_heating_kw,
            "communications_kw": zone_comms_kw,
            "quarters_kw": zone_quarters_kw,
            "total_kw": total_load_kw,
        },
        "storage": {
            "battery_soc_percent": battery_soc,
        },
        "economics": {
            "fuel_saved_lph": fuel_saved_lph,
            "cost_saved_inr_hr": cost_saved_inr_per_hour,
        },
    }


def get_historical_batch(n_hours: int = 48) -> list[dict]:
    """
    Generate a batch of past readings for chart initialization.
    Uses the same physics model, just called in a loop.
    """
    # Freeze seed for reproducibility on each page load
    original_state = random.getstate()
    random.seed(42)
    readings = [get_current_readings() for _ in range(n_hours)]
    random.setstate(original_state)
    return readings
