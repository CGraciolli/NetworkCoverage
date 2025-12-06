from abc import ABC, abstractmethod
from typing import List
from src.network_coverage.domain.network_coverage import NetworkCoverage as NetworkCoverageEntity


class NetworkCoverageRepository(ABC):
    @abstractmethod
    def get_coverage_data_by_coordinates(self, long: float, lat: float) -> List[NetworkCoverageEntity]:
        raise NotImplementedError()