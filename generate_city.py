import bpy

import math
import sys

'''
Generates the city and saves it as .blend

argv[0].. File to save to
argv[1].. osm coordinates to generate
'''

argv = sys.argv
argv = argv[argv.index("--") + 1:] 

if len(argv) < 2:
    exit()

# setup villevite
osm_coords = argv[1]
bpy.data.scenes["Scene"].cityproperties.coordinates = osm_coords

# generate city
bpy.ops.villevite.clear_all()
bpy.ops.villevite.generate_city()

# save city
bpy.ops.wm.save_as_mainfile(filepath=argv[0])

exit()