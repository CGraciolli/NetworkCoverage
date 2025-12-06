from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import Base

# Path to the real on-disk SQLite file
DATABASE_URL = "sqlite:///coverage.db"

engine = create_engine(
    DATABASE_URL,
    future=True,
    connect_args={"check_same_thread": False},  # Required for SQLite + FastAPI
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# FastAPI dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
