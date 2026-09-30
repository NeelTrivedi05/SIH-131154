import React, { useState } from 'react';
import styles from './HourlyScheduleTable.module.css';

export default function HourlyScheduleTable({ schedule, station = 'maitri' }) {
  const [downloaded, setDownloaded] = useState(false);

  if (!schedule || schedule.length === 0) return null;

  const downloadCSV = () => {
    const headers = [
      'index',
      'time',
      'load',
      'forecast',
      'solar',
      'wind',
      'diesel',
      'ch',
      'dis',
      'soc',
      'unmet'
    ];

    const rows = schedule.map((row) => [
      row.idx,
      `"${row.time}"`,
      row.load,
      row.forecast,
      row.solar,
      row.wind,
      row.diesel,
      row.ch,
      row.dis,
      row.soc,
      row.unmet
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map((r) => r.join(','))
    ].join('\r\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const dateStr = new Date().toISOString().slice(0, 10);
    link.href = url;
    link.setAttribute('download', `hourly_schedule_${station}_${dateStr}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 2000);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3 className={styles.title}>Hourly schedule</h3>
      </div>

      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th className={styles.thIndex}></th>
              <th className={styles.thTime}>time</th>
              <th>load</th>
              <th>forecast</th>
              <th>solar</th>
              <th>wind</th>
              <th>diesel</th>
              <th>ch</th>
              <th>dis</th>
              <th>soc</th>
              <th>unmet</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map((row) => (
              <tr key={row.idx} className={styles.tr}>
                <td className={styles.tdIndex}>{row.idx}</td>
                <td className={styles.tdTime}>{row.time}</td>
                <td className={styles.tdNum}>{row.load}</td>
                <td className={styles.tdNum}>{row.forecast}</td>
                <td className={`${styles.tdNum} ${styles.colSolar}`}>{row.solar}</td>
                <td className={`${styles.tdNum} ${styles.colWind}`}>{row.wind}</td>
                <td className={`${styles.tdNum} ${styles.colDiesel}`}>{row.diesel}</td>
                <td className={styles.tdNum}>{row.ch}</td>
                <td className={styles.tdNum}>{row.dis}</td>
                <td className={`${styles.tdNum} ${styles.colSoc}`}>{row.soc}</td>
                <td className={`${styles.tdNum} ${row.unmet > 0 ? styles.colUnmetAlert : styles.colUnmetZero}`}>{row.unmet}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Sensible, clean Download CSV button below table */}
      <div className={styles.actionRow}>
        <button
          type="button"
          onClick={downloadCSV}
          className={`${styles.csvBtn} ${downloaded ? styles.csvBtnSuccess : ''}`}
          id="btn-download-schedule-csv"
        >
          {downloaded ? 'Downloaded CSV' : 'Download a CSV file'}
        </button>
      </div>
    </div>
  );
}
