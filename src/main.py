from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import select, func
from src.network_coverage.infrastructure.http.network_coverage_router import router

from src.network_coverage.infrastructure.csv.csv_parser import import_csv
from src.network_coverage.infrastructure.persistence.sqlite.database import SessionLocal
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import NetworkCoverage


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ----- STARTUP -----
    session = SessionLocal()

    # Check if DB is empty
    count = session.scalar(select(func.count()).select_from(NetworkCoverage))

    if count == 0:
        print("📥 Importing CSV into SQLite…")
        import_csv("docs/providers.csv", db_file="coverage.db", session=session)
        print("✔ Import finished")

    session.close()

    # Continue app startup
    yield

    # ----- SHUTDOWN -----
    print("🛑 FastAPI shutting down…")


app = FastAPI(title="My API")

app.include_router(router, prefix="/papernest")
