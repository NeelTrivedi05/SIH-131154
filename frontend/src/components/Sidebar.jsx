/**
 * Sidebar — Environment metrics, battery SoC, and savings
 */
import { motion } from 'framer-motion';
import styles from './Sidebar.module.css';

export function Sidebar({ readings, dispatch, cumulative }) {
  const env  = readings?.environment ?? {};
  const batt = readings?.storage ?? {};
  const soc  = batt.battery_soc_percent ?? 0;
  const renPct = ((dispatch?.renewable_fraction ?? 0) * 100).toFixed(0);

  return (
    <aside className={styles.sidebar}>
      {/* Environment Block */}
      <Section title="Environment" subtitle="Maitri ~70°S">
        <div className={styles.envGrid}>
          <EnvTile icon={<TempIcon />} label="Temp" value={env.temperature_c?.toFixed(1)} unit="°C" color="#8baa70" />
          <EnvTile icon={<WindIcon />} label="Wind" value={env.wind_speed_ms?.toFixed(1)} unit="m/s" color="#8b9e68" />
          <EnvTile icon={<SolarIcon />} label="Irradiance" value={env.solar_irradiance_wm2?.toFixed(0)} unit="W/m²" color="#d97706" />
          <EnvTile icon={<SnowIcon />} label="Visibility" value="Clear" unit="" color="#9b9590" raw />
        </div>
      </Section>

      {/* Battery SoC */}
      <Section title="Battery Storage">
        <BatterySoC soc={soc} />
      </Section>

      {/* Renewable Fraction */}
      <Section title="Renewable Fraction">
        <RenewableArc pct={Number(renPct)} />
      </Section>

      {/* Savings */}
      <Section title="Session Savings">
        <SavingsBlock cumulative={cumulative} />
      </Section>
    </aside>
  );
}

/* ── Sub-components ── */

function Section({ title, subtitle, children }) {
  return (
    <div className={styles.section}>
      <div className={styles.sectionHeader}>
        <span className={styles.sectionTitle}>{title}</span>
        {subtitle && <span className={styles.sectionSub}>{subtitle}</span>}
      </div>
      {children}
    </div>
  );
}

function EnvTile({ icon, label, value, unit, color, raw }) {
  return (
    <div className={styles.envTile} style={{ borderColor: `${color}15` }}>
      <div className={styles.envIcon} style={{ color }}>{icon}</div>
      <div className={styles.envLabel}>{label}</div>
      <div className={styles.envValue} style={{ color }}>
        {raw ? value : <><span className="mono">{value ?? '—'}</span></>}
        {unit && <span className={styles.envUnit}>{unit}</span>}
      </div>
    </div>
  );
}

function BatterySoC({ soc }) {
  const pct = Math.min(100, Math.max(0, soc));
  const isLow  = pct < 15;
  const isWarn = pct < 25 && !isLow;
  const barColor = isLow ? '#f43f5e' : isWarn ? '#f59e0b' : '#10b981';

  return (
    <div className={styles.batteryWrap}>
      <div className={styles.batteryHeader}>
        <span className={styles.socValue} style={{ color: barColor }}>{pct.toFixed(1)}%</span>
        <span className={styles.socLabel}>State of Charge</span>
      </div>

      {/* Visual battery */}
      <div className={styles.battVisual}>
        <div className={styles.battOuter}>
          <motion.div
            className={styles.battFill}
            style={{ background: `linear-gradient(90deg, ${barColor}cc, ${barColor})` }}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          />
        </div>
        <div className={styles.battTerminal} />
      </div>

      {isLow && (
        <div className={styles.battWarn}>⚡ Critical — charging required</div>
      )}
    </div>
  );
}

