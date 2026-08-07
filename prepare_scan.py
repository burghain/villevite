"""Generate a city and scan it, chaining the two Blender steps.

    python3 prepare_scan.py --output-dir out/

City generation needs a current Blender (villevite is built against 5.2); scanning needs the
Blender the vLiDAR add-on's GPU backend supports, which is a patched 4.5 build (see
`generator/README.md` in the curbstone-detection tree). This script therefore drives two
executables and tries hard to find both without being told:

    --gen-blender    $VILLEVITE_BLENDER,  else ./blender/blender-<version>/blender (downloaded)
    --scan-blender   $VLIDAR_BLENDER,     else ../blender-scancam/blender
    --vlidar         $VLIDAR_ADDON,       else ../pointCloudRender, zipped on the fly
    --classes        $PCNN_CLASSES,       else ../../model/pcnn/data/classes.json

Anything it cannot find is reported by name, with the flag and the environment variable that
would supply it -- there are no paths to edit in this file.
"""

import argparse
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import dev

HERE = Path(__file__).resolve().parent
GEN_BLENDER_VERSION = "5.2.0"

# not part of the add-on at runtime, and test_data is large
ADDON_EXCLUDES = {".git", ".github", "__pycache__", "test", "test_data", ".pytest_cache"}


def first_existing(*candidates):
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate).resolve()
    return None


def require(value, what, flag, variable):
    if value is None:
        raise SystemExit(f"ERROR: could not find {what}. Pass {flag} or set ${variable}.")
    return value


def resolve_gen_blender(explicit):
    """The Blender that generates cities: villevite needs a current one, so fetch it if absent."""
    found = first_existing(explicit, os.environ.get("VILLEVITE_BLENDER"),
                           HERE / "blender" / f"blender-{GEN_BLENDER_VERSION}" / "blender")
    if found:
        return found

    print(f"Generation Blender not found, downloading {GEN_BLENDER_VERSION}")
    dev.setup_blender(str(HERE / "blender"), GEN_BLENDER_VERSION)
    return HERE / "blender" / f"blender-{GEN_BLENDER_VERSION}" / "blender"


def resolve_scan_blender(explicit):
    return require(
        first_existing(explicit, os.environ.get("VLIDAR_BLENDER"),
                       HERE.parent / "blender-scancam" / "blender"),
        "the patched Blender that runs the vLiDAR GPU backend",
        "--scan-blender", "VLIDAR_BLENDER")


def resolve_classes(explicit):
    return require(
        first_existing(explicit, os.environ.get("PCNN_CLASSES"),
                       HERE.parent.parent / "model" / "pcnn" / "data" / "classes.json"),
        "the class definition to label against", "--classes", "PCNN_CLASSES")


def package_addon(source, destination):
    """Zip the vLiDAR add-on so Blender can install it, keeping the module name as the root."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if any(part in ADDON_EXCLUDES for part in path.relative_to(source).parts):
                continue
            if path.is_file():
                archive.write(path, Path("pointCloudRender") / path.relative_to(source))
    return destination


def resolve_vlidar(explicit, build_dir):
    found = first_existing(explicit, os.environ.get("VLIDAR_ADDON"),
                           HERE.parent / "pointCloudRender")
    require(found, "the vLiDAR add-on", "--vlidar", "VLIDAR_ADDON")

    if found.is_dir():
        print(f"Packaging vLiDAR add-on from {found}")
        return package_addon(found, build_dir / "pointCloudRender.zip")
    return found


def blender_python(blender):
    """The interpreter bundled with a Blender install, used to add the scanner's deps."""
    for python in sorted(blender.parent.glob("*/python/bin/python3*")):
        return python
    raise SystemExit(f"ERROR: no bundled python found next to {blender}")


def run(command, what):
    print(f"\n=== {what} ===\n$ {' '.join(str(part) for part in command)}", flush=True)
    result = subprocess.run(command)
    if result.returncode != 0:
        raise SystemExit(f"ERROR: {what} failed with exit code {result.returncode}")


def parse_args():
    parser = argparse.ArgumentParser(prog="prepare_scan.py", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="where the city .blend and its point clouds are written")
    parser.add_argument("--name", default="city", help="basename of the generated city")

    parser.add_argument("--gen-blender", type=Path, default=None)
    parser.add_argument("--scan-blender", type=Path, default=None)
    parser.add_argument("--vlidar", type=Path, default=None)
    parser.add_argument("--classes", type=Path, default=None)

    parser.add_argument("--graph", type=Path, default=None,
                        help=".blend with a user-prepared road graph")
    parser.add_argument("--graph-object", default="Road Graph")
    parser.add_argument("--city-preset", type=Path, default=HERE / "presets" / "city_default.json")
    parser.add_argument("--scanner-preset", type=Path,
                        default=HERE / "presets" / "scanner_mobile_mapping.json")
    parser.add_argument("--class-map", type=Path, default=HERE / "presets" / "class_map.json")
    parser.add_argument("--set", dest="overrides", action="append", default=[],
                        metavar="NAME=VALUE", help="override a city preset parameter")

    parser.add_argument("--skip-generate", action="store_true",
                        help="scan an existing city .blend in --output-dir")
    parser.add_argument("--skip-deps", action="store_true",
                        help="do not install laspy/openexr into the scanning Blender")
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = args.output_dir.resolve()
    build_dir = HERE / "build"
    city = output_dir / f"{args.name}.blend"

    scan_blender = resolve_scan_blender(args.scan_blender)
    classes = resolve_classes(args.classes)
    vlidar = resolve_vlidar(args.vlidar, build_dir)

    if not args.skip_generate:
        gen_blender = resolve_gen_blender(args.gen_blender)

        dev.build()
        run([gen_blender, "--command", "extension", "install-file",
             "-r", "user_default", "-e", "villevite.zip"],
            "installing villevite")

        command = [gen_blender, "-b", "--python", HERE / "generate_city.py", "--",
                   "--output", city, "--preset", args.city_preset]
        if args.graph:
            command += ["--graph", args.graph, "--graph-object", args.graph_object]
        for override in args.overrides:
            command += ["--set", override]
        run(command, "generating the city")

    if not city.exists():
        raise SystemExit(f"ERROR: {city} does not exist, drop --skip-generate to build it")

    if not args.skip_deps:
        run([blender_python(scan_blender), "-m", "pip", "install",
             "openexr==3.2.4", "openexr_numpy==0.0.6", "laspy==2.5.4"],
            "installing scanner dependencies")

    run([scan_blender, "-b", "--python", HERE / "scan_city.py", "--",
         "--city", city, "--output", output_dir, "--vlidar", vlidar,
         "--classes", classes, "--class-map", args.class_map,
         "--scanner", args.scanner_preset],
        "scanning the city")

    print(f"\nDone. City and point clouds are in {output_dir}")


if __name__ == "__main__":
    sys.exit(main())
