import bpy

import math
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] 

if len(argv) < 2:
    exit()

bpy.ops.preferences.addon_install(overwrite=True, target='DEFAULT', filepath=argv[1], filter_folder=True, filter_python=False, filter_glob="*.py;*.zip")
bpy.ops.preferences.addon_enable(module="pointCloudRender")

vLiDAR_preferences = bpy.context.preferences.addons["pointCloudRender"].preferences
vLiDAR_preferences.backend_type = "GPUScanningBackend"
vLiDAR_preferences.GPUScanningBackendSettings.camera_type = "ScannerCamera"


#bpy.ops.wm.open_mainfile(filepath=blend_file_path)
#bpy.ops.preferences.addon_enable(module="villevite")

# deal with villevite stuff
bpy.ops.villevite.clear_all()
bpy.ops.villevite.generate_city()

print("\nPreparing Scanning...")

point_cloud_file_path = argv[0]

bpy.ops.pcscanner.add_scanner()
bpy.ops.pcscanner.assign_unique_material_ids()

laser_scanner = bpy.data.objects.get("LaserScanner")
laser_scanner.rotation_euler[0] = math.radians(60)
laser_scanner.rotation_euler[2] = math.radians(-30)

vLiDAR_scanner = bpy.data.scenes["Scene"].pointCloudRenderProperties.laser_scanners[0]
vLiDAR_scanner.file_path = point_cloud_file_path
vLiDAR_scanner.scanner_type = "mobile_mapping_scanner"

path = bpy.data.objects.get("Scan Path")

if path:
    vLiDAR_scanner.path.path_object = path

    bpy.ops.pcscanner.update_path_length()

velocity = 8.33  # 8.33 m/s corresponds to 30 km/h

vLiDAR_scanner.scan_duration = vLiDAR_scanner.path.length / velocity
vLiDAR_scanner.samples_per_second = 500000
vLiDAR_scanner.mobile_mapping_AV = 72000.0
vLiDAR_scanner.mobile_mapping_velocity = velocity
vLiDAR_scanner.save_material_ids = True

print("\nScanning...")

bpy.ops.render.render_point_cloud()