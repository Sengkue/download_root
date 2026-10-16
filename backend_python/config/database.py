from datetime import datetime, timezone
from pathlib import Path
import re
from sqlalchemy import create_engine, TypeDecorator, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

class SequelizeDateTime(TypeDecorator):
    impl = String
    cache_ok = True

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            val_str = value.strip()
            # Handle Sequelize space before timezone offset: '2026-06-19 10:41:45.906 +00:00'
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

BASE_DIR = Path(__file__).resolve().parent.parent
# Look for database.sqlite in backend or locally in backend_python
DB_PATH = BASE_DIR.parent / "backend" / "database.sqlite"
if not DB_PATH.exists():
    DB_PATH = BASE_DIR / "database.sqlite"

DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

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

import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"[OK] SQLite Database connected at {DB_PATH}")
