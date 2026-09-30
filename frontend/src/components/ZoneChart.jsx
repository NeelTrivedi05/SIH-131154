/**
 * ZoneChart — Horizontal bar chart for per-zone power consumption
 */
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Cell, ResponsiveContainer, LabelList,
} from 'recharts';
import styles from './ZoneChart.module.css';

const ZONE_CONFIG = [
  { key: 'laboratory_kw',    label: 'Lab',      color: '#8baa70' },
  { key: 'heating_kw',       label: 'Heating',  color: '#d97706' },
  { key: 'communications_kw', label: 'Comms',   color: '#8b9e68' },
  { key: 'quarters_kw',      label: 'Quarters', color: '#a07340' },
];

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className={styles.tooltip}>
      <div className={styles.tooltipLabel}>{label}</div>
      <div className={styles.tooltipVal}>{payload[0].value?.toFixed(1)} kW</div>
    </div>
  );
}

export function ZoneChart({ zones }) {
  const data = ZONE_CONFIG.map(z => ({
    name:  z.label,
    value: zones?.[z.key] ?? 0,
    color: z.color,
  }));

  const maxVal = Math.max(...data.map(d => d.value), 60);

  return (
    <ResponsiveContainer width="100%" height={180}>
      <BarChart
        data={data}
        layout="vertical"
        margin={{ top: 4, right: 48, left: 8, bottom: 4 }}
      >
        <CartesianGrid
          horizontal={false}
          stroke="rgba(46, 43, 38, 0.5)"
          strokeDasharray="3 3"
        />
        <XAxis
          type="number"
          domain={[0, maxVal * 1.1]}
          tick={{ fontSize: 9, fill: '#5c5850', fontFamily: 'IBM Plex Mono, monospace' }}
          tickLine={false}
          axisLine={false}
          tickFormatter={v => `${v.toFixed(0)}`}
        />
        <YAxis
          type="category"
          dataKey="name"
          tick={{ fontSize: 11, fill: '#9b9590' }}
          tickLine={false}
          axisLine={false}
          width={52}
        />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(46,43,38,0.2)' }} />
        <Bar dataKey="value" radius={[0, 5, 5, 0]} maxBarSize={18}>
          {data.map((entry) => (
            <Cell key={entry.name} fill={entry.color} fillOpacity={0.85} />
          ))}
          <LabelList
            dataKey="value"
            position="right"
            formatter={v => `${v.toFixed(0)} kW`}
            style={{ fontSize: 10, fill: '#5c5850', fontFamily: 'IBM Plex Mono, monospace' }}
          />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
