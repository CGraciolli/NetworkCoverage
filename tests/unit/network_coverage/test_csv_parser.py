import pytest
from unittest.mock import patch, mock_open
from src.network_coverage.infrastructure.csv.csv_parser import import_csv
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import NetworkCoverage, Base
from src.network_coverage.infrastructure.csv.lambert93_to_gps import lambert93_to_gps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


CSV_DATA = """Operateur;x;y;2G;3G;4G
1;102980;6847973;1;0;1
2;103000;6848000;0;1;1
"""

@pytest.fixture
def session():
    # Create an in-memory SQLite engine
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()

def test_import_csv_inserts_rows(session):
    # Patch open to use the CSV_DATA string
    with patch("builtins.open", mock_open(read_data=CSV_DATA)):
        import_csv("fake.csv", session=session, batch_size=1)

        rows = session.query(NetworkCoverage).all()
        assert len(rows) == 2

        # Row 0
        expected_long0, expected_lat0 = lambert93_to_gps(102980, 6847973)
        assert rows[0].code == 1
        assert rows[0].long == expected_long0
        assert rows[0].lat == expected_lat0
        assert rows[0].g2 is True
        assert rows[0].g3 is False
        assert rows[0].g4 is True

        # Row 1
        expected_long1, expected_lat1 = lambert93_to_gps(103000, 6848000)
        assert rows[1].code == 2
        assert rows[1].long == expected_long1
        assert rows[1].lat == expected_lat1
        assert rows[1].g2 is False
        assert rows[1].g3 is True
        assert rows[1].g4 is True

