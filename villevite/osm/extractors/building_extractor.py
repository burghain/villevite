import itertools
from .basic_extractor import BasicExtractor
from ..objects.building import Building
from ..utils import CoordToMeterConverter

class BuildingExtractor(BasicExtractor):

    def __init__(self, df, map_bounds):
        super().__init__(df)

        self.map_bounds = map_bounds
        self.ctm_conv = CoordToMeterConverter(map_bounds)

    def write_to_array(self, arr):
        for _, row in self.df.iterrows():
            geom = []

            for coord in row['geometry'].exterior.coords:
                geom.append(self.ctm_conv.geo_coords_to_meter(coord))

            arr.append(Building(geom))