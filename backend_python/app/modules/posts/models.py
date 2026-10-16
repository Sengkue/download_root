from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base, SequelizeDateTime

class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    viewCount = Column(Integer, default=0)
    likeCount = Column(Integer, default=0)
    commentCount = Column(Integer, default=0)
    userId = Column(Integer, ForeignKey("Users.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    createdAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updatedAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("app.modules.auth.models.User", back_populates="posts")
