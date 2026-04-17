import numpy as np
from app.models.loader import get_model
from app.utils.feature_extractor import extract_features

EMOTION_META = {
    "angry":     {"emoji": "😠", "color": "#ef4444"},
    "calm":      {"emoji": "😌", "color": "#60a5fa"},
    "disgust":   {"emoji": "🤢", "color": "#84cc16"},
    "fearful":   {"emoji": "😨", "color": "#a855f7"},
    "happy":     {"emoji": "😄", "color": "#22c55e"},
    "neutral":   {"emoji": "😐", "color": "#94a3b8"},
    "sad":       {"emoji": "😢", "color": "#3b82f6"},
    "surprised": {"emoji": "😲", "color": "#f97316"},
}

LABELS = ["angry", "calm", "disgust", "fearful", "happy", "neutral", "sad", "surprised"]


def predict_emotion(audio_bytes: bytes) -> dict:
    features = extract_features(audio_bytes)          # (194,)
    model, scaler, pca = get_model()

    scaled = scaler.transform(features.reshape(1, -1))  # (1, 194)
    reduced = pca.transform(scaled)                      # (1, n_components)
    probs = model.predict(reduced, verbose=0)[0]         # (8,)

    idx = int(np.argmax(probs))
    emotion = LABELS[idx]
    confidence = float(probs[idx])
    meta = EMOTION_META[emotion]

    all_emotions = [
        {
            "label": LABELS[i],
            "probability": float(probs[i]),
            "emoji": EMOTION_META[LABELS[i]]["emoji"],
            "color": EMOTION_META[LABELS[i]]["color"],
        }
        for i in range(len(LABELS))
    ]

    return {
        "emotion": emotion,
        "confidence": round(confidence, 4),
        "emoji": meta["emoji"],
        "color": meta["color"],
        "all_emotions": all_emotions,
    }