import React, { useState, useCallback } from 'react';
import api from '../api';
import AudioUploader from '../components/AudioUploader';
import Recorder from '../components/Recorder';
import ResultCard from '../components/ResultCard';
import Loader from '../components/Loader';
import styles from './PredictPage.module.css';

export default function PredictPage() {
  const [mode, setMode] = useState('upload');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const handleFile = useCallback((f) => {
    setFile(f);
    setResult(null);
    setError(null);
  }, []);

  const handleBlob = useCallback((blob) => {
    const f = new File([blob], 'recording.webm', { type: blob.type });
    setFile(f);
    setResult(null);
    setError(null);
  }, []);

  const analyze = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/predict', formData);
      const data = response.data;

      setResult(data);
      setHistory((prev) => [
        {
          ...data,
          fileName: file.name,
          timestamp: new Date().toLocaleTimeString(),
        },
        ...prev.slice(0, 4),
      ]);
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.message ||
        'Something went wrong. Is the backend running?';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <main className={styles.page}>
      <div className={styles.layout}>

        {/* LEFT PANEL */}
        <div className={styles.inputPanel}>

          <div className={styles.panelHeader}>
            <h1 className={styles.title}>Emotion Analyzer</h1>
            <p className={styles.subtitle}>
              Upload an audio file or record with your mic to detect speech emotion.
            </p>
          </div>

          {/* Tabs */}
          <div className={styles.tabs}>
            <button
              className={`${styles.tab} ${mode === 'upload' ? styles.tabActive : ''}`}
              onClick={() => { setMode('upload'); reset(); }}
            >
              ↑ Upload File
            </button>
            <button
              className={`${styles.tab} ${mode === 'record' ? styles.tabActive : ''}`}
              onClick={() => { setMode('record'); reset(); }}
            >
              ● Record
            </button>
          </div>

          {/* Input */}
          <div className={styles.inputArea}>
            {mode === 'upload' ? (
              <AudioUploader onFile={handleFile} />
            ) : (
              <Recorder onBlob={handleBlob} />
            )}
          </div>

          {/* Button */}
          {!loading && (
            <button className={styles.analyzeBtn} onClick={analyze}>
              ⚡ Analyze Emotion
            </button>
          )}

          {/* Error */}
          {error && (
            <div className={styles.errorBox}>
              <span>⚠</span> {error}
            </div>
          )}

          {/* History */}
          {history.length > 0 && (
            <div className={styles.history}>
              <p className={styles.historyTitle}>Recent Predictions</p>
              <div className={styles.historyList}>
                {history.map((h, i) => (
                  <div key={i} className={styles.historyItem}>
                    <span className={styles.historyEmoji}>{h.emoji}</span>
                    <div className={styles.historyInfo}>
                      <span className={styles.historyEmotion}>{h.emotion}</span>
                      <span className={styles.historyMeta}>
                        {(h.confidence * 100).toFixed(1)}% · {h.timestamp}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* RIGHT PANEL */}
        <div className={styles.resultPanel}>
          {loading && <Loader message="Processing..." />}
          {!loading && result && <ResultCard result={result} />}
          {!loading && !result && (
            <div className={styles.placeholder}>
              <div className={styles.placeholderIcon}>🎙</div>
              <p className={styles.placeholderText}>
                Your emotion prediction will appear here
              </p>
            </div>
          )}
        </div>

      </div>
    </main>
  );
}