from fastapi import APIRouter, HTTPException, status

from app.core.google_sheets import (
    get_learning_videos as fetch_videos,
    add_learning_video,
    update_learning_video,
    delete_learning_video
)
from app.modules.learning.schemas import VideoData

router = APIRouter(prefix="/learning-videos", tags=["Learning Videos"])

@router.get("")
@router.get("/")
def get_videos():
    return fetch_videos()

@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_video(data: VideoData):
    new_video = add_learning_video(data.model_dump())
    if new_video:
        return new_video
    raise HTTPException(status_code=500, detail="Database not connected or failed to add video")

@router.put("/{video_id}")
def update_video(video_id: str, data: VideoData):
    success = update_learning_video(video_id, data.model_dump())
    if success:
        return {"success": True}
    raise HTTPException(status_code=404, detail="Video not found or database not connected")

@router.delete("/{video_id}")
def delete_video(video_id: str):
    success = delete_learning_video(video_id)
    if success:
        return {"success": True}
    raise HTTPException(status_code=404, detail="Video not found or database not connected")
