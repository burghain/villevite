import math
from pyproj import Transformer

class CoordToMeterConverter():
    
    def __init__(self, map_bounds):
        self.transformer = Transformer.from_crs("EPSG:4326", "EPSG:4647", always_xy=True)

        self.MIN_X, self.MIN_Y = self.transformer.transform(map_bounds[0], map_bounds[1])
        self.MAX_X, self.MAX_Y = self.transformer.transform(map_bounds[2], map_bounds[3])

    def geo_coords_to_meter(self, lonlat):
            lon = lonlat[0]
            lat = lonlat[1]

            x, y = self.transformer.transform(lon, lat)

            print(f'x: {x}, y: {y}')

            x -= self.MIN_X
            y -= self.MIN_Y

            return (x, y, 0)