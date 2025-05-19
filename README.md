# Villevite City Generator

Villevite is a Blender add-on designed to procedurally generate cities for training data synthesis, including buildings, streets with variable width and intelligent crossroad calculation and vegetation. It provides tools for creating realistic urban environments and customization through assets and parameters.

## Features

- Procedural generation of cities with buildings, streets, and trees.
- Asset-based architecture for modular and reusable components.
- Integration with Blender's 3D Viewport for real-time visualization.
- Support for generating and managing city elements through a custom UI panel.

## Development Setup

### Prerequisites

- **Blender**: The add-on has been tested with Blender versions 4.3.2 and 4.4.0.
- **Python**: Python 3.9 or later is required for development.

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

1. Open Blender and navigate to the 3D Viewport.
2. Access the Villevite panel from the side toolbar under the "Villevite" tab.
3. Use the provided operators to generate city elements:
   - **Generate City**: Creates a procedural city layout.
   - **Generate Street Mesh**: Generates street meshes based on OSM data.

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
