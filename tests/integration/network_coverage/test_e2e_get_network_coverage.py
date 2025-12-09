import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import Base, NetworkCoverage
from src.network_coverage.infrastructure.persistence.sqlite.database import get_session


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
            pass  # do not close, fixture handles it

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    return client


# --- E2E test ---
def test_get_network_coverage_e2e(client, test_db_session):
    # Arrange: insert fake coverage data
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

    # Patch geocoder to return coordinates that match test DB
    with patch(
        "src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
        return_value=(2.3785, 48.8575)
    ):
        # Act: call API
        response = client.get("/papernest/network-coverage/?address=42+rue+papernest+75011+Paris")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "Orange": {"2G": True, "3G": True, "4G": False},
        "SFR": {"2G": True, "3G": True, "4G": True},
    }
