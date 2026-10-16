from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from config.google_sheets import (
    get_typing_lessons as fetch_lessons,
    add_typing_lesson,
    update_typing_lesson,
    delete_typing_lesson,
    save_typing_result,
    get_typing_leaderboard as fetch_leaderboard
)

router = APIRouter(prefix="/api", tags=["Typing"])

class CreateLessonRequest(BaseModel):
    title: str
    content: str

class TypingResultRequest(BaseModel):
    username: str = None
    lessonTitle: str
    cpm: int = 0
    wpm: int = 0
    accuracy: float = 0.0
    timeSeconds: str = None

@router.get("/typing-lessons")
def get_typing_lessons():
    lessons = fetch_lessons()
    return lessons

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

@router.post("/typing-result")
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
