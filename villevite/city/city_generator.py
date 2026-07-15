"""Main class that orchestrates the city generation"""
import bpy
from typing import Dict, List, Tuple, Optional


from .. import nodes, assets


class CityGenerator:
    """
    A class to generate a city from a manually built road graph.

    The road graph is a wire mesh (vertices and edges) that the GeoCity
    geometry node group consumes as its input geometry. All generation
    parameters live on the GeoCity modifier itself.
    """
    SCAN_PATH_NAME: str = "Scan Path"
    SCAN_PATH_COLLECTION_NAME: str = "Scan Paths"
    CITY_NAME: str = "City"
    GEO_CITY_GROUP: str = "GeoCity"

    def __init__(self, road_graph: bpy.types.Object) -> None:
        """
        Initialize the CityGenerator with the road graph object to build from.
        """
        self.road_graph = road_graph
        assets.import_assets_and_nodes()

    def _has_geocity_modifier(self, obj: bpy.types.Object) -> bool:
        return any(
            modifier.type == 'NODES'
            and modifier.node_group is not None
            and modifier.node_group.name == self.GEO_CITY_GROUP
            for modifier in obj.modifiers
        )

    def generate(self) -> bpy.types.Object:
        """
        Attach the GeoCity modifier to the road graph in place (idempotent).

        Returns:
            bpy.types.Object: The road graph object carrying the GeoCity modifier.
        """
        self.city = self.road_graph
        if not self._has_geocity_modifier(self.city):
            print(f"Adding City Generator geometry node group to {self.city.name}...")
            nodes.add_to_object(self.city, self.GEO_CITY_GROUP, {})
        return self.city

    def generate_for_scanning(self) -> Optional[Dict[str, bpy.types.Collection]]:
        """
        Generate the city and convert it to scanning objects.

        The bake runs on a copy of the road graph so the user's manually
        built graph survives the conversion.

        Returns:
            Dict[str, bpy.types.Collection]: Dictionary of created collections or None if conversion failed.
        """
        city = self.road_graph.copy()
        city.name = self.CITY_NAME
        bpy.context.scene.collection.objects.link(city)
        self.city = city
        if not self._has_geocity_modifier(city):
            nodes.add_to_object(city, self.GEO_CITY_GROUP, {})

        # Convert the city to scanning objects
        result = self._convert_to_scanning_objects()

        # Check if scan paths were created
        scan_paths_collection = result.get(f"{self.SCAN_PATH_NAME}s")
        if scan_paths_collection and len(scan_paths_collection.objects) > 0:
            print(f"{len(scan_paths_collection.objects)} scan paths created")
        else:
            print(f"WARNING: No scan paths were created. The city may not be scannable.")

        return result

    def _convert_to_scanning_objects(self):
        """
        Convert the city to real objects and organize them into collections.

        Returns:
            Dict[str, bpy.types.Collection]: Dictionary of created collections or None if conversion failed.
        """
        print("Converting city individual objects for scanning...")

        # Convert geometry nodes to real objects
        new_objects, new_collections = self._convert_to_objects()

        if not new_objects:
            print("No new objects created during conversion.")
            return

        return self._organize_city_collections(new_objects, new_collections)

    def _convert_to_objects(self) -> Tuple[List[bpy.types.Object], List[bpy.types.Collection]]:
        """
        Convert the geometry nodes to real objects using visual_geometry_to_objects.

        Returns:
            Tuple[List[bpy.types.Object], List[bpy.types.Collection]]: Lists of new objects and collections.
        """
        if not self.city:
            print(f"ERROR: City object attribute isn't set.")
            return [], []

        pre_objects = frozenset(obj.name for obj in bpy.data.objects)
        pre_collections = frozenset(coll.name for coll in bpy.data.collections)

        original_mode = bpy.context.mode
        try:
            if original_mode != 'OBJECT':
                print(f"Switching from {original_mode} to OBJECT mode")
                bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.object.select_all(action='DESELECT')
            self.city.select_set(True)
            bpy.context.view_layer.objects.active = self.city

            print("Converting geometry nodes to objects...")
            bpy.ops.object.visual_geometry_to_objects()

            new_objects = [obj for obj in bpy.data.objects if obj.name not in pre_objects]
            new_collections = [coll for coll in bpy.data.collections if coll.name not in pre_collections]

            print(f"Generated {len(new_objects)} new objects and {len(new_collections)} new collections")
            self._safe_remove_city_object()

            return new_objects, new_collections

        except Exception as e:
            print(f"Error during object conversion: {str(e)}")
            return [], []
        finally:
            if original_mode != 'OBJECT' and bpy.context.mode == 'OBJECT':
                try:
                    bpy.ops.object.mode_set(mode=original_mode.split('_')[0])
                except:
                    pass

    def _organize_city_collections(self, new_objects: List[bpy.types.Object],
                                  new_collections: List[bpy.types.Collection]) -> Dict[str, bpy.types.Collection]:
        """
        Extract and organize only scan path objects, ignoring all other objects and collections.

        Args:
            new_objects: List of newly created objects.
            new_collections: List of newly created collections (ignored).

        Returns:
            Dict[str, bpy.types.Collection]: Dictionary containing only the scan paths collection.
        """
        print("Extracting scan paths only...")

        scan_path_objects = []
        for obj in new_objects:
            base_name = obj.name.split('.')[0]
            if base_name == self.SCAN_PATH_NAME:
                scan_path_objects.append(obj)

        scan_path_collection = self._create_scan_path_collection_optimized(scan_path_objects)

        result = {
            f"{self.SCAN_PATH_NAME}s": scan_path_collection
        }

        print(f"Extracted {len(scan_path_objects)} scan path objects, ignored {len(new_objects) - len(scan_path_objects)} other objects")
        return result

    def _create_scan_path_collection_optimized(self, scan_path_objects: List[bpy.types.Object]) -> bpy.types.Collection:
        print(f"Creating collection named {self.SCAN_PATH_COLLECTION_NAME} for {len(scan_path_objects)} scan path objects")
        scan_path_collection = self._create_collection(self.SCAN_PATH_COLLECTION_NAME)

        if not scan_path_objects:
            print("No scan path objects found")
            return scan_path_collection

        for obj in scan_path_objects:
            self._move_object_to_collection(obj, scan_path_collection)

        print(f"Processing {len(scan_path_objects)} scan path objects...")
        self._batch_convert_scan_paths(scan_path_objects)

        print(f"Found and organized {len(scan_path_collection.objects)} scan path objects")
        return scan_path_collection

    def _batch_convert_scan_paths(self, scan_path_objects: List[bpy.types.Object]) -> None:
        if not scan_path_objects:
            return

        print(f"Converting {len(scan_path_objects)} scan path objects to bezier curves...")

        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        for obj in scan_path_objects:
            obj.select_set(True)

        if scan_path_objects:
            bpy.context.view_layer.objects.active = scan_path_objects[0]

        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.convert(target='CURVE')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.spline_type_set(type='BEZIER')
        bpy.ops.object.mode_set(mode='OBJECT')

        for obj in scan_path_objects:
            try:
                curve_data = obj.data
                if hasattr(curve_data, 'splines'):
                    for spline in curve_data.splines:
                        if spline.type == 'BEZIER' and hasattr(spline, 'bezier_points'):
                            for point in spline.bezier_points:
                                point.co = (point.co.x, point.co.y, 2.5)
                                point.handle_left_type = 'AUTO'
                                point.handle_right_type = 'AUTO'
            except Exception as e:
                print(f"Warning: Failed to process scan path '{obj.name}': {str(e)}")

        bpy.ops.object.select_all(action='DESELECT')
        print(f"Successfully converted {len(scan_path_objects)} scan path objects")

    def _create_collection(self, name: str) -> bpy.types.Collection:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        return collection

    def _move_object_to_collection(self, obj, target_collection):
        collections_to_unlink = [c for c in obj.users_collection if obj.name in c.objects]

        for c in collections_to_unlink:
            c.objects.unlink(obj)

        if obj.name not in target_collection.objects:
            target_collection.objects.link(obj)

    def _move_objects_to_collection_batch(self, objects: List[bpy.types.Object], target_collection):
        for obj in objects:
            self._move_object_to_collection(obj, target_collection)

    def _safe_remove_city_object(self) -> None:
        try:
            if self.city and self.city.name in bpy.data.objects:
                city_name = self.city.name
                print(f"Removing original city object '{city_name}'")
                bpy.data.objects.remove(self.city, do_unlink=True)
                print(f"Successfully removed city object '{city_name}'")
            else:
                print("City object no longer exists or was already removed")
        except Exception as e:
            print(f"Warning: Failed to remove city object: {str(e)}")
        finally:
            self.city = None
