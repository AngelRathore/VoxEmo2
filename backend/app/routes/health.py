from fastapi import APIRouter
from app.config import settings
from app.models.loader import is_model_ready

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Voxemo API",
        "model_ready": is_model_ready(),
        "model_dir": settings.model_dir,
        "max_audio_size_mb": settings.max_audio_size_mb,
        "max_audio_duration_sec": settings.max_audio_duration_sec,
    }