# Villevite City Generator

Villevite is a Blender add-on designed to procedurally generate cities for training data synthesis, including buildings, streets with variable width and intelligent crossroad calculation and vegetation. It provides tools for creating realistic urban environments and customization through assets and parameters.

## Features

- Procedural generation of cities with buildings, streets, and trees.
- Asset-based architecture for modular and reusable components.
- Integration with Blender's 3D Viewport for real-time visualization.
- Support for generating and managing city elements through a custom UI panel.

## Development Setup

### Prerequisites

- **Blender**: The add-on requires Blender 5.2.0 (bundled Python 3.13).
- **Python**: Python 3.13 is recommended for development.

### Setting Up the Development Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/burghain/villevite.git
   cd villevite
   ```

2. Initialze the Assets submodule:

   ```bash
   git submodule init
   git submodule update
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r development_requirements.txt
   ```

4. Set up Blender to recognize the Villevite Assets:
   - Open Blender.
   - Go to `Edit > Preferences > File Paths > Asset Catalogs`.
   - Add the absolute path to the `./villevite/Assets` directory as an Asset Catalog.
   - Change the import policy to "Link".

### Running Tests

Villevite includes a test suite to ensure the functionality of its components. To run the tests:

  ```bash
  python ./dev.py test
  ```

## Usage

The city is generated from a **road graph**: a plain wire mesh (vertices and edges, no
faces) that you build manually. All road attributes (lanes, sidewalks, bike lanes, …) and
building floor plans are generated automatically by the GeoCity geometry node group.

1. Open Blender and navigate to the 3D Viewport.
2. Access the Villevite panel from the side toolbar under the "villevite" tab.
3. Use the provided operators:
   - **Load Default Road Graph**: Appends the starter road graph from the bundled
     Nodes.blend. Edit it in Edit Mode (or build your own wire mesh from scratch).
     Note: linked graphs (e.g. "Example Road Graph" from Templates.blend) must be made
     local before they can be used.
   - **Generate City**: Attaches the GeoCity modifier to the active (or first valid
     selected) road graph object — if none is selected, the Default Road Graph is loaded
     automatically. All generation parameters (seed, probabilities, densities, …) are
     edited directly on the modifier.
   - **Prepare for Scanning**: Bakes the city to real objects and extracts the scan paths
     (runs on a copy, so your road graph is preserved).
   - **Clear All**: Resets the scene.

### Headless generation

With the extension installed into Blender:

```bash
blender -b --python generate_city.py -- <output.blend> [<graph.blend> [<object_name>]]
```

Without a graph file, the city is generated from the bundled Default Road Graph. With a
graph file, the object named `<object_name>` (default: "Road Graph") is used, falling back
to the file's active object. `prepare_scan.py` reads the same options from
`scan_config.json` (`road_graph_blend`, `road_graph_object`) or the environment variables
`ROAD_GRAPH_BLEND` / `ROAD_GRAPH_OBJECT`, e.g. for Docker:

```bash
docker run -e ROAD_GRAPH_BLEND=/data/graph.blend -v <host_graphs>:/data ...
```

Note: the Docker base image still provides the Blender 4.4 scanning toolchain (vLiDAR);
only city generation runs on Blender 5.2.0.

## Architecture

### Assets

- Assets are sorted into different `.blend` files.
- Each collection that needs to be used individually (e.g., Building Walls) is stored as a separate asset.

### City Generator

- The city generator uses procedural algorithms to create realistic urban layouts.

### General Add-on Structure

- The add-on follows the structure outlined in the BlenderAddonTemplate.

## References

### Assets

- The vehicles were selected from the CADillac dataset and can be used under the Creative Commons Public License Version 4.0.
- "Cyclist - racing position - free 3d printable" (https://skfb.ly/6TM97) by Andy Woodhead is licensed under Creative Commons Attribution



## Future Work
### Potential Additions to the City Generator
- Street Furniture Sidewalk:
  - Bollards, Railings
  - Electrical Boxes
  - Parked Motocycles, Bikes, E-Scooter
  - Bicycle Racks
  - Advertisement Boards
  - Restaurants, chairs & tables
  - Construction sites on strett/ sidewalk
  -  Mailboxes
  -  Parking Metres
  -  Trash cans (on poles, standalone)
  -  Pedestrians
-