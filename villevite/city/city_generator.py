"""Main class that orchestrates the city generation"""
import bpy
from typing import Dict, List, Tuple, Optional


from .. import nodes, assets
from ..osm.osm_generator import OSMGenerator


class CityGenerator:
    """
    A class to generate a city using Blender and OpenStreetMap (OSM) data.

    Attributes:
        source (str): The data source for the city generation.
        source_file (str): The file path to the source data if using OSM-Attributes.
        parameters (Dict[str, Any]): A dictionary of parameters for city generation.
    """
    # Constants for object and collection names
    SCAN_PATH_NAME: str = "Scan Path"
    SCAN_PATH_COLLECTION_NAME: str = "Scan Paths"
    CITY_NAME: str = "City"

    def __init__(self, properties: bpy.types.PropertyGroup) -> None:
        """
        Initialize the CityGenerator with the given properties.
        """
        self.set_parameters(properties)
        self.coordinates = properties.coordinates
        assets.import_assets_and_nodes()

    def set_parameters(self, parameters: bpy.types.PropertyGroup) -> None:
        """
        Set the city generation parameters from the cityProperties Group.
        """
        self.parameters = {
            "Roadway Vehicle Density": parameters.roadway_vehicle_density,
            "Parking Lot Vehicle Density": parameters.parking_lot_vehicle_density,
            "Preview": False,
            "Seed": 0,
        }

    def retrieve_map(self) -> Optional[bpy.types.Object]:
        """
        Retrieve the city map .

        Returns:
            Optional[bpy.types.Object]: The generated city map object or None if unsuccessful.
        """

        print(f"Retrieving OSM data with coordinates: {self.coordinates}")

        city_map = OSMGenerator(stringcoords=self.coordinates).generate()

        return city_map

    def generate(self) -> Optional[bpy.types.Object]:
        """
        Generate the city using the specified parameters.

        Returns:
            Optional[bpy.types.Object]: The generated city object or None if unsuccessful.
        """
        self.city = self.retrieve_map()

        print(f"Adding City Generator geometry node group to {self.city.name}...")
        self.city = nodes.add_to_object(self.city, "City Generator", self.parameters)
        self.city.name = self.CITY_NAME

        return self.city

    def generate_for_scanning(self) -> Optional[Dict[str, bpy.types.Collection]]:
        """
        Generate the city and convert it to scanning objects.

        Returns:
            Dict[str, bpy.types.Collection]: Dictionary of created collections or None if conversion failed.
        """
        # Generate the city
        self.city = self.generate()

        # Convert the city to scanning objects
        result = self.convert_to_scanning_objects()

        # Check if scan paths were created
        scan_paths_collection = result.get(f"{self.SCAN_PATH_NAME}s")
        if scan_paths_collection and len(scan_paths_collection.objects) > 0:
            print(f"{len(scan_paths_collection.objects)} scan paths created")
        else:
            print(f"WARNING: No scan paths were created. The city may not be scannable.")

        return result

    def convert_to_scanning_objects(self):
        """
        Convert the city to real objects and organize them into collections.

        Returns:
            Dict[str, bpy.types.Collection]: Dictionary of created collections or None if conversion failed.
        """
        print("Converting city individual objects for scanning...")

        # Convert geometry nodes to real objects
        new_objects, new_collections = self.convert_to_objects()

        if not new_objects:
            print("No new objects created during conversion.")
            return

        return self.organize_city_collections(new_objects, new_collections)

    def convert_to_objects(self) -> Tuple[List[bpy.types.Object], List[bpy.types.Collection]]:
        """
        Convert the geometry nodes to real objects using visual_geometry_to_objects.

        Returns:
            Tuple[List[bpy.types.Object], List[bpy.types.Collection]]: Lists of new objects and collections.
        """
        if not self.city:
            print(f"ERROR: City object attribute isn't set.")
            return [], []
        # Keep track of objects before conversion
        pre_objects = set(obj.name for obj in bpy.data.objects)
        pre_collections = set(coll.name for coll in bpy.data.collections)

        if bpy.context.mode != 'OBJECT':
            print(f"Switching from {bpy.context.mode} to OBJECT mode")
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        self.city.select_set(True)
        bpy.context.view_layer.objects.active = self.city

        bpy.ops.object.visual_geometry_to_objects()

        # Find all objects newly created by the operator
        new_objects = [obj for obj in bpy.data.objects if obj.name not in pre_objects]
        new_collections = [coll for coll in bpy.data.collections if coll.name not in pre_collections]
        print(f"Generated {len(new_objects)} new objects and {len(new_collections)} new collections")

        bpy.data.objects.remove(self.city, do_unlink=True)

        return new_objects, new_collections

    def organize_city_collections(self, new_objects: List[bpy.types.Object],
                                  new_collections: List[bpy.types.Collection]) -> Dict[str, bpy.types.Collection]:
        """
        Organize the collections and objects created by visual_geometry_to_objects.

        Args:
            new_objects: List of newly created objects.
            new_collections: List of newly created collections.

        Returns:
            Dict[str, bpy.types.Collection]: Dictionary of created collection names to collection objects.
        """

        scan_path_collection = self._create_scan_path_collection(new_objects)
        asset_collection = self._create_asset_collection(new_collections)
        instances_collection = self._create_instance_collections(new_objects)

        # Return a dictionary of all top-level collections
        result = {
            f"{self.SCAN_PATH_NAME}s": scan_path_collection,
            "Assets": asset_collection,
            "Instances": instances_collection
        }

        return result

    def _create_asset_collection(self, new_collections: List[bpy.types.Collection]) -> bpy.types.Collection:
        """
        Move all geometry collections to the parent asset collection.

        Args:
            new_collections: List of newly created collections.

        Returns:
            bpy.types.Collection: The parent collection for all geometry collections.
        """

        # Create a parent collection for all geometry collections
        print("Creating Assets collection for geometry")
        asset_collection = bpy.data.collections.new("Assets")
        bpy.context.scene.collection.children.link(asset_collection)

        # Hide the asset collection and exclude from renders
        asset_collection.hide_viewport = True
        asset_collection.hide_render = True

        for coll in new_collections:
            # Find all parent collections
            parent_collections = self.find_parent_collections(coll)

            # Unlink from all parent collections
            for parent in parent_collections:
                parent.children.unlink(coll)
                asset_collection.children.link(coll)
        return asset_collection

    def find_parent_collections(self, target_coll):
        """
        Find all collections that have the given collection as a child.

        Args:
            target_coll (bpy.types.Collection): The collection to find parents for.

        Returns:
            List[bpy.types.Collection]: List of parent collections.
        """
        parents = []
        for potential_parent in bpy.data.collections:
            if potential_parent == target_coll:
                continue  # Skip self-reference

            # Check if the target is directly a child of this collection
            if target_coll.name in [c.name for c in potential_parent.children]:
                parents.append(potential_parent)

        # Also check if it's linked to the scene collection
        if target_coll.name in [c.name for c in bpy.context.scene.collection.children]:
            parents.append(bpy.context.scene.collection)

        return parents
    def _create_scan_path_collection(self, new_objects: List[bpy.types.Object]) -> bpy.types.Collection:
        """
        Create a collection for scan path objects and move relevant objects into it.

        Args:
            new_objects: List of newly created objects.

        Returns:
            bpy.types.Collection: The scan path collection.
        """

        print(f"Creating collection named {self.SCAN_PATH_COLLECTION_NAME} for {self.SCAN_PATH_NAME} objects")
        scan_path_collection = self._create_collection(self.SCAN_PATH_COLLECTION_NAME)

        for obj in new_objects:
            base_name = obj.name.split('.')[0]
            if base_name == self.SCAN_PATH_NAME:
                self._move_object_to_collection(obj, scan_path_collection)

        print(f"Found and organized {len(scan_path_collection.objects)} scan path objects")
        return scan_path_collection

    def _create_instance_collections(self, new_objects: List[bpy.types.Object]) -> bpy.types.Collection:
        """
        Organize objects by their type into appropriate collections.
        All instance collections are added as children of a main "Instances" collection.

        Args:
            new_objects: List of newly created objects.
        Returns:
            bpy.types.Collection: The main Instances collection containing all instance collections.
        """
        # Organize objects by their base names (removing .001, .002, etc.)
        object_collections = {}
        word1_collections = {}  # Collections for objects with matching first word
        word2_collections = {}  # Collections for objects with matching first two words
        result_collections = {}  # Dictionary to track all created collections

        print("Organizing newly created objects into collections")

        # Create main Instances collection
        instances_collection = self._create_collection("Instances")
        result_collections["Instances"] = instances_collection

        # Temporarily unlink from scene collection to avoid duplication
        # We'll link it back at the end of the process
        bpy.context.scene.collection.children.unlink(instances_collection)

        for obj in new_objects:
            # Get base name by removing the suffix like .001, .002
            base_name = obj.name.split('.')[0]

            # Skip the original object
            if obj.name == base_name:
                continue

            # Check if it's an empty with linked collection
            if obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION':
                self._process_instance_empty(obj, base_name, object_collections, word1_collections,
                                           word2_collections, result_collections, instances_collection)

        # Final cleanup: make sure all word1 collections are linked directly to the main instances collection
        # and not to the scene collection
        for word1, word1_coll in word1_collections.items():
            # Check if it's linked to the scene collection
            if word1_coll.name in [c.name for c in bpy.context.scene.collection.children]:
                bpy.context.scene.collection.children.unlink(word1_coll)

            # Link to main instances collection if not already linked
            if word1_coll.name not in [c.name for c in instances_collection.children]:
                instances_collection.children.link(word1_coll)

        # Link the main instances collection back to the scene collection
        bpy.context.scene.collection.children.link(instances_collection)

        print(f"Organized {len(object_collections)} types of instances into collections")
        return instances_collection

    def _process_instance_empty(self, obj, base_name, object_collections, word1_collections,
                              word2_collections, result_collections, instances_collection):
        """
        Process an instance empty object and organize it into collections.

        Args:
            obj: The object to process.
            base_name: The base name of the object (without numeric suffix).
            object_collections: Dictionary of object type to collection mapping.
            word1_collections: Dictionary of first-word collections.
            word2_collections: Dictionary of two-word collections.
            result_collections: Dictionary of created collections.
            instances_collection: The main Instances collection.
        """
        # Create collection if it doesn't exist
        if base_name not in object_collections:
            # Split the base name by spaces to get words
            words = base_name.split(' ')

            # Handle first word collection hierarchy
            if len(words) >= 1:
                self._create_word1_collection(words[0], word1_collections, result_collections)

                # Handle second word collection hierarchy (if applicable)
                if len(words) >= 2 and words[0] in word1_collections:
                    self._create_word2_collection(words[0], words[1], word1_collections,
                                                word2_collections, result_collections)

            # Create type-specific collection
            self._create_instance_collection(base_name, words, word1_collections,
                                          word2_collections, result_collections, object_collections)

        # Move this empty into the corresponding collection if it exists
        if base_name in object_collections:
            self._move_object_to_collection(obj, object_collections[base_name])

    def _create_word1_collection(self, word1, word1_collections, result_collections):
        """Create a collection for objects with the same first word"""
        if word1 not in word1_collections:
            word1_collection = bpy.data.collections.new(f"{word1}")
            # Don't link to scene collection, it will be linked to the instances collection later
            # to avoid duplication in the hierarchy
            word1_collections[word1] = word1_collection
            result_collections[word1] = word1_collection

    def _create_word2_collection(self, word1, word2, word1_collections, word2_collections, result_collections):
        """Create a collection for objects with the same first two words"""
        word2_key = f"{word1} {word2}"
        if word2_key not in word2_collections:
            word2_collection = bpy.data.collections.new(word2_key)
            word1_collections[word1].children.link(word2_collection)
            word2_collections[word2_key] = word2_collection
            result_collections[word2_key] = word2_collection

    def _create_instance_collection(self, base_name, words, word1_collections,
                                  word2_collections, result_collections, object_collections):
        """Create a collection for a specific instance type"""
        collection_name = f"{base_name} Instances"
        collection = bpy.data.collections.new(collection_name)
        result_collections[collection_name] = collection

        # Link to appropriate parent collection based on word count
        if len(words) >= 2 and words[0] in word1_collections:
            word2_key = f"{words[0]} {words[1]}"
            if word2_key in word2_collections:
                word2_collections[word2_key].children.link(collection)
            elif words[0] in word1_collections:
                word1_collections[words[0]].children.link(collection)
            # We don't link to scene_collection anymore - it will be handled later
        elif len(words) >= 1 and words[0] in word1_collections:
            word1_collections[words[0]].children.link(collection)
        # We don't link to scene_collection anymore - orphaned collections
        # will be linked to instances_collection in the cleanup phase

        object_collections[base_name] = collection

    def _create_collection(self, name: str) -> bpy.types.Collection:
        """
        Create a new collection with the given name.

        Args:
            name (str): The name of the collection to create.

        Returns:
            bpy.types.Collection: The created collection.
        """
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        return collection

    def _move_object_to_collection(self, obj, target_collection):
        """Move an object to a target collection"""
        old_collections = [c for c in obj.users_collection]
        for c in old_collections:
            c.objects.unlink(obj)
        target_collection.objects.link(obj)
