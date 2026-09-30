/**
 * EnergyMixChart — Recharts Radial donut with center label
 * Shows Wind / Solar / Diesel split live
 */
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { motion } from 'framer-motion';
import styles from './EnergyMixChart.module.css';

const COLORS = {
  Wind:    '#4A7A70',  /* data-wind */
  Solar:   '#C58A24',  /* data-solar */
  Diesel:  '#59635F',  /* data-grid / generator */
  Battery: '#357A6B',  /* data-battery */
};

const RADIAN = Math.PI / 180;

function CustomLabel({ cx, cy, midAngle, outerRadius, value, name }) {
  if (value < 5) return null;
  const radius = outerRadius + 20;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  return (
    <text x={x} y={y} fill={COLORS[name]} textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={10} fontFamily="IBM Plex Mono">
      {value.toFixed(0)}kW
    </text>
  );
}

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const { name, value } = payload[0];
  return (
    <div className={styles.tooltip}>
      <span style={{ color: COLORS[name] }}>{name}</span>
      <span className={styles.tooltipVal}>{value.toFixed(1)} kW</span>
    </div>
  );
}

export function EnergyMixChart({ generation }) {
  const data = [
    { name: 'Wind',   value: generation?.wind_kw   ?? 0 },
    { name: 'Solar',  value: generation?.solar_kw  ?? 0 },
    { name: 'Diesel', value: generation?.diesel_kw ?? 0 },
  ];

  const total = data.reduce((s, d) => s + d.value, 0);
  const renewable = ((data[0].value + data[1].value) / (total || 1) * 100).toFixed(0);

  return (
    <div className={styles.wrap}>
      <div className={styles.chartArea}>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={62}
              outerRadius={88}
              paddingAngle={3}
              dataKey="value"
              animationBegin={0}
              animationDuration={600}
              labelLine={false}
              label={CustomLabel}
            >
              {data.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={COLORS[entry.name]}
                  stroke="rgba(17,16,9,0.9)"
                  strokeWidth={2}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>

        {/* Center label */}
        <div className={styles.centerLabel}>
          <div className={styles.centerPct}>{renewable}%</div>
          <div className={styles.centerSub}>Renewable</div>
        </div>
      </div>

      {/* Legend */}
      <div className={styles.legend}>
        {data.map((d) => (
          <div key={d.name} className={styles.legendItem}>
            <span className={styles.legendDot} style={{ background: COLORS[d.name] }} />
            <span className={styles.legendName}>{d.name}</span>
            <span className={styles.legendVal}>{d.value.toFixed(1)} kW</span>
          </div>
        ))}
      </div>
    </div>
  );
}
