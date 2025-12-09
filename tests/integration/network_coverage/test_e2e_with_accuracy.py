import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import Base, NetworkCoverage
from src.network_coverage.domain.network_coverage import NetworkCoverage as NetworkCoverageEntity
from src.network_coverage.infrastructure.persistence.sqlite.database import get_session
from src.network_coverage.application.get_network_coverage_by_address import GetNetworkCoverageByAddress
from src.network_coverage.infrastructure.http.dependencies import get_network_coverage_use_case

# --- Fixture: in-memory database ---
@pytest.fixture
def test_db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=connection)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        connection.close()


# --- Fixture: TestClient with overridden DB dependency ---
@pytest.fixture
def client(test_db_session):
    def override_get_session():
        try:
            yield test_db_session
        finally:
            pass  # fixture handles closing

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


# --- E2E test: check accuracy propagation ---
def test_get_network_coverage_accuracy_propagation(client, test_db_session):
    # Arrange: insert fake coverage data into DB
    orange = NetworkCoverage(
        code=20801,
        long=2.378,
        lat=48.857,
        g2=True,
        g3=True,
        g4=False,
    )
    sfr = NetworkCoverage(
        code=20810,
        long=2.379,
        lat=48.858,
        g2=True,
        g3=True,
        g4=True,
    )
    test_db_session.add_all([orange, sfr])
    test_db_session.commit()

    # Create a mock repository
    mock_repo = MagicMock()
    mock_repo.get_coverage_data_by_coordinates.return_value = [
        orange.to_entity(),
        sfr.to_entity()
    ]

    # Override the use case dependency to inject the mock repository
    mock_use_case = GetNetworkCoverageByAddress(repository=mock_repo)
    app.dependency_overrides[get_network_coverage_use_case] = lambda: mock_use_case

    # Patch the geocoder to return controlled coordinates
    with patch(
        "src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
        return_value=(2.3785, 48.8575)
    ):
        # Act: call API with accuracy=2
        response = client.get(
            "/papernest/network-coverage/?address=42+rue+papernest+75011+Paris&accuracy=2"
        )

    # Assert: endpoint returns expected coverage
    assert response.status_code == 200
    assert response.json() == {
        "Orange": {"2G": True, "3G": True, "4G": False},
        "SFR": {"2G": True, "3G": True, "4G": True},
    }

    # Assert: repository was called with the correct coordinates and accuracy
    mock_repo.get_coverage_data_by_coordinates.assert_called_with(2.3785, 48.8575, 2)
