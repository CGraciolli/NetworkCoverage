import pytest
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import Base, NetworkCoverage
from src.network_coverage.domain.network_coverage import (
    NetworkCoverage as NetworkCoverageEntity,
    Provider as ProviderEntity,
)


@pytest.fixture
def session():
    """Create an in-memory database and provide a session."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


def test_table_exists(session):
    result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = {row[0] for row in result}

    assert "network_coverage" in tables


def test_insert_and_read(session):
    """Insert one NetworkCoverage row and verify fields."""

    nc = NetworkCoverage(
        code=42,
        long=12.5,
        lat=55.8,
        g2=True,
        g3=False,
        g4=True,
    )

    session.add(nc)
    session.commit()

    stored = session.query(NetworkCoverage).first()

    assert stored.code == 42
    assert stored.long == 12.5
    assert stored.lat == 55.8
    assert stored.g2 is True
    assert stored.g3 is False
    assert stored.g4 is True

    # UUID default should generate a valid UUID4 string
    assert uuid.UUID(stored.id)  # raises if not valid UUID


def test_to_entity_mapping(session):
    """Ensure to_entity() creates correct NetworkCoverageEntity + ProviderEntity."""

    nc = NetworkCoverage(
        code=7,
        long=99.1,
        lat=88.2,
        g2=False,
        g3=True,
        g4=False,
    )

    session.add(nc)
    session.commit()

    entity = nc.to_entity()

    assert isinstance(entity, NetworkCoverageEntity)
    assert entity.long == 99.1
    assert entity.lat == 88.2

    assert isinstance(entity.provider_list, list)
    assert len(entity.provider_list) == 1

    provider = entity.provider_list[0]
    assert isinstance(provider, ProviderEntity)

    # Verify mapping
    assert provider.code == 7
    assert provider.twoG is False
    assert provider.threeG is True
    assert provider.fourG is False
