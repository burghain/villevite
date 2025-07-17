import itertools
from .basic_extractor import BasicExtractor
from ..objects.building import Building
from ..utils import CoordToMeterConverter

class BuildingExtractor(BasicExtractor):

    def __init__(self, df, map_bounds):
        super().__init__(df.explode())

        self.map_bounds = map_bounds
        self.ctm_conv = CoordToMeterConverter(map_bounds)

    def write_to_array(self, arr, prop_register):
        for _, row in self.df.iterrows():
            geom = []

            for coord in row['geometry'].exterior.coords:
                geom.append(self.ctm_conv.geo_coords_to_meter(coord))

            b = Building(geom)

            prop_register.process_all_props(row)
            prop_register.write_all_props(b)

            arr.append(b)