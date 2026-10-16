from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base, SequelizeDateTime

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    gender = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    profileImage = Column(String(255), nullable=True)
    createdAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updatedAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
