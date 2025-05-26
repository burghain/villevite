import bpy
import bmesh
import igraph as ig


def merge_meshes(name: str, meshes: list) -> bpy.types.Object:
    bm = bmesh.new()
    for mesh in meshes:
        bm.from_mesh(mesh)
    merged_mesh = bpy.data.meshes.new(name)
    bm.to_mesh(merged_mesh)

    return merged_mesh


class BlenderMeshGen:

    def __init__(self, graph, buildings, prop_reg):
        self.g = graph
        self.b = buildings
        self.prop_reg = prop_reg

    def generate(self):

        collection = bpy.data.collections.new('City Generator')
        bpy.context.scene.collection.children.link(collection)
        road_graph = self.generate_roads()
        buildings = self.generate_buildings()

        city_map_mesh = merge_meshes('City', [road_graph, buildings])
        city_map = bpy.data.objects.new('City', city_map_mesh)
        collection.objects.link(city_map)

        return city_map

    def generate_roads(self):
        g = self.g

        components = g.connected_components(mode='weak')

        no_components = len(components)

        print(f"Computed {no_components} components")

        # iterate through components
        # build blender mesh for every subgraph
        vertices = []
        edges = []

        sorter = EdgePropertySorter(self.prop_reg.get_prop_names())

        for subgraph in components.subgraphs():
            print("new subgraph")

            # fill in vertices
            for v in subgraph.vs:
                coord = v['coord']

                vertices.append(coord)

                v['bvertex_id'] = len(vertices) - 1

            # fill in edges
            for e in subgraph.es:
                source = subgraph.vs[e.source]
                target = subgraph.vs[e.target]

                edges.append((source['bvertex_id'], target['bvertex_id']))

                sorter.add_element(e)

        # create mesh
        new_mesh = bpy.data.meshes.new('mesh')
        new_mesh.from_pydata(vertices, edges, [])
        new_mesh.update()

        # add edge properties
        for name, dtype in zip(self.prop_reg.get_prop_names(), self.prop_reg.get_prop_dtypes()):
            edge_attr = new_mesh.attributes.new(
                name=name, type=dtype, domain='EDGE')
            edge_attr.data.foreach_set('value', sorter.get_property(name))

        print("Subgraph generation done")
        return new_mesh

    def generate_buildings(self):
        b = self.b

        vertices = []
        edges = []
        faces = []
        floors = []

        for building in b:
            v_start_id = len(vertices)

            vertices = vertices + building.geometry

            v_end_id = len(vertices) - 1

            for i in range(v_start_id, v_end_id):
                edges.append((i, i+1))

                faces.append(range(v_start_id, v_end_id + 1))

                floors.append(building.levels)

        # create mesh
        new_mesh = bpy.data.meshes.new('mesh')
        new_mesh.from_pydata(vertices, edges, faces)
        new_mesh.update()

        face_attr = new_mesh.attributes.new(
            name='Number Of Floors', type='INT8', domain='FACE')
        face_attr.data.foreach_set('value', floors)

        # make object from mesh
        new_object = bpy.data.objects.new('Buildings', new_mesh)

        return new_mesh


class EdgePropertySorter():

    def __init__(self, property_names):
        self.property_names = property_names

        self.values = {}

        for name in property_names:
            self.values[name] = []

    def add_element(self, e):
        for name in self.property_names:
            self.values[name].append(e[name])

    def get_property(self, property_name):
        return self.values[property_name]
