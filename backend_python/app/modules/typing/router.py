from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.google_sheets import (
    get_typing_lessons as fetch_lessons,
    add_typing_lesson,
    update_typing_lesson,
    delete_typing_lesson,
    save_typing_result,
    get_typing_leaderboard as fetch_leaderboard
)
from app.modules.typing.models import TypingHistory
from app.modules.typing.schemas import CreateLessonRequest, TypingResultRequest, SaveHistoryRequest

router = APIRouter(tags=["Typing"])

# --- Lessons ---

@router.get("/typing-lessons")
def get_typing_lessons():
    return fetch_lessons()

@router.post("/typing-lessons")
def create_lesson(data: CreateLessonRequest):
    if not data.title or not data.content:
        raise HTTPException(status_code=400, detail="Title and content are required")
    lesson = add_typing_lesson(data.title, data.content)
    if lesson:
        return lesson
    raise HTTPException(status_code=500, detail="Failed to save lesson to Google Sheets")

@router.put("/typing-lessons/{lesson_id}")
def update_lesson(lesson_id: str, data: CreateLessonRequest):
    if not lesson_id or not data.title or not data.content:
        raise HTTPException(status_code=400, detail="ID, title and content are required")
    success = update_typing_lesson(lesson_id, data.title, data.content)
    if success:
        return {"success": True, "id": lesson_id, "title": data.title, "content": data.content}
    raise HTTPException(status_code=500, detail="Failed to update lesson in Google Sheets")

@router.delete("/typing-lessons/{lesson_id}")
def delete_lesson(lesson_id: str):
    success = delete_typing_lesson(lesson_id)
    if success:
        return {"success": True, "id": lesson_id}
    raise HTTPException(status_code=500, detail="Failed to delete lesson from Google Sheets")

# --- Results & Leaderboard ---

@router.post("/typing-result")
@router.post("/typing-results")
def post_typing_result(data: TypingResultRequest):
    if not data.lessonTitle:
        raise HTTPException(status_code=400, detail="Lesson Title is required")
    success = save_typing_result(
        data.username, data.lessonTitle, data.cpm, data.wpm, data.accuracy, data.timeSeconds
    )
    if success:
        return {"success": True}
    raise HTTPException(status_code=500, detail="Failed to save to Google Sheets")

@router.get("/typing-leaderboard")
def get_typing_leaderboard(lessonTitle: str = Query(None)):
    return fetch_leaderboard(lessonTitle)

# --- User History ---

@router.post("/typing-history")
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
            "createdAt": history.createdAt.isoformat() if hasattr(history.createdAt, "isoformat") else str(history.createdAt)
        }
    }

@router.get("/typing-history")
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
            "createdAt": r.createdAt.isoformat() if hasattr(r.createdAt, "isoformat") else str(r.createdAt)
        }
        for r in records
    ]
