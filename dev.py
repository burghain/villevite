import argparse
import os
import shutil
import subprocess

out_dir = os.path.abspath("out/cityGen")


def extract_files(include_tests=False):
    addon_files = ["__init__.py", "blender_manifest.toml"]
    print("Copying files to ", out_dir)
    shutil.copytree(
        "core", f"{out_dir}/core", ignore=shutil.ignore_patterns("__pycache__")
    )
    if include_tests:
        shutil.copytree(
            "tests", f"{out_dir}/tests", ignore=shutil.ignore_patterns("__pycache__")
        )
    for item in addon_files:
        shutil.copy(item, f"{out_dir}/{item}")


def build(out_dir=None, include_tests=False):
    cleanup()
    extract_files(include_tests=include_tests)

    print("Creating ZIP archive.")
    shutil.make_archive("cityGen", "zip", root_dir="out", base_dir="cityGen")
    print("Build done!")


def run_tests(blender_path):
    blender_executable = f"{blender_path}/blender"
    test_process = subprocess.Popen(
        [
            blender_executable,
            "--factory-startup",
            "--background",
            "--python",
            "run_tests.py",
        ]
    )
    test_process.wait()


def cleanup():
    shutil.rmtree(out_dir, True)
    os.remove("cityGen.zip")


### COMMAND LINE INTERFACE

parser = argparse.ArgumentParser()
parser.add_argument(
    "command",
    choices=["build", "test", "release"],
    help="""
  TEST = build with test files and run tests
  BUILD = copy relevant files into ./out/blenderkit and zip to addon.
  RELEASE = build the add-on .zip with already built client binaries.
  """,
)
parser.add_argument(
    "--directory",
    type=str,
    default=None,
    help="If a path is specified, then addon will be copied to that location.",
)
args = parser.parse_args()

if args.command == "build":
    build(args.directory)
elif args.command == "release":
    build(args.install_at)
elif args.command == "test":
    build(include_tests=True)
    run_tests(blender_path="/home/josua/Documents/bin/blender-4.3.2-linux-x64")
else:
    parser.print_help()
