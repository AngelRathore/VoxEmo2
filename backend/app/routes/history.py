import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import Prediction, get_db

router = APIRouter()


@router.get("/history")
def get_history(
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """Return paginated prediction history from SQLite."""
    total = db.query(Prediction).count()
    rows = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    results = []
    for r in rows:
        try:
            all_emotions = json.loads(r.all_emotions_json or "[]")
        except Exception:
            all_emotions = []

        results.append({
            "id": r.id,
            "filename": r.filename,
            "emotion": r.emotion,
            "confidence": r.confidence,
            "emoji": r.emoji,
            "all_emotions": all_emotions,
            "created_at": str(r.created_at),
        })

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "results": results,
    }


@router.delete("/history")
def clear_history(db: Session = Depends(get_db)):
    """Clear all prediction history."""
    deleted = db.query(Prediction).delete()
    db.commit()
    return {"deleted": deleted, "message": "History cleared."}
