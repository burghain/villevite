"""Scan a generated city with the vLiDAR add-on, one point cloud per scan path.

Runs inside a Blender that has the vLiDAR (pointCloudRender) add-on available:

    blender -b --python scan_city.py -- --city city.blend --output clouds/ \\
        --vlidar pointCloudRender.zip --classes classes.json

Labels come from a class definition file (--classes) in the format the vLiDAR add-on imports:
a `base_class_map` of id -> name plus a `hierarchy` of base id -> {subclass id -> name}. Points
are labelled by name, not by index:

  * a material whose name is a class path ("Ground:Curbstone") classifies every point sampled
    from it. This is the finest granularity the generator offers -- one object made of several
    materials still yields several classes.
  * objects are classified from the rules in --class-map, which covers geometry whose materials
    come from the asset library and carry no class of their own (trees, vehicles, ...).
  * where both apply, the material wins.

Names are matched after stripping Blender's ".001" duplicate suffix and a trailing
parenthesised discriminator, so "Ground:Curbstone", "Ground:Curbstone.003" and
"HighVegetation:Tree (Leaves)" all resolve to their class.
"""

import argparse
import fnmatch
import json
import math
import re
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
DEFAULT_CLASS_MAP = HERE / "presets" / "class_map.json"
DEFAULT_SCANNER = HERE / "presets" / "scanner_mobile_mapping.json"

SCAN_PATH_COLLECTION = "Scan Paths"
DUPLICATE_SUFFIX = re.compile(r"\.\d{3}$")
DISCRIMINATOR = re.compile(r"\s*\([^()]*\)$")


# --------------------------------------------------------------------------------------------
# class space
# --------------------------------------------------------------------------------------------

class ClassSpace:
    """The label space, indexed by class path ("Ground:Curbstone")."""

    def __init__(self, path):
        definition = json.loads(Path(path).read_text())
        base_names = definition["base_class_map"]
        self.by_path = {}

        for class_id, name in base_names.items():
            self.by_path[name] = (int(class_id), 0, name)
        for class_id, subclasses in definition.get("hierarchy", {}).items():
            for subclass_id, name in subclasses.items():
                path_name = f"{base_names[class_id]}:{name}"
                self.by_path[path_name] = (int(class_id), int(subclass_id), name)

    @staticmethod
    def canonical(name):
        """Strip Blender's duplicate suffix and a trailing '(discriminator)'."""
        name = DUPLICATE_SUFFIX.sub("", name)
        return DISCRIMINATOR.sub("", name).strip()

    def resolve(self, class_path):
        """The (class id, subclass id, add-on class name) for a class path, or None."""
        return self.by_path.get(class_path)

    def resolve_name(self, name):
        """Same, but for a datablock name that is expected to *be* a class path."""
        return self.by_path.get(self.canonical(name))


def import_classes(classes_path):
    """Load the class definition into the scene using the add-on's own importer."""
    bpy.ops.pcscanner.import_classes(filepath=str(classes_path))
    count = len(bpy.context.scene.pointCloudRenderProperties.classes)
    print(f"Imported {count} classes from {classes_path}")
    return count


def assign(target, class_space, class_path, kind):
    """Assign a class to an object or material; returns True when it took."""
    resolved = class_space.resolve(class_path)
    if resolved is None:
        print(f"WARNING: {kind} {target.name!r} maps to unknown class {class_path!r}, skipping")
        return False

    _, _, class_name = resolved
    # assigning the name is what the add-on's UI does; its update callback copies the ids over
    target.class_name = class_name
    if not target.class_uid:
        print(f"WARNING: class {class_name!r} did not stick on {kind} {target.name!r}")
        return False
    return True


def classify_materials(class_space, extra_rules):
    """Classify materials named after their class, plus any listed in the class map."""
    overrides = dict(extra_rules)
    classified, unclassified = 0, []

    for material in bpy.data.materials:
        class_path = overrides.get(ClassSpace.canonical(material.name))
        if class_path is None:
            resolved = class_space.resolve_name(material.name)
            class_path = ClassSpace.canonical(material.name) if resolved else None

        if class_path is None:
            unclassified.append(material.name)
            continue
        classified += assign(material, class_space, class_path, "material")

    print(f"Classified {classified}/{len(bpy.data.materials)} materials")
    if unclassified:
        print(f"  materials left to their object's class: {sorted(unclassified)}")
    return classified


