#!/usr/bin/env python
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

import argparse
import os
import shutil
import subprocess

ADDON_NAME = "villevite"


def build() -> None:
    """
    Builds the addon by either zipping the folder directly or using Blender's extension builder.
    """
    source_dir = f"./{ADDON_NAME}"
    filename = ADDON_NAME

    version = "4.5.0"
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


def run_tests(blender_executable: str) -> None:
    """
    Runs tests for the addon by installing it in Blender and executing the test script.

    Args:
        blender_executable (str): Path to the Blender executable.
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
            "./tests/run_tests.py",
        ], check=True
    )


def setup_blender(blender_path: str, version: str) -> None:
    """
    Sets up Blender by downloading and preparing the specified version.

    Args:
        blender_path (str): Path to the directory where Blender is set up.
        version (str): Version of Blender to set up.
    """
    major_version = version[:3]
    if not os.path.exists(blender_path):
        os.makedirs(blender_path)
    if not os.path.exists(f"{blender_path}/blender-{version}"):
        url = f"https://download.blender.org/release/Blender{major_version}/blender-{version}-linux-x64.tar.xz"

        print(f"Downloading Blender {version} from {url}.")

        subprocess.run(
            [
                "wget",
                "-nv",
                url,
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


def install_test_deps(blender_path: str, version: str) -> None:
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


def test() -> None:
    """
    Runs tests for the addon across specified Blender versions.
    """
    blender_versions = ["4.5.0"]
    blender_path = "./blender"
    for version in blender_versions:

        setup_blender(blender_path, version)
        install_test_deps(blender_path, version)
        print(f"Running tests for Blender version {version}")
        run_tests(
            blender_executable=f"{blender_path}/blender-{version}/blender")


def update_mock_module() -> None:
    """
    Copies the addon contents to the mock module directory for linting purposes.
    """
    source_dir = f"./{ADDON_NAME}"
    destination_dir = f"./bl_ext/user_default/{ADDON_NAME}"
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
    with open("bl_ext/__init__.py", "w") as f:
        pass
    with open("bl_ext/user_default/__init__.py", "w") as f:
        pass
    print(f"Copied {source_dir} to {destination_dir} for linting.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="CLI to manage the development environment")
    subparsers = parser.add_subparsers(dest="command", required=True)
    test_parser = subparsers.add_parser(
        "test", help="Build the addon run all tests using pytest")
    test_parser.add_argument(
        "--skip-rebuild",
        action=argparse.BooleanOptionalAction,
        help="Do not rebuild the addon when running the tests, only viable when there are no changes in the addon code",
    )
    build_parser = subparsers.add_parser(
        "build", help="Build the addon zip file")
    setup_parser = subparsers.add_parser(
        "setup", help="Update the mock module for linting")
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.command == "test":
        if not args.skip_rebuild:
            build()
        test()
    elif args.command == "setup":
        update_mock_module()
    else:
        parser.print_help()