function RenewableArc({ pct }) {
  // Simple SVG arc
  const r = 40;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ * 0.75; // 270° arc
  const color = pct > 60 ? '#d97706' : pct > 30 ? '#d4a85a' : '#9b9590';

  return (
    <div className={styles.arcWrap}>
      <svg width="110" height="80" viewBox="0 0 110 80">
        {/* Background arc */}
        <circle
          cx="55" cy="70" r={r}
          fill="none"
          stroke="rgba(56,189,248,0.08)"
          strokeWidth="10"
          strokeDasharray={`${circ * 0.75} ${circ * 0.25}`}
          strokeDashoffset={circ * 0.375}
          strokeLinecap="round"
          transform="rotate(135, 55, 70)"
        />
        {/* Value arc */}
        <motion.circle
          cx="55" cy="70" r={r}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={`${circ * 0.75} ${circ * 0.25}`}
          strokeDashoffset={circ * 0.375}
          strokeLinecap="round"
          transform="rotate(135, 55, 70)"
          initial={{ strokeDashoffset: circ * 0.375 + circ * 0.75 }}
          animate={{ strokeDashoffset: offset < 0 ? circ * 0.375 : circ * 0.375 + (circ * 0.75 - (pct / 100) * circ * 0.75) }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          style={{ filter: `drop-shadow(0 0 6px ${color}60)` }}
        />
        <text x="55" y="62" textAnchor="middle" fill={color} fontSize="18" fontWeight="700" fontFamily="IBM Plex Mono, monospace">{pct}%</text>
        <text x="55" y="74" textAnchor="middle" fill="#5c5850" fontSize="8" fontFamily="IBM Plex Mono, monospace" letterSpacing="1">RENEWABLE</text>
      </svg>
    </div>
  );
}

function SavingsBlock({ cumulative }) {
  const fuel = cumulative?.fuel_saved_litres ?? 0;
  const cost = cumulative?.cost_saved_inr ?? 0;

  return (
    <div className={styles.savings}>
      <SavingsRow
        icon={<FuelIcon />}
        label="Fuel Saved"
        value={`${fuel.toFixed(2)} L`}
        color="#10b981"
      />
      <SavingsRow
        icon={<RupeeIcon />}
        label="Cost Avoided"
        value={`₹${cost.toFixed(0)}`}
        color="#2dd4bf"
      />
    </div>
  );
}

function SavingsRow({ icon, label, value, color }) {
  return (
    <div className={styles.savingsRow} style={{ borderColor: `${color}18` }}>
      <span className={styles.savingsIcon} style={{ color }}>{icon}</span>
      <span className={styles.savingsLabel}>{label}</span>
      <span className={styles.savingsVal} style={{ color }}>{value}</span>
    </div>
  );
}

/* ── SVG Icons ── */
const TempIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M7 1v7M5 3h4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
    <circle cx="7" cy="10" r="2" fill="currentColor" fillOpacity="0.8"/>
  </svg>
);
const WindIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M1 5h8a2 2 0 1 0 0-4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
    <path d="M1 9h10a2 2 0 1 0 0-4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
    <path d="M1 13h6a2 2 0 1 1 0-4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
);
const SolarIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <circle cx="7" cy="7" r="2.5" fill="currentColor" fillOpacity="0.8"/>
    <path d="M7 1v1.5M7 11.5V13M1 7h1.5M11.5 7H13M3.1 3.1l1 1M9.9 9.9l1 1M3.1 10.9l1-1M9.9 4.1l1-1" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
);
const SnowIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M7 1v12M1 7h12M3.5 3.5l7 7M10.5 3.5l-7 7" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
);
const FuelIcon = () => (
  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
    <rect x="2" y="1" width="6" height="9" rx="1" stroke="currentColor" strokeWidth="1.1"/>
    <path d="M8 4h1a1 1 0 0 1 1 1v2a1 1 0 0 0 1 1" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round"/>
    <path d="M4 4h2" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round"/>
  </svg>
);
const RupeeIcon = () => (
  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
    <path d="M3 2h6M3 5h6M3 5a3 3 0 0 0 3 3M6 8l-3 2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
);
