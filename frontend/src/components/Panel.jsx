/** Panel — reusable glass card with header */
import { motion } from 'framer-motion';
import styles from './Panel.module.css';

export function Panel({ title, subtitle, badge, badgeType, children, className }) {
  return (
    <motion.div
      className={`${styles.panel} ${className ?? ''}`}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className={styles.header}>
        <div>
          <div className={styles.title}>{title}</div>
          {subtitle && <div className={styles.subtitle}>{subtitle}</div>}
        </div>
        {badge && <Badge label={badge} type={badgeType} />}
      </div>
      <div className={styles.body}>
        {children}
      </div>
    </motion.div>
  );
}

function Badge({ label, type }) {
  const cls = type === 'live' ? styles.badgeLive : type === 'ml' ? styles.badgeMl : styles.badgeDefault;
  return <span className={`${styles.badge} ${cls}`}>{label}</span>;
}
