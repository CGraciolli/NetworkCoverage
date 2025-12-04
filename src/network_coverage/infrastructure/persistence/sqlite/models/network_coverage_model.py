import uuid
from sqlalchemy import Integer, String, Boolean, UniqueConstraint, Float
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from src.network_coverage.domain.network_coverage import NetworkCoverage as NetworkCoverageEntity


Base = declarative_base()

class NetworkCoverage(Base):
    __tablename__ = "network_coverage"
    __table_args__ = (
        UniqueConstraint("code", "x", "y", name="_network_coverage_unique_constraint"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    long: Mapped[float] = mapped_column(Float, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    g2: Mapped[bool] = mapped_column(Boolean, nullable=False)
    g3: Mapped[bool] = mapped_column(Boolean, nullable=False)
    g4: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_entity(self) -> NetworkCoverageEntity:
        return NetworkCoverageEntity(
            code=self.code,
            long=self.long,
            lat=self.lat,
            g2=self.g2,
            g3=self.g3,
            g4=self.g4,
        )