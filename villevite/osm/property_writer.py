import math
import json

class BasicPropertyWriter():

    def __init__(self, default):
        self.default = default

    def write_prop(self):
        raise NotImplementedError

class EdgePropertyWriter(BasicPropertyWriter):

    def __init__(self, name, default, dtype):
        super().__init__(default)
        self.name = name
        self.dtype = dtype

    def process_prop(self, row):
        raise NotImplementedError

    def write_prop(self, edge):
        edge[self.name] = self.prop

class NumberOfLanesWriter(EdgePropertyWriter):

    def process_prop(self, row):
        if 'lanes' in row:
            if row['lanes'] != None:
               self.prop = int(row['lanes'])
               return

            if 'width' in row:
                if row['width'] != None:
                    self.prop = max(math.floor(float(row['width']) / 5), 1)
                    return

        self.prop = self.default

class HasParkingLotsWriter(EdgePropertyWriter):

    def process_prop(self, row):
        tags = json.loads(row['tags'])

        self.prop = 'parking:both' in tags

class HasBikeLaneWriter(EdgePropertyWriter):

    def process_prop(self, row):
        self.prop = row['cycleway'] != None

class HasSidewalkWriter(EdgePropertyWriter):

    def process_prop(self, row):
        if row['sidewalk'] != None:
            self.prop = row['sidewalk'] in ['both', 'separate']

class StreetIDWriter(EdgePropertyWriter):

    def __init__(self, name, default, dtype):
        super().__init__(name, default, dtype)

        self.street_names = []

    def process_prop(self, row):
        if 'name' in row:
            street_name = row['name']
        else:
            street_name = ''

        if street_name in self.street_names:
            self.prop = self.street_names.index(street_name)
        else:
            self.prop = len(self.street_names)
            self.street_names.append(street_name)

class BasicBuildingPropertyWriter(BasicPropertyWriter):

    def process_prop(self, row):
        raise NotImplementedError

    def write_prop(self, e):
        raise NotImplementedError

class LevelWriter(BasicBuildingPropertyWriter):

    def process_prop(self, row):
        if 'building:levels' in row and row['building:levels'] != None:
            self.prop = math.ceil(float(row['building:levels']))
        else:
            self.prop = self.default

    def write_prop(self, e):
        e.levels = self.prop