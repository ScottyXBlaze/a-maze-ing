import random
import sys
from typing import Any
from multiprocessing import Process

try:
    import mlx
except ImportError:
    print("Error: mlx is not installed yet")
    print("Please type 'make re'")
    sys.exit(1)

try:
    from mazegen import MazeGenerator
    from src import InputParser, DFSSolver, BFSSolver, AStarSolver, BaseSolver
except ImportError as e:
    print(f"Error: {e.name} can't be imported")
    print("Please Verify your file")
    sys.exit(1)


def rgba(r: int, g: int, b: int, a: int = 255) -> int:
    """Convert rgba format into an integer (#ffffffff format)

    Args:
        r (int): red
        g (int): green
        b (int): blue
        a (int, optional): opacity. Defaults to 255.

    Returns:
        int: The transformed rgba color
    """
    return (a << 24) | (r << 16) | (g << 8) | b


class Main:
    """The main program"""

    def __init__(self) -> None:
        """Every Initialization starts here"""

        self.config: InputParser.MazeConfig = self.get_input()

        self.cell_size = 19

        self.color_choices = [
            (rgba(236, 102, 102), rgba(137, 169, 238), rgba(255, 255, 255)),
            (rgba(255, 111, 105), rgba(222, 248, 255), rgba(127, 229, 186)),
            (rgba(44, 43, 72), rgba(25, 41, 156), rgba(32, 43, 122)),
            (rgba(107, 170, 117), rgba(203, 255, 77), rgba(179, 57, 81)),
            (rgba(222, 165, 197), rgba(241, 136, 140), rgba(249, 209, 220)),
        ]
        self.color_choice = random.choice(self.color_choices)

        self.showed_path = 0

        self.m: Any = mlx.Mlx()

        self.maze_generator = MazeGenerator(
            (self.config["WIDTH"], self.config["HEIGHT"]),
            perfect=self.config["PERFECT"],
        )
        self.maze: list[list[str]] = self.maze_generator.generate_maze(
            seed=self.config["SEED"]
        )

        self.maze_solver = self.get_algorithm()

        self.mlx_ptr: Any = self.m.mlx_init()
        self.width, self.height = self.get_window_size()
        self.win_mlx: Any = self.m.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "A-Maze-Ing!"
        )

    def get_algorithm(self) -> BaseSolver:
        """Get the algorithm from the settings

        Returns:
            BaseSolver: The class of the solver
        """
        entry = (
            self.config["ENTRY"][1],
            self.config["ENTRY"][0]
        )
        exit = (
            self.config["EXIT"][1],
            self.config["EXIT"][0]
        )
        if self.config["ALGO"] == "DFS":
            return DFSSolver(
                self.maze,
                entry,
                exit
            )
        elif self.config["ALGO"] == "BFS":
            return BFSSolver(
                self.maze,
                entry,
                exit
            )
        elif self.config["ALGO"] == "ASTAR":
            return AStarSolver(
                self.maze,
                entry,
                exit
            )
        else:
            return AStarSolver(
                self.maze,
                entry,
                exit
            )

    def get_window_size(self) -> tuple[int, int]:
        """Return the best size of the window

        Returns:
            tuple[int, int]: The width and height of the window
        """
        width = self.config["WIDTH"] * self.cell_size + 2
        height = self.config["HEIGHT"] * self.cell_size + 2
        return (width, height)

    def show_help(self) -> None:
        """Show help message
        """
        print("------------------------------------")
        print("=== Welcome to the world of maze ===")
        print("------------------------------------")
        print("      <<< Instruction: >>>")
        print("S - Show/Hide path")
        print("G - Generate new maze")
        print("O - Write the output in a file")
        print("C - Change the color of the maze")
        print("A - Toggle animation")
        print("------------------------------------")

    def draw(
        self,
        nbr_str: str,
        pos: tuple[int, int],
        color: int = rgba(255, 255, 255)
    ) -> None:
        """Draw a cell on the window

        Args:
            nbr (str): the number in hexa to be printed
            pos (tuple[int, int]): the position of the cell
            color (int, optional): the color of the cell
        """
        nbr: int = int(nbr_str, 16)
        i = 0
        while (nbr >> i) != 0:
            if ((nbr >> i) & 1) == 1:
                if i == 0:
                    for x in range(pos[0], pos[0] + self.cell_size):
                        self.m.mlx_pixel_put(
                            self.mlx_ptr, self.win_mlx, x, pos[1], color
                        )
                if i == 1:
                    for y in range(pos[1], pos[1] + self.cell_size):
                        self.m.mlx_pixel_put(
                            self.mlx_ptr,
                            self.win_mlx,
                            pos[0] + self.cell_size,
                            y,
                            color,
                        )
                if i == 2:
                    for x in range(pos[0], pos[0] + self.cell_size):
                        self.m.mlx_pixel_put(
                            self.mlx_ptr,
                            self.win_mlx,
                            x,
                            pos[1] + self.cell_size,
                            color,
                        )
                if i == 3:
                    for y in range(pos[1], pos[1] + self.cell_size):
                        self.m.mlx_pixel_put(
                            self.mlx_ptr, self.win_mlx, pos[0], y, color
                        )
            i += 1

    def get_input(self) -> InputParser.MazeConfig:
        """Get the input from the config file

        Returns:
            dict: the dictionary that contains every settings
        """
        if len(sys.argv) != 2:
            print("Error: Missing config file argument.")
            print("Usage: python a_maze_ing.py <config_file>")
            sys.exit(1)
        else:
            self.show_help()
            self.input_parsers = InputParser()
            return (self.input_parsers.load_config(sys.argv[1]))

    def draw_cells(self, maze: list[list[str]], color: int) -> None:
        """Draw every cell on the window

        Args:
            maze (list): the maze you want to draw
        """
        pos: list[int] = [0, 0]
        tmp_pos = (pos[0], pos[1])
        for row in maze:
            for colons in row:
                self.draw(colons, tmp_pos, color)
                pos[0] += self.cell_size
                tmp_pos = (pos[0], pos[1])

            pos[0] = 0
            pos[1] += self.cell_size
            tmp_pos = (pos[0], pos[1])
        for logo_pos in self.maze_generator.get_forty_two_positions():
            self.color_cell(
                (logo_pos[1] * self.cell_size, logo_pos[0] * self.cell_size),
                self.color_choice[1],
            )
        self.color_cell(
            (
                self.config["ENTRY"][0] * self.cell_size,
                self.config["ENTRY"][1] * self.cell_size,
            ),
            rgba(0, 0, 255),
        )
        self.color_cell(
            (
                self.config["EXIT"][0] * self.cell_size,
                self.config["EXIT"][1] * self.cell_size,
            ),
            rgba(255, 0, 255),
        )

    def draw_path(self, path: str, color: int, animation: bool = True) -> None:
        """Draw the path on the window

        Args:
            path (str): the path you want to follow
        """
        x = self.config["ENTRY"][0] * self.cell_size
        y = self.config["ENTRY"][1] * self.cell_size
        path_color: int = color
        line_thickness: int = 2

        start_center: tuple[int, int] = self.cell_center((x, y))
        self.draw_thick_segment(
            start_center, start_center, path_color, line_thickness
        )

        for direction in path:
            old_pos: tuple[int, int] = (x, y)
            if direction == "N":
                y -= self.cell_size
            elif direction == "E":
                x += self.cell_size
            elif direction == "S":
                y += self.cell_size
            elif direction == "W":
                x -= self.cell_size
            else:
                continue
            self.draw_thick_segment(
                self.cell_center(old_pos),
                self.cell_center((x, y)),
                path_color,
                line_thickness,
            )
            if self.config["ANIMATION"] and animation:
                self.m.mlx_do_sync(self.mlx_ptr)

    def cell_center(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Calculate the center of the maze

        Args:
            pos (tuple[int, int]): the position of the cell in the grid

        Returns:
            tuple[int, int]: the position of the center on the window
        """
        return (
            pos[0] + (self.cell_size // 2),
            pos[1] + (self.cell_size // 2),
        )

    def get_colors(self) -> list[tuple[int, int, int]]:
        """Return The list of color in the maze

        Returns:
            list[tuple[int, int, int]]: list of 3 color each
        """
        return [
            (rgba(236, 102, 102), rgba(137, 169, 238), rgba(255, 255, 255)),
            (rgba(255, 111, 105), rgba(222, 248, 255), rgba(127, 229, 186)),
            (rgba(44, 43, 72), rgba(25, 41, 156), rgba(32, 43, 122)),
            (rgba(107, 170, 117), rgba(203, 255, 77), rgba(179, 57, 81)),
            (rgba(222, 165, 197), rgba(241, 136, 140), rgba(249, 209, 220)),
        ]

    def draw_thick_segment(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: int,
        thickness: int
    ) -> None:
        """Draw line in the window

        Args:
            start (tuple[int, int]): The starting point of the maze
            end (tuple[int, int]): The ending point of the maze
            color (int): The color of the line
            thickness (int): The thickness of the line
        """
        x1, y1 = start
        x2, y2 = end
        half = thickness // 2
        if x1 == x2:
            y_min, y_max = sorted((y1, y2))
            for x in range(x1 - half, x1 + half + 1):
                for y in range(y_min, y_max + 1):
                    self.m.mlx_pixel_put(
                        self.mlx_ptr, self.win_mlx, x, y, color
                    )
        elif y1 == y2:
            x_min, x_max = sorted((x1, x2))
            for x in range(x_min, x_max + 1):
                for y in range(y1 - half, y1 + half + 1):
                    self.m.mlx_pixel_put(
                        self.mlx_ptr, self.win_mlx, x, y, color
                    )
        self.m.mlx_hook(self.win_mlx, 33, 0, self.exit_window, None)

    def color_cell(self, pos: tuple[int, int], color: int) -> None:
        """Color a cells

        Args:
            pos (tuple[int, int]): The position of the cell
            color (int): The color of the cell in rgba format
        """
        for x in range(
            pos[0] + 2,
            pos[0] + self.cell_size - 2,
        ):
            for y in range(
                pos[1] + 2,
                pos[1] + self.cell_size - 2,
            ):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_mlx, x, y, color)

    def get_maze_output(self, file_path: str | None = None) -> None:
        """Give the output of the program in a file

        Args:
            file_path (str | None, optional): The path of the output we want.
              Defaults to None.
        """
        maze = ""
        path = self.maze_solver.solve_as_string()
        for row in self.maze:
            for cell in row:
                maze += cell
            maze += "\n"
        entry = (
            str(self.config["ENTRY"][0]) + "," + str(self.config["ENTRY"][1])
        )
        exit = str(self.config["EXIT"][0]) + "," + str(self.config["EXIT"][1])
        with open(file_path or "maze.txt", "w") as f:
            f.write(maze)
            f.write("\n")
            f.write(entry)
            f.write("\n")
            f.write(exit)
            f.write("\n")
            f.write(path if path is not None else "No solution")

    def exit_window(self, _: object) -> None:
        """Exit the window

        Args:
            _ (object): Nothing (just to avoid error with mlx)
        """
        self.m.mlx_loop_exit(self.mlx_ptr)

    def new_maze(self) -> None:
        """Generate a new maze and show it in the window
        """
        self.maze = self.maze_generator.generate_maze()
        self.maze_solver.set_new_maze(self.maze)
        self.m.mlx_clear_window(self.mlx_ptr, self.win_mlx)
        self.draw_cells(self.maze, self.color_choice[0])
        if self.showed_path:
            path = self.maze_solver.solve_as_string()
            self.draw_path(path, self.color_choice[2])

    def hide_path(self) -> None:
        """Hide the path in the window
        """
        self.m.mlx_clear_window(self.mlx_ptr, self.win_mlx)
        self.draw_cells(self.maze, self.color_choice[0])

    def give_output_file(self) -> None:
        """Give the output file with the OUTPUT_FILE in the config
        """
        self.get_maze_output(self.config["OUTPUT_FILE"])

    def change_color(self) -> None:
        """Change the color of the cell and path
        """
        if not self.color_choices:
            self.color_choices = self.get_colors()

        self.color_choice = random.choice(self.color_choices)
        self.color_choices.remove(self.color_choice)

        self.m.mlx_clear_window(self.mlx_ptr, self.win_mlx)
        self.draw_cells(self.maze, self.color_choice[0])

        if self.showed_path:
            path = self.maze_solver.solve_as_string()
            self.draw_path(path, self.color_choice[2], animation=False)

    def toggle_animation(self) -> None:
        """Toggle animation with on and off
        """
        if self.config["ANIMATION"]:
            self.config["ANIMATION"] = False
            print("Animation Turned off!")
        else:
            self.config["ANIMATION"] = True
            print("Animation Turned on!")

    def key_pressed(self, keynum: int, _: object) -> None:
        """Handle key pressed by the users

        Args:
            keynum (int): the X11 key the user pressed
            _ (object): Just to avoid error with mlx
        """
        if keynum == 103:
            self.new_maze()
        elif keynum == 115:
            if not self.showed_path:
                path = self.maze_solver.solve_as_string()
                self.draw_path(path, self.color_choice[2])
                self.showed_path = 1
            else:
                self.hide_path()
                self.showed_path = 0
        elif keynum == 113:
            self.exit_window(_)
        elif keynum == 111:
            self.give_output_file()
        elif keynum == 99:
            self.change_color()
        elif keynum == 97:
            self.toggle_animation()

    def run(self) -> None:
        """Run the program
        """
        self.draw_cells(self.maze, self.color_choice[0])
        self.m.mlx_hook(self.win_mlx, 33, 0, self.exit_window, None)
        self.m.mlx_key_hook(self.win_mlx, self.key_pressed, None)
        self.m.mlx_loop(self.mlx_ptr)


def main() -> None:
    """The main program
    """
    main = Main()
    main.run()


if __name__ == "__main__":
    p = Process(target=main)
    try:
        p.start()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
        print("\n=== Exiting... ===")
