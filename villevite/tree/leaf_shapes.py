"""Pre-defined geometries for leaf and blossom meshes"""

from .chturtle import Vector

# these can't be global (static) or the shared instances gets modified by other stuff
# performing deepcopies is slow and causes other issues
# wrapping a function around the definitions prevents external access and solves all other issues


def leaves(t):
    return [
        (  # 1 = ovate
            [
                Vector([0.005, 0, 0]),
                Vector([0.005, 0, 0.1]),
                Vector([0.15, 0, 0.15]),
                Vector([0.25, 0, 0.3]),
                Vector([0.2, 0, 0.6]),
                Vector([0, 0, 1]),
                Vector([-0.2, 0, 0.6]),
                Vector([-0.25, 0, 0.3]),
                Vector([-0.15, 0, 0.15]),
                Vector([-0.005, 0, 0.1]),
                Vector([-0.005, 0, 0]),
            ],
            [[0, 1, 9, 10], [1, 2, 3, 4], [4, 5, 6], [6, 7, 8, 9], [4, 6, 9, 1]],
        ),
        (  # 2 = linear
            [
                Vector([0.005, 0, 0]),
                Vector([0.005, 0, 0.1]),
                Vector([0.1, 0, 0.15]),
                Vector([0.1, 0, 0.95]),
                Vector([0, 0, 1]),
                Vector([-0.1, 0, 0.95]),
                Vector([-0.1, 0, 0.15]),
                Vector([-0.005, 0, 0.1]),
                Vector([-0.005, 0, 0]),
            ],
            [[0, 1, 7, 8], [1, 2, 3], [3, 4, 5], [5, 6, 7], [1, 3, 5, 7]],
        ),
        (  # 3 = cordate
            [
                Vector([0.005, 0, 0]),
                Vector([0.01, 0, 0.2]),
                Vector([0.2, 0, 0.1]),
                Vector([0.35, 0, 0.35]),
                Vector([0.25, 0, 0.6]),
                Vector([0.1, 0, 0.8]),
                Vector([0, 0, 1]),
                Vector([-0.1, 0, 0.8]),
                Vector([-0.25, 0, 0.6]),
                Vector([-0.35, 0, 0.35]),
                Vector([-0.2, 0, 0.1]),
                Vector([-0.01, 0, 0.2]),
                Vector([-0.005, 0, 0]),
            ],
            [
                [0, 1, 11, 12],
                [1, 2, 3, 4],
                [11, 10, 9, 8],
                [11, 1, 4, 8],
                [8, 7, 6, 5, 4],
            ],
        ),
        (  # 4 = maple
            [
                Vector([0.005, 0, 0]),
                Vector([0.005, 0, 0.1]),
                Vector([0.25, 0, 0.07]),
                Vector([0.2, 0, 0.18]),
                Vector([0.5, 0, 0.37]),
                Vector([0.43, 0, 0.4]),
                Vector([0.45, 0, 0.58]),
                Vector([0.3, 0, 0.57]),
                Vector([0.27, 0, 0.67]),
                Vector([0.11, 0, 0.52]),
                Vector([0.2, 0, 0.82]),
                Vector([0.08, 0, 0.77]),
                Vector([0, 0, 1]),
                Vector([-0.08, 0, 0.77]),
                Vector([-0.2, 0, 0.82]),
                Vector([-0.11, 0, 0.52]),
                Vector([-0.27, 0, 0.67]),
                Vector([-0.3, 0, 0.57]),
                Vector([-0.45, 0, 0.58]),
                Vector([-0.43, 0, 0.4]),
                Vector([-0.5, 0, 0.37]),
                Vector([-0.2, 0, 0.18]),
                Vector([-0.25, 0, 0.07]),
                Vector([-0.005, 0, 0.1]),
                Vector([-0.005, 0, 0]),
            ],
            [
                [0, 1, 23, 24],
                [1, 2, 3, 4, 5],
                [23, 22, 21, 20, 19],
                [1, 5, 6, 7, 8],
                [23, 19, 18, 17, 16],
                [1, 8, 9, 10, 11],
                [23, 16, 15, 14, 13],
                [1, 11, 12, 13, 23],
            ],
        ),
        (  # 5 = palmate
            [
                Vector([0.005, 0, 0]),
                Vector([0.005, 0, 0.1]),
                Vector([0.25, 0, 0.1]),
                Vector([0.5, 0, 0.3]),
                Vector([0.2, 0, 0.45]),
                Vector([0, 0, 1]),
                Vector([-0.2, 0, 0.45]),
                Vector([-0.5, 0, 0.3]),
                Vector([-0.25, 0, 0.1]),
                Vector([-0.005, 0, 0.1]),
                Vector([-0.005, 0, 0]),
            ],
            [[0, 1, 9, 10], [1, 2, 3, 4], [1, 4, 5, 6, 9], [9, 8, 7, 6]],
        ),
        (  # 6 = spiky oak
            [
                Vector([0.005, 0, 0]),
                Vector([0.005, 0, 0.1]),
                Vector([0.16, 0, 0.17]),
                Vector([0.11, 0, 0.2]),
                Vector([0.23, 0, 0.33]),
                Vector([0.15, 0, 0.34]),
                Vector([0.32, 0, 0.55]),
                Vector([0.16, 0, 0.5]),
                Vector([0.27, 0, 0.75]),
                Vector([0.11, 0, 0.7]),
                Vector([0.18, 0, 0.9]),
                Vector([0.07, 0, 0.86]),
                Vector([0, 0, 1]),
                Vector([-0.07, 0, 0.86]),
                Vector([-0.18, 0, 0.9]),
                Vector([-0.11, 0, 0.7]),
                Vector([-0.27, 0, 0.75]),
                Vector([-0.16, 0, 0.5]),
                Vector([-0.32, 0, 0.55]),
                Vector([-0.15, 0, 0.34]),
                Vector([-0.23, 0, 0.33]),
                Vector([-0.11, 0, 0.2]),
                Vector([-0.16, 0, 0.17]),
                Vector([-0.005, 0, 0.1]),
                Vector([-0.005, 0, 0]),
            ],
            [
                [0, 1, 23, 24],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [1, 3, 5, 7, 9, 11, 12, 13, 15, 17, 19, 21, 23],
                [23, 22, 21],
                [21, 20, 19],
                [19, 18, 17],
                [17, 16, 15],
                [15, 14, 13],
            ],
        ),
        (  # 7 = round oak
            [
                Vector([0.005, 0, 0]),
                Vector([0.005, 0, 0.1]),
                Vector([0.11, 0, 0.16]),
                Vector([0.11, 0, 0.2]),
                Vector([0.22, 0, 0.26]),
                Vector([0.23, 0, 0.32]),
                Vector([0.15, 0, 0.34]),
                Vector([0.25, 0, 0.45]),
                Vector([0.23, 0, 0.53]),
                Vector([0.16, 0, 0.5]),
                Vector([0.23, 0, 0.64]),
                Vector([0.2, 0, 0.72]),
                Vector([0.11, 0, 0.7]),
                Vector([0.16, 0, 0.83]),
                Vector([0.12, 0, 0.87]),
                Vector([0.06, 0, 0.85]),
                Vector([0.07, 0, 0.95]),
                Vector([0, 0, 1]),
                Vector([-0.07, 0, 0.95]),
                Vector([-0.06, 0, 0.85]),
                Vector([-0.12, 0, 0.87]),
                Vector([-0.16, 0, 0.83]),
                Vector([-0.11, 0, 0.7]),
                Vector([-0.2, 0, 0.72]),
                Vector([-0.23, 0, 0.64]),
                Vector([-0.16, 0, 0.5]),
                Vector([-0.23, 0, 0.53]),
                Vector([-0.25, 0, 0.45]),
                Vector([-0.15, 0, 0.34]),
                Vector([-0.23, 0, 0.32]),
                Vector([-0.22, 0, 0.26]),
                Vector([-0.11, 0, 0.2]),
                Vector([-0.11, 0, 0.16]),
                Vector([-0.005, 0, 0.1]),
                Vector([-0.005, 0, 0]),
            ],
            [
                [0, 1, 33, 34],
                [1, 2, 3],
                [3, 4, 5, 6],
                [6, 7, 8, 9],
                [9, 10, 11, 12],
                [12, 13, 14, 15],
                [15, 16, 17],
                [1, 3, 6, 9, 12, 15, 17, 19, 22, 25, 28, 31, 33],
                [33, 32, 31],
                [31, 30, 29, 28],
                [28, 27, 26, 25],
                [25, 24, 23, 22],
                [22, 21, 20, 19],
                [19, 18, 17],
            ],
        ),
        (  # 8 = elliptic (default)
            [
                Vector([0.005, 0, 0]),
                Vector([0.005, 0, 0.1]),
                Vector([0.15, 0, 0.2]),
                Vector([0.25, 0, 0.45]),
                Vector([0.2, 0, 0.75]),
                Vector([0, 0, 1]),
                Vector([-0.2, 0, 0.75]),
                Vector([-0.25, 0, 0.45]),
                Vector([-0.15, 0, 0.2]),
                Vector([-0.005, 0, 0.1]),
                Vector([-0.005, 0, 0]),
            ],
            [[0, 1, 9, 10], [1, 2, 3, 4], [4, 5, 6], [6, 7, 8, 9], [4, 6, 9, 1]],
        ),
        (  # 9 = rectangle
            [
                Vector([-0.5, 0, 0]),
                Vector([-0.5, 0, 1]),
                Vector([0.5, 0, 1]),
                Vector([0.5, 0, 0]),
            ],
            [[0, 1, 2, 3]],
            [(0, 0), (0, 1), (1, 1), (1, 0)],
        ),
        (  # 10 = triangle
            [Vector([-0.5, 0, 0]), Vector([0, 0, 1]), Vector([0.5, 0, 0])],
            [[0, 1, 2]],
            [(0, 0), (0.5, 1), (1, 0)],
        ),
    ][t]
