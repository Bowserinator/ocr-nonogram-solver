import numpy as np
import base64
from src import ocr
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


def encode_solution(solution):
    """
    Base64 encode a solution for comparison
    :param solution: Matrix, must contain only 0s and 1s
    :return: string
    """
    solution = solution.flatten()
    bs = []
    for i in range(0, len(solution), 8):
        b = int("".join([str(x) for x in solution[i: i + 8]]), 2)
        bs.append(b)
    return str(base64.b64encode(bytes(bs)))[2:-1]


def solve_image(path):
    """
    OCR + solve
    :param path: Path to image
    :return: solution (matrix), success
    """
    row, col = ocr.recognize(path)
    return solve(row, col)
