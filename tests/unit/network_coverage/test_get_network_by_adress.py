import pytest
from unittest.mock import patch, MagicMock

from src.network_coverage.application.get_network_coverage_by_address import (
    GetNetworkCoverageByAddress,
)
from src.network_coverage.domain.network_coverage import NetworkCoverage


def test_execute_returns_expected_coverage_list():

    mock_repo = MagicMock()
    usecase = GetNetworkCoverageByAddress(repository=mock_repo)

    fake_address = "10 Rue de Rivoli, Paris"

    fake_coverage_1 = NetworkCoverage(long=1, lat=2, provider_list=[])
    fake_coverage_2 = NetworkCoverage(long=3, lat=4, provider_list=[])

    # Mock coordinates returned by geocoder
    with patch(
        "src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
        return_value=[(1, 2), (3, 4)]
    ):
        # Mock repository calls
        mock_repo.get_coverage_data_by_coordinates.side_effect = [
            fake_coverage_1,
            fake_coverage_2,
        ]

        result = usecase.execute(fake_address)

        assert result == [fake_coverage_1, fake_coverage_2]

        # Verify repository was called with correct params
        mock_repo.get_coverage_data_by_coordinates.assert_any_call(1, 2)
        mock_repo.get_coverage_data_by_coordinates.assert_any_call(3, 4)

        assert mock_repo.get_coverage_data_by_coordinates.call_count == 2
