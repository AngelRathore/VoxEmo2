import React from 'react';
import styles from './ResultCard.module.css';

export default function ResultCard({ result }) {
  const { emotion, confidence, emoji, color, all_emotions } = result;

  return (
    <div className={styles.card}>
      {/* Hero result */}
      <div className={styles.hero} style={{ '--emotion-color': color }}>
        <span className={styles.emoji}>{emoji}</span>
        <div className={styles.emotionInfo}>
          <p className={styles.label}>Detected Emotion</p>
          <h2 className={styles.emotion}>{emotion}</h2>
          <p className={styles.confidence}>
            {(confidence * 100).toFixed(1)}% confidence
          </p>
        </div>
        <div className={styles.ring} style={{ '--ring-color': color }} />
      </div>

      {/* All emotions breakdown */}
      <div className={styles.breakdown}>
        <h3 className={styles.breakdownTitle}>Full Breakdown</h3>
        <div className={styles.bars}>
          {all_emotions.map((e) => (
            <div key={e.label} className={styles.barRow}>
              <span className={styles.barEmoji}>{e.emoji}</span>
              <span className={styles.barLabel}>{e.label}</span>
              <div className={styles.barTrack}>
                <div
                  className={styles.barFill}
                  style={{
                    width: `${(e.probability * 100).toFixed(1)}%`,
                    background: e.color,
                  }}
                />
              </div>
              <span className={styles.barPct}>
                {(e.probability * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
