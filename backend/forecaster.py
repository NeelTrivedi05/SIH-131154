"""
forecaster.py — Measured Load Forecaster with Real Scikit-Learn Ridge Model
PS SIH26061 — AI-Driven Smart Energy Management System for Polar Research Stations

Fitted on synthetic polar load series with train/test split.
Reports measured test MAE vs 24-hour persistence baseline.
"""

import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from sklearn.linear_model import Ridge


def generate_synthetic_series(days: int = 30, seed: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate synthetic polar station series:
    - hours array
    - ambient temperature (°C)
    - electrical load (kW)
    """
    np.random.seed(seed)
    n_hours = days * 24
    hours = np.arange(n_hours)
    
    # Hour of day (0-23)
    hod = hours % 24
    
    # Ambient temp with diurnal cycle and multi-day synoptic weather waves
    synoptic = 6.0 * np.sin(2 * np.pi * hours / (24 * 7)) # 7-day storm cycle
    daily_temp = 3.0 * np.sin(2 * np.pi * (hod - 14) / 24)
    temp = -22.0 + synoptic + daily_temp + np.random.normal(0, 1.2, n_hours)
    
    # Station load: base (38 kW) + heating demand driven by temperature + human routine peaks
    base_load = 38.0
    heating_demand = 0.55 * np.maximum(0.0, -10.0 - temp) # colder = more heating
    human_routine = 7.0 * np.sin(np.pi * (hod - 6) / 12.0) * (hod >= 6) * (hod <= 22)
    evening_peak = 5.0 * np.exp(-0.5 * ((hod - 18) / 2.0) ** 2)
    noise = np.random.normal(0, 1.8, n_hours)
    
    load = np.maximum(25.0, base_load + heating_demand + human_routine + evening_peak + noise)
    return hours, temp, load


def build_dataset(hours: np.ndarray, temp: np.ndarray, load: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Build feature matrix X, target y, and 24h persistence benchmark.
    Features:
    [sin_hour, cos_hour, temp, lag_1h, lag_2h, lag_24h, rolling_6h_mean]
    """
    n = len(load)
    X_list = []
    y_list = []
    persistence_list = []
    
    hod = hours % 24
    
    for t in range(24, n):
        sin_h = math.sin(2 * math.pi * hod[t] / 24.0)
        cos_h = math.cos(2 * math.pi * hod[t] / 24.0)
        t_c = temp[t]
        lag_1 = load[t - 1]
        lag_2 = load[t - 2]
        lag_24 = load[t - 24]
        roll_6 = np.mean(load[t - 6:t])
        
        X_list.append([sin_h, cos_h, t_c, lag_1, lag_2, lag_24, roll_6])
        y_list.append(load[t])
        persistence_list.append(lag_24)
        
    return np.array(X_list), np.array(y_list), np.array(persistence_list)


# Module-level model training on module load
_hours, _temp, _load = generate_synthetic_series(days=35, seed=42)
_X, _y, _persistence = build_dataset(_hours, _temp, _load)

# 80/20 Chronological Train/Test Split
_split_idx = int(len(_X) * 0.8)
_X_train, _X_test = _X[:_split_idx], _X[_split_idx:]
_y_train, _y_test = _y[:_split_idx], _y[_split_idx:]
_pers_test = _persistence[_split_idx:]

# Fit Scikit-Learn Ridge Regression
_ridge_model = Ridge(alpha=1.0)
_ridge_model.fit(_X_train, _y_train)

# Evaluate on held-out test split
_y_test_pred = _ridge_model.predict(_X_test)
MEASURED_RIDGE_MAE = round(float(np.mean(np.abs(_y_test - _y_test_pred))), 2)
MEASURED_PERSISTENCE_MAE = round(float(np.mean(np.abs(_y_test - _pers_test))), 2)


def get_model_metrics() -> Dict[str, Any]:
    """Return verified metrics on held-out test set."""
    return {
        "model_type": "Ridge(alpha=1.0) [Fitted on synthetic series]",
        "train_samples": len(_X_train),
        "test_samples": len(_X_test),
        "measured_ridge_mae_kw": MEASURED_RIDGE_MAE,
        "measured_persistence_mae_kw": MEASURED_PERSISTENCE_MAE,
        "improvement_pct": round(
            ((MEASURED_PERSISTENCE_MAE - MEASURED_RIDGE_MAE) / MEASURED_PERSISTENCE_MAE) * 100.0, 1
        ),
    }


def predict_horizon(current_load: float, current_temp: float, start_hour: int, horizon: int = 24) -> List[float]:
    """
    Generate multi-step autoregressive forecast using the fitted Ridge model.
    """
    predictions = []
    # Seed lag history
    recent = [current_load] * 24
    
    for h in range(horizon):
        target_hod = (start_hour + h) % 24
        sin_h = math.sin(2 * math.pi * target_hod / 24.0)
        cos_h = math.cos(2 * math.pi * target_hod / 24.0)
        
        # Slight diurnal temperature cycle
        simulated_temp = current_temp + 2.0 * math.sin(2 * math.pi * (target_hod - 14) / 24.0)
        
        lag_1 = recent[-1]
        lag_2 = recent[-2] if len(recent) >= 2 else current_load
        lag_24 = recent[-24] if len(recent) >= 24 else current_load
        roll_6 = float(np.mean(recent[-6:]))
        
        feat = np.array([[sin_h, cos_h, simulated_temp, lag_1, lag_2, lag_24, roll_6]])
        pred = float(_ridge_model.predict(feat)[0])
        pred = round(max(25.0, min(180.0, pred)), 1)
        
        predictions.append(pred)
        recent.append(pred)
        
    return predictions


def get_forecast(current_readings: dict, n_hours: int = 24) -> list[dict]:
    """
    Format standard API forecast list matching FastAPI contract.
    """
    now = datetime.utcnow()
    temp_c = current_readings.get("environment", {}).get("temperature_c", -22.0)
    current_load = current_readings.get("load_zones", {}).get("total_kw", 45.0)
    start_hour = now.hour
    
    preds = predict_horizon(current_load, temp_c, start_hour, n_hours)
    
    result = []
    for offset, p in enumerate(preds):
        future_time = now + timedelta(hours=offset)
        result.append({
            "hour_offset": offset,
            "timestamp": future_time.isoformat() + "Z",
            "hour": future_time.hour,
            "predicted_load_kw": p,
            "lower_bound_kw": round(p * 0.92, 1),
            "upper_bound_kw": round(p * 1.08, 1),
        })
    return result
