#!/usr/bin/env python
import argparse
import os
import shutil
import subprocess

ADDON_NAME = "villevite"

"""
    Command-line interface for building, testing, or releasing the addon.

    Commands:
        build: Creates the addon zip file.
        test: Builds the addon and runs tests.
        release: Reserved for future implementation.

    Args:
        --fast: Skips using Blender's extension builder and zips the folder directly.
        --skip-rebuild: Skips rebuilding the addon when running tests.
    """


def build(fast=False):
    """
    Builds the addon by either zipping the folder directly or using Blender's extension builder.

    Args:
        fast (bool): If True, zips the folder directly without using Blender's extension builder.
    """
    source_dir = f"./{ADDON_NAME}"
    filename = ADDON_NAME
    if fast:
        print(f"Building addon: Zipping folder {source_dir} to {filename}.zip")
        shutil.make_archive(ADDON_NAME, "zip", ADDON_NAME)
    else:
        version = "4.4.0"
        print(f"Building addon: Using blender version {version} to build")
        setup_blender("./blender", version)
        subprocess.run(
            [
                f"./blender/blender-{version}/blender",
                "--command",
                "extension",
                "build",
                "--source-dir",
                source_dir,
                "--output-filepath",
                f"{filename}.zip",
            ], check=True
        )


def run_tests(blender_executable):
    """
    Runs tests for the addon by installing it in Blender and executing the test script.

    Args:
        blender_executable (str): Path to the Blender executable to use for running tests.
    """
    # Install the addon
    subprocess.run(
        [
            blender_executable,
            "--command",
            "extension",
            "install-file",
            "-r",
            "user_default",
            "-e",
            f"{ADDON_NAME}.zip",
        ], check=True
    )
    subprocess.run(
        [
            blender_executable,
            "--background",
            "--python-exit-code",
            "1",
            "--python",
            "run_tests.py",
        ], check=True
    )


def setup_blender(blender_path, version):
    """
    Sets up Blender by downloading and preparing the specified version.

    Args:
        blender_path (str): Path to the directory where Blender should be set up.
        version (str): Version of Blender to download and set up.
    """
    major_version = version[:3]
    if not os.path.exists(blender_path):
        os.makedirs(blender_path)
    if not os.path.exists(f"{blender_path}/blender-{version}"):
        print(f"Downloading Blender {version}.")

        subprocess.run(
            [
                "wget",
                "-nv",
                f"https://download.blender.org/release/Blender{major_version}/blender-{version}-linux-x64.tar.xz",
            ], check=True
        )

        shutil.unpack_archive(f"blender-{version}-linux-x64.tar.xz")
        shutil.move(f"blender-{version}-linux-x64",
                    f"{blender_path}/blender-{version}")
        os.remove(f"blender-{version}-linux-x64.tar.xz")
        os.mkdir(f"{blender_path}/blender-{version}/portable")
    else:
        print(
            f"Blender {version} already downloaded. Resetting existing installation."
        )
        shutil.rmtree(f"{blender_path}/blender-{version}/portable")
        os.mkdir(f"{blender_path}/blender-{version}/portable")


def install_test_deps(blender_path, version):
    """
    Installs test dependencies (e.g., pytest) in the specified Blender version's Python environment.

    Args:
        blender_path (str): Path to the directory where Blender is set up.
        version (str): Version of Blender whose Python environment will be used.
    """
    major_version = version[:3]
    python_dir = f"{blender_path}/blender-{version}/{major_version}/python/bin/"
    python_executable = f"{python_dir}/{next(name for name in os.listdir(python_dir) if name.startswith('python3.'))}"
    subprocess.run([python_executable, "-m", "pip",
                   "install", "pytest", "-q", "-q"], check=True)


def test():
    """
    Runs tests for the addon across specified Blender versions.
    """
    blender_versions = ["4.4.0"]
    blender_path = "./blender"
    for version in blender_versions:

        setup_blender(blender_path, version)
        install_test_deps(blender_path, version)
        print(f"Running tests for Blender version {version}")
        run_tests(
            blender_executable=f"{blender_path}/blender-{version}/blender")


# COMMAND LINE INTERFACE

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["build", "test", "release"],
        help="""
    test = build with test files and run tests
    build = Create the zip
    """,
    )
    parser.add_argument(
        "--fast",
        action=argparse.BooleanOptionalAction,
        help="Do not use the blender addon builder and instead just zip the folder",
    )
    parser.add_argument(
        "--skip-rebuild",
        action=argparse.BooleanOptionalAction,
        help="Do not rebuild the addon when running the tests, only viable when there are no changes in the addon code",
    )
    args = parser.parse_args()

    if args.command == "build":
        build(args.fast)
    elif args.command == "test":
        if not args.skip_rebuild:
            build(args.fast)
        test()
    else:
        parser.print_help()
