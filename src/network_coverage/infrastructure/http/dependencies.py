from fastapi import Depends
from sqlalchemy.orm import Session

from src.network_coverage.domain.network_coverage_repository import NetworkCoverageRepository
from src.network_coverage.application.get_network_coverage_by_address import GetNetworkCoverageByAddress


def network_coverage_repository(db: Session = Depends(get_database_session)) -> NetworkCoverageRepository:
    return NetworkCoverageRepository(db)

def get_network_coverage_use_case(
    repository: NetworkCoverageRepository = Depends(network_coverage_repository)
) -> GetNetworkCoverageByAddress:
    return GetNetworkCoverageByAddress(repository)