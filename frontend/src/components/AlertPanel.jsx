import React from 'react';
import styles from './AlertPanel.module.css';

const SEVERITY_STYLES = {
  critical: { color: 'var(--color-warning)', label: 'CRIT', bg: '#FDF2F0' },
  warning:  { color: 'var(--amber)', label: 'WARN', bg: '#FEF9EC' },
  info:     { color: 'var(--color-battery)', label: 'INFO', bg: '#F0F7F5' },
};

export function AlertPanel({ alerts = [] }) {
  const count = alerts.length;

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" className={styles.bellIcon}>
            <path d="M7 1a4 4 0 0 1 4 4v2.5l1 1.5H2l1-1.5V5a4 4 0 0 1 4-4zM5.5 11.5a1.5 1.5 0 0 0 3 0" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className={styles.title}>Safety Alerts & Interlocks</span>
          <span className={`${styles.countBadge} ${count > 0 ? styles.countBadgeActive : ''}`}>
            {count} Active
          </span>
        </div>
        <span className={styles.alertTime}>Advisory Monitoring</span>
      </div>

      <div className={styles.alertList}>
        {count === 0 ? (
          <div className={styles.emptyState}>
            ✓ All microgrid safety thresholds nominal — no active interlocks or furling conditions.
          </div>
        ) : (
          alerts.map((alert, i) => {
            const sev = SEVERITY_STYLES[alert.severity] || SEVERITY_STYLES.info;
            return (
              <div key={`${alert.code}-${i}`} className={styles.alertItem} style={{ backgroundColor: sev.bg }}>
                <div className={styles.alertStripe} style={{ backgroundColor: sev.color }} />
                <span className={styles.severityBadge} style={{ color: sev.color, backgroundColor: '#FFFFFF', border: `1px solid ${sev.color}` }}>
                  {sev.label}
                </span>
                <div className={styles.alertMsg}>
                  <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: 2 }}>
                    {alert.message}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                    {alert.action} • Code: <code>{alert.code}</code>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
