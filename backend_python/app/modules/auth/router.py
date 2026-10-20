from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user_id
from app.modules.auth.models import User
from app.modules.auth.schemas import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="Username and password required")

    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = hash_password(data.password)
    new_user = User(
        username=data.username,
        password=hashed,
        name=data.name,
        gender=data.gender,
        location=data.location,
        profileImage=""
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(new_user.id)
    return {
        "token": token,
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "name": new_user.name,
            "profileImage": new_user.profileImage
        }
    }

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(user.id)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "profileImage": user.profileImage
        }
    }

@router.get("/me")
@router.get("/profile")
def get_profile(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "profileImage": user.profileImage,
        "createdAt": user.createdAt.isoformat() if hasattr(user.createdAt, "isoformat") else str(user.createdAt)
    }
