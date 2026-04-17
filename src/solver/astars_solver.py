import heapq
from typing import List, Tuple, Optional
from .base_solver import BaseSolver


class AStarSolver(BaseSolver):
    """A Stars algorithm is probably the most used algo to solve
    path efficiently. it gives the most optimal path without
    checking all the cells of the maze, it is faster than BFS
    because of his pathfinding method and can be easily implemented
    with some easy math

    Args:
        BaseSolver (Class): The base of all the solver
    """

    def heuristic(self, pos: Tuple[int, int]) -> int:
        """Calculate the distance between a postion and
        the ending of the maze using the Manhattan distance

        Args:
            pos (Tuple[int, int]): the postion to do the math

        Returns:
            int: the distance between the pos and the ending
        """
        return abs(pos[0] - self.ending[0]) + abs(pos[1] - self.ending[1])

    def solve(self) -> Optional[List[str]]:
        """This solve the entire maze, it calculate the cost of each cell
        using a formula and prioritize the cell that has the minimal cost
        estimation to finish the maze, it can optimize the program
        because we don't have to checks every cells but we can still
        find the most optimal path

        Returns:
            Optional[List[str]]: the path in a list or None if no path was
            found
        """
        start = self.starting
        goal = self.ending

        open_set: list[tuple[int, int, tuple[int, int], list[str]]] = []

        heapq.heappush(open_set, (0 + self.heuristic(start), 0, start, []))

        visited = set()
        self.visited_cells = []

        while open_set:
            _, cost_so_far, current, path = heapq.heappop(open_set)

            if current in visited:
                continue

            visited.add(current)
            if not current == self.starting and not current == self.ending:
                self.visited_cells.append(current)

            if current == goal:
                return path

            for direction, neighbor in self.neighbors(current):
                if neighbor in visited:
                    continue

                new_cost = cost_so_far + 1

                new_path = path + [direction]

                priority = new_cost + self.heuristic(neighbor)

                heapq.heappush(
                    open_set, (priority, new_cost, neighbor, new_path)
                    )

        return None

    def solve_as_string(self) -> str:
        """Solve the maze and transorm the path into a string

        Returns:
            str: the formated string
        """
        path = self.solve()
        if path is None:
            return ""
        return "".join(path)
