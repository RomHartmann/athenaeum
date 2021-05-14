"""recursive Factorial:"""


def calculate_factorial(n):
    """Calc n!"""
    total = n
    while n > 2:
        n -= 1
        total *= n
    return total


def recursive_factorial(n, total=1):
    """calc n! recursively"""
    total = n*total
    if n > 2:
        total = recursive_factorial(n-1, total)

    return total


if __name__ == '__main__':
    tot = calculate_factorial(5)
    print(tot)

    tot_rec = recursive_factorial(5)
    print(tot_rec)




"""
Number of Islands

Given a 2d grid map of '1's (land) and '0's (water), count the number of islands.
An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
You may assume all four edges of the grid are all surrounded by water.

Example 1:
    Input:
        11110
        11010
        11000
        00000
    Output: 1
        1

Example 2:
    Input:
        11000
        11000
        00100
        00011
    Output: 3
        3
"""


def represent_sparse(ascii_grid):
    """Convert 2d matrix in 1d sparse representation.

    :param ascii_grid: Matrix of 1s & 0s
    :type ascii_grid: str
    :return: Coordinates in matrix that are 1s
    :rtype: list of tuple
    """
    ascii_grid = ascii_grid.strip()
    sparse_repr = []
    lines = ascii_grid.split("\n")
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "1":
                sparse_repr.append((i, j))
    return sparse_repr


def island_detection(grid):
    """Recursive detection of number of islands.

    Depth first: find all neighbours

    :param grid: Coordinates of uncategorized coordinates
    :type grid: list of tuple
    :return: Coordinates for discreet islands
    :rtype: list of tuple
    """
    def depth_traverse(leftover_grid, current_island):
        """Depth first traversal to add all touching land to island."""
        this_point = current_island[-1]
        for coord in leftover_grid.copy():
            if distance(this_point, coord) == 1:
                if len(leftover_grid) == 0:
                    return
                current_island.append(coord)
                leftover_grid.remove(coord)
                depth_traverse(leftover_grid, current_island)

    islands = []
    while len(grid) > 0:
        land = grid.pop()
        island = [land]

        depth_traverse(grid, island)

        islands.append(island)

    return islands


def distance(coord1, coord2):
    """Euclidian distance between 2 coords

    :param coord1: Coordinate 1
    :type coord1: tuple
    :param coord2: Coordinate 2
    :type coord2: tuple
    :return: Distance between 2 coordinates
    :rtype: float
    """
    import math
    return math.sqrt(
        (coord1[0] - coord2[0])**2 +
        (coord1[1] - coord2[1])**2
    )


island1 = """
11110
11010
11000
00000
"""
island2 = """
11000
11000
00100
00011
"""

if __name__ == '__main__':
    sparse = represent_sparse(island1)
    # sparse = represent_sparse(island2)
    print(sparse)
    print("="*30)
    all_islands = []
    islnds = island_detection(sparse)
    print(islnds)
    print(len(islnds))
