import bpy
import igraph as ig
from .edge_properties import *


class BlenderMeshGen:

    def __init__(self, graph):
        self.g = graph

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

            sorter = EdgePropertySorter(edge_property_names)

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

                sorter.add_element(e)

            # create mesh
            new_mesh = bpy.data.meshes.new('mesh')
            new_mesh.from_pydata(vertices, edges, [])
            new_mesh.update()

            # add edge properties
            for name, dtype in zip(edge_property_names, edge_property_dtype):
                edge_attr = new_mesh.attributes.new(
                    name=name, type=dtype, domain='EDGE')
                edge_attr.data.foreach_set('value', sorter.get_property(name))

            # make object from mesh
            new_object = bpy.data.objects.new('x', new_mesh)

            # add object to scene collection
            collection = bpy.data.collections.new('City Generator')
            bpy.context.scene.collection.children.link(collection)
            collection.objects.link(new_object)

            print("Subgraph generation done")
            return new_object


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
