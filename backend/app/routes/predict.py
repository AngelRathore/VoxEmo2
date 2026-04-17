import io
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.config import settings
from app.db.database import get_db, Prediction
from app.services.predictor import predict_emotion

router = APIRouter()

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".m4a"}
ALLOWED_MIMES = {"audio/wav", "audio/mpeg", "audio/ogg", "audio/flac", "audio/mp4",
                 "audio/x-wav", "audio/wave"}

@router.post("/predict")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Extension check
    import os
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(415, f"Unsupported file type '{ext}'")

    # 2. Read & size check
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(400, "Empty file")
    max_bytes = settings.max_audio_size_mb * 1024 * 1024
    if len(audio_bytes) > max_bytes:
        raise HTTPException(413, f"File exceeds {settings.max_audio_size_mb} MB limit")

    # 3. Run inference (validates duration + corruption internally)
    try:
        result = predict_emotion(audio_bytes)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"Inference failure: {e}")

    # 4. Persist to DB
    row = Prediction(
        emotion=result["emotion"],
        confidence=result["confidence"],
        emoji=result["emoji"],
        color=result["color"],
        filename=file.filename,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return {**result, "id": row.id, "saved_at": row.created_at.strftime("%Y-%m-%d %H:%M:%S")}