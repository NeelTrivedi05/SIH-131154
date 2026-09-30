/**
 * KpiCard — Animated metric card with accent glow
 * Props: label, value, unit, delta, accentColor, icon (SVG element)
 */
import { motion, useSpring, useTransform } from 'framer-motion';
import { useEffect, useRef } from 'react';
import styles from './KpiCard.module.css';

export function KpiCard({ label, value, unit, delta, accentColor, icon, trend }) {
  const isNumeric = typeof value === 'number' && !isNaN(value);

  return (
    <motion.div
      className={styles.card}
      style={{ '--accent': accentColor }}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.015, borderColor: `${accentColor}40` }}
      transition={{ duration: 0.25 }}
    >
      {/* Accent line top */}
      <div className={styles.accentLine} style={{ background: accentColor }} />

      {/* Glow behind the card */}
      <div className={styles.glow} style={{ background: `radial-gradient(ellipse at 50% 0%, ${accentColor}18 0%, transparent 70%)` }} />

      <div className={styles.row}>
        <div className={styles.iconWrap} style={{ background: `${accentColor}15`, border: `1px solid ${accentColor}25` }}>
          {icon}
        </div>
        {trend !== undefined && (
          <TrendBadge trend={trend} />
        )}
      </div>

      <div className={styles.valueRow}>
        <AnimatedNumber value={isNumeric ? value : 0} decimals={1} className={styles.value} />
        <span className={styles.unit}>{unit}</span>
      </div>

      <div className={styles.label}>{label}</div>

      {delta && (
        <div className={styles.delta}>{delta}</div>
      )}
    </motion.div>
  );
}

function TrendBadge({ trend }) {
  if (trend === 0) return null;
  const up = trend > 0;
  return (
    <span className={`${styles.trendBadge} ${up ? styles.trendUp : styles.trendDown}`}>
      {up ? '▲' : '▼'} {Math.abs(trend).toFixed(1)}
    </span>
  );
}

function AnimatedNumber({ value, decimals = 1, className }) {
  const spring = useSpring(value, { stiffness: 80, damping: 20 });
  const display = useTransform(spring, (v) => v.toFixed(decimals));
  const ref = useRef(null);

  useEffect(() => {
    spring.set(value);
  }, [value, spring]);

  useEffect(() => {
    return display.on('change', (v) => {
      if (ref.current) ref.current.textContent = v;
    });
  }, [display]);

  return <span ref={ref} className={className}>{value.toFixed(decimals)}</span>;
}
