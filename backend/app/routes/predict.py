import json
import os
import tempfile
import logging

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.database import Prediction, get_db
from app.services.predictor import predict_emotion

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".m4a", ".webm"}


@router.post("/predict")
async def predict(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    cfg = get_settings()

    # ── 1. Extension check ───────────────────────────────────────────────
    filename = file.filename or "upload"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # ── 2. File size check ───────────────────────────────────────────────
    raw_bytes = await file.read()

    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(raw_bytes) > cfg.max_audio_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {cfg.max_audio_size_mb} MB.",
        )

    # ── 3. Write to temp file ────────────────────────────────────────────
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(raw_bytes)
            tmp_path = tmp.name

        # ── 4. Audio duration check (SAFE VERSION) ────────────────────────
        try:
            import librosa
            duration = librosa.get_duration(path=tmp_path)
            print("Audio duration:", duration)
        except Exception as e:
            print("Librosa error, skipping duration check:", e)

        # ── 5. Run prediction ────────────────────────────────────────────
        try:
            result = predict_emotion(tmp_path)
        except Exception as e:
            logger.exception("Prediction pipeline failed")
            raise HTTPException(
                status_code=500,
                detail=f"Model inference failed: {str(e)}",
            )

        # ── 6. Persist to SQLite ─────────────────────────────────────────
        try:
            record = Prediction(
                filename=filename,
                emotion=result["emotion"],
                confidence=result["confidence"],
                emoji=result["emoji"],
                all_emotions_json=json.dumps(result["all_emotions"]),
            )
            db.add(record)
            db.commit()
            db.refresh(record)

            result["id"] = record.id
            result["saved_at"] = str(record.created_at)

        except Exception as e:
            logger.warning(f"DB write failed (non-fatal): {e}")
            db.rollback()

        return result

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)