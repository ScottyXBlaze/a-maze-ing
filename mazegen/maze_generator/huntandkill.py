from random import Random


class HuntAndKill:
    def __init__(
            self,
            size: tuple[int, int],
            grid: list[list[str]],
            forty_two_positions: set[tuple[int, int]],
            seed: int | None = None,
            perfect: bool = True
            ):
        """Initialize all the config for the config

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
        self.dir_offsets: dict[str, tuple[int, int]] = {
            "N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)
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

    def delete_wall_between(
            self,
            pos1: tuple[int, int],
            pos2: tuple[int, int]
            ) -> None:
        if pos1[0] == pos2[0]:  # same row
            direction = "E" if pos1[1] < pos2[1] else "W"
        else:  # same column
            direction = "S" if pos1[0] < pos2[0] else "N"

        opposite_path = {"N": "S", "S": "N", "E": "W", "W": "E"}
        opposite = opposite_path[direction]
        self.delete_wall(pos1, direction)
        self.delete_wall(pos2, opposite)

    def delete_wall(self, pos: tuple[int, int], direction: str) -> None:
        bits = int(self.maze[pos[0]][pos[1]], 16)
        bit_index = self.dir_bits[direction]
        bits &= ~(1 << bit_index)  # Clear the bit
        self.maze[pos[0]][pos[1]] = hex(bits)[2:].upper()

    def __is_valid_pos(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def check_directions_visited(self, pos: tuple[int, int]) -> list[str]:
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
        available_wall = []
        try:
            number = int(self.maze[pos[0]][pos[1]], 16)
            for i in range(4):
                if (((number >> i) & 1) == 1):
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

    def delete_random_walls(self) -> None:
        # Take a random position
        available_wall: list[str] = []
        pos: tuple[int, int] = (0, 0)

        while len(available_wall) < 2:
            pos = (
                self.rng.randint(0, self.height - 1),
                self.rng.randint(0, self.width - 1)
            )
            available_wall = self.check_walls(pos)

        for wall in available_wall:
            opposite_cell_pos = (
                pos[0] + self.dir_offsets.get(wall, (0, 0))[0],
                pos[1] + self.dir_offsets.get(wall, (0, 0))[1]
            )

            # condition in the maze
            if not self.__is_valid_pos(
                opposite_cell_pos[0], opposite_cell_pos[1]
            ):
                continue

            opposite_wall = self.check_walls(opposite_cell_pos)

            if len(opposite_wall) < 2:
                continue

            self.delete_wall_between(pos, opposite_cell_pos)
            return

    def check_directions_unvisited(self, pos: tuple[int, int]) -> list[str]:
        directions = []
        for direction, (dx, dy) in self.dir_offsets.items():
            new_row, new_col = pos[0] + dx, pos[1] + dy
            if self.__is_valid_pos(new_row, new_col):
                if self.maze[new_row][new_col] == "F":
                    directions.append(direction)
        return directions

    def generate_path(self, pos: tuple[int, int]) -> None:
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
        visited_neighbors = self.check_directions_visited(pos)
        if visited_neighbors:
            direction = self.rng.choice(visited_neighbors)
            dx, dy = self.dir_offsets[direction]
            new_pos = (pos[0] + dx, pos[1] + dy)
            self.delete_wall_between(pos, new_pos)

    def run(self) -> None:
        start_pos = (0, 0)
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
            for _ in range((self.width*self.height) // 5):
                self.delete_random_walls()
        for pos in self.forty_two_positions:
            self.maze[pos[0]][pos[1]] = "F"
