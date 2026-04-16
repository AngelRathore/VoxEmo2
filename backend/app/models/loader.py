import pickle
import logging
from threading import Lock
from tensorflow.keras.models import load_model as keras_load_model
from app.config import get_settings

logger = logging.getLogger(__name__)

_model = None
_scaler = None
_pca = None
_lock = Lock()


def get_assets():
    """
    Lazy singleton loader — loads model/scaler/PCA only once on first
    prediction request. Thread-safe via Lock. All paths come from .env.
    """
    global _model, _scaler, _pca

    if _model is not None and _scaler is not None and _pca is not None:
        return _model, _scaler, _pca

    with _lock:
        cfg = get_settings()

        if _model is None:
            logger.info(f"Loading Keras model from: {cfg.model_path}")
            _model = keras_load_model(cfg.model_path, compile=False)
            logger.info("Model loaded successfully")

        if _scaler is None:
            logger.info(f"Loading scaler from: {cfg.scaler_path}")
            with open(cfg.scaler_path, "rb") as f:
                _scaler = pickle.load(f)
            logger.info("Scaler loaded successfully")

        if _pca is None:
            logger.info(f"Loading PCA from: {cfg.pca_path}")
            with open(cfg.pca_path, "rb") as f:
                _pca = pickle.load(f)
            logger.info("PCA loaded successfully")

    return _model, _scaler, _pca


def is_model_ready() -> bool:
    """Quick file-existence check used by /health."""
    try:
        import os
        cfg = get_settings()
        return all([
            os.path.exists(cfg.model_path),
            os.path.exists(cfg.scaler_path),
            os.path.exists(cfg.pca_path),
        ])
    except Exception:
        return False
