import bpy
import math
import sys
from pathlib import Path

'''
Takes in a .blend file, opens it and scans all scan paths within the 'Scan Paths' collection

argv[0].. path to .blend
argv[1].. path to folder to save point clouds to
argv[2].. path to vlidar zip
'''

argv = sys.argv
argv = argv[argv.index("--") + 1:] 

if len(argv) < 3:
    exit()

print("installing vlidar from " + argv[2])
# install vlidar plugin
bpy.ops.preferences.addon_install(overwrite=True, target='DEFAULT', filepath=argv[2], filter_folder=True, filter_python=False, filter_glob="*.py;*.zip")
print("enable vlidar")
bpy.ops.preferences.addon_enable(module="pointCloudRender")
print("vlidar installed")
# Enable CUDA GPU
preferences = bpy.context.preferences
cycles_preferences = preferences.addons["cycles"].preferences
cycles_preferences.compute_device_type = "CUDA"
bpy.context.scene.cycles.device = "GPU"
cycles_preferences.refresh_devices()
devices = cycles_preferences.devices

if not devices:
    raise RuntimeError("Unsupported device type")

for device in devices:
    if device.type == "CPU":
        device.use = False
    else:
        device.use = True
        print('Activated GPU', device.name)


# Enable vLidar GPU Acceleration
vLiDAR_preferences = bpy.context.preferences.addons["pointCloudRender"].preferences
vLiDAR_preferences.backend_type = "GPUScanningBackend"
vLiDAR_preferences.writer_type = "LasSampleWriter"
vLiDAR_preferences.GPUScanningBackendSettings.camera_type = "ScannerCamera"

# clear scene
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)
for collection in bpy.data.collections:
    bpy.data.collections.remove(collection, do_unlink=True)

print("add scanner")
# configure vlidar
bpy.ops.pcscanner.add_scanner()

new_collections = ['Instances', 'Assets', 'City Generator', 'Scan Paths']

with bpy.data.libraries.load(argv[0]) as (data_from, data_to):
    data_to.collections = new_collections

for c_name in new_collections:
    bpy.context.scene.collection.children.link(c_name)

print("assign ids")
bpy.ops.pcscanner.assign_unique_material_ids()

laser_scanner = bpy.data.objects.get("LaserScanner")
laser_scanner.rotation_euler[0] = math.radians(60)
laser_scanner.rotation_euler[2] = math.radians(-30)

vLiDAR_scanner = bpy.data.scenes["Scene"].pointCloudRenderProperties.laser_scanners[0]
vLiDAR_scanner.scanner_type = "mobile_mapping_scanner"

velocity = 8.33  # 8.33 m/s corresponds to 30 km/h

vLiDAR_scanner.samples_per_second = 500000
vLiDAR_scanner.mobile_mapping_AV = 72000.0
vLiDAR_scanner.mobile_mapping_velocity = velocity
vLiDAR_scanner.save_material_ids = True

print("Scanning objects...")
Path(argv[1]).mkdir(parents=True, exist_ok=True)

for i, obj in enumerate(bpy.data.collections['Scan Paths'].objects):
    vLiDAR_scanner.file_path = f'{argv[1]}/pc-{i}.las'

    vLiDAR_scanner.path.path_object = obj
    bpy.ops.pcscanner.update_path_length()
    vLiDAR_scanner.scan_duration = vLiDAR_scanner.path.length / velocity

    print(f'\nScanning path {obj.name}...')

    bpy.ops.render.render_point_cloud()

print(f'Scanned {len(bpy.data.collections["Scan Paths"].objects)} paths to {argv[1]}')