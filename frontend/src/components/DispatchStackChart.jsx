import React, { memo } from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import styles from './Charts.module.css';

// Exact spec colors — 5 colors, no gimmicks
const C = {
  load:   '#17201D',  // main text color — the actual load line
  solar:  '#C58A24',  // data-solar
  wind:   '#4A7A70',  // data-wind
  diesel: '#59635F',  // data-grid / generator
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

function DispatchStackChart({ data }) {
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
        <h3 className={styles.chartTitle}>Optimized dispatch stack vs load</h3>
        <div className={styles.legend}>
          <div className={styles.legendItem}>
            <span className={styles.dashedLine} style={{ borderColor: C.load }} />
            <span>Load</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.squareIcon} style={{ backgroundColor: C.diesel }} />
            <span>Diesel</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.squareIcon} style={{ backgroundColor: C.wind }} />
            <span>Wind</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.squareIcon} style={{ backgroundColor: C.solar }} />
            <span>Solar</span>
          </div>
        </div>
      </div>

      <div className={styles.chartBody} style={{ height: 210 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: -10, bottom: 0 }}>
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
              domain={[0, 'auto']}
              label={{ value: 'kW', position: 'insideTopLeft', offset: -10, fill: '#8A948F', fontSize: 11 }}
            />
            <Tooltip content={<CustomTooltip />} />

            {/* Stacked Areas */}
            <Area
              type="monotone"
              dataKey="solar"
              name="Solar"
              stackId="1"
              stroke={C.solar}
              fill={C.solar}
              fillOpacity={0.8}
              isAnimationActive={false}
            />
            <Area
              type="monotone"
              dataKey="wind"
              name="Wind"
              stackId="1"
              stroke={C.wind}
              fill={C.wind}
              fillOpacity={0.8}
              isAnimationActive={false}
            />
            <Area
              type="monotone"
              dataKey="diesel"
              name="Diesel"
              stackId="1"
              stroke={C.diesel}
              fill={C.diesel}
              fillOpacity={0.85}
              isAnimationActive={false}
            />

            {/* Overlaid Load Line */}
            <Line
              type="monotone"
              dataKey="load"
              name="Load"
              stroke={C.load}
              strokeWidth={2}
              strokeDasharray="4 4"
              dot={false}
              isAnimationActive={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <div className={styles.xAxisCaption}>Time</div>
    </div>
  );
}

export default memo(DispatchStackChart);
