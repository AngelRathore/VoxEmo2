import React from 'react';
import { Link } from 'react-router-dom';
import styles from './HomePage.module.css';

const EMOTIONS = [
  { label: 'Happy', emoji: '😄', color: '#22c55e' },
  { label: 'Sad', emoji: '😢', color: '#3b82f6' },
  { label: 'Angry', emoji: '😠', color: '#ef4444' },
  { label: 'Fearful', emoji: '😨', color: '#f59e0b' },
  { label: 'Calm', emoji: '😌', color: '#6366f1' },
  { label: 'Surprised', emoji: '😮', color: '#a855f7' },
  { label: 'Disgust', emoji: '🤢', color: '#84cc16' },
  { label: 'Neutral', emoji: '😐', color: '#94a3b8' },
];

const FEATURES = [
  { icon: '⚡', title: 'Real-time Analysis', desc: 'Upload or record audio and get instant emotion predictions powered by deep learning.' },
  { icon: '🧠', title: 'Deep Learning Model', desc: 'Trained on RAVDESS dataset with 194 audio features: MFCC, Chroma, Mel, Contrast, Tonnetz.' },
  { icon: '📊', title: 'Probability Breakdown', desc: 'See confidence scores across all 8 emotion classes in a clear, visual format.' },
  { icon: '🎙️', title: 'Record or Upload', desc: 'Use your browser microphone or upload any WAV/MP3 file directly.' },
];

export default function HomePage() {
  return (
    <main className={styles.page}>
      {/* Hero */}
      <section className={styles.hero}>
        <div className={styles.heroBadge}>
          <span className={styles.badgeDot} />
          Speech Emotion AI — RAVDESS Trained
        </div>

        <h1 className={styles.heroTitle}>
          Decode the emotion<br />
          <span className={styles.heroGradient}>hidden in your voice</span>
        </h1>

        <p className={styles.heroSub}>
          Voxemo uses deep neural networks to classify 8 distinct emotions
          from raw audio — with confidence scores and visual breakdowns.
        </p>

        <div className={styles.heroCta}>
          <Link to="/predict" className={styles.ctaPrimary}>
            Start Analyzing →
          </Link>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" className={styles.ctaSecondary}>
            View on GitHub
          </a>
        </div>

        {/* Floating waveform decoration */}
        <div className={styles.waveDecor}>
          {Array.from({ length: 40 }).map((_, i) => (
            <div
              key={i}
              className={styles.waveBar}
              style={{
                height: `${20 + Math.sin(i * 0.5) * 30 + Math.random() * 20}px`,
                animationDelay: `${i * 0.06}s`,
              }}
            />
          ))}
        </div>
      </section>

      {/* Emotions grid */}
      <section className={styles.emotionsSection}>
        <h2 className={styles.sectionTitle}>8 Emotions Detected</h2>
        <div className={styles.emotionsGrid}>
          {EMOTIONS.map((e) => (
            <div key={e.label} className={styles.emotionChip} style={{ '--chip-color': e.color }}>
              <span className={styles.emotionEmoji}>{e.emoji}</span>
              <span className={styles.emotionLabel}>{e.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className={styles.featuresSection}>
        <h2 className={styles.sectionTitle}>How it works</h2>
        <div className={styles.featuresGrid}>
          {FEATURES.map((f) => (
            <div key={f.title} className={styles.featureCard}>
              <div className={styles.featureIcon}>{f.icon}</div>
              <h3 className={styles.featureTitle}>{f.title}</h3>
              <p className={styles.featureDesc}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA band */}
      <section className={styles.ctaBand}>
        <h2 className={styles.ctaBandTitle}>Ready to hear your emotions?</h2>
        <Link to="/predict" className={styles.ctaPrimary}>
          Launch Analyzer →
        </Link>
      </section>
    </main>
  );
}
