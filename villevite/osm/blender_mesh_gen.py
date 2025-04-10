import bpy
import igraph as ig


class BlenderMeshGen:

    def __init__(self, graph, road_attributes):
        self.g = graph
        self.road_attributes = road_attributes

    def generate(self):
        g = self.g
        components = g.connected_components(mode='weak')

        no_components = len(components)

        print(f"Computed {no_components} components")

        # iterate through components
        # build blender mesh for every subgraph
        for subgraph in components.subgraphs():
            # gather vertex and edge info
            vertices = []
            edges = []

            # fill in vertices
            for v in subgraph.vs:
                coords = v['coord']

                vertices.append((coords[0], coords[1], 0))

                v['bvertex_id'] = len(vertices) - 1

            # fill in edges
            for e in subgraph.es:
                source = subgraph.vs[e.source]
                target = subgraph.vs[e.target]

                edges.append((source['bvertex_id'], target['bvertex_id']))

            # create mesh
            new_mesh = bpy.data.meshes.new('mesh')
            new_mesh.from_pydata(vertices, edges, [])
            new_mesh.update()

            # make object from mesh
            new_object = bpy.data.objects.new('x', new_mesh)

            # add object to scene collection
            collection = bpy.data.collections.new('collection')
            bpy.context.scene.collection.children.link(collection)
            collection.objects.link(new_object)

            print("Subgraph generation done")

        self._add_road_attributes()

    def _add_road_attributes(self):
        # create mesh
        new_mesh = bpy.data.meshes.new('mesh')
        new_mesh.from_pydata([(0, 0, 0) for _ in range(0, len(self.road_attributes))], [], [])
        new_mesh.update()

        print(self.road_attributes.get_intersection_a_positions())

        # add intersection a position
        vert_attr = new_mesh.attributes.new(name='Intersection Position 0', type='FLOAT_VECTOR', domain='POINT')
        vert_attr.data.foreach_set('vector', self.road_attributes.get_intersection_a_positions())

        # add intersection b position
        vert_attr = new_mesh.attributes.new(name='Intersection Position 1', type='FLOAT_VECTOR', domain='POINT')
        vert_attr.data.foreach_set('vector', self.road_attributes.get_intersection_b_positions())

        for x in self.road_attributes:
            print("aaa")
            print(x[1])
            # add vertex property
            vert_attr = new_mesh.attributes.new(name=x[0][0], type=x[0][1], domain='POINT')
            vert_attr.data.foreach_set('value', x[1])

        # make object from mesh
        new_object = bpy.data.objects.new('data', new_mesh)

        # add object to scene collection
        collection = bpy.data.collections.new('collection')
        bpy.context.scene.collection.children.link(collection)
        collection.objects.link(new_object)
