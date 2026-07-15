import subprocess
from dev import build
import json
import os
import shutil

"""
Build and scan city model to a point cloud

Expects a json named 'scan_config.json' with needed configuration.

blender_scancam_dir.. path to the scanning Blender folder
bpy_scancam_executable.. Path to the scanning Blender's python executable
blender_gen_dir.. path to the Blender folder used for city generation
vlidar_zip.. path to the zip containing the vlidar addon
pc_save_folder.. path to where the point clouds should be saved
road_graph_blend.. optional path to a .blend with a user-prepared road graph
                   (empty = generate from the bundled Default Road Graph)
road_graph_object.. optional name of the road graph object in that file
generate_script.. path of the generation python file to be executed within blender
scan_script.. path of the scanning python file to be executed within blender

The environment variables ROAD_GRAPH_BLEND and ROAD_GRAPH_OBJECT override the
corresponding config values.
"""


def reset_blender(dir, portable_dir):
    if os.path.isdir(portable_dir):
        shutil.rmtree(portable_dir)

    os.mkdir(dir + "/portable")


if __name__ == "__main__":
    with open("scan_config.json") as f:
        BYPASS_GEN = False

        d = json.load(f)

        blender_sc_dir = d["blender_scancam_dir"]
        blender_sc_portable_dir = blender_sc_dir + "/portable"
        blender_sc_executable = blender_sc_dir + "/blender"

        bpy_sc_executable = d["bpy_scancam_executable"]

        if not BYPASS_GEN:
            blender_gen_dir = d["blender_gen_dir"]
            blender_gen_portable_dir = blender_gen_dir + "/portable"
            blender_gen_executable = blender_gen_dir + "/blender"
            reset_blender(blender_gen_dir, blender_gen_portable_dir)

        vlidar_zip = d["vlidar_zip"]

        road_graph_blend = os.environ.get("ROAD_GRAPH_BLEND") or d.get("road_graph_blend") or None
        road_graph_object = os.environ.get("ROAD_GRAPH_OBJECT") or d.get("road_graph_object") or None

        generate_script = d["generate_script"]
        scan_script = d["scan_script"]

        reset_blender(blender_sc_dir, blender_sc_portable_dir)

        point_cloud_save_folder = d["pc_save_folder"]

        blend_savefile = f"{os.getcwd()}/city.blend"

        graph_source = road_graph_blend if road_graph_blend else "Default Road Graph"
        print(f"Generate city model from {graph_source}")

        if not BYPASS_GEN:
            # install villevite into the generation blender
            subprocess.run(
                [
                    blender_gen_executable,
                    "--command",
                    "extension",
                    "install-file",
                    "-r",
                    "user_default",
                    "-e",
                    "villevite.zip",
                ]
            )

            # run villevite in the generation blender
            generate_cmd = [
                blender_gen_executable,
                "-b",
                "--python",
                generate_script,
                "--",
                blend_savefile,
            ]
            if road_graph_blend:
                generate_cmd.append(road_graph_blend)
                if road_graph_object:
                    generate_cmd.append(road_graph_object)
            subprocess.run(generate_cmd)

        # install vlidar deps into blender sc
        subprocess.run(
            [
                bpy_sc_executable,
                "-m",
                "pip",
                "install",
                "openexr==3.2.4",
                "openexr_numpy==0.0.6",
                "laspy==2.5.4",
            ]
        )

        # scan in blender sc
        subprocess.run(
            [
                blender_sc_executable,
                "-b",
                "--python",
                scan_script,
                "--",
                blend_savefile,
                point_cloud_save_folder,
                vlidar_zip,
            ]
        )
