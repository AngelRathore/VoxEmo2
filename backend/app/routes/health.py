from fastapi import APIRouter
from app.models.loader import is_model_ready
from app.config import get_settings

router = APIRouter()


@router.get("/health")
def health_check():
    cfg = get_settings()
    model_ready = is_model_ready()
    return {
        "status": "ok" if model_ready else "degraded",
        "service": "Voxemo API",
        "model_ready": model_ready,
        "model_dir": cfg.model_dir,
        "max_audio_size_mb": cfg.max_audio_size_mb,
        "max_audio_duration_sec": cfg.max_audio_duration_sec,
    }
