import pytest  # noqa: F401
from src.network_coverage.infrastructure.csv.lambert93_to_gps import lambert93_to_gps


def test_lambert93_to_gps():

    # Example Lambert 93 coordinates
    x, y = 389003, 6324484

    # Expected GPS coordinates (these values should be pre-calculated)
    expected_long, expected_lat = -0.875659260, 43.950656461  # Example values for Paris

    long, lat = lambert93_to_gps(x, y)

    assert abs(long - expected_long) < 0.01
    assert abs(lat - expected_lat) < 0.01
