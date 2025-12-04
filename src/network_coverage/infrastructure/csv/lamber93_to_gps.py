import pyproj
from typing import Tuple

def lamber93_to_gps(x, y) -> Tuple[float, float]:
	lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
	wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
	x = 102980
	y = 6847973
	long, lat = pyproj.transform(lambert, wgs84, x, y)
	return long, lat