from fastapi import FastAPI
from src.network_coverage.infrastructure.http.api_router import api_router


app = FastAPI(title="My API")

app.include_router(api_router, prefix="/papernest")

#TODO: flake 8