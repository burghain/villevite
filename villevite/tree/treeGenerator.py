from .gen import Tree, TreeParam
from .tree_params import acer, apple, balsam_fir, bamboo, black_oak, black_tupelo, douglas_fir, european_larch, fan_palm, hill_cherry, lombardy_poplar, palm, quaking_aspen, sassafras, silver_birch, small_pine, sphere_tree, weeping_willow
import csv
from copy import copy


def generate_tree(tree_type):
    # tree = Tree(TreeParam(params), True)
    # tree.make()
    # list all files in the directory tree_params

    params = load_params()
    tree_params = params[tree_type]


def load_params() -> dict:
    """Load all params as a dict from tree_params.csv"""
    with open("tree_params.csv") as params_csv:
        reader = csv.DictReader(params_csv)
        all_params_dict = {}
        for row in reader:
            all_params_dict[row["name"]] = row
        return all_params_dict


def write_csv():
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

    with open('tree_params.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        keys = ["name"] + [*all_params[0].keys()]
        writer.writerow(keys)
        for i, params in enumerate(all_params):
            values = [names[i]] + [*params.values()]
            writer.writerow(values)
    print("Parameters saved to csv")
