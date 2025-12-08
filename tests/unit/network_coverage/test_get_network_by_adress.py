import pytest
from unittest.mock import patch, MagicMock

from src.network_coverage.application.get_network_coverage_by_address import GetNetworkCoverageByAddress
from src.network_coverage.domain.network_coverage import NetworkCoverage, Provider

def test_execute_returns_expected_coverage_list():
    mock_repo = MagicMock()
    usecase = GetNetworkCoverageByAddress(repository=mock_repo)

    fake_address = "10 Rue de Rivoli, Paris"

    fake_coverage_1 = NetworkCoverage(
        long=1, lat=2,
        provider_list=[Provider(code=20801, twoG=True, threeG=True, fourG=False)],
    )
    fake_coverage_2 = NetworkCoverage(
        long=3, lat=4,
        provider_list=[Provider(code=20813, twoG=True, threeG=True, fourG=True)],
    )

    with patch(
        "src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
        return_value=[(1, 2), (3, 4)]
    ):
        # IMPORTANT: return lists of coverage items
        mock_repo.get_coverage_data_by_coordinates.side_effect = [
            [fake_coverage_1],
            [fake_coverage_2],
        ]

        result = usecase.execute(fake_address)

    expected_result = {
        "Orange": {"2G": True, "3G": True, "4G": False},
        "SFR":    {"2G": True, "3G": True, "4G": True},
    }

    assert result == expected_result

    mock_repo.get_coverage_data_by_coordinates.assert_any_call(1, 2)
    mock_repo.get_coverage_data_by_coordinates.assert_any_call(3, 4)
    assert mock_repo.get_coverage_data_by_coordinates.call_count == 2
