"""Module that contain the BFS solver."""

from .base_solver import BaseSolver
from collections import deque


class BFSSolver(BaseSolver):
    """The BFS algorithm is a popular algorithm that solve maze.

    It give the most optimal path, even if it consume a lot of
    processor, it is easy to implement and understand making it
    beginner-friendly

    Args:
        BaseSolver (class): The base of all the solver
    """

    def solve(self) -> list[str] | None:
        """Solve the entire maze, it traverse cell step by step.

        It doesn't go any deeper without checking all other
        way at the same time. example he checks all the cells situated 1
        steps of the starting point, the all the cells situated 2 steps, ...
        That means that he is able to find the shortest path without doing a
        lot of math

        Returns:
            list[str] | None:
             The path of the maze or None is the ending can't be
             reached
        """
        if (
            not self.maze
            or not self._is_valid_pos(*self.starting)
            or not self._is_valid_pos(*self.ending)
        ):
            return None

        if self.starting == self.ending:
            return []

        queue: deque[tuple[int, int]] = deque([self.starting])
        visited: set[tuple[int, int]] = {self.starting}
        self.visited_cells = []
        previous: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        while queue:
            current: tuple[int, int] = queue.popleft()

            if current == self.ending:
                break

            for direction, nxt in self.neighbors(current):
                if nxt in visited:
                    continue
                visited.add(nxt)
                if not nxt == self.ending:
                    self.visited_cells.append(nxt)
                previous[nxt] = (current, direction)
                queue.append(nxt)

        if self.ending not in visited:
            return None

        directions: list[str] = []
        cursor: tuple[int, int] = self.ending
        while cursor != self.starting:
            parent, direction = previous[cursor]
            directions.append(direction)
            cursor = parent
        directions.reverse()
        return directions

    def solve_as_string(self) -> str:
        """Solve the maze and return the path as a string.

        Returns:
            str: The start-end path of the maze
        """
        path: list[str] | None = self.solve()
        if path is None:
            return "NO PATH"
        return "".join(path)
