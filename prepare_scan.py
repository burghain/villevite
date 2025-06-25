import subprocess
from dev import build
import json
import os
import shutil

'''
Build and scan city model to a point cloud

Expects a json named 'scan_params.json' with needed configuration.

blender_dir.. path to the blender folder
bpy_executable.. Path to Blender's python executable
vlidar_zip.. path to the zip containing the vlidar addon
pc_save_file.. path to where the point cloud should be saved
osm_coords.. string with the coordinates of the map excerpt to use; format: 'minlon,minlat,maxlon,maxlat'
blender_script.. path of the python file to be executed within blender
'''

def reset_blender(dir, portable_dir):
    if os.path.isdir(portable_dir):
        shutil.rmtree(portable_dir)
        
    os.mkdir(dir + '/portable')

if __name__ == '__main__':
    with open('scan_config.json') as f:
        BYPASS_GEN = False

        d = json.load(f)

        blender_sc_dir = d['blender_scancam_dir']
        blender_sc_portable_dir = blender_sc_dir + '/portable'
        blender_sc_executable = blender_sc_dir + '/blender'

        bpy_sc_executable = d['bpy_scancam_executable']

        if not BYPASS_GEN:
            blender_45_dir = d['blender_45_dir']
            blender_45_portable_dir = blender_45_dir + '/portable'
            blender_45_executable = blender_45_dir + '/blender'
            reset_blender(blender_45_dir, blender_45_portable_dir)

        vlidar_zip = d['vlidar_zip']

        osm_coords = d['osm_coords']

        generate_script = d['generate_script']
        scan_script = d['scan_script']

        reset_blender(blender_sc_dir, blender_sc_portable_dir)

        point_cloud_save_folder = d['pc_save_folder']

        blend_savefile = f'{os.getcwd()}/city.blend'

        if not BYPASS_GEN:
            build()

            # install villevite into blender 4.5
            subprocess.run(
                [
                    blender_45_executable,
                    "--command",
                    "extension",
                    "install-file",
                    "-r",
                    "user_default",
                    "-e",
                    "villevite.zip"
                ]
            )

            # run villevite in blender 45
            subprocess.run(
                [
                    blender_45_executable,
                    '-b',
                    "--python",
                    generate_script,
                    "--",
                    blend_savefile,
                    osm_coords
                ]
            )

        # install vlidar deps into blender sc
        subprocess.run(
            [
                bpy_sc_executable,
                '-m',
                'pip',
                'install',
                'openexr==3.2.4',
                'openexr_numpy==0.0.6',
                'laspy==2.5.4'
            ]
        )

        # scan in blender sc
        subprocess.run(
            [
                blender_sc_executable,
                '-b',
                "--python",
                scan_script,
                "--",
                blend_savefile,
                point_cloud_save_folder,
                vlidar_zip
            ]
        )