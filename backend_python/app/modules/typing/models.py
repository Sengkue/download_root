from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float

from app.core.database import Base, SequelizeDateTime

class TypingHistory(Base):
    __tablename__ = "TypingHistories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, nullable=False)
    lessonTitle = Column(String(255), nullable=False)
    wpm = Column(Integer, nullable=False, default=0)
    cpm = Column(Integer, nullable=False, default=0)
    accuracy = Column(Float, nullable=False, default=0.0)
    timeSeconds = Column(String(255), nullable=True)
    createdAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updatedAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
