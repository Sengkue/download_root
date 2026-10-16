import os
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.post import Post
from models.user import User
from middlewares.auth import get_current_user_id

router = APIRouter(prefix="/api/posts", tags=["Posts"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("")
async def create_post(
    description: str = Form(None),
    image: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if not image or not image.filename:
        raise HTTPException(status_code=400, detail="Image file is required")

    file_ext = Path(image.filename).suffix or ".jpg"
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    dest_path = UPLOAD_DIR / unique_filename

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_post = Post(
        userId=user_id,
        image=f"/uploads/{unique_filename}",
        description=description or ""
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    user = db.query(User).filter(User.id == user_id).first()
    user_data = None
    if user:
        user_data = {
            "name": user.name,
            "gender": user.gender,
            "location": user.location,
            "profileImage": user.profileImage
        }

    return {
        "post": {
            "id": new_post.id,
            "image": new_post.image,
            "description": new_post.description,
            "viewCount": new_post.viewCount,
            "likeCount": new_post.likeCount,
            "commentCount": new_post.commentCount,
            "userId": new_post.userId,
            "createdAt": new_post.createdAt.isoformat() if new_post.createdAt else None,
            "user": user_data
        }
    }

@router.get("/local")
def get_local_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.createdAt.desc()).all()
    results = []
    for p in posts:
        user_data = None
        if p.user:
            user_data = {
                "name": p.user.name,
                "gender": p.user.gender,
                "location": p.user.location,
                "profileImage": p.user.profileImage
            }
        results.append({
            "id": p.id,
            "image": p.image,
            "description": p.description,
            "viewCount": p.viewCount,
            "likeCount": p.likeCount,
            "commentCount": p.commentCount,
            "userId": p.userId,
            "createdAt": p.createdAt.isoformat() if p.createdAt else None,
            "user": user_data
        })
    return {"posts": results}
