import sys

import bpy

'''
Generates a city from a road graph and saves it as .blend

Usage:
    blender -b --python generate_city.py -- <output.blend> [<graph.blend> [<object_name>]]

argv[0].. File to save the generated city to
argv[1].. Optional .blend file containing a user-prepared road graph
argv[2].. Optional name of the road graph object in that file (default: "Road Graph";
          falls back to the file's active object if the named object is absent)

Without a graph file, the city is generated from the bundled Default Road Graph.
Requires the villevite extension to be installed in the executing Blender.
'''

argv = sys.argv
argv = argv[argv.index("--") + 1:]

if not argv:
    print("Usage: blender -b --python generate_city.py -- <output.blend> [<graph.blend> [<object_name>]]")
    sys.exit(1)

from bl_ext.user_default.villevite import road_graph  # noqa: E402

if len(argv) > 1:
    bpy.ops.wm.open_mainfile(filepath=argv[1])
    object_name = argv[2] if len(argv) > 2 else "Road Graph"
    graph = bpy.data.objects.get(object_name)
    if not road_graph.is_valid_road_graph(graph):
        graph = bpy.context.view_layer.objects.active
    if not road_graph.is_valid_road_graph(graph):
        print(f"ERROR: no valid road graph '{object_name}' in {argv[1]}")
        sys.exit(1)
    bpy.context.view_layer.objects.active = graph
    graph.select_set(True)
else:
    # Empty scene: the generate operator loads the Default Road Graph itself
    bpy.ops.villevite.clear_all()

bpy.ops.villevite.generate_city(for_scanning=True)

bpy.ops.wm.save_as_mainfile(filepath=argv[0])
