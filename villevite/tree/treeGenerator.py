from .gen import Tree, TreeParam
from .tree_params import acer, apple, balsam_fir, bamboo, black_oak, black_tupelo, douglas_fir, european_larch, fan_palm, hill_cherry, lombardy_poplar, palm, quaking_aspen, sassafras, silver_birch, small_pine, sphere_tree, weeping_willow
import csv
from copy import deepcopy
import os


def generate_tree(tree_type):
    params = load_params()
    tree_params = params[tree_type]
    del tree_params["name"]
    print(tree_params)
    # return
    tree = Tree(TreeParam(tree_params), True)
    tree.make()


def load_params() -> dict:
    """Load all params as a dict from tree_params.csv"""
    with open("tree_params.csv") as params_csv:
        reader = csv.DictReader(params_csv)
        all_params_dict = {}
        for row in reader:
            params_dict = {}
            for key in row.keys():
                if row[key] == '':
                    continue
                elif key == "name":
                    params_dict["name"] = row[key]
                elif type(row[key]) == str:
                    params_dict[key] = eval(row[key])
            all_params_dict[params_dict["name"]] = deepcopy(params_dict)
        return all_params_dict


def write_csv():
    defaults = {
        'shape': 7,
        'g_scale': 13,
        'g_scale_v': 3,
        'levels': 3,
        'ratio': 0.015,
        'ratio_power': 1.2,
        'flare': 0.6,
        'base_splits': 0,
        'base_size': [0.3, 0.02, 0.02, 0.02],
        'down_angle': [-0, 60, 45, 45],
        'down_angle_v': [-0, -50, 10, 10],
        'rotate': [-0, 140, 140, 77],
        'rotate_v': [-0, 0, 0, 0],
        'branches': [1, 50, 30, 10],
        'length': [1, 0.3, 0.6, 0],
        'length_v': [0, 0, 0, 0],
        'taper': [1, 1, 1, 1],
        'seg_splits': [0, 0, 0, 0],
        'split_angle': [40, 0, 0, 0],
        'split_angle_v': [5, 0, 0, 0],
        'bevel_res': [10, 10, 10, 10],
        'curve_res': [5, 5, 3, 1],
        'curve': [0, -40, -40, 0],
        'curve_back': [0, 0, 0, 0],
        'curve_v': [20, 50, 75, 0],
        'bend_v': [-0, 50, 0, 0],
        'branch_dist': [-0, 0, 0, 0],
        'radius_mod': [1, 1, 1, 1],
        'leaf_blos_num': 40,
        'leaf_shape': 0,
        'leaf_scale': 0.17,
        'leaf_scale_x': 1,
        'leaf_bend': 0.6,
        'blossom_shape': 1,
        'blossom_scale': 0,
        'blossom_rate': 0,
        'tropism': [0, 0, 0.5],
        'prune_ratio': 0,
        'prune_width': 0.5,
        'prune_width_peak': 0.5,
        'prune_power_low': 0.5,
        'prune_power_high': 0.5
    }
    all_params = [
        acer.params,
        apple.params,
        balsam_fir.params,
        bamboo.params,
        black_oak.params,
        black_tupelo.params,
        douglas_fir.params,
        european_larch.params,
        fan_palm.params,
        hill_cherry.params,
        lombardy_poplar.params,
        palm.params,
        quaking_aspen.params,
        sassafras.params,
        silver_birch.params,
        small_pine.params,
        sphere_tree.params,
        weeping_willow.params,
    ]
    # Tree names as their display name, i.e ACER -> Acer
    names = [
        "Acer",
        "Apple",
        "Balsam Fir",
        "Bamboo",
        "Black Oak",
        "Black Tupelo",
        "Douglas Fir",
        "European Larch",
        "Fan Palm",
        "Hill Cherry",
        "Lombardy Poplar",
        "Palm",
        "Quaking Aspen",
        "Sassafras",
        "Silver Birch",
        "Small Pine",
        "Sphere Tree",
        "Weeping Willow"
    ]
    all_keys = ["name"] + [*defaults.keys()]
    csv_path = os.path.join(os.path.dirname(__file__), "tree_params.csv")
    with open(csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(all_keys)
        for i, params in enumerate(all_params):
            values = [names[i]]
            for key in all_keys[1:]:
                if key in params.keys():
                    values.append(params[key])
                else:
                    values.append(None)
            writer.writerow(values)
    print("Parameters saved to csv")
