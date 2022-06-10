import numpy as np
from picross_solver import picross_solver


def solve(rows, cols):
    """
    Solve the nonogram
    :param rows: Array of rows, ie [[1,2], [1]]. Empty are to be indicated as [0]
    :param rows: Array of cols, ie [[1,2], [1]]. Empty are to be indicated as [0]
    :return: Numpy matrix of solution
    """
    puzzle = np.full((len(rows), len(cols)), -1)
    success = picross_solver.solve(rows, cols, puzzle)
    return puzzle, success


def pretty_print_solution(puzzle):
    """
    Pretty print matrix output
    :param puzzle: Numpy matrix of solution
    """
    print("Puzzle size:", puzzle.shape)
    for row in puzzle:
        for char in row:
            out = "."
            if char == 1:
                out = "█"
            elif char == -1:
                out = "?"
            print(out, end="")
        print("")
