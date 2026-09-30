import React from 'react';
import styles from './TierSheddingRelay.module.css';

export default function TierSheddingRelay({ tiers, economics }) {
  if (!tiers || !economics) return null;

  return (
    <div className={styles.section}>
      <h3 className={styles.title}>3-tier shedding relay + fuel economics</h3>

      {/* Tier Cards Row */}
      <div className={styles.tiersGrid}>
        <div className={`${styles.tierCard} ${styles.tier1Card}`}>
          <div className={styles.tierName}>Tier 1 · Life support</div>
          <div className={styles.tierStatus}>{tiers.tier1Status}</div>
          <div className={`${styles.badge} ${styles.badgeGreen}`}>
            <span className={styles.arrow}>↑</span> served {tiers.tier1ServedKwh} kWh
          </div>
        </div>

        <div className={`${styles.tierCard} ${styles.tier2Card}`}>
          <div className={styles.tierName}>Tier 2 · Living</div>
          <div className={styles.tierStatus}>{tiers.tier2Status}</div>
          <div className={`${styles.badge} ${styles.badgeBlue}`}>
            <span className={styles.arrow}>↑</span> served {tiers.tier2ServedKwh} kWh
          </div>
        </div>

        <div className={`${styles.tierCard} ${styles.tier3Card}`}>
          <div className={styles.tierName}>Tier 3 · Science</div>
          <div className={styles.tierStatus}>{tiers.tier3Status}</div>
          <div className={`${styles.badge} ${styles.badgeAmber}`}>
            <span className={styles.arrow}>↑</span> served {tiers.tier3ServedKwh} kWh
          </div>
        </div>
      </div>

      {/* Economics Stats Row */}
      <div className={styles.econGrid}>
        <div className={styles.econCard}>
          <div className={styles.econLabel}>Rs saved / day (Est)</div>
          <div className={`${styles.econValue} ${styles.econGreen}`}>{economics.rsSavedDay}</div>
        </div>

        <div className={styles.econCard}>
          <div className={styles.econLabel}>Seasonal Range (Est)</div>
          <div className={`${styles.econValue} ${styles.econTeal}`}>{economics.projectedRangeYr}</div>
        </div>

        <div className={styles.econCard}>
          <div className={styles.econLabel}>Relative Policy Delta</div>
          <div className={`${styles.econValue} ${styles.econBlue}`}>{economics.savingPctStr}</div>
        </div>

        <div className={styles.econCard}>
          <div className={styles.econLabel}>Integrity Notice</div>
          <div className={`${styles.econValue} ${styles.econSlate}`} style={{ fontSize: '0.85rem', fontWeight: 600 }}>
            {economics.statusTag}
          </div>
        </div>
      </div>

      {/* Footnote */}
      <div className={styles.footnote}>
        Simulation Note: Assumes 120 kW genset with 55% clamp (66 kW) [ASSUMED]. Compared against conventional uncoordinated rule-based policy. Advisory decision support only; figures are estimated ranges for mission planning.
      </div>
    </div>
  );
}
