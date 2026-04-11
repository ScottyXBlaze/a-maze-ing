from .huntandkill import HuntAndKill


class MazeGenerator:
    """Maze Generator class to generate maze
    """
    def __init__(self, size: tuple[int, int], perfect: bool = True) -> None:
        """setup and init for all the config of the maze

        Args:
            size (tuple[int, int]): the size of the maze
            perfect (bool, optional): True to have only one path.
        """
        self.width = size[0]
        self.height = size[1]

        self.maze = self.generate_grid()

        self.perfect = perfect

    def generate_grid(self) -> list[list[str]]:
        """Generate a grid full of walls 'F'

        Returns:
            list[list[str]]: grid in 2D
        """
        grid = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append("F")
            grid.append(row)
        return grid

    def get_forty_two_positions(
        self,
    ) -> set[tuple[int, int]]:
        """Checks all the positions for the 42 logo in the maze and None
        if the maze is too small

        Returns:
            set[tuple[int, int]]: all the positions of the logo in the maze
        """
        center_row = self.height // 2
        center_col = self.width // 2
        positions: list[tuple[int, int]] = []
        if self.width <= 8 or self.height <= 6:
            return set(positions)
        for i in range(3, 0, -1):
            positions.extend(
                [
                    (center_row - i + 1, center_col - 3),
                    (center_row - i + 1, center_col + 3),
                    (center_row + i - 1, center_col - 1),
                    (center_row + i - 1, center_col + 1),
                    (center_row, center_col - i),
                    (center_row, center_col + i),
                    (center_row + 2, center_col + i),
                    (center_row - 2, center_col + i),
                ]
            )
        return set(positions)

    def generate_maze(self, seed: int | None = None) -> list[list[str]]:
        """Generate the maze

        Args:
            seed (int | None, optional): The seed provided to generate maze.
            Defaults to None.

        Returns:
            list[list[str]]: le maze created
        """
        self.maze = self.generate_grid()
        positions = self.get_forty_two_positions()
        for pos in positions:
            self.maze[pos[0]][pos[1]] = "42"
        generator = HuntAndKill(
            (self.width, self.height),
            self.maze,
            positions,
            seed=seed,
            perfect=self.perfect
            )
        generator.run()
        for pos in self.get_forty_two_positions():
            self.maze[pos[0]][pos[1]] = "F"
        return self.maze
