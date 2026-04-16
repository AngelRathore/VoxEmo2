import numpy as np
import logging

from app.models.loader import get_assets
from app.utils.feature_extractor import extract_features

logger = logging.getLogger(__name__)

EMOTION_LABELS = {
    0: "angry",
    1: "calm",
    2: "disgust",
    3: "fearful",
    4: "happy",
    5: "neutral",
    6: "sad",
    7: "surprised",
}

EMOTION_METADATA = {
    "angry":     {"emoji": "😠", "color": "#ef4444"},
    "calm":      {"emoji": "😌", "color": "#6366f1"},
    "disgust":   {"emoji": "🤢", "color": "#84cc16"},
    "fearful":   {"emoji": "😨", "color": "#f59e0b"},
    "happy":     {"emoji": "😄", "color": "#22c55e"},
    "neutral":   {"emoji": "😐", "color": "#94a3b8"},
    "sad":       {"emoji": "😢", "color": "#3b82f6"},
    "surprised": {"emoji": "😮", "color": "#a855f7"},
}


def predict_emotion(file_path: str) -> dict:
    try:
        # ── Load model assets ─────────────────────────────
        model, scaler, pca = get_assets()

        # ── Extract features ─────────────────────────────
        features = extract_features(file_path)

        if features is None:
            raise ValueError("Feature extraction failed")

        features = np.array(features)

        # 🔥 Ensure 2D shape (CRITICAL FIX)
        if len(features.shape) == 1:
            features = features.reshape(1, -1)

        print("Features shape:", features.shape)

        # ── Scale + PCA ──────────────────────────────────
        features_scaled = scaler.transform(features)
        features_pca = pca.transform(features_scaled)

        print("After PCA shape:", features_pca.shape)

        # ── Prediction ───────────────────────────────────
        probs = model.predict(features_pca, verbose=0)[0]

        pred_idx = int(np.argmax(probs))
        emotion = EMOTION_LABELS[pred_idx]
        confidence = float(probs[pred_idx])

        # ── Build response ───────────────────────────────
        all_emotions = [
            {
                "label": EMOTION_LABELS[i],
                "probability": float(probs[i]),
                **EMOTION_METADATA[EMOTION_LABELS[i]],
            }
            for i in range(len(EMOTION_LABELS))
        ]

        all_emotions.sort(key=lambda x: x["probability"], reverse=True)

        return {
            "emotion": emotion,
            "confidence": round(confidence, 4),
            "emoji": EMOTION_METADATA[emotion]["emoji"],
            "color": EMOTION_METADATA[emotion]["color"],
            "all_emotions": all_emotions,
        }

    except Exception as e:
        logger.exception("Prediction failed")
        raise ValueError(f"Prediction pipeline error: {str(e)}")