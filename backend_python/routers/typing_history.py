from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.database import get_db
from models.typing_history import TypingHistory
from middlewares.auth import get_current_user_id

router = APIRouter(prefix="/api/typing-history", tags=["Typing History"])

class SaveHistoryRequest(BaseModel):
    lessonTitle: str
    wpm: int = 0
    cpm: int = 0
    accuracy: float = 0.0
    timeSeconds: str = None

@router.post("")
def save_history(
    data: SaveHistoryRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if not data.lessonTitle:
        raise HTTPException(status_code=400, detail="Lesson Title is required")

    history = TypingHistory(
        userId=user_id,
        lessonTitle=data.lessonTitle,
        wpm=data.wpm,
        cpm=data.cpm,
        accuracy=data.accuracy,
        timeSeconds=data.timeSeconds
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    return {
        "success": True,
        "data": {
            "id": history.id,
            "userId": history.userId,
            "lessonTitle": history.lessonTitle,
            "wpm": history.wpm,
            "cpm": history.cpm,
            "accuracy": history.accuracy,
            "timeSeconds": history.timeSeconds,
            "createdAt": history.createdAt.isoformat() if history.createdAt else None
        }
    }

@router.get("")
def get_history(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    records = db.query(TypingHistory).filter(TypingHistory.userId == user_id).order_by(TypingHistory.createdAt.desc()).all()
    return [
        {
            "id": r.id,
            "userId": r.userId,
            "lessonTitle": r.lessonTitle,
            "wpm": r.wpm,
            "cpm": r.cpm,
            "accuracy": r.accuracy,
            "timeSeconds": r.timeSeconds,
            "createdAt": r.createdAt.isoformat() if r.createdAt else None
        }
        for r in records
    ]
