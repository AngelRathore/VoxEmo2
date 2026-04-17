import numpy as np
import librosa
from app.config import settings


def extract_features(file_path: str) -> np.ndarray:
    """
    Extracts 194-dimensional feature vector from an audio file.
    Sample rate and duration come from .env via Settings.
    Raises ValueError on corrupt/unreadable audio.
    """
    sr = settings.audio_sample_rate
    duration = settings.audio_feature_duration

    try:
        y, sr = librosa.load(file_path, sr=sr)
    except Exception as e:
        raise ValueError(f"librosa could not decode audio: {e}") from e

    if len(y) == 0:
        raise ValueError("Audio loaded but contains no samples.")

    # Pad or trim to fixed length
    desired_len = duration * sr
    if len(y) < desired_len:
        y = np.pad(y, (0, desired_len - len(y)))
    else:
        y = y[:desired_len]

    features = []

    # MFCC (40)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    features.extend(np.mean(mfcc, axis=1))

    # Chroma (12)
    stft = np.abs(librosa.stft(y))
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    features.extend(np.mean(chroma, axis=1))

    # Mel Spectrogram (128)
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    features.extend(np.mean(mel, axis=1))

    # Spectral Contrast (7)
    contrast = librosa.feature.spectral_contrast(S=stft, sr=sr)
    features.extend(np.mean(contrast, axis=1))

    # Tonnetz (6)
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
    features.extend(np.mean(tonnetz, axis=1))

    # Spectral Flatness (1)
    flatness = librosa.feature.spectral_flatness(y=y)
    features.append(float(np.mean(flatness)))

    arr = np.array(features, dtype=np.float32)

    if len(arr) != 194:
        raise ValueError(f"Feature length mismatch: expected 194, got {len(arr)}")

    return arr.reshape(1, -1)
