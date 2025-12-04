from fastapi import APIRouter
from .endpoints import network_coverage

api_router = APIRouter()
router.include_router(network_coverage.router, prefix="/network-coverage", tags=["Network Coverage"])