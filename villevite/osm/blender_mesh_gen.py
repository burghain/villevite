import bpy
import igraph as ig

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

            osm_id_to_bvertex_idx = {}


            # fill in vertices
            for v in subgraph.vs:
                coords = v['coord']
                vertices.append((coords[0], coords[1], 0))

                osm_id_to_bvertex_idx[v['osm_id']] = len(vertices) - 1

            # fill in edges
            for e in subgraph.es:
                source = subgraph.vs[e.source]
                target = subgraph.vs[e.target]

                edges.append( (osm_id_to_bvertex_idx[source['osm_id']], osm_id_to_bvertex_idx[target['osm_id']]) )

                
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