import math

class CoordToMeterConverter():
    
    def __init__(self, map_bounds):
        self.R = 6378137.0

        self.MIN_X = self._lon2x(map_bounds[0])
        self.MIN_Y = self._lat2y(map_bounds[1])
        self.MAX_X = self._lon2x(map_bounds[2])
        self.MAX_Y = self._lat2y(map_bounds[3])

    def geo_coords_to_meter(self, latlon):
            lat = latlon[0]
            lon = latlon[1]

            x = self._lon2x(lon) - ((self.MIN_X + self.MAX_X) / 2)
            y = self._lat2y(lat) - ((self.MIN_Y + self.MAX_Y) / 2)

            return (x, y, 0)
    
    def _lat2y(self, lat):
                return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * self.R

    def _lon2x(self, lon):
        return math.radians(lon) * self.R