import os, pickle, threading
from app.config import settings

_lock = threading.Lock()
_model = _scaler = _pca = None
_loaded = False

def _load_all():
    global _model, _scaler, _pca, _loaded
    from tensorflow import keras
    _model  = keras.models.load_model(os.path.join(settings.model_dir, settings.model_file))
    with open(os.path.join(settings.model_dir, settings.scaler_file), "rb") as f:
        _scaler = pickle.load(f)
    with open(os.path.join(settings.model_dir, settings.pca_file), "rb") as f:
        _pca = pickle.load(f)
    _loaded = True

def get_model():
    global _loaded
    if not _loaded:
        with _lock:
            if not _loaded:
                _load_all()
    return _model, _scaler, _pca

def is_model_ready() -> bool:
    return all(os.path.exists(os.path.join(settings.model_dir, f))
               for f in [settings.model_file, settings.scaler_file, settings.pca_file])