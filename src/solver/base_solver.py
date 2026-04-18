"""Module that has the base class for all the solver."""

from abc import abstractmethod, ABC


class BaseSolver(ABC):
    """Contains all the base function and variable for a maze solver."""

    def __init__(
        self,
        maze: list[list[str]],
        starting: tuple[int, int],
        ending: tuple[int, int],
    ) -> None:
        """Every Initialization starts here.

        Args:
            maze (list[list[str]]): The maze to solve
            starting (tuple[int, int]): The starting position
            ending (tuple[int, int]): The ending position
        """
        self.dir_to_bit = {"N": 0, "E": 1, "S": 2, "W": 3}
        self.dir_to_offset = {
            "N": (-1, 0),
            "E": (0, 1),
            "S": (1, 0),
            "W": (0, -1),
        }
        self.direction_order = ("N", "E", "S", "W")

        self.maze = maze
        self.starting = starting
        self.ending = ending
        self.height = len(maze)
        self.width = len(maze[0]) if maze else 0
        self.visited_cells: list[tuple[int, int]] = []
        self._visited_cached: bool = False

    def _is_valid_pos(self, row: int, col: int) -> bool:
        """Verify if the coordinate is in the maze.

        Args:
            row (int): row in the maze
            col (int): colon in the maze

        Returns:
            bool: True if it's in the maze else false
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def _cell_value(self, row: int, col: int) -> int:
        """Give the value of a point in the maze.

        Args:
            row (int): the row of the cell
            col (int): the colon of the cell

        Returns:
            int: the value of the as integer of base 16
        """
        return int(self.maze[row][col], 16)

    def neighbors(
        self, position: tuple[int, int]
    ) -> list[tuple[str, tuple[int, int]]]:
        """Check all the neighbors of the cell.

        Args:
            position (tuple[int, int]): the position of the cell
             that we want to check

        Returns:
            list[tuple[str, tuple[int, int]]]: direciton and position of
             the neighbors cells
        """
        row, col = position
        cell: int = self._cell_value(row, col)
        result: list[tuple[str, tuple[int, int]]] = []

        for direction in self.direction_order:
            bit_index: int = self.dir_to_bit[direction]
            has_wall: bool = ((cell >> bit_index) & 1) == 1
            if has_wall:
                continue

            dr, dc = self.dir_to_offset[direction]
            new_row, new_col = row + dr, col + dc
            if self._is_valid_pos(new_row, new_col):
                result.append((direction, (new_row, new_col)))

        return result

    def set_new_maze(self, maze: list[list[str]]) -> None:
        """Change the maze in the solver.

        Args:
            maze (list[list[str]]): The new maze
        """
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0]) if maze else 0
        self.visited_cells = []
        self._visited_cached = False

    @abstractmethod
    def solve_as_string(self) -> str:
        """Solve the maze and return a string of the path.

        Returns:
            str: The string of the path
        """
        pass

    @abstractmethod
    def solve(self) -> list[str] | None:
        """Solve the maze and return the path in a list.

        Returns:
            list[str] | None: The path of the start to end path
        """
        return [""]

    def get_visited_cells(self) -> list[tuple[int, int]]:
        """Get a list of all the visited cells.

        Returns:
            list[tuple[int, int]]: The list of all the position of the cell
        """
        if not self._visited_cached:
            self.solve()
            self._visited_cached = True
        return self.visited_cells
