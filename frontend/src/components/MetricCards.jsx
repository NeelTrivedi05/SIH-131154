import React, { memo } from 'react';
import styles from './MetricCards.module.css';

function MetricCards({ kpis }) {
  if (!kpis) return null;

  return (
    <div className={styles.grid}>
      {/* Forecast MAE kW */}
      <div className={`${styles.card} ${styles.cardMae}`}>
        <div className={styles.label}>Measured MAE (Ridge)</div>
        <div className={styles.value}>{kpis.forecastMaeKw} <span className={styles.unit}>kW</span></div>
        <div className={`${styles.badge} ${styles.badgeBlue}`}>
          <span className={styles.arrow}>•</span> vs Persistence {kpis.persistenceMaeKw || '2.96'} kW
        </div>
      </div>

      {/* Fuel optimized L/day */}
      <div className={`${styles.card} ${styles.cardDiesel}`}>
        <div className={styles.label}>Advisory Fuel (Est)</div>
        <div className={styles.value}>{kpis.fuelOptimizedLDay} <span className={styles.unit}>L/day</span></div>
        <div className={`${styles.badge} ${styles.badgeSlate}`}>
          <span className={styles.arrow}>vs</span> Rule-based {kpis.baselineRuleBasedLDay || 180} L
        </div>
      </div>

      {/* Fuel saved */}
      <div className={`${styles.card} ${styles.cardFuel}`}>
        <div className={styles.label}>Simulated Saving</div>
        <div className={styles.value}>{kpis.fuelSavedLDay} <span className={styles.unit}>L/day</span></div>
        <div className={`${styles.badge} ${styles.badgeGreen}`}>
          <span className={styles.arrow}>↓</span> ~{kpis.fuelSavedPct}% vs Baseline
        </div>
      </div>

      {/* Advisory Decision Support */}
      <div className={`${styles.card} ${styles.cardCo2}`}>
        <div className={styles.label}>Control Architecture</div>
        <div className={styles.value}>Advisory <span className={styles.unit}>Support</span></div>
        <div className={`${styles.badge} ${styles.badgeTeal}`}>
          <span className={styles.arrow}>•</span> Human-in-the-Loop
        </div>
      </div>

      {/* Unmet kWh / RE frac */}
      <div className={`${styles.card} ${styles.cardRe}`}>
        <div className={styles.label}>Unmet Load / RE Share</div>
        <div className={styles.value}>{kpis.unmetKwh} <span className={styles.unit}>kWh</span></div>
        <div className={`${styles.badge} ${styles.badgeAmber}`}>
          <span className={styles.arrow}>•</span> RE {kpis.reFractionPct}% · Assumed Inputs
        </div>
      </div>
    </div>
  );
}

export default memo(MetricCards);