def assign_material_ids():
    """Give every material a distinct MaterialID and return the name -> id mapping.

    The class tells you *what* a point is; the material id tells you which material it came
    from within that class. That is what keeps distinctions the label space folds away
    recoverable -- a gutter and a road surface are both `Street`, a lowered curb and an
    ordinary one are both `Ground:Curbstone` -- so the special-analysis slices can be cut
    without giving them classes of their own. Meaningless unless the mapping is recorded, so
    it goes into the scan's sidecar.
    """
    bpy.ops.pcscanner.assign_unique_material_ids()
    return {material.name: material.vLiDAR_material_id for material in bpy.data.materials}


def classify_objects(class_space, rules):
    """Classify objects by fnmatch rules, first match wins."""
    classified, unmatched = 0, []

    for obj in bpy.data.objects:
        name = ClassSpace.canonical(obj.name)
        for pattern, class_path in rules:
            if fnmatch.fnmatchcase(name, pattern):
                classified += assign(obj, class_space, class_path, "object")
                break
        else:
            if obj.type == 'MESH':
                unmatched.append(name)

    print(f"Classified {classified}/{len(bpy.data.objects)} objects")
    if unmatched:
        print(f"  unmatched mesh objects: {sorted(set(unmatched))}")
    return classified


# --------------------------------------------------------------------------------------------
# scanner setup
# --------------------------------------------------------------------------------------------

def enable_addon(vlidar_path):
    """Install (if a zip was given) and enable the vLiDAR add-on."""
    if vlidar_path is not None:
        print(f"Installing vLiDAR add-on from {vlidar_path}")
        bpy.ops.preferences.addon_install(overwrite=True, target='DEFAULT',
                                          filepath=str(vlidar_path), filter_folder=True,
                                          filter_python=False, filter_glob="*.py;*.zip")
    bpy.ops.preferences.addon_enable(module="pointCloudRender")


def enable_compute_devices(device_type):
    """Point Cycles at the GPU. Falls back to CPU rather than failing the scan."""
    if not device_type or device_type.upper() == "NONE":
        bpy.context.scene.cycles.device = "CPU"
        return "CPU"

    cycles_preferences = bpy.context.preferences.addons["cycles"].preferences
    try:
        cycles_preferences.compute_device_type = device_type
    except TypeError:
        print(f"WARNING: compute device type {device_type!r} unavailable, scanning on the CPU")
        bpy.context.scene.cycles.device = "CPU"
        return "CPU"

    cycles_preferences.refresh_devices()
    devices = [device for device in cycles_preferences.devices if device.type != "CPU"]
    if not devices:
        print(f"WARNING: no {device_type} device found, scanning on the CPU")
        bpy.context.scene.cycles.device = "CPU"
        return "CPU"

    for device in cycles_preferences.devices:
        device.use = device.type != "CPU"
        if device.use:
            print(f"Activated {device.type} device {device.name}")
    bpy.context.scene.cycles.device = "GPU"
    return device_type


def configure_backend(settings):
    """Set the add-on preferences: which backend samples, and which writer stores."""
    preferences = bpy.context.preferences.addons["pointCloudRender"].preferences
    preferences.scanning_backend_type = settings["backend"]
    preferences.writer_type = settings["writer"]

    if settings["backend"] == "GPUScanningBackend":
        preferences.GPUScanningBackendSettings.camera_type = settings["camera_type"]
        return enable_compute_devices(settings.get("compute_device"))
    return "CPU"


def add_scanner(settings):
    """Create the scanner and apply the preset. Returns (scanner, velocity in m/s)."""
    bpy.ops.pcscanner.add_scanner()
    scanner = bpy.context.scene.pointCloudRenderProperties.laser_scanners[0]

    scanner.scanner_type = settings["scanner_type"]
    scanner.samples_per_second = settings["samples_per_second"]

    velocity = settings["velocity_kmh"] / 3.6
    scanner.velocity = velocity
    if settings["scanner_type"] == "mobile_mapping_scanner":
        scanner.mobile_mapping_velocity = velocity
        scanner.mobile_mapping_AV = settings["angular_velocity_deg_per_s"]

    scanner.camera.rotation_euler = [math.radians(angle) for angle in settings["rotation_deg"]]

    outputs = settings["outputs"]
    scanner.save_normals = outputs["normals"]
    scanner.save_class_ids = outputs["class_ids"]
    scanner.save_object_ids = outputs["object_ids"]
    scanner.save_material_ids = outputs["material_ids"]
    scanner.save_rgb = outputs["rgb"]

    noise = settings["noise"]
    scanner.noise_generator.enabled = noise["enabled"]
    scanner.noise_generator.measurement_noise_mean = noise["measurement_mean"]
    scanner.noise_generator.measurement_noise_standard_deviation = \
        noise["measurement_standard_deviation"]
    scanner.noise_generator.position_noise_standard_deviation = \
        noise["position_standard_deviation"]
    scanner.noise_generator.view_noise_standard_deviation = noise["view_standard_deviation"]

    divergence = settings["beam_divergence"]
    scanner.beam_divergence.enabled = divergence["enabled"]
    scanner.beam_divergence.divergence = divergence["divergence"]
    scanner.beam_divergence.accuracy = divergence["accuracy"]
    scanner.beam_divergence.max_echoes = divergence["max_echoes"]

    return scanner, velocity


