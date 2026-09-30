import { motion } from 'framer-motion';
import { useClock } from '../hooks/useClock';
import styles from './Header.module.css';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

export function Header({ status, month }) {
  const time = useClock();
  const monthName = month ? MONTHS[month - 1] : '—';

  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        {/* SVG Logo Mark */}
        <motion.div
          className={styles.logoMark}
          animate={{ rotate: [0, 360] }}
          transition={{ duration: 30, repeat: Infinity, ease: 'linear' }}
        >
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="14" stroke="rgba(56,189,248,0.3)" strokeWidth="1" />
            <circle cx="16" cy="16" r="9" stroke="rgba(217,119,6,0.35)" strokeWidth="1" />
            {/* Polar grid lines */}
            <line x1="16" y1="2" x2="16" y2="30" stroke="rgba(217,119,6,0.18)" strokeWidth="0.5" />
            <line x1="2" y1="16" x2="30" y2="16" stroke="rgba(217,119,6,0.18)" strokeWidth="0.5" />
            <line x1="6.5" y1="6.5" x2="25.5" y2="25.5" stroke="rgba(217,119,6,0.12)" strokeWidth="0.5" />
            <line x1="25.5" y1="6.5" x2="6.5" y2="25.5" stroke="rgba(217,119,6,0.12)" strokeWidth="0.5" />
            {/* Center dot */}
            <circle cx="16" cy="16" r="3" fill="#d97706" opacity="0.9" />
            {/* Orbiting pulse */}
            <circle cx="16" cy="7" r="1.5" fill="#a07340" />
          </svg>
        </motion.div>

        <div className={styles.brandText}>
          <h1 className={styles.title}>PolarGrid<span className={styles.titleAccent}> AI</span></h1>
          <p className={styles.subtitle}>Ministry of Earth Sciences · Maitri Station · PS SIH26061</p>
        </div>
      </div>

      <div className={styles.meta}>
        <div className={styles.seasonTag}>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M6 1v10M1 6h10M2.5 2.5l7 7M9.5 2.5l-7 7" stroke="#9b9590" strokeWidth="1.2" strokeLinecap="round"/>
          </svg>
          {monthName} Season
        </div>

        <div className={styles.clock}>{time}</div>

        <StatusPill status={status} />
      </div>
    </header>
  );
}

function StatusPill({ status }) {
  const config = {
    live: { label: 'Live', color: '#10b981', pulse: true },
    connecting: { label: 'Connecting', color: '#f59e0b', pulse: false },
    error: { label: 'Offline', color: '#f43f5e', pulse: false },
  }[status] ?? { label: 'Connecting', color: '#f59e0b', pulse: false };

  return (
    <div className={styles.statusPill} style={{ borderColor: `${config.color}40`, color: config.color }}>
      <span
        className={styles.statusDot}
        style={{
          background: config.color,
          boxShadow: `0 0 6px ${config.color}`,
          animation: config.pulse ? 'statusPulse 2s ease-in-out infinite' : 'none',
        }}
      />
      {config.label}
    </div>
  );
}
