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
def test_get_network_coverage_invalid_address(client):
    # Patch geocoding to simulate a ValueError for invalid address
    with patch("src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
               side_effect=ValueError("No coordinates found for address")):

        response = client.get("/papernest/network-coverage/?address=INVALID_ADDRESS")

    # Assert 400 response
    assert response.status_code == 400
    assert "Failed to geocode address 'INVALID_ADDRESS'" in response.text
