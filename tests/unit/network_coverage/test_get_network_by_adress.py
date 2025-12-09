import pytest
from unittest.mock import patch, MagicMock
from src.network_coverage.application.get_network_coverage_by_address import GetNetworkCoverageByAddress
from src.network_coverage.domain.network_coverage import NetworkCoverage, Provider

def test_execute_returns_expected_coverage_list():
    # Mock repository
    mock_repo = MagicMock()
    usecase = GetNetworkCoverageByAddress(repository=mock_repo)

    fake_address = "10 Rue de Rivoli, Paris"

    # Fake coverage data
    fake_coverage_1 = NetworkCoverage(
        long=1, lat=2,
        provider_list=[Provider(code=20801, twoG=True, threeG=True, fourG=False)],
    )

    # Patch geocoding function to return a single coordinate
    with patch(
        "src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
        return_value=(1, 2)
    ):
        # Repository returns coverage for that single coordinate
        mock_repo.get_coverage_data_by_coordinates.return_value = [fake_coverage_1]

        result = usecase.execute(fake_address)

    # Expected result
    expected_result = {
        "Orange": {"2G": True, "3G": True, "4G": False},
    }

    assert result == expected_result

    # Repository should be called once with default accuracy
    mock_repo.get_coverage_data_by_coordinates.assert_called_once_with(1, 2, 1)


def test_execute_with_custom_accuracy():
    # Mock repository
    mock_repo = MagicMock()
    usecase = GetNetworkCoverageByAddress(repository=mock_repo)

    fake_address = "10 Rue de Rivoli, Paris"

    fake_coverage_1 = NetworkCoverage(
        long=1, lat=2,
        provider_list=[Provider(code=20801, twoG=True, threeG=True, fourG=False)],
    )

    # Patch geocoding to return a single coordinate
    with patch(
        "src.network_coverage.application.get_network_coverage_by_address.get_coordinates_from_address",
        return_value=(1, 2)
    ):
        mock_repo.get_coverage_data_by_coordinates.return_value = [fake_coverage_1]

        # Act: call use case with a custom accuracy
        result = usecase.execute(fake_address, accuracy=5)

    # Expected result
    expected_result = {
        "Orange": {"2G": True, "3G": True, "4G": False},
    }

    assert result == expected_result

    # Repository should be called once with custom accuracy
    mock_repo.get_coverage_data_by_coordinates.assert_called_once_with(1, 2, 5)
