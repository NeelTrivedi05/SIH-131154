import React, { memo } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import styles from './Charts.module.css';

const C = {
  actual:   '#17201D',  // Actual load line (dark charcoal / primary text)
  forecast: '#174A45',  // Synthetic demo forecast (Deep Arctic Green)
  ridge:    '#8A948F',  // Ridge baseline (muted tertiary grey)
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className={styles.tooltip}>
        <div className={styles.tooltipTime}>{label}</div>
        {payload.map((entry, index) => (
          <div key={`item-${index}`} className={styles.tooltipRow}>
            <span
              className={styles.tooltipDot}
              style={{ backgroundColor: entry.color }}
            />
            <span className={styles.tooltipName}>{entry.name}:</span>
            <span className={styles.tooltipVal}>{entry.value} kW</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

function LoadForecastChart({ data }) {
  if (!data || data.length === 0) return null;

  const chartData = data.map((d, i) => {
    let tickName = d.timeShort;
    if (i === 0) tickName = '00:00\nMar 1, 2025';
    else if (i === 24) tickName = '00:00\nMar 2, 2025';
    return {
      ...d,
      tickLabel: tickName,
    };
  });

  return (
    <div className={styles.chartCard}>
      <div className={styles.chartHeader}>
        <h3 className={styles.chartTitle}>Load vs forecast (test window)</h3>
        <div className={styles.legend}>
          <div className={styles.legendItem}>
            <span className={styles.solidLine} style={{ backgroundColor: C.actual }} />
            <span>Actual load</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.solidLine} style={{ backgroundColor: C.forecast, height: 3 }} />
            <span>Synthetic demo forecast</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.dashedLine} style={{ borderColor: C.ridge }} />
            <span>Ridge baseline (fitted)</span>
          </div>
        </div>
      </div>

      <div className={styles.chartBody} style={{ height: 210 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#EEF1EF" vertical={false} />
            <XAxis
              dataKey="tickLabel"
              stroke="#D9DEDB"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#D9DEDB' }}
              tick={{ fill: '#8A948F', fontFamily: 'IBM Plex Mono, Consolas, monospace' }}
              interval={2}
            />
            <YAxis
              stroke="#D9DEDB"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#D9DEDB' }}
              tick={{ fill: '#8A948F', fontFamily: 'IBM Plex Mono, Consolas, monospace' }}
              domain={['auto', 'auto']}
              label={{ value: 'kW', position: 'insideTopLeft', offset: -10, fill: '#8A948F', fontSize: 11 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="load"
              name="Actual load"
              stroke={C.actual}
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
            <Line
              type="monotone"
              dataKey="forecast"
              name="Synthetic demo forecast"
              stroke={C.forecast}
              strokeWidth={2.2}
              dot={{ r: 2.5, fill: C.forecast, stroke: '#103B37' }}
              isAnimationActive={false}
            />
            <Line
              type="monotone"
              dataKey="ridge"
              name="Ridge baseline (fitted)"
              stroke={C.ridge}
              strokeWidth={1.5}
              strokeDasharray="3 3"
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className={styles.xAxisCaption}>Time</div>
    </div>
  );
}

export default memo(LoadForecastChart);
