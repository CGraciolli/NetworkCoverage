from fastapi import APIRouter, Query, Depends, HTTPException
from src.network_coverage.application.get_network_coverage_by_address import GetNetworkCoverageByAddress
from src.network_coverage.infrastructure.http.dependencies import get_network_coverage_use_case
from typing import Optional

router = APIRouter(prefix="/network-coverage", tags=["network-coverage"])


@router.get("/")
def get_network_coverage(
    address: str = Query(..., description="The address to get network coverage for"),
    accuracy: Optional[int] = Query(
        1,
        description="Optional accuracy level for the query"
    ),
    use_case: GetNetworkCoverageByAddress = Depends(get_network_coverage_use_case)
    ):
    try:
        return use_case.execute(address, accuracy)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
