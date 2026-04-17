from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db, Prediction

router = APIRouter()

@router.get("/history")
def get_history(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    total = db.query(Prediction).count()
    rows = db.query(Prediction).order_by(Prediction.id.desc()).offset(offset).limit(limit).all()
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "results": [
            {
                "id": r.id,
                "emotion": r.emotion,
                "confidence": r.confidence,
                "emoji": r.emoji,
                "color": r.color,
                "filename": r.filename,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None,
            }
            for r in rows
        ],
    }

@router.delete("/history")
def clear_history(db: Session = Depends(get_db)):
    deleted = db.query(Prediction).delete()
    db.commit()
    return {"deleted": deleted, "message": "History cleared"}