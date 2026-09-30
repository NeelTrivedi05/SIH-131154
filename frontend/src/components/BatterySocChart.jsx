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

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className={styles.tooltip}>
        <div className={styles.tooltipTime}>{label}</div>
        <div className={styles.tooltipRow}>
          <span className={styles.tooltipDot} style={{ backgroundColor: '#357A6B' }} />
          <span className={styles.tooltipName}>Battery SoC:</span>
          <span className={styles.tooltipVal}>{payload[0].value} kWh</span>
        </div>
      </div>
    );
  }
  return null;
};

function BatterySocChart({ data }) {
  if (!data || data.length === 0) return null;

  const chartData = data.map((d, i) => {
    let tickName = d.timeShort;
    if (i === 0) tickName = '00:00\nMar 1, 2025';
    return {
      ...d,
      tickLabel: tickName,
    };
  });

  return (
    <div className={styles.chartCard}>
      <div className={styles.chartHeader}>
        <h3 className={styles.chartTitle}>Battery SoC trajectory (kWh)</h3>
        <div className={styles.toolIcons}>
          <span style={{ fontSize: '0.72rem', color: '#8A948F', fontFamily: 'IBM Plex Mono, monospace', letterSpacing: '0.06em' }}>24H HORIZON</span>
        </div>
      </div>

      <div className={styles.chartBody} style={{ height: 180 }}>
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
              interval={4}
            />
            <YAxis
              stroke="#D9DEDB"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#D9DEDB' }}
              tick={{ fill: '#8A948F', fontFamily: 'IBM Plex Mono, Consolas, monospace' }}
              domain={['auto', 'auto']}
              label={{ value: 'kWh', position: 'insideTopLeft', offset: -10, fill: '#8A948F', fontSize: 11 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="stepAfter"
              dataKey="soc"
              name="Battery SoC"
              stroke="#357A6B"
              strokeWidth={2}
              dot={{ r: 3, fill: '#357A6B', stroke: '#174A45' }}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default memo(BatterySocChart);
