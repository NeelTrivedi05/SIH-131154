/**
 * AlertPanel — System alerts with severity badges and slide-in animation
 */
import { motion, AnimatePresence } from 'framer-motion';
import styles from './AlertPanel.module.css';

const SEVERITY = {
  critical: { color: '#b94a3b', bg: 'rgba(185,74,59,0.08)',  border: 'rgba(185,74,59,0.2)',  label: 'CRIT' },
  warning:  { color: '#c89030', bg: 'rgba(200,144,48,0.08)', border: 'rgba(200,144,48,0.2)', label: 'WARN' },
  info:     { color: '#7090a8', bg: 'rgba(91,127,166,0.08)', border: 'rgba(91,127,166,0.18)', label: 'INFO' },
};

export function AlertPanel({ alerts = [] }) {
  const count = alerts.length;

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" className={styles.bellIcon}>
            <path d="M7 1a4 4 0 0 1 4 4v2.5l1 1.5H2l1-1.5V5a4 4 0 0 1 4-4zM5.5 11.5a1.5 1.5 0 0 0 3 0" stroke="#5c5850" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className={styles.title}>System Alerts</span>
          <CountBadge count={count} />
        </div>
        <span className={styles.tick}>2s refresh</span>
      </div>

      <div className={styles.list}>
        <AnimatePresence mode="sync">
          {count === 0 ? (
            <motion.div
              key="empty"
              className={styles.empty}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style={{ opacity: 0.4 }}>
                <circle cx="10" cy="10" r="8" stroke="#10b981" strokeWidth="1.5"/>
                <path d="M7 10l2 2 4-4" stroke="#10b981" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              All systems nominal
            </motion.div>
          ) : (
            alerts.map((alert, i) => (
              <AlertItem key={`${alert.code}-${i}`} alert={alert} index={i} />
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function CountBadge({ count }) {
  const style = count > 0
    ? { background: '#f43f5e', color: '#fff' }
    : { background: 'rgba(71,85,105,0.3)', color: '#475569' };
  return (
    <span className={styles.badge} style={style}>{count}</span>
  );
}

function AlertItem({ alert, index }) {
  const s = SEVERITY[alert.severity] ?? SEVERITY.info;

  return (
    <motion.div
      className={styles.item}
      style={{ background: s.bg, borderColor: s.border }}
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 12 }}
      transition={{ delay: index * 0.04, duration: 0.2 }}
      layout
    >
      <div className={styles.itemLeft}>
        <div className={styles.dot} style={{ background: s.color, boxShadow: `0 0 6px ${s.color}` }} />
      </div>
      <div className={styles.itemBody}>
        <div className={styles.itemRow}>
          <span className={styles.severityTag} style={{ color: s.color, background: `${s.color}15`, borderColor: `${s.color}30` }}>
            {s.label}
          </span>
          <span className={styles.message}>{alert.message}</span>
        </div>
        <div className={styles.action}>{alert.action}</div>
        <div className={styles.code}>{alert.code}</div>
      </div>
    </motion.div>
  );
}
