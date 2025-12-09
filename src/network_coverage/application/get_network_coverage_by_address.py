from src.network_coverage.domain.network_coverage import Provider
from src.network_coverage.domain.network_coverage_repository import NetworkCoverageRepository
from src.network_coverage.application.helpers.address_to_gps import get_coordinates_from_address
from typing import List, Optional


class GetNetworkCoverageByAddress:
    def __init__(self, repository: NetworkCoverageRepository):
        self.repository = repository

    def execute(self, address: str, accuracy: int = 1) -> dict:
        try:
            long, lat = get_coordinates_from_address(address)
        except Exception as e:
            raise RuntimeError(f"Failed to geocode address '{address}'") from e
        list_of_providers: List[Provider] = []
        coverage_data = self.repository.get_coverage_data_by_coordinates(long, lat, accuracy)
        for coverage_datum in coverage_data:
            list_of_providers += coverage_datum.provider_list

        providers_dict = {}
        for provider in list_of_providers:
            provider.add_to_dict(providers_dict)

        return providers_dict