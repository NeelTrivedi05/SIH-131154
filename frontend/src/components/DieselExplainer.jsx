import React from 'react';
import styles from './DieselExplainer.module.css';

export default function DieselExplainer({ explainer }) {
  if (!explainer) return null;

  return (
    <div className={styles.explainerCard}>
      <h3 className={styles.title}>Why diesel ON? (auto explainer)</h3>
      <div className={styles.content}>
        <p className={styles.paragraph}>{explainer.p1}</p>
        <p className={styles.paragraph}>{explainer.p2}</p>
        <p className={styles.paragraph}>{explainer.p3}</p>
      </div>
    </div>
  );
}
