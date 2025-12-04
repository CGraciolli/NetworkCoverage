from src.network_coverage.domain.network_coverage import NetworkCoverage
from src.network_coverage.domain.network_coverage_repository import NetworkCoverageRepository
from src.network_coverage.application.helpers.address_to_gps import get_coordinates_from_address
from typing import List


class GetNetworkCoverageByAddress:
    def __init__(self, repository: NetworkCoverageRepository):
        self.repository = repository

    def execute(self, address: str) -> List[NetworkCoverage]:
        list_of_coordinates = get_coordinates_from_address(address)
        list_of_coverage_data = []
        for coordinates in list_of_coordinates:
            long, lat = coordinates
            coverage_data = self.repository.get_coverage_data_by_coordinates(long, lat)
            list_of_coverage_data.append(coverage_data)
        return list_of_coverage_data