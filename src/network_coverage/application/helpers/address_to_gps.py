from typing import Tuple
import requests
from urllib.parse import quote


def get_coordinates_from_address(address: str) -> Tuple[float, float]:
    """
    Convert an address string into GPS coordinates (lon, lat)
    using the Geoportail geocoding API:
    https://data.geopf.fr/geocodage/search?q={address}
    """
    encoded_address = quote(address)

    url = f"https://data.geopf.fr/geocodage/search?q={encoded_address}"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise RuntimeError(f"Geoportail API error {response.status_code}: {response.text}")

    data = response.json()

    if "features" not in data or len(data["features"]) == 0:
        raise ValueError(f"No coordinates found for address: '{address}'")

    best_match = data["features"][0]
    long, lat = best_match["geometry"]["coordinates"]

    return long, lat
