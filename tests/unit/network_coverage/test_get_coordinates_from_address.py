import pytest
from unittest.mock import patch, MagicMock
from src.network_coverage.application.helpers.address_to_gps import get_coordinates_from_address

# --- Test successful API response ---
def test_get_coordinates_success():
    fake_response = {
        "features": [
            {"geometry": {"coordinates": [2.3522, 48.8566]}},  # Paris
            {"geometry": {"coordinates": [2.295, 48.8738]}},   # Eiffel Tower
        ]
    }

    mock_get = MagicMock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_response

    with patch("requests.get", mock_get):
        coords = get_coordinates_from_address("10 rue de Rivoli, Paris")

    assert coords == (2.3522, 48.8566), (2.295, 48.8738)


# --- Test API returns empty features ---
def test_get_coordinates_no_features():
    mock_get = MagicMock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"features": []}

    with patch("requests.get", mock_get):
        with pytest.raises(ValueError, match="No coordinates found"):
            get_coordinates_from_address("nonexistent address")


# --- Test API returns non-200 status ---
def test_get_coordinates_api_error():
    mock_get = MagicMock()
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "Server error"

    with patch("requests.get", mock_get):
        with pytest.raises(RuntimeError, match="Geoportail API error 500"):
            get_coordinates_from_address("any address")


# --- Test API returns malformed JSON ---
def test_get_coordinates_malformed_json():
    mock_get = MagicMock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = ValueError("invalid JSON")

    with patch("requests.get", mock_get):
        with pytest.raises(ValueError):
            get_coordinates_from_address("any address")
