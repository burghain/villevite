import numpy as np
from .road_attributes import RoadAttributes

class RoadAttributeStore():

    def __init__(self):
        self._attributes = [('Number Of Lanes', 'INT8'), ('Has Sidewalk', 'BOOLEAN'), ('Has Bike Lane', 'BOOLEAN')]

        self._array = np.empty(shape=(0, len(self._attributes)))
        self._positions = np.empty(shape=(0, 6))

    def add_road_attributes(self, road_attributes):
        data_row = np.array([
            int(road_attributes.number_of_lanes),
            road_attributes.sidewalk,
            road_attributes.cycleway
        ])

        pos_row = np.array(
            list(road_attributes.intersection_a_position) +
            list(road_attributes.intersection_b_position)
        )
        
        self._array = np.vstack((self._array, data_row))
        self._positions = np.vstack((self._positions, pos_row))

    def get_intersection_a_positions(self):
        return list(self._positions[:, 0:3].flatten())

    def get_intersection_b_positions(self):
        return list(self._positions[:, 3:6].flatten())

    def __len__(self):
        return len(self._array)
    
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self._attributes):
            x = (self._attributes[self.i], list(self._array[:, self.i].astype(int)))
            self.i += 1
            return x
        else:
            raise StopIteration
