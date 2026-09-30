import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import ScenarioSidebar from './components/ScenarioSidebar';
import MetricCards from './components/MetricCards';
import LoadForecastChart from './components/LoadForecastChart';
import DispatchStackChart from './components/DispatchStackChart';
import BatterySocChart from './components/BatterySocChart';
import DieselExplainer from './components/DieselExplainer';
import TierSheddingRelay from './components/TierSheddingRelay';
import { AlertPanel } from './components/AlertPanel';
import HourlyScheduleTable from './components/HourlyScheduleTable';
import { calculateSimulation } from './lib/simulationEngine';
import styles from './App.module.css';

const DEFAULT_PARAMS = {
  station: 'maitri',
  preset: 'polar_night',
  forecastHorizon: 24,
  batteryKwh: 300,
  batteryKw: 60,
  fuelRsL: 160,
  windMultiplier: 1.0,
};

export default function App() {
  const [params, setParams] = useState(DEFAULT_PARAMS);
  const [backendData, setBackendData] = useState(null);
  const abortControllerRef = useRef(null);

  // Fast local deterministic physics engine for ultra-smooth 60fps slider scrubbing
  const localSimData = useMemo(() => {
    return calculateSimulation(params);
  }, [params]);

  // Sync with FastAPI backend /api/simulate with request cancellation
  const syncWithBackend = useCallback(async (currentParams) => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const query = new URLSearchParams({
        station: currentParams.station,
        preset: currentParams.preset,
        forecast_horizon: currentParams.forecastHorizon,
        battery_kwh: currentParams.batteryKwh,
        battery_kw: currentParams.batteryKw,
        fuel_rs_l: currentParams.fuelRsL,
        wind_multiplier: currentParams.windMultiplier,
      }).toString();

      const res = await fetch(`/api/simulate?${query}`, { signal: controller.signal });
      if (res.ok) {
        const json = await res.json();
        if (json && json.schedule) {
          setBackendData({
            station: json.station,
            preset: json.preset,
            forecastHorizon: json.forecast_horizon,
            kpis: {
              forecastMaeKw: json.kpis.forecast_mae_kw,
              persistenceMaeKw: json.kpis.persistence_mae_kw,
              fuelOptimizedLDay: json.kpis.fuel_optimized_l_day,
              fuelSavedLDay: json.kpis.fuel_saved_l_day,
              fuelSavedPct: json.kpis.fuel_saved_pct,
              baselineRuleBasedLDay: json.kpis.baseline_rule_based_l_day,
              unmetKwh: json.kpis.unmet_kwh,
              reFractionPct: json.kpis.re_fraction_pct,
              dispatchMode: json.kpis.dispatch_mode || 'Advisory Decision Support',
            },
            tiers: {
              tier1Status: json.tiers.tier1_status,
              tier1ServedKwh: json.tiers.tier1_served_kwh,
              tier2Status: json.tiers.tier2_status,
              tier2ServedKwh: json.tiers.tier2_served_kwh,
              tier3Status: json.tiers.tier3_status,
              tier3ServedKwh: json.tiers.tier3_served_kwh,
            },
            economics: {
              rsSavedDay: json.economics.rs_saved_day,
              projectedRangeYr: json.economics.projected_range_yr,
              savingPctStr: json.economics.saving_pct_str,
              statusTag: json.economics.status_tag || 'SIMULATED, ASSUMED INPUTS',
            },
            explainer: json.explainer,
            alerts: json.alerts || [],
            schedule: json.schedule.map((s, i) => ({
              ...s,
              timeShort: s.time_short || s.time.slice(11, 16),
              timeLabel: i === 0 ? '00:00\nMar 1, 2025' : s.time_short,
            })),
          });
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        // Backend not running — fallback smoothly to local physics engine
      }
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      syncWithBackend(params);
    }, 120);
    return () => {
      clearTimeout(timer);
    };
  }, [params, syncWithBackend]);

  const handlePreset = (presetName) => {
    let updated = { ...params, preset: presetName };
    if (presetName === 'calm') {
      updated.windMultiplier = 0.4;
    } else if (presetName === 'blizzard') {
      updated.windMultiplier = 2.2;
    } else if (presetName === 'polar_night') {
      updated.windMultiplier = 1.0;
    }
    setParams(updated);
  };

  const handleResetDefaults = () => {
    setParams(DEFAULT_PARAMS);
  };

  const sim = backendData || localSimData;

  return (
    <div className={styles.appContainer}>
      {/* Left Sidebar Scenario Controls */}
      <ScenarioSidebar
        params={params}
        onChange={setParams}
        onPreset={handlePreset}
      />

      {/* Main Content Area */}
      <main className={styles.mainContent}>
        {/* Antarctic Station Telemetry Status Bar */}
        <div className={styles.stationStatusBar}>
          <div className={`${styles.statusPill} ${styles.statusPillOnline}`}>
            <span className={styles.liveDot} />
            <span>NCPOR EDGE SYSTEM ONLINE</span>
          </div>
          <div className={styles.statusPill}>
            <span>STATION: {params.station.toUpperCase()} ({params.station === 'maitri' ? '70°45′S' : '69°24′S'})</span>
          </div>
          <div className={styles.statusPill}>
            <span>TIME: ANTARCTIC UTC+05:00</span>
          </div>
          <button
            type="button"
            className={styles.resetBtn}
            onClick={handleResetDefaults}
            title="Reset simulation parameters to default baseline"
          >
            Reset Defaults
          </button>
        </div>

        {/* Hero Header */}
        <header className={styles.heroHeader}>
          <h1 className={styles.heroTitle}>Dhruv Energy Twin Lite — SIH26061 Polar Smart Energy</h1>
          <p className={styles.heroSubtitle}>
            AI load forecast + Advisory dispatch support + Digital twin dashboard (Maitri / Bharati). Synthetic open-data demo.
          </p>
        </header>

        {/* 5 KPI Metric Cards */}
        <MetricCards kpis={sim.kpis} />

        {/* Chart 1: Load vs forecast */}
        <LoadForecastChart data={sim.schedule} />

        {/* Chart 2: Optimized dispatch stack vs load */}
        <DispatchStackChart data={sim.schedule} />

        {/* Two-Column Row: Battery SoC Trajectory + Auto Explainer */}
        <div className={styles.splitRow}>
          <div className={styles.leftCol}>
            <BatterySocChart data={sim.schedule} />
          </div>
          <div className={styles.rightCol}>
            <DieselExplainer explainer={sim.explainer} />
          </div>
        </div>

        {/* 3-tier shedding relay + fuel economics */}
        <TierSheddingRelay
          tiers={sim.tiers}
          economics={sim.economics}
        />

        {/* Real-time system & weather alerts with dynamic severity */}
        <AlertPanel alerts={sim.alerts || []} />

        {/* Hourly schedule data table with Download CSV Button */}
        <HourlyScheduleTable
          schedule={sim.schedule}
          station={params.station}
        />
      </main>
    </div>
  );
}
