import argparse
import os
import shutil
import subprocess
import urllib.request

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


def build():
    print("Building addon")
    shutil.make_archive("cityGen", "zip", "cityGen")


def run_tests(blender_executable):
    # python_dir = f"{blender_path}/blender-{version}/{major_version}/python/bin"
    # python_interpreter = f"{python_dir}/{os.listdir(python_dir)[0]}"
    # subprocess.run([python_interpreter, "-m", "ensurepip"])
    # subprocess.run([python_interpreter, "-m", "pip", "install", "pytest"])
    subprocess.run(
        [blender_executable, "--command", "extension", "install-file", "cityGen.zip"]
    )
    test_process = subprocess.Popen(
        [
            blender_executable,
            "--background",
            "--python",
            "run_tests.py",
        ]
    )
    test_process.wait()


def cleanup():
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, True)
    if os.path.exists("cityGen.zip"):
        os.remove("cityGen.zip")


def download_blender(blender_path, version):
    major_version = version[:3]
    if not os.path.exists(blender_path):
        os.makedirs(blender_path)
    if not os.path.exists(f"{blender_path}/blender-{version}"):
        print(f"Downloading Blender {version}.")

        subprocess.run(
            [
                "wget",
                f"https://download.blender.org/release/Blender{major_version}/blender-{version}-linux-x64.tar.xz",
            ]
        )

        shutil.unpack_archive(f"blender-{version}-linux-x64.tar.xz")
        shutil.move(f"blender-{version}-linux-x64", f"{blender_path}/blender-{version}")
        os.remove(f"blender-{version}-linux-x64.tar.xz")
    else:
        print(
            f"Blender {version} already downloaded. Continuing with existing installation"
        )


def test():

    blender_versions = ["4.3.2"]
    blender_path = "./blender"
    build(include_tests=True)
    for version in blender_versions:
        download_blender(blender_path, version)
        # run_tests(blender_path=f"{blender_path}/blender-{version}/blender")


### COMMAND LINE INTERFACE

parser = argparse.ArgumentParser()
parser.add_argument(
    "command",
    choices=["build", "test", "release"],
    help="""
  TEST = build with test files and run tests
  BUILD = copy relevant files into ./out/cityGen and zip to addon.
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
    build()
elif args.command == "release":
    build()
elif args.command == "test":
    test()
else:
    parser.print_help()
