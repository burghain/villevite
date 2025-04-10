import xml.etree.ElementTree as ET
import igraph as ig
import math
from .road_attributes import RoadAttributes
from .road_attribute_store import RoadAttributeStore
from mathutils import Vector


class OSMParser():

    KM_PER_LAT_DEG = 111

    # min building size
    min_size = 0.01

    #######

    # to compute bbox
    x_max = None
    y_max = None

    DEFAULT_STREET_LANE_COUNT = {
        'primary': 6,
        'secondary': 4,
        'tertiary': 2,
        'living_street': 2,
        'residential': 1
    }


    def geo_coords_to_meter(self, latlon, map_bounds):
        # Crop
        minlon = map_bounds[0]
        minlat = map_bounds[1]
        maxlon = map_bounds[2]
        maxlat = map_bounds[3]

        # compute meter extent
        delta_lat_geo = maxlat - minlat
        delta_lon_geo = maxlon - minlon

        lonlat_ratio = delta_lon_geo / delta_lat_geo

        delta_lat_meter = (delta_lat_geo * self.KM_PER_LAT_DEG) * 1000
        delta_lon_meter = delta_lat_meter * lonlat_ratio

        lat = latlon[0]
        lon = latlon[1]

        norm_lat = (maxlat - lat) / delta_lat_geo
        norm_lon = (maxlon - lon) / delta_lon_geo

        vec = Vector(((float(norm_lon * delta_lon_meter),
                     float(norm_lat * delta_lat_meter))))

        # calculate the bbox
        if self.x_max == None or self.x_max < vec[0]:
            self.x_max = vec[0]

        if self.y_max == None or self.y_max > vec[1]:
            self.y_max = vec[1]

        return Vector(( float(norm_lon * delta_lon_meter), float(norm_lat * delta_lat_meter), 0))

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

        road_attributes_store = RoadAttributeStore()

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
                v['coord'] = self.geo_coords_to_meter([lat, lon], self.map_bounds)
                v['osm_id'] = node_id

        # build graph
        # building ways from node dict
        for child in root:
            if child.tag == 'way':
                is_desired_type = False
                lanes = 1
                sidewalk = False
                cycleway = False

                # check for ways' properties
                for n in child:
                    if n.tag == 'tag':
                        if n.attrib['k'] == 'highway' and n.attrib['v'] in desired_type:
                            is_desired_type = True
                            lanes = self.DEFAULT_STREET_LANE_COUNT[n.attrib['v']]

                        if n.attrib['k'] == 'sidewalk':
                            sidewalk = True

                        if n.attrib['k'] == 'cycleway':
                            cycleway = True
                            
                for n in child:
                    if n.tag == 'tag':
                        # capture the ways width
                        if n.attrib['k'] == 'width':
                            lanes = max(math.floor(float(n.attrib['v']) / 5), 1)

                        if n.attrib['k'] == 'lanes':
                            lanes = int(n.attrib['v'])

                if not is_desired_type:
                    continue

                no_highways += 1

                road_attributes = RoadAttributes()
                road_attributes.number_of_lanes = lanes
                road_attributes.sidewalk = sidewalk
                road_attributes.cycleway = cycleway
                intersection_a = None
                intersection_b = None

                # iterate over osm_nodes that belong to the way and add them
                # and their respective connections to other nodes to the graph
                prev_vertex = None
                for n in child:
                    if n.tag == 'nd':
                        osm_id = n.attrib['ref']

                        current_vertex = g.vs.find(osm_id=osm_id)

                        if intersection_a == None:
                            intersection_a = current_vertex
                        
                        intersection_b = current_vertex

                        if prev_vertex != None:
                            # Connect previous with current node
                            e = g.add_edge(current_vertex, prev_vertex)

                            if lanes != None:
                                e['lanes'] = lanes

                        prev_vertex = current_vertex
                

                road_attributes.intersection_a_position = intersection_a['coord']
                road_attributes.intersection_b_position = intersection_b['coord']

                road_attributes_store.add_road_attributes(road_attributes)

        # clear unconnected verts away
        lonely_vertices = g.vs.select(lambda v: v.degree() == 0)
        g.delete_vertices(lonely_vertices)

        print("Built graph")
        print(f"no. verts: {len(g.vs)}, no. edges: {len(g.es)}")

        print(f'no highways: {no_highways}')

        return g, road_attributes_store, Vector((self.x_max, self.y_max))
