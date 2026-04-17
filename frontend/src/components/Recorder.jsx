import React, { useEffect, useRef } from 'react';
import useAudioRecorder from '../hooks/useAudioRecorder';
import styles from './Recorder.module.css';

export default function Recorder({ onBlob }) {
  const { isRecording, audioBlob, audioUrl, error, duration, startRecording, stopRecording, reset } = useAudioRecorder();
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const analyserRef = useRef(null);

  useEffect(() => {
    if (audioBlob) onBlob(audioBlob);
  }, [audioBlob, onBlob]);

  useEffect(() => {
    if (!isRecording) {
      cancelAnimationFrame(animFrameRef.current);
      return;
    }

    let stream;
    let audioCtx;

    navigator.mediaDevices.getUserMedia({ audio: true }).then((s) => {
      stream = s;
      audioCtx = new AudioContext();
      const source = audioCtx.createMediaStreamSource(s);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 128;
      source.connect(analyser);
      analyserRef.current = analyser;

      const canvas = canvasRef.current;
      const ctx = canvas?.getContext('2d');

      const draw = () => {
        if (!canvas || !ctx || !analyserRef.current) return;
        const data = new Uint8Array(analyserRef.current.frequencyBinCount);
        analyserRef.current.getByteFrequencyData(data);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const barW = canvas.width / data.length;
        data.forEach((val, i) => {
          const barH = (val / 255) * canvas.height;
          const hue = 260 + (i / data.length) * 60;
          ctx.fillStyle = `hsla(${hue}, 80%, 70%, 0.9)`;
          ctx.fillRect(i * barW, canvas.height - barH, barW - 1, barH);
        });

        animFrameRef.current = requestAnimationFrame(draw);
      };
      draw();
    });

    return () => {
      cancelAnimationFrame(animFrameRef.current);
      if (audioCtx) audioCtx.close();
      if (stream) stream.getTracks().forEach((t) => t.stop());
    };
  }, [isRecording]);

  const formatTime = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

  return (
    <div className={styles.recorder}>
      <canvas ref={canvasRef} className={styles.canvas} width={400} height={80} />

      <div className={styles.controls}>
        {!isRecording && !audioUrl && (
          <button className={styles.recordBtn} onClick={startRecording}>
            <span className={styles.dot} />
            Start Recording
          </button>
        )}

        {isRecording && (
          <button className={`${styles.recordBtn} ${styles.stop}`} onClick={stopRecording}>
            <span className={styles.square} />
            Stop — {formatTime(duration)}
          </button>
        )}

        {audioUrl && !isRecording && (
          <div className={styles.playbackRow}>
            <audio src={audioUrl} controls className={styles.audio} />
            <button className={styles.resetBtn} onClick={reset}>
              ↩ Re-record
            </button>
          </div>
        )}
      </div>

      {error && <p className={styles.error}>{error}</p>}
    </div>
  );
}
