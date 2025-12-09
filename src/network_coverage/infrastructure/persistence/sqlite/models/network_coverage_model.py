import uuid
from sqlalchemy import Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from src.network_coverage.domain.network_coverage import NetworkCoverage as NetworkCoverageEntity
from src.network_coverage.domain.network_coverage import Provider as ProviderEntity


Base = declarative_base()


class NetworkCoverage(Base):
    __tablename__ = "network_coverage"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    long: Mapped[float] = mapped_column(Float, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    g2: Mapped[bool] = mapped_column(Boolean, nullable=False)
    g3: Mapped[bool] = mapped_column(Boolean, nullable=False)
    g4: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_entity(self) -> NetworkCoverageEntity:
        return NetworkCoverageEntity(
            long=self.long,
            lat=self.lat,
            provider_list=[ProviderEntity(
                code=self.code,
                twoG=self.g2,
                threeG=self.g3,
                fourG=self.g4
            )]
        )
