import subprocess
from dev import build
import json
import os
import shutil

'''
Build and scan city model to a point cloud

Expects a json named 'scan_params.json' with needed configuration.

blender_dir.. path to the blender folder
vlidar_zip.. path to the zip containing the vlidar addon
pc_save_file.. path to where the point cloud should be saved
osm_coords.. string with the coordinates of the map excerpt to use; format: 'minlon,minlat,maxlon,maxlat'
blender_script.. path of the python file to be executed within blender
'''

if __name__ == '__main__':
    with open('scan_config.json') as f:
        d = json.load(f)

        blender_dir = d['blender_dir']
        blender_portable_dir = blender_dir + '/portable'

        vlidar_zip = d['vlidar_zip']

        osm_coords = d['osm_coords']

        blender_script = d['blender_script']

        # delete portable dir if exists to reset blender installation
        if os.path.isdir(blender_portable_dir):
            shutil.rmtree(blender_portable_dir)

        os.mkdir(blender_dir + '/portable')

        blender_executable = blender_dir + '/blender'
        point_cloud_save_file = d['pc_save_file']

        build()

        subprocess.run(
            [
                blender_executable,
                "--command",
                "extension",
                "install-file",
                "-r",
                "user_default",
                "-e",
                "villevite.zip"
            ]
        )

        subprocess.run(
            [
                blender_executable,
                "--python",
                blender_script,
                "--",
                point_cloud_save_file,
                vlidar_zip,
                osm_coords
            ]
        )
