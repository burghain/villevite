import xml.etree.ElementTree as ET
import igraph as ig
import math
from .edge_properties import edge_property_names, edge_property_defaults
from .objects.building import Building


class OSMParser():

    MIN_X = None
    MIN_Y = None
    MAX_X = None
    MAX_Y = None

    DEFAULT_STREET_LANE_COUNT = {
        'primary': 6,
        'secondary': 4,
        'tertiary': 2,
        'living_street': 2,
        'residential': 1
    }

    def geo_coords_to_meter(self, latlon, map_bounds):
        R = 6378137.0

        def lat2y(lat):
            return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * R

        def lon2x(lon):
            return math.radians(lon) * R

        if self.MIN_X == None:
            self.MIN_X = lon2x(map_bounds[0])

        if self.MIN_Y == None:
            self.MIN_Y = lat2y(map_bounds[1])

        if self.MAX_X == None:
            self.MAX_X = lon2x(map_bounds[2])

        if self.MAX_Y == None:
            self.MAX_Y = lat2y(map_bounds[3])

        lat = latlon[0]
        lon = latlon[1]

        x = lon2x(lon) - ((self.MIN_X + self.MAX_X) / 2)
        y = lat2y(lat) - ((self.MIN_Y + self.MAX_Y) / 2)

        return (x, y, 0)

    '''
    Read a plain XML OpenStreetMap File and output an igraph.Graph object
    where every node in the graph represents a vertex in the OSM data. Two nodes are
    connected iff the respective vertices are on the same OSM way. Real-world coordinates of the
    vertices are accessible via the 'coord' attribute of the node.

    filename (string).. Path to the OSM file.
    '''

    def parse(self, filename):

        # create graph and helper vars
        g = ig.Graph(directed=False)

        buildings = []

        no_highways = 0
        desired_type = ['primary', 'secondary',
                        'tertiary', 'living_street', 'residential']

        # read osm xml

        tree = ET.parse(filename)
        root = tree.getroot()

        bounds_tag = root.find('bounds')
        if bounds_tag != None:
            self.map_bounds = [float(bounds_tag.attrib['minlon']),
                               float(bounds_tag.attrib['minlat']),
                               float(bounds_tag.attrib['maxlon']),
                               float(bounds_tag.attrib['maxlat'])]

        # create node_to_coord dict
        for child in root:
            if child.tag == 'node':
                lat = float(child.attrib['lat'])
                lon = float(child.attrib['lon'])
                node_id = child.attrib['id']

                v = g.add_vertex()
                v['coord'] = self.geo_coords_to_meter(
                    [lat, lon], self.map_bounds)
                v['osm_id'] = node_id

        # build graph
        # building ways from node dict
        for child in root.findall("way"):
            if child.tag == 'way':
                is_desired_type = False

                way_property_watcher = PropertyWatcher(
                    edge_property_names, edge_property_defaults)

                # check for ways' properties
                for n in child:
                    if n.tag == 'tag':
                        if n.attrib['k'] == 'highway' and n.attrib['v'] in desired_type:
                            is_desired_type = True
                            way_property_watcher.watch(
                                'Number Of Lanes', self.DEFAULT_STREET_LANE_COUNT[n.attrib['v']])

                        way_property_watcher.watch(
                            'Has Sidewalk', n.attrib['k'] == 'sidewalk')
                        way_property_watcher.watch(
                            'Has Bike Lane', n.attrib['k'] == 'cycleway')
                        way_property_watcher.watch(
                            'Has Parking Lots', n.attrib['k'] == 'parking:both')

                for n in child:
                    if n.tag == 'tag':
                        # capture the ways width
                        if n.attrib['k'] == 'width':
                            way_property_watcher.watch('Number Of Lanes', max(
                                math.floor(float(n.attrib['v']) / 5), 1))

                        if n.attrib['k'] == 'lanes':
                            way_property_watcher.watch(
                                'Number Of Lanes', int(n.attrib['v']))

                if not is_desired_type:
                    continue

                no_highways += 1

                # iterate over osm_nodes that belong to the way and add them
                # and their respective connections to other nodes to the graph
                prev_vertex = None
                for n in child:
                    if n.tag == 'nd':
                        osm_id = n.attrib['ref']

                        current_vertex = g.vs.find(osm_id=osm_id)

                        if prev_vertex != None:
                            # Connect previous with current node
                            e = g.add_edge(current_vertex, prev_vertex)

                            way_properties = way_property_watcher.get_values()

                            for k, v in way_properties.items():
                                e[k] = v

                        prev_vertex = current_vertex

        # parse buildings
        for child in root.findall("way"):
            # is our osm way a building?
            is_building = False

            for tagtag in child.findall("tag"):
                if tagtag.attrib['k'] == 'building':
                    is_building = True

            if not is_building:
                continue

            # get geometry
            building_geom = []

            for n in child.findall("nd"):
                osm_id = n.attrib['ref']

                v = g.vs.find(osm_id=osm_id)

                building_geom.append(v['coord'])

            building_levels = 1

            # get attributes
            for tagtag in child.findall("tag"):
                if tagtag.attrib['k'] == 'building:levels':
                    building_levels = math.floor(float(tagtag.attrib['v']))

            building = Building(geom=building_geom)
            building.levels = building_levels

            buildings.append(building)

        # clear unconnected verts away
        lonely_vertices = g.vs.select(lambda v: v.degree() == 0)
        g.delete_vertices(lonely_vertices)

        print("Built graph")
        print(f"no. verts: {len(g.vs)}, no. edges: {len(g.es)}")

        print(f'no highways: {no_highways}')

        return g, buildings


class PropertyWatcher():

    def __init__(self, property_names, default_value):
        self.values = {}

        for i, name in enumerate(property_names):
            self.values[name] = default_value[i]

    def watch(self, name, value):
        if name in self.values:
            self.values[name] = self.values[name] if value == False else value
        else:
            self.values[name] = value

    def get_values(self):
        return self.values
