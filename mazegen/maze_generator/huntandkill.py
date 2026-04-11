from random import Random


class HuntAndKill:
    """Hunt and kill maze generator algorithm
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
        """Initialize all the config for the maze Generator

        Args:
            size (tuple[int, int]): the size of the maze
            grid (list[list[str]]): the maze we want to build with
            forty_two_positions (set[tuple[int, int]]):
              all the positions for the 42 logo
            seed (int | None, optional): the seed to make the maze.
              Defaults to None.
            perfect (bool): if the maze has a loops or not
        """
        self.width = size[0]
        self.height = size[1]
        self.maze = grid
        self.forty_two_positions = forty_two_positions

        self.rng = Random(seed)
        self.dir_bits = {"N": 0, "E": 1, "S": 2, "W": 3}
        self.opposite_path = {"N": "S", "S": "N", "E": "W", "W": "E"}
        self.dir_offsets: dict[str, tuple[int, int]] = {
            "N": (-1, 0),
            "E": (0, 1),
            "S": (1, 0),
            "W": (0, -1),
        }

        self.perfect = perfect
        self.perfect_percent = 0.2

    def hunt(self) -> tuple[int, int] | None:
        """Checks an unvisited cell that is near a visited one

        Returns:
            tuple[int, int] | None: the unvisited cell
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == "F":
                    visited_neighbors = self.check_directions_visited((i, j))
                    if visited_neighbors:
                        return (i, j)
        return None

    def delete_wall_between(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
        """Remove the wall between two positions

        Args:
            pos1 (tuple[int, int]): Initial position
            pos2 (tuple[int, int]): position adjacent with the
            initial one
        """
        if pos1[0] == pos2[0]:  # same row
            direction = "E" if pos1[1] < pos2[1] else "W"
        else:  # same column
            direction = "S" if pos1[0] < pos2[0] else "N"

        opposite = self.opposite_path[direction]
        self.delete_wall(pos1, direction)
        self.delete_wall(pos2, opposite)

    def delete_wall(self, pos: tuple[int, int], direction: str) -> None:
        """Delete a wall of a cell

        Args:
            pos (tuple[int, int]): The position of the cell in the maze
            direction (str): the direction of the wall to delete (N, S, E, W)
        """
        bits = int(self.maze[pos[0]][pos[1]], 16)
        bit_index = self.dir_bits[direction]
        bits &= ~(1 << bit_index)  # Clear the bit
        self.maze[pos[0]][pos[1]] = hex(bits)[2:].upper()

    def add_wall(self, pos: tuple[int, int], direction: str) -> None:
        """Add a wall to a cell

        Args:
            pos (tuple[int, int]): The position of the cell in the maze
            direction (str): the direction of the wall to add (N, S, E, W)
        """
        bits = int(self.maze[pos[0]][pos[1]], 16)
        bit_index = self.dir_bits[direction]
        bits |= 1 << bit_index
        self.maze[pos[0]][pos[1]] = hex(bits)[2:].upper()

    def __is_valid_pos(self, row: int, col: int) -> bool:
        """Check if the position is valid for the maze

        Args:
            row (int): the row in the maze
            col (int): the colon in the maze

        Returns:
            bool: True if the position is valid, False otherwise
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def check_directions_visited(self, pos: tuple[int, int]) -> list[str]:
        """Checks all the visited direction of the cells

        Args:
            pos (tuple[int, int]): the position of the cells

        Returns:
            list[str]: the list of direction that is visited (N, S, E, W)
        """
        directions = []
        for direction, (dx, dy) in self.dir_offsets.items():
            new_row, new_col = pos[0] + dx, pos[1] + dy
            if self.__is_valid_pos(new_row, new_col):
                if (
                    self.maze[new_row][new_col] != "F"
                    and self.maze[new_row][new_col] != "42"
                ):
                    directions.append(direction)
        return directions

    def check_walls(self, pos: tuple[int, int]) -> list[str]:
        """Checks all the walls of the cell

        Args:
            pos (tuple[int, int]): The position of the cell in the maze

        Returns:
            list[str]: the list of walls (N, S, E, W)
        """

        available_wall = []
        try:
            number = int(self.maze[pos[0]][pos[1]], 16)
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

    def delete_random_wall(self) -> None:
        while True:
            pos = (
                self.rng.randint(0, self.height - 1),
                self.rng.randint(0, self.width - 1),
            )
            available_wall = self.check_walls(pos)
            if len(available_wall) < 2:
                continue
            for wall in available_wall:
                offset = self.dir_offsets.get(wall, (0, 0))
                neighbor = (pos[0] + offset[0], pos[1] + offset[1])
                if not self.__is_valid_pos(neighbor[0], neighbor[1]):
                    continue
                wall_pos = self.check_walls(pos)
                wall_neighbor = self.check_walls(neighbor)
                if len(wall_pos) > 1 and len(wall_neighbor) > 1:
                    print(f"Position is {pos}")
                    print(f"available_wall: {available_wall}")
                    print(f"neighbor Position is {neighbor}")
                    print(f"Wall neighbor: {wall_neighbor}")
                    self.delete_wall_between(pos, neighbor)
                    return

    def delete_random_walls(self) -> None:
        """Delete a random wall in the maze"""
        available_wall: list[str] = []
        pos: tuple[int, int] = (0, 0)

        while len(available_wall) < 2:
            pos = (
                self.rng.randint(0, self.height - 1),
                self.rng.randint(0, self.width - 1),
            )
            available_wall = self.check_walls(pos)

        for wall in available_wall:
            opposite_cell_pos = (
                pos[0] + self.dir_offsets.get(wall, (0, 0))[0],
                pos[1] + self.dir_offsets.get(wall, (0, 0))[1],
            )

            # condition in the maze
            if not self.__is_valid_pos(opposite_cell_pos[0], opposite_cell_pos[1]):
                continue

            opposite_wall = self.check_walls(opposite_cell_pos)

            if len(opposite_wall) < 2:
                continue
            else:
                self.delete_wall_between(pos, opposite_cell_pos)
                return

    def restore_one_wall(self, pos: tuple[int, int]) -> None:
        """Restore a random wall of a cell that has no walls

        Args:
            pos (tuple[int, int]): The position of the cell
        """
        available_neighbors: list[str] = []
        for direction, (dx, dy) in self.dir_offsets.items():
            new_row, new_col = pos[0] + dx, pos[1] + dy
            if self.__is_valid_pos(new_row, new_col):
                available_neighbors.append(direction)

        if not available_neighbors:
            return

        direction = self.rng.choice(available_neighbors)
        dx, dy = self.dir_offsets[direction]
        neighbor = (pos[0] + dx, pos[1] + dy)
        self.add_wall(pos, direction)
        self.add_wall(neighbor, self.opposite_path[direction])

    def open_one_wall(self, pos: tuple[int, int]) -> bool:
        """Open one wall of a fully closed cell.

        Args:
            pos (tuple[int, int]): The position of the cell.

        Returns:
            bool: True if a wall was opened, False otherwise.
        """
        available_neighbors: list[str] = []
        for direction, (dx, dy) in self.dir_offsets.items():
            new_row, new_col = pos[0] + dx, pos[1] + dy
            if self.__is_valid_pos(new_row, new_col):
                available_neighbors.append(direction)

        if not available_neighbors:
            return False

        self.rng.shuffle(available_neighbors)
        for direction in available_neighbors:
            dx, dy = self.dir_offsets[direction]
            neighbor = (pos[0] + dx, pos[1] + dy)
            if self.maze[neighbor[0]][neighbor[1]] == "42":
                continue
            self.delete_wall_between(pos, neighbor)
            return True

        return False

    def avoid_zero_cells(self) -> None:
        """Verify and solve every cell that has no wall"""
        for row in range(self.height):
            for col in range(self.width):
                if self.maze[row][col] == "0":
                    self.restore_one_wall((row, col))

    def avoid_full_wall_cells(self) -> None:
        """Open one wall for every fully blocked cell ("F")."""
        for row in range(self.height):
            for col in range(self.width):
                if self.maze[row][col] == "F":
                    self.open_one_wall((row, col))

    def normalize_forbidden_cells(self) -> None:
        """Remove forbidden output values ("0" and "F") from final maze."""
        self.avoid_zero_cells()
        self.avoid_full_wall_cells()
        # Opening a closed cell can create a new "0" on the neighbor side.
        self.avoid_zero_cells()

    def check_directions_unvisited(self, pos: tuple[int, int]) -> list[str]:
        """Checks every directions of a cell that are unvisited

        Args:
            pos (tuple[int, int]): the position of the cell

        Returns:
            list[str]: The list of the unvisited direction (N, E, S, W)
        """
        directions = []
        for direction, (dx, dy) in self.dir_offsets.items():
            new_row, new_col = pos[0] + dx, pos[1] + dy
            if self.__is_valid_pos(new_row, new_col):
                if self.maze[new_row][new_col] == "F":
                    directions.append(direction)
        return directions

    def generate_path(self, pos: tuple[int, int]) -> None:
        """Generate a randomized path in the maze

        Args:
            pos (tuple[int, int]): The initial position of the cell
        """
        current_pos = pos
        while True:
            unvisited_neighbors = self.check_directions_unvisited(current_pos)
            if not unvisited_neighbors:
                break
            direction = self.rng.choice(unvisited_neighbors)
            dx, dy = self.dir_offsets[direction]
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            self.delete_wall_between(current_pos, new_pos)
            current_pos = new_pos

    def link_with_visited(self, pos: tuple[int, int]) -> None:
        """Link and unvisited cell with a visited one

        Args:
            pos (tuple[int, int]): The position of the unvisited cell
        """
        visited_neighbors = self.check_directions_visited(pos)
        if visited_neighbors:
            direction = self.rng.choice(visited_neighbors)
            dx, dy = self.dir_offsets[direction]
            new_pos = (pos[0] + dx, pos[1] + dy)
            self.delete_wall_between(pos, new_pos)

    def run(self) -> None:
        """Run the Hunt and Kill algorithm to solve the maze"""
        start_pos = (
            self.rng.randint(0, self.height - 1),
            self.rng.randint(0, self.width - 1),
        )
        for pos in self.forty_two_positions:
            self.maze[pos[0]][pos[1]] = "42"
        self.generate_path(start_pos)
        while True:
            next_pos = self.hunt()
            if not next_pos:
                break
            self.link_with_visited(next_pos)
            self.generate_path(next_pos)
        if not self.perfect:
            for _ in range(int((self.width * self.height) * self.perfect_percent)):
                self.delete_random_wall()
        for pos in self.forty_two_positions:
            self.maze[pos[0]][pos[1]] = "F"
        self.normalize_forbidden_cells()
