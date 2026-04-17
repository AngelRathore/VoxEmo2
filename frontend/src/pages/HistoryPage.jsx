import React, { useEffect, useState, useCallback } from 'react';
import api from '../api';
import styles from './HistoryPage.module.css';

export default function HistoryPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [clearing, setClearing] = useState(false);

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('/history?limit=50');
      setData(res.data);
    } catch (e) {
      setError('Could not load history. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const clearHistory = async () => {
    if (!window.confirm('Clear all prediction history?')) return;
    setClearing(true);
    try {
      await api.delete('/history');
      await fetchHistory();
    } catch {
      setError('Failed to clear history.');
    } finally {
      setClearing(false);
    }
  };

  return (
    <main className={styles.page}>
      <div className={styles.container}>
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>Prediction History</h1>
            <p className={styles.subtitle}>
              Stored in SQLite · {data ? `${data.total} total predictions` : '…'}
            </p>
          </div>

          {data?.total > 0 && (
            <button
              className={styles.clearBtn}
              onClick={clearHistory}
              disabled={clearing}
            >
              {clearing ? 'Clearing…' : '🗑 Clear All'}
            </button>
          )}
        </div>

        {loading && (
          <div className={styles.loading}>
            <div className={styles.loadingBars}>
              {Array.from({ length: 8 }).map((_, i) => (
                <div
                  key={i}
                  className={styles.loadingBar}
                  style={{ animationDelay: `${i * 0.1}s` }}
                />
              ))}
            </div>
          </div>
        )}

        {error && <div className={styles.errorBox}>⚠ {error}</div>}

        {!loading && data?.results?.length === 0 && (
          <div className={styles.empty}>
            <span className={styles.emptyIcon}>🎙</span>
            <p>No predictions yet. Go analyze some audio!</p>
          </div>
        )}

        {!loading && data?.results?.length > 0 && (
          <div className={styles.table}>
            <div className={styles.tableHead}>
              <span>#</span>
              <span>Emotion</span>
              <span>Confidence</span>
              <span>File</span>
              <span>Time</span>
            </div>

            {data.results.map((r, i) => (
              <div key={r.id} className={styles.tableRow}>
                <span className={styles.rowIndex}>{data.total - i}</span>

                <span className={styles.rowEmotion}>
                  {r.emoji} <strong>{r.emotion}</strong>
                </span>

                <span className={styles.rowConf}>
                  <div className={styles.confBar}>
                    <div
                      className={styles.confFill}
                      style={{ width: `${(r.confidence * 100).toFixed(0)}%` }}
                    />
                  </div>
                  {(r.confidence * 100).toFixed(1)}%
                </span>

                <span className={styles.rowFile} title={r.filename}>
                  {r.filename || '—'}
                </span>

                <span className={styles.rowTime}>
                  {r.created_at
                    ? new Date(r.created_at).toLocaleString()
                    : '—'}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}