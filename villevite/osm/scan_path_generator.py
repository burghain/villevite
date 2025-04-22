import igraph as ig
import networkx as nx
import bpy

class ScanPathGenerator:

    def __init__(self, graph):
        self.g = graph

    def generate_path(self):
        path = self.find_path()
        self.draw_path(path=path)

    def find_path(self):
        nx_g = self.g.to_networkx()

        intersections = [ v for v in nx_g.nodes if nx_g.degree(v) > 2 ]

        solution = nx.approximation.traveling_salesman_problem(nx_g, nodes=intersections)

        return [self.g.vs[i]['coord'] for i in solution]

    def draw_path(self, path):
        vertices = path
        edges = []

        for i in range(0, len(vertices) - 1):
            edges.append((i, i+1))

        new_mesh = bpy.data.meshes.new('mesh')
        new_mesh.from_pydata(vertices, edges, [])
        new_mesh.update()

        new_object = bpy.data.objects.new('Scan Path', new_mesh)
        new_object.location = (0, 0, 1.5)

        collection = bpy.data.collections.new('Path')
        bpy.context.scene.collection.children.link(collection)
        collection.objects.link(new_object)
