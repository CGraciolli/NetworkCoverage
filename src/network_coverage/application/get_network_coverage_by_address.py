from src.network_coverage.domain.network_coverage import NetworkCoverage
from src.network_coverage.domain.network_coverage_repository import NetworkCoverageRepository
from src.network_coverage.application.helpers.address_to_gps import get_coordinates_from_address
from typing import List


class GetNetworkCoverageByAddress:
    def __init__(self, repository: NetworkCoverageRepository):
        self.repository = repository

    def execute(self, address: str) -> List[NetworkCoverage]:
        long, lat = get_coordinates_from_address(address)
        coverage_data = self.repository.get_coverage_data_by_coordinates(long, lat)
        return coverage_data