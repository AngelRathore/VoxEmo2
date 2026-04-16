import React from 'react';
import styles from './Loader.module.css';

export default function Loader({ message = 'Analyzing audio...' }) {
  return (
    <div className={styles.wrapper}>
      <div className={styles.bars}>
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            className={styles.bar}
            style={{ animationDelay: `${i * 0.08}s` }}
          />
        ))}
      </div>
      <p className={styles.message}>{message}</p>
    </div>
  );
}
