# Usage:
# python3 -m unittest tests.test
# from /server directory
import unittest
from src import solver


"""Ensure OCR solving works for various images"""
class TestOCR(unittest.TestCase):
    def test_5_5(self):
        """5x5 puzzle"""
        solution, success = solver.solve_image("./tests/examples/1.jpg")
        self.assertEqual(success, True, "Failed to solve")
        self.assertEqual(solver.encode_solution(solution), "/D4fAQ==", "Solution is incorrect")

    def test_25_25_1(self):
        """25x25 puzzle"""
        solution, success = solver.solve_image("./tests/examples/2.png")
        self.assertEqual(success, True, "Failed to solve")
        self.assertEqual(
            solver.encode_solution(solution),
            "/ou/wGSAb6KvtApAWuNDrXZN1riq6gAAABYkgCqltuqa22qP7ZvldvdVW07hbaXNlZ8AxDQAIoA/qg6gV9dfokOoUqgXqpL71KsB6qq/AQ==",
            "Solution is incorrect")

    def test_25_25_2(self):
        """25x25 puzzle"""
        solution, success = solver.solve_image("./tests/examples/3.png")
        self.assertEqual(success, True, "Failed to solve")
        self.assertEqual(
            solver.encode_solution(solution),
            "rqK7pVHVU7juoAAAAPwfgP8f4H/f8H///D///h///w///4f//8H//8D//+A//+AP/+AD/+AA/+AAH8AAB8AAAcAAAAAB1d1cju5IdVUkAA==",
            "Solution is incorrect")

if __name__ == '__main__':
    unittest.main()