def scan_paths(scanner, velocity, output_dir, stem, suffix, limit=None):
    """Scan every path in the Scan Paths collection; returns the files written."""
    collection = bpy.data.collections.get(SCAN_PATH_COLLECTION)
    if collection is None or not collection.objects:
        raise SystemExit(f"ERROR: the city has no '{SCAN_PATH_COLLECTION}' collection to scan")

    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    paths = sorted(collection.objects, key=lambda o: o.name)[:limit]

    for index, path_object in enumerate(paths):
        cloud = output_dir / f"{stem}_path{index:03d}{suffix}"
        scanner.file_path = str(cloud)

        scanner.path.path_object = path_object
        bpy.ops.pcscanner.update_path_length()
        scanner.scan_duration = scanner.path.length / velocity

        print(f"Scanning {path_object.name} "
              f"({scanner.path.length:.1f} m, {scanner.scan_duration:.1f} s) -> {cloud.name}")
        bpy.ops.render.render_point_cloud()
        written.append(cloud)

    return written


# --------------------------------------------------------------------------------------------

def parse_args(argv):
    argv = argv[argv.index("--") + 1:] if "--" in argv else []

    parser = argparse.ArgumentParser(prog="scan_city.py", description=__doc__)
    parser.add_argument("--city", required=True, type=Path, help="the .blend to scan")
    parser.add_argument("--output", required=True, type=Path,
                        help="directory to write the point clouds to")
    parser.add_argument("--classes", required=True, type=Path,
                        help="class definition (base_class_map + hierarchy) to label against")
    parser.add_argument("--vlidar", type=Path, default=None,
                        help="vLiDAR add-on zip to install; omit if it is already installed")
    parser.add_argument("--class-map", type=Path, default=DEFAULT_CLASS_MAP,
                        help=f"villevite name -> class path rules (default: {DEFAULT_CLASS_MAP.name})")
    parser.add_argument("--scanner", type=Path, default=DEFAULT_SCANNER,
                        help=f"scanner preset (default: {DEFAULT_SCANNER.name})")
    parser.add_argument("--limit-paths", type=int, default=None,
                        help="scan only the first N paths, for smoke tests")
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv)

    settings = {key: value for key, value in json.loads(args.scanner.read_text()).items()
                if not key.startswith("_")}
    class_map = json.loads(args.class_map.read_text())
    class_space = ClassSpace(args.classes)

    enable_addon(args.vlidar)

    # opening the city rather than linking its collections into a fresh scene keeps the view
    # layer intact -- villevite excludes the collections its instances point at, and scanning
    # them as well would put a second copy of every asset into the cloud
    bpy.ops.wm.open_mainfile(filepath=str(args.city))

    import_classes(args.classes)
    classify_materials(class_space, class_map.get("materials", []))
    classify_objects(class_space, class_map.get("objects", []))
    material_ids = assign_material_ids()

    device = configure_backend(settings)
    scanner, velocity = add_scanner(settings)

    suffix = ".las" if settings["writer"] == "LASSampleWriter" else ".csv"
    clouds = scan_paths(scanner, velocity, args.output, args.city.stem, suffix, args.limit_paths)

    sidecar = args.output / f"{args.city.stem}_scan.json"
    sidecar.write_text(json.dumps({
        "city": str(args.city),
        "clouds": [cloud.name for cloud in clouds],
        "classes": str(args.classes),
        "class_map": str(args.class_map),
        "scanner_preset": str(args.scanner),
        "scanner": settings,
        "material_ids": material_ids,
        "compute_device": device,
        "blender_version": ".".join(str(part) for part in bpy.app.version),
    }, indent=2) + "\n")

    print(f"Scanned {len(clouds)} paths to {args.output} (sidecar: {sidecar.name})")


if __name__ == "__main__":
    main()
