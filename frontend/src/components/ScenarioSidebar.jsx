import React from 'react';
import styles from './ScenarioSidebar.module.css';

export default function ScenarioSidebar({ params, onChange, onPreset }) {
  const handleChange = (key, value) => {
    onChange({ ...params, [key]: value });
  };

  return (
    <aside className={styles.sidebar}>
      <h2 className={styles.title}>Scenario controls</h2>

      <div className={styles.section}>
        <div className={styles.sectionHeader}>One-click presets</div>
        <div className={styles.presetGroup}>
          <button
            type="button"
            className={`${styles.presetBtn} ${params.preset === 'calm' ? styles.activeCalm : ''}`}
            onClick={() => onPreset('calm')}
          >
            Calm
          </button>
          <button
            type="button"
            className={`${styles.presetBtn} ${params.preset === 'blizzard' ? styles.activeBlizzard : ''}`}
            onClick={() => onPreset('blizzard')}
          >
            Blizzard
          </button>
          <button
            type="button"
            className={`${styles.presetBtn} ${params.preset === 'polar_night' ? styles.activePolar : ''}`}
            onClick={() => onPreset('polar_night')}
          >
            Polar night
          </button>
        </div>
      </div>

      <div className={styles.controlGroup}>
        <label className={styles.controlLabel}>Station</label>
        <div className={styles.selectWrapper}>
          <select
            className={styles.select}
            value={params.station}
            onChange={(e) => handleChange('station', e.target.value)}
          >
            <option value="maitri">maitri</option>
            <option value="bharati">bharati</option>
          </select>
          <span className={styles.chevron}>▾</span>
        </div>
      </div>

      {/* Forecast horizon */}
      <div className={styles.controlGroup}>
        <div className={styles.sliderHeader}>
          <label className={styles.controlLabel}>Forecast horizon (h)</label>
          <span className={styles.sliderVal}>{params.forecastHorizon}</span>
        </div>
        <input
          type="range"
          min="6"
          max="72"
          step="6"
          value={params.forecastHorizon}
          onChange={(e) => handleChange('forecastHorizon', Number(e.target.value))}
          className={styles.rangeInput}
        />
      </div>

      {/* Battery kWh */}
      <div className={styles.controlGroup}>
        <div className={styles.sliderHeader}>
          <label className={styles.controlLabel}>Battery kWh</label>
          <span className={styles.sliderVal}>{params.batteryKwh}</span>
        </div>
        <input
          type="range"
          min="50"
          max="1000"
          step="25"
          value={params.batteryKwh}
          onChange={(e) => handleChange('batteryKwh', Number(e.target.value))}
          className={styles.rangeInput}
        />
      </div>

      {/* Battery kW */}
      <div className={styles.controlGroup}>
        <div className={styles.sliderHeader}>
          <label className={styles.controlLabel}>Battery kW</label>
          <span className={styles.sliderVal}>{params.batteryKw}</span>
        </div>
        <input
          type="range"
          min="10"
          max="200"
          step="5"
          value={params.batteryKw}
          onChange={(e) => handleChange('batteryKw', Number(e.target.value))}
          className={styles.rangeInput}
        />
      </div>

      {/* Fuel Rs/L (landed) */}
      <div className={styles.controlGroup}>
        <div className={styles.sliderHeader}>
          <label className={styles.controlLabel}>Fuel Rs/L (landed)</label>
          <span className={styles.sliderVal}>{params.fuelRsL}</span>
        </div>
        <input
          type="range"
          min="50"
          max="300"
          step="5"
          value={params.fuelRsL}
          onChange={(e) => handleChange('fuelRsL', Number(e.target.value))}
          className={styles.rangeInput}
        />
      </div>

      {/* Wind multiplier */}
      <div className={styles.controlGroup}>
        <div className={styles.sliderHeader}>
          <label className={styles.controlLabel}>Wind multiplier</label>
          <span className={styles.sliderVal}>{Number(params.windMultiplier).toFixed(1)}</span>
        </div>
        <input
          type="range"
          min="0.1"
          max="3.0"
          step="0.1"
          value={params.windMultiplier}
          onChange={(e) => handleChange('windMultiplier', Number(e.target.value))}
          className={styles.rangeInput}
        />
      </div>
    </aside>
  );
}
