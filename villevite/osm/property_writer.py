import math
import json

class BasicPropertyWriter():

    def __init__(self, name, default, dtype):
        self.name = name
        self.default = default
        self.dtype = dtype

    def process_prop(self, row):
        raise NotImplementedError

    def write_prop(self, edge):
        edge[self.name] = self.prop

class NumberOfLanesWriter(BasicPropertyWriter):

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

class HasParkingLotsWriter(BasicPropertyWriter):

    def process_prop(self, row):
        tags = json.loads(row['tags'])

        self.prop = 'parking:both' in tags

class HasBikeLaneWriter(BasicPropertyWriter):

    def process_prop(self, row):
        self.prop = row['cycleway'] != None

class HasSidewalkWriter(BasicPropertyWriter):

    def process_prop(self, row):
        self.prop = row['sidewalk'] != None

class StreetIDWriter(BasicPropertyWriter):

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