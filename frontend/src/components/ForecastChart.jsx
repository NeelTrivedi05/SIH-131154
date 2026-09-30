/**
 * ForecastChart — 24h load forecast with confidence band
 * Uses Recharts AreaChart with gradient fill
 */
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts';
import styles from './ForecastChart.module.css';

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const pred = payload.find(p => p.dataKey === 'predicted');
  return (
    <div className={styles.tooltip}>
      <div className={styles.tooltipTime}>{label}</div>
      {pred && (
        <div className={styles.tooltipRow}>
          <span className={styles.tooltipDot} style={{ background: '#a07340' }} />
          <span className={styles.tooltipLabel}>Forecast</span>
          <span className={styles.tooltipVal}>{pred.value?.toFixed(1)} kW</span>
        </div>
      )}
    </div>
  );
}

export function ForecastChart({ forecast }) {
  if (!forecast?.length) {
    return <div className={styles.empty}>Awaiting forecast data…</div>;
  }

  const data = forecast.map(f => {
    const d = new Date(f.timestamp);
    const hh = String(d.getUTCHours()).padStart(2, '0');
    return {
      time: `${hh}:00`,
      predicted: f.predicted_load_kw,
      upper: f.upper_bound_kw,
      lower: f.lower_bound_kw,
    };
  });

  const now = new Date();
  const nowLabel = String(now.getUTCHours()).padStart(2, '0') + ':00';

  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={data} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="gradForecast" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#a07340" stopOpacity={0.12} />
            <stop offset="95%" stopColor="#a07340" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="gradBounds" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#a07340" stopOpacity={0.05} />
            <stop offset="95%" stopColor="#a07340" stopOpacity={0} />
          </linearGradient>
        </defs>

        <CartesianGrid
          stroke="rgba(46, 43, 38, 0.5)"
          strokeDasharray="3 3"
          vertical={false}
        />

        <XAxis
          dataKey="time"
          tick={{ fontSize: 10, fill: '#5c5850', fontFamily: 'IBM Plex Mono, monospace' }}
          tickLine={false}
          axisLine={false}
          interval={2}
        />

        <YAxis
          tick={{ fontSize: 10, fill: '#5c5850', fontFamily: 'IBM Plex Mono, monospace' }}
          tickLine={false}
          axisLine={false}
          tickFormatter={v => `${v}`}
          width={36}
          domain={['auto', 'auto']}
        />

        <Tooltip content={<CustomTooltip />} />

        <ReferenceLine
          x={nowLabel}
          stroke="rgba(217, 119, 6, 0.35)"
          strokeDasharray="4 3"
          label={{ value: 'Now', fill: '#d97706', fontSize: 9, fontFamily: 'IBM Plex Mono, monospace' }}
        />

        {/* Confidence band */}
        <Area
          type="monotone"
          dataKey="upper"
          stroke="none"
          fill="url(#gradBounds)"
          activeDot={false}
          legendType="none"
        />

        {/* Predicted line */}
        <Area
          type="monotone"
          dataKey="predicted"
          stroke="#a07340"
          strokeWidth={2}
          fill="url(#gradForecast)"
          dot={false}
          activeDot={{ r: 4, fill: '#a07340', strokeWidth: 2, stroke: '#111009' }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
