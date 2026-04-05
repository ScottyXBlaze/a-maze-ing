from .base_solver import BaseSolver
from collections import deque

class DFSSolver(BaseSolver):
    def __init__(
        self, maze: list[list[str]], starting: tuple[int, int], ending: tuple[int, int]
    ):
        super().__init__(maze, starting, ending)

    def solve(self) -> list[str] | None:
        if (
            not self.maze
            or not self._is_valid_pos(*self.starting)
            or not self._is_valid_pos(*self.ending)
        ):
            return None

        if self.starting == self.ending:
            return []

        queue = deque([self.starting])
        visited = {self.starting}
        previous: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        while queue:
            current = queue.popleft()

            if current == self.ending:
                break

            for direction, nxt in self.neighbors(current):
                if nxt in visited:
                    continue
                visited.add(nxt)
                previous[nxt] = (current, direction)
                queue.append(nxt)

        if self.ending not in visited:
            return None

        directions = []
        cursor = self.ending
        while cursor != self.starting:
            parent, direction = previous[cursor]
            directions.append(direction)
            cursor = parent
        directions.reverse()
        return directions

    def solve_as_string(self) -> str:
        path = self.solve()
        if path is None:
            return "NO PATH"
        return "".join(path)
