import uuid
from sqlalchemy import Integer, String, Boolean, UniqueConstraint, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column


Base = declarative_base()

class Coverage(Base):
    __tablename__ = "coverage"
    __table_args__ = (
        UniqueConstraint("code", "x", "y", name="_coverage_unique_constraint"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    long: Mapped[float] = mapped_column(Float, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    g2: Mapped[bool] = mapped_column(Boolean, nullable=False)
    g3: Mapped[bool] = mapped_column(Boolean, nullable=False)
    g4: Mapped[bool] = mapped_column(Boolean, nullable=False)
