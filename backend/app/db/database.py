from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=True)
    emotion = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    emoji = Column(String(10), nullable=True)
    all_emotions_json = Column(Text, nullable=True)   # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
