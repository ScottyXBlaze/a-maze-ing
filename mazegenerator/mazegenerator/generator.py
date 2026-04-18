"""Maze generator that contains The main class MazeGenerator.

Raises:
    ValueError: If Invalid parameters is given
"""

from .huntandkill import HuntAndKill


class MazeGenerator:
    """Maze Generator class to generate maze."""

    def __init__(self, size: tuple[int, int], perfect: bool = True) -> None:
        """Init all the config of the maze.

        Args:
            size (tuple[int, int]): the size of the maze
            perfect (bool, optional): True to have only one path.
        """
        if not self.validate_size(size):
            raise ValueError(
                "[Error] Invalid size for the maze (negative or too big)"
            )
        self._width = size[0]
        self._height = size[1]

        self._maze = self.generate_grid()

        self._perfect = perfect

    @staticmethod
    def validate_size(size: tuple[int, int]) -> bool:
        """Check if the maze can be generated properly.

        Args:
            size (tuple[int, int]): The size of the maze (width, height)

        Returns:
            bool: True if the maze can be generated
        """
        try:
            return 0 < size[0] <= 500 and 0 < size[1] <= 500
        except TypeError as e:
            print(f"Error: {e}")
            return False

    def toggle_perfect(self) -> None:
        """Toggle generation perfection."""
        self._perfect = not self._perfect

    def generate_grid(self) -> list[list[str]]:
        """Generate a grid full of walls 'F'.

        Returns:
            list[list[str]]: grid in 2D
        """
        grid: list[list[str]] = []
        for _ in range(self._height):
            row: list[str] = []
            for _ in range(self._width):
                row.append("F")
            grid.append(row)
        return grid

    def get_forty_two_positions(
        self,
    ) -> set[tuple[int, int]]:
        """Check all the positions for the 42 logo in the maze.

        Returns:
            set[tuple[int, int]]: all the positions of the logo in the maze
             None if the logo doesn't fit
        """
        center_row: int = self._height // 2
        center_col: int = self._width // 2
        positions: list[tuple[int, int]] = []
        if self._width <= 8 or self._height <= 6:
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
        """Generate the maze.

        Args:
            seed (int | None, optional): The seed provided to generate maze.
            Defaults to None.

        Returns:
            list[list[str]]: le maze created
        """
        self._maze = self.generate_grid()
        positions: set[tuple[int, int]] = self.get_forty_two_positions()
        for pos in positions:
            self._maze[pos[0]][pos[1]] = "42"
        generator = HuntAndKill(
            (self._width, self._height),
            self._maze,
            positions,
            seed=seed,
            perfect=self._perfect,
        )
        generator.run()
        for pos in self.get_forty_two_positions():
            self._maze[pos[0]][pos[1]] = "F"
        return self._maze
