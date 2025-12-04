from abc import ABC, abstractmethod


class NetworkCoverageRepository(ABC):
    @abstractmethod
    def get_coverage_data_by_coordinates(self, long: float, lat: float):
        raise NotImplementedError()