import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from src.network_coverage.infrastructure.persistence.sqlite.network_coverage_sqlite_repository import NetworkCoverageSQLiteRepository
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import NetworkCoverage


def test_get_coverage_data_by_coordinates_sqlite():
    # Setup in-memory SQLite
    engine = sa.create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)

    # Create the table defined by the ORM model
    NetworkCoverage.metadata.create_all(engine)

    session = Session()

    # Insert test rows using THE ORM MODEL
    inside = NetworkCoverage(
        code=1,
        long=1.005,   # inside 1 km longitude window (epsilon_long = 0.014)
        lat=2.007,    # inside 1 km latitude window  (epsilon_lat  = 0.009)
        g2=True,
        g3=False,
        g4=True,
    )

    outside = NetworkCoverage(
        code=2,
        long=1.20,    # far outside 1 km
        lat=2.30,
        g2=False,
        g3=False,
        g4=False,
    )

    session.add_all([inside, outside])
    session.commit()

    repo = NetworkCoverageSQLiteRepository(session)

    # Act — this uses epsilon=0.09, 0.13
    results = repo.get_coverage_data_by_coordinates(long=1.0, lat=2.0)

    # Assert
    assert len(results) == 1

    entity = results[0]
    assert entity.long == 1.005
    assert entity.lat == 2.007

    # Provider list should have 1 ProviderEntity (from to_entity())
    assert len(entity.provider_list) == 1
    provider = entity.provider_list[0]

    assert provider.code == 1
    assert provider.twoG is True
    assert provider.threeG is False
    assert provider.fourG is True
