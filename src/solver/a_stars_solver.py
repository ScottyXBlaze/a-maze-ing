from .base_solver import BaseSolver
from queue import PriorityQueue

class AStarsSolver(BaseSolver):
    def __init__(self, maze: list[list[str]], starting: tuple[int, int], ending: tuple[int, int]):
        super().__init__(maze, starting, ending)

    def heuristic(self, pos: list[int, int]) -> int:
        return abs(pos[0] - self.ending[0]) + abs(pos[1] - self.ending[1])
    
    def solve(self):
        open_list = PriorityQueue()
        open_list.put((0, self.starting))