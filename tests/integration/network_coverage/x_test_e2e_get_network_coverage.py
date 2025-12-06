import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from unittest.mock import patch

# Import FastAPI app
from src.main import app

# Import database dependency to override
from src.network_coverage.infrastructure.persistence.sqlite.database import get_session

# Import ORM model + Base
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import (
    Base,
    NetworkCoverage,
)


# -----------------------------
# Test database setup
# -----------------------------
@pytest.fixture
def test_db():
    """Creates an in-memory SQLite database and yields a Session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        future=True,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    Base.metadata.create_all(bind=engine)

    def _get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    return _get_db


@pytest.fixture
def client(test_db):
    """Create a TestClient with overridden DB dependency."""
    app.dependency_overrides[get_session] = test_db
    return TestClient(app)


# -----------------------------
# Actual E2E test
# -----------------------------
def test_get_network_coverage_e2e(client, test_db):
    # Insert test rows into the in-memory DB
    db = next(test_db())

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

    db.add_all([orange, sfr])
    db.commit()

    # Mock geocoding result to coordinates near the test data
    with patch(
        "src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
        return_value=[(2.3785, 48.8575)]
    ):
        response = client.get(
            "/network-coverage/",
            params={"q": "42 rue papernest 75011 Paris"}
        )

    assert response.status_code == 200

    assert response.json() == {
        "orange": {"2G": True, "3G": True, "4G": False},
        "SFR":    {"2G": True, "3G": True, "4G": True},
    }
