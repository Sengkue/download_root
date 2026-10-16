from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String

from app.core.database import Base, SequelizeDateTime

class WebviewLink(Base):
    __tablename__ = "WebviewLinks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    createdAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updatedAt = Column(SequelizeDateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
