from src.network_coverage.domain.network_coverage_repository import NetworkCoverageRepository
from sqlalchemy.orm import Session
from typing import List
from src.network_coverage.domain.network_coverage import NetworkCoverage as NetworkCoverageEntity
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import NetworkCoverage


class NetworkCoverageSQLiteRepository(NetworkCoverageRepository):
    def __init__(self, session: Session) -> None:
        self._session = session
    
    def get_coverage_data_by_coordinates(
            self,
            long: float,
            lat: float,
            epsilon_lat: float = 0.009,
            epsilon_long: float = 0.014
            ) -> List[NetworkCoverageEntity]:
        results = (
            self._session
            .query(NetworkCoverage)
            .filter(
                NetworkCoverage.lat.between(lat - epsilon_lat, lat + epsilon_lat),
                NetworkCoverage.long.between(long - epsilon_long, long + epsilon_long)
            )
            .all()
        )

        return [result.to_entity() for result in results]