from fastapi import FastAPI
from network_coverage.infrastructure.http.network_coverage_router import router


app = FastAPI(title="My API")

app.include_router(router, prefix="/papernest")

#TODO: flake 8