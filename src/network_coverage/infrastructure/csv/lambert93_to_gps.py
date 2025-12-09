from pyproj import Transformer
from typing import Tuple


def lambert93_to_gps(x: float, y: float) -> Tuple[float, float]:
    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat
