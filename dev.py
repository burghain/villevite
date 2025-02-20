import argparse
import os
import shutil
import subprocess


def build(include_tests=False):
    if include_tests:
        shutil.copytree("tests", "cityGen/tests")
    print("Building addon")
    download_blender("./blender", "4.3.2")
    subprocess.run(
        [
            "./blender/blender-4.3.2/blender",
            "--factory-startup",
            "--command",
            "extension",
            "build",
            "--source-dir",
            "./cityGen",
            "--output-filepath",
            "cityGen.zip",
        ]
    )
    if include_tests:
        shutil.rmtree("cityGen/tests")


def run_tests(blender_executable):
    subprocess.run(
        [
            blender_executable,
            "--command",
            "extension",
            "install-file",
            "-r",
            "user_default",
            "-e",
            "cityGen.zip",
        ]
    )
    test = subprocess.Popen(
        [
            blender_executable,
            "--background",
            "--python-exit-code",
            "1",
            "--python",
            "run_tests.py",
        ]
    )
    test.wait()
    if test.returncode != 0:
        raise Exception("Tests failed")
    print("Tests passed")


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
            f"Blender {version} already downloaded. Continuing with existing installation."
        )


def install_test_deps(blender_path, version):
    major_version = version[:3]
    python_dir = f"{blender_path}/blender-{version}/{major_version}/python/bin/"
    python_executable = f"{python_dir}/{next(name for name in os.listdir(python_dir) if name.startswith('python3.'))}"
    subprocess.run([python_executable, "-m", "pip", "install", "pytest", "-q", "-q"])


def test():

    blender_versions = ["4.3.2"]
    blender_path = "./blender"
    build(include_tests=False)
    for version in blender_versions:
        download_blender(blender_path, version)
        install_test_deps(blender_path, version)
        run_tests(blender_executable=f"{blender_path}/blender-{version}/blender")


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
