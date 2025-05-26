import math

class BasicPropertyWriter():

    def __init__(self, name, default, dtype):
        self.name = name
        self.default = default
        self.dtype = dtype

    def process_prop(self, row):
        raise NotImplementedError

    def write_prop(self, edge):
        raise NotImplementedError
    
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

    def write_prop(self, edge):
        edge[self.name] = self.prop