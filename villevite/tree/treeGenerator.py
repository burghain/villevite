from .gen import Tree
from .tree_param import TreeParam


def generate_tree(tree_type):
    tree = Tree(TreeParam(tree_type="Acer"), True)
    tree.make()
