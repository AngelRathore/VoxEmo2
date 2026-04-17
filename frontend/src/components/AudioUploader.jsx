import React, { useRef, useState } from 'react';
import styles from './AudioUploader.module.css';

export default function AudioUploader({ onFile }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);
  const [fileName, setFileName] = useState(null);

  const handleFile = (file) => {
    if (!file) return;
    setFileName(file.name);
    onFile(file);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const onDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const onDragLeave = () => setDragging(false);

  const onInputChange = (e) => handleFile(e.target.files[0]);

  return (
    <div
      className={`${styles.dropzone} ${dragging ? styles.dragging : ''} ${fileName ? styles.hasFile : ''}`}
      onDrop={onDrop}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".wav,.mp3,.ogg,.flac,.m4a"
        onChange={onInputChange}
        className={styles.hiddenInput}
      />

      <div className={styles.icon}>
        {fileName ? '🎵' : '☁️'}
      </div>

      {fileName ? (
        <>
          <p className={styles.fileName}>{fileName}</p>
          <p className={styles.hint}>Click to choose a different file</p>
        </>
      ) : (
        <>
          <p className={styles.label}>Drop your audio file here</p>
          <p className={styles.hint}>WAV · MP3 · OGG · FLAC · M4A</p>
        </>
      )}
    </div>
  );
}
