from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base, SequelizeDateTime

class YouTubeChannel(Base):
    __tablename__ = "youtube_channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channelId = Column(String(255), unique=True, nullable=False)
    channelTitle = Column(String(255), nullable=False)
    thumbnailUrl = Column(String(255), nullable=True)
    accessToken = Column(Text, nullable=False)
    refreshToken = Column(Text, nullable=True)
    tokenExpiry = Column(SequelizeDateTime, nullable=True)
    createdAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updatedAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class TikTokChannel(Base):
    __tablename__ = "tiktok_channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channelId = Column(String(255), unique=True, nullable=False)
    channelTitle = Column(String(255), nullable=False)
    thumbnailUrl = Column(String(255), nullable=True)
    accessToken = Column(Text, nullable=False)
    refreshToken = Column(Text, nullable=True)
    tokenExpiry = Column(SequelizeDateTime, nullable=True)
    createdAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updatedAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
