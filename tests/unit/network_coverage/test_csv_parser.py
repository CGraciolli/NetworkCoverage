import pytest
from unittest.mock import patch, mock_open
from src.network_coverage.infrastructure.csv.csv_parser import import_csv, create_session
from src.network_coverage.infrastructure.persistence.sqlite.models.network_coverage_model import NetworkCoverage
from src.network_coverage.infrastructure.csv.lambert93_to_gps import lambert93_to_gps

CSV_DATA = """Operateur;x;y;2G;3G;4G
1;102980;6847973;1;0;1
2;103000;6848000;0;1;1
"""

@pytest.fixture
def session():
    # In-memory SQLite DB for fast tests
    return create_session(":memory:")

def test_import_csv_inserts_rows(session):
    # Mock CSV file contents
    with patch("builtins.open", mock_open(read_data=CSV_DATA)):

        import_csv("fake.csv", session=session, batch_size=1)

        # Fetch rows
        rows = session.query(NetworkCoverage).all()

        assert len(rows) == 2

        assert rows[0].code == 1
        assert rows[0].long == lambert93_to_gps(102980, 6847973)[0]
        assert rows[0].lat == lambert93_to_gps(102980, 6847973)[1]
        assert rows[0].g2 is True
        assert rows[0].g3 is False
        assert rows[0].g4 is True

        assert rows[1].code == 2
        assert rows[1].g2 is False
