from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings


_engine = None
SessionLocal = sessionmaker(autoflush=False, autocommit=False, future=True)


def init_engine():
    global _engine
    settings = get_settings()
    if _engine is None or str(_engine.url) != str(settings.DATABASE_URL):
        if _engine is not None:
            _engine.dispose()
        _engine = create_engine(settings.DATABASE_URL, future=True)
        SessionLocal.configure(bind=_engine)
    return _engine


def get_db():
    init_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    init_engine()
    return SessionLocal()


def reset_engine():
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None
