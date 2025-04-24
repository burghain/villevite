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
        curve = bpy.data.curves.new('curve', type='CURVE')
        curve.dimensions = '3D'
        curve.resolution_u = 2

        polyline = curve.splines.new('BEZIER')
        polyline.bezier_points.add(len(path) - 1)
        for i, coord in enumerate(path):
            x, y, z = coord
            polyline.bezier_points[i].co = (x, y, 2.5)
            polyline.bezier_points[i].handle_left_type = 'ALIGNED'
            polyline.bezier_points[i].handle_right_type = 'ALIGNED'

        new_object = bpy.data.objects.new('Scan Path', curve)
        bpy.context.collection.objects.link(new_object)
