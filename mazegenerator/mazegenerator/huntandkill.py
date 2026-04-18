"""Module that contain the Hunt And Kill stategy."""

from random import Random


class HuntAndKill:
    """Hunt and kill maze generator algorithm.

    it is a randomized algorithm that creates random path like a random walk,
    but when it reaches a dead-end,it hunts for an unvisited cell that is
    adjacent to a visited one and creates a path between them, then it
    continues the random walk until all the cells are visited.
    if the maze is not perfect, it will delete some walls randomly to
    create loops in the maze.
    """

    def __init__(
        self,
        size: tuple[int, int],
        grid: list[list[str]],
        forty_two_positions: set[tuple[int, int]],
        seed: int | None = None,
        perfect: bool = True,
    ):
        """Initialize all the config for the maze Generator.

        Args:
            size (tuple[int, int]): the size of the maze
            grid (list[list[str]]): the maze we want to build with
            forty_two_positions (set[tuple[int, int]]):
              all the positions for the 42 logo
            seed (int | None, optional): the seed to make the maze.
              Defaults to None.
            perfect (bool): if the maze has a loops or not
        """
        self._width = size[0]
        self._height = size[1]
        self._maze = grid
        self._forty_two_positions = forty_two_positions

        self._rng = Random(seed)
        self._dir_bits = {"N": 0, "E": 1, "S": 2, "W": 3}
        self._dir_offsets: dict[str, tuple[int, int]] = {
            "N": (-1, 0),
            "E": (0, 1),
            "S": (1, 0),
            "W": (0, -1),
        }

        self._perfect = perfect
        self._perfect_percent = 0.2

    def _hunt(self) -> tuple[int, int] | None:
        """Check an unvisited cell that is near a visited one.

        Returns:
            tuple[int, int] | None: the unvisited cell
        """
        for i in range(self._height):
            for j in range(self._width):
                if self._maze[i][j] == "F":
                    visited_neighbors = self.check_directions_visited((i, j))
                    if visited_neighbors:
                        return (i, j)
        return None

    def _delete_wall_between(
        self, pos1: tuple[int, int], pos2: tuple[int, int]
    ) -> None:
        """Remove the wall between two positions.

        Args:
            pos1 (tuple[int, int]): Initial position
            pos2 (tuple[int, int]): position adjacent with the
            initial one
        """
        if pos1[0] == pos2[0]:  # same row
            direction = "E" if pos1[1] < pos2[1] else "W"
        else:  # same column
            direction = "S" if pos1[0] < pos2[0] else "N"

        opposite_path = {"N": "S", "S": "N", "E": "W", "W": "E"}
        opposite = opposite_path[direction]
        self._delete_wall(pos1, direction)
        self._delete_wall(pos2, opposite)

    def _delete_wall(self, pos: tuple[int, int], direction: str) -> None:
        """Delete a wall of a cell.

        Args:
            pos (tuple[int, int]): The position of the cell in the maze
            direction (str): the direction of the wall to delete (N, S, E, W)
        """
        bits = int(self._maze[pos[0]][pos[1]], 16)
        bit_index = self._dir_bits[direction]
        bits &= ~(1 << bit_index)  # Clear the bit
        self._maze[pos[0]][pos[1]] = hex(bits)[2:].upper()

    def _add_wall(self, pos: tuple[int, int], direction: str) -> None:
        """Add a wall to a cell.

        Args:
            pos (tuple[int, int]): The position of the cell in the maze
            direction (str): the direction of the wall to add (N, S, E, W)
        """
        bits = int(self._maze[pos[0]][pos[1]], 16)
        bit_index = self._dir_bits[direction]
        bits |= 1 << bit_index
        self._maze[pos[0]][pos[1]] = hex(bits)[2:].upper()

    def _is_valid_pos(self, row: int, col: int) -> bool:
        """Check if the position is valid for the maze.

        Args:
            row (int): the row in the maze
            col (int): the colon in the maze

        Returns:
            bool: True if the position is valid, False otherwise
        """
        return 0 <= row < self._height and 0 <= col < self._width

    def check_directions_visited(self, pos: tuple[int, int]) -> list[str]:
        """Check all the visited direction of the cells.

        Args:
            pos (tuple[int, int]): the position of the cells

        Returns:
            list[str]: the list of direction that is visited (N, S, E, W)
        """
        directions: list[str] = []
        for direction, (dx, dy) in self._dir_offsets.items():
            new_row, new_col = pos[0] + dx, pos[1] + dy
            if self._is_valid_pos(new_row, new_col):
                if (
                    self._maze[new_row][new_col] != "F"
                    and self._maze[new_row][new_col] != "42"
                ):
                    directions.append(direction)
        return directions

    def check_walls(self, pos: tuple[int, int]) -> list[str]:
        """Check all the walls of the cell.

        Args:
            pos (tuple[int, int]): The position of the cell in the maze

        Returns:
            list[str]: the list of walls (N, S, E, W)
        """
        available_wall = []
        try:
            number = int(self._maze[pos[0]][pos[1]], 16)
            for i in range(4):
                if ((number >> i) & 1) == 1:
                    if i == 0:
                        available_wall.append("N")
                    elif i == 1:
                        available_wall.append("E")
                    elif i == 2:
                        available_wall.append("S")
                    elif i == 3:
                        available_wall.append("W")
        except ValueError as e:
            print(e)
        return available_wall

    def _delete_random_walls(self) -> None:
        """Delete a random wall in the maze."""
        available_wall: list[str] = []
        pos: tuple[int, int] = (0, 0)

        while len(available_wall) < 2:
            pos = (
                self._rng.randint(0, self._height - 1),
                self._rng.randint(0, self._width - 1),
            )
            available_wall = self.check_walls(pos)

        for wall in available_wall:
            opposite_cell_pos = (
                pos[0] + self._dir_offsets.get(wall, (0, 0))[0],
                pos[1] + self._dir_offsets.get(wall, (0, 0))[1],
            )

            # condition in the maze
            if not self._is_valid_pos(
                opposite_cell_pos[0], opposite_cell_pos[1]
            ):
                continue

            opposite_wall = self.check_walls(opposite_cell_pos)

            if len(opposite_wall) < 2 or len(available_wall) < 2:
                continue
            else:
                self._delete_wall_between(pos, opposite_cell_pos)
                return

    def check_directions_unvisited(self, pos: tuple[int, int]) -> list[str]:
        """Check every directions of a cell that are unvisited.

        Args:
            pos (tuple[int, int]): the position of the cell

        Returns:
            list[str]: The list of the unvisited direction (N, E, S, W)
        """
        directions = []
        for direction, (dx, dy) in self._dir_offsets.items():
            new_row, new_col = pos[0] + dx, pos[1] + dy
            if self._is_valid_pos(new_row, new_col):
                if self._maze[new_row][new_col] == "F":
                    directions.append(direction)
        return directions

    def _generate_path(self, pos: tuple[int, int]) -> None:
        """Generate a randomized path in the maze.

        Args:
            pos (tuple[int, int]): The initial position of the cell
        """
        current_pos = pos
        while True:
            unvisited_neighbors = self.check_directions_unvisited(current_pos)
            if not unvisited_neighbors:
                break
            direction = self._rng.choice(unvisited_neighbors)
            dx, dy = self._dir_offsets[direction]
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            self._delete_wall_between(current_pos, new_pos)
            current_pos = new_pos

    def _link_with_visited(self, pos: tuple[int, int]) -> None:
        """Link and unvisited cell with a visited one.

        Args:
            pos (tuple[int, int]): The position of the unvisited cell
        """
        visited_neighbors = self.check_directions_visited(pos)
        if visited_neighbors:
            direction = self._rng.choice(visited_neighbors)
            dx, dy = self._dir_offsets[direction]
            new_pos = (pos[0] + dx, pos[1] + dy)
            self._delete_wall_between(pos, new_pos)

    def avoid_3x3(self) -> None:
        """Avoid 3x3 wall by adding a wall to the center."""
        no_walls: list[tuple[int, int]] = []
        for row in range(self._width):
            for col in range(self._height):
                if self._maze[row][col] == "0":
                    no_walls.append((row, col))

        for no_wall in no_walls:
            if self.is_open(no_wall):
                self._add_wall(no_wall, "N")
                opposite = no_wall[0] - 1, no_wall[1]
                self._add_wall(opposite, "S")

    def is_open(self, pos: tuple[int, int]) -> bool:
        """Check if the position have a big open area.

        Args:
            pos (tuple[int, int]): The position of the center
             of the area

        Returns:
            bool: True if it can have the big 3x3 area
        """
        for direction, offset in self._dir_offsets.items():
            tmp = pos[0] + offset[0], pos[1] + offset[1]
            if self.check_walls(tmp) != ["N"]:
                return False
        return True

        checks = "NE"
        offset = pos
        for check in checks:
            tmp = self._dir_offsets.get(check)
            offset = offset[0] + tmp[0], offset[1] + tmp[1]
        for wall in self.check_walls(offset):
            if wall in checks:
                continue
            return True

    def run(self) -> None:
        """Run the Hunt and Kill algorithm to solve the maze."""
        start_pos = (
            self._rng.randint(0, self._height - 1),
            self._rng.randint(0, self._width - 1),
        )
        for pos in self._forty_two_positions:
            self._maze[pos[0]][pos[1]] = "42"
        self._generate_path(start_pos)
        while True:
            next_pos = self._hunt()
            if not next_pos:
                break
            self._link_with_visited(next_pos)
            self._generate_path(next_pos)
        if not self._perfect:
            for _ in range(
                int((self._width * self._height) * self._perfect_percent)
            ):
                self._delete_random_walls()
        for pos in self._forty_two_positions:
            self._maze[pos[0]][pos[1]] = "F"
