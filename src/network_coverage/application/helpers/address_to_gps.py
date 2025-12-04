from typing import Tuple, List
import requests
from urllib.parse import quote


def get_coordinates_from_address(address: str) -> List[Tuple[float, float]]:
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
    
    list_of_coordinates = []
    for feature in data["features"]:
        long, lat = feature["geometry"]["coordinates"]
        list_of_coordinates.append((long, lat))

    return list_of_coordinates