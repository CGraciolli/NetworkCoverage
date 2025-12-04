from fastapi import APIRouter, Query, Depends
from src.network_coverage.application.get_network_coverage_by_address import GetNetworkCoverageByAddress
from src.network_coverage.infrastructure.http.dependencies import get_network_coverage_use_case

router = APIRouter(prefix="/network-coverage", tags=["network-coverage"])

@router.get("/")
def get_network_coverage(
    q: str = Query(..., description="The address to get network coverage for"),
    use_case: GetNetworkCoverageByAddress = Depends(get_network_coverage_use_case)
    ):
    return use_case.execute(q)
    