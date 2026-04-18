"""Module that contain the DFS solver."""

from typing import Any, List, Optional
from .base_solver import BaseSolver


class DFSSolver(BaseSolver):
    """The DFS algorithm who is used for basic maze.

      It is not as good as other algorithm but it is
      easy to learn and understand and can easily solve
      perfect maze and unperfect one (but not the most optimal
      path sadly)

    Args:
        BaseSolver (Class): The base class of all the Solver algorithm
    """

    def solve(self) -> Optional[List[str]]:
        """Solve the entire maze.

        It is done by checking random path and traverse them until he reach a
        dead-end, then go back until he founds another unvisited path and
        wander there. the algo end only if he founds the path or that every
        available cells are visited.

        Returns:
            Optional[List[str]]: the path in a list or None if no path was
            found
        """
        if (
            not self.maze
            or not self._is_valid_pos(*self.starting)
            or not self._is_valid_pos(*self.ending)
        ):
            return None

        if self.starting == self.ending:
            return []

        stack: list[tuple[tuple[int, int], list[Any]]] = [(self.starting, [])]

        visited = {self.starting}
        self.visited_cells = []

        while stack:
            current_pos, path = stack.pop()

            if current_pos == self.ending:
                return path

            for direction, neighbor in self.neighbors(current_pos):
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                if not neighbor == self.ending:
                    self.visited_cells.append(neighbor)

                new_path = path + [direction]
                stack.append((neighbor, new_path))

        return None

    def solve_as_string(self) -> str:
        """Convert the path into a string.

        Returns:
            str: the path combined
        """
        path = self.solve()
        if path is None:
            return ""
        return "".join(path)
