import argparse
import os
import shutil
import subprocess
import bpy


def install_addon(install_dir):
    extract_files(include_tests=True)
    # shutil.copytree("out", install_dir)


def extract_files(include_tests=False):
    out_dir = os.path.abspath("out/cityGen")
    shutil.rmtree(out_dir, True)

    ignore_files = [
        ".gitignore",
        "dev.py",
        "README.md",
        "cityGen.zip",
    ]
    print("Copying files to ", out_dir)
    shutil.copytree(
        "buildingGen",
        f"{out_dir}/buildingGen",
        ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"),
    )
    if include_tests:
        shutil.copytree(
            "tests",
            f"{out_dir}/tests",
            ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"),
        )
    for item in os.listdir():
        if not os.path.isdir(item) and not item in ignore_files:
            shutil.copy(item, f"{out_dir}/{item}")


def build(out_dir=None):
    extract_files(include_tests=False)

    print("Creating ZIP archive.")
    shutil.make_archive("cityGen", "zip", root_dir="out", base_dir="cityGen")
    print("Build done!")


def install_to(install_dir):
    if not install_dir:
        print("No install directory specified.")
        return

    print(f"Installing to {install_dir}")
    shutil.copytree("out", install_dir)
    print("Done!")


def run_tests(args):
    extract_files()
    install_addon("/home/josua/Documents/bin/blender-4.3 (2).2-linux-x64/blender"


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
    run_tests(args)
else:
    parser.print_help()
