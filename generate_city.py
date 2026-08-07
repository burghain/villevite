"""Generate a city from a road graph and save it as a .blend, ready to be scanned.

Runs inside Blender with the villevite extension installed:

    blender -b --python generate_city.py -- --output city.blend [options]

Without --graph the city is built from the bundled Default Road Graph. All generation
parameters come from a preset (see presets/city_default.json) and can be overridden
individually with --set, which is what varies a single axis across an experiment:

    blender -b --python generate_city.py -- --output city.blend --set Seed=7

Alongside the .blend a <output>.json is written recording the preset actually used, the
resolved parameters, the road graph and the villevite/Blender versions, so that any city can
be regenerated from its own sidecar.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
DEFAULT_PRESET = HERE / "presets" / "city_default.json"


def parse_args(argv):
    argv = argv[argv.index("--") + 1:] if "--" in argv else []

    parser = argparse.ArgumentParser(prog="generate_city.py", description=__doc__)
    parser.add_argument("--output", required=True, type=Path,
                        help="path of the .blend to write")
    parser.add_argument("--graph", type=Path, default=None,
                        help=".blend holding a user-prepared road graph "
                             "(default: the bundled Default Road Graph)")
    parser.add_argument("--graph-object", default="Road Graph",
                        help="name of the road graph object inside --graph; falls back to that "
                             "file's active object")
    parser.add_argument("--preset", type=Path, default=DEFAULT_PRESET,
                        help=f"GeoCity parameter preset (default: {DEFAULT_PRESET.name})")
    parser.add_argument("--set", dest="overrides", action="append", default=[],
                        metavar="NAME=VALUE",
                        help="override a single preset parameter, repeatable")
    return parser.parse_args(argv)


def load_preset(path, overrides):
    """Read the preset and apply NAME=VALUE overrides, keeping each value's JSON type."""
    parameters = {name: value for name, value in json.loads(path.read_text()).items()
                  if not name.startswith("_")}

    for override in overrides:
        name, _, raw = override.partition("=")
        if not _:
            raise SystemExit(f"ERROR: --set expects NAME=VALUE, got {override!r}")
        try:
            parameters[name] = json.loads(raw)
        except json.JSONDecodeError:
            parameters[name] = raw
    return parameters


def resolve_road_graph(args):
    """Return the road graph object to build from, loading --graph if one was given.

    The graph is made active and selected either way, so that the generate operator picks up
    exactly this object rather than searching for one itself.
    """
    from bl_ext.user_default.villevite import road_graph

    if args.graph is None:
        bpy.ops.villevite.clear_all()
        graph = road_graph.ensure_default_road_graph(bpy.context)
    else:
        bpy.ops.wm.open_mainfile(filepath=str(args.graph))
        graph = bpy.data.objects.get(args.graph_object)
        if not road_graph.is_valid_road_graph(graph):
            graph = bpy.context.view_layer.objects.active
        if not road_graph.is_valid_road_graph(graph):
            raise SystemExit(f"ERROR: no valid road graph '{args.graph_object}' in {args.graph}")

    for other in bpy.context.selected_objects:
        other.select_set(False)
    bpy.context.view_layer.objects.active = graph
    graph.select_set(True)
    return graph


def geocity_modifier(graph):
    """The graph's GeoCity modifier, attached first if it does not carry one yet."""
    from bl_ext.user_default.villevite import assets, nodes

    for modifier in graph.modifiers:
        if (modifier.type == 'NODES' and modifier.node_group is not None
                and modifier.node_group.name == "GeoCity"):
            return modifier

    assets.import_assets_and_nodes()
    nodes.add_to_object(graph, "GeoCity", {})
    return graph.modifiers[-1]


def apply_parameters(modifier, parameters):
    """Push the preset onto the GeoCity modifier and report what was actually applied."""
    from bl_ext.user_default.villevite import nodes

    applied = nodes.set_inputs(modifier, parameters)
    return {name: parameters[name] for name in applied}


def blender_version():
    return ".".join(str(part) for part in bpy.app.version)


def villevite_commit():
    """The villevite revision this ran from, so a city can be traced back to its generator."""
    try:
        result = subprocess.run(["git", "-C", str(HERE), "rev-parse", "HEAD"],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main():
    args = parse_args(sys.argv)
    parameters = load_preset(args.preset, args.overrides)

    graph = resolve_road_graph(args)

    # the bake runs on a copy of the graph and inherits its modifier, so the preset has to be
    # on the modifier before generating
    applied = apply_parameters(geocity_modifier(graph), parameters)
    bpy.ops.villevite.generate_city(for_scanning=True)

    # the baked objects are the city now; leaving a live generator on the graph would put a
    # second, procedurally evaluated copy of the whole city into every render
    for modifier in list(graph.modifiers):
        graph.modifiers.remove(modifier)

    scan_paths = bpy.data.collections.get("Scan Paths")
    path_count = len(scan_paths.objects) if scan_paths else 0
    if not path_count:
        raise SystemExit("ERROR: the generated city has no scan paths, there would be "
                         "nothing to scan")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output))

    sidecar = args.output.with_suffix(".json")
    sidecar.write_text(json.dumps({
        "city": args.output.name,
        "road_graph": str(args.graph) if args.graph else "Default Road Graph",
        "road_graph_object": args.graph_object if args.graph else None,
        "preset": str(args.preset),
        "parameters": applied,
        "scan_paths": path_count,
        "villevite_commit": villevite_commit(),
        "blender_version": blender_version(),
    }, indent=2) + "\n")

    print(f"Generated {args.output} with {path_count} scan paths (sidecar: {sidecar.name})")


if __name__ == "__main__":
    main()
