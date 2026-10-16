from datetime import datetime, timezone
import re
from sqlalchemy import create_engine, TypeDecorator, String
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_URL, DB_PATH

class SequelizeDateTime(TypeDecorator):
    """
    Handles SQLite datetime strings stored by Sequelize,
    which include a space before the timezone offset, e.g. '2026-06-19 10:41:45.906 +00:00'.
    """
    impl = String
    cache_ok = True

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            val_str = value.strip()
            clean = re.sub(r"\s+([+-]\d{2}:\d{2})$", r"\1", val_str)
            try:
                return datetime.fromisoformat(clean)
            except Exception:
                pass
            for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(val_str.split("+")[0].strip(), fmt)
                except Exception:
                    pass
        return value

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " +00:00"
        return str(value)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"[OK] SQLite Database connected at {DB_PATH}")
