import random
import sys
from typing import Any
import multiprocessing

try:
    import mlx
except ImportError as e:
    print(f"[Error] {e}")
    print("Install it manually or use make instead")
    sys.exit(1)

try:
    from mazegenerator import MazeGenerator
except ImportError as e:
    print(f"[Error] {e}")
    print(
        "Make sure to have the 'mazegen' file in the root"
        + " or install the package as is"
    )
    sys.exit(1)

try:
    from src import InputParser, DFSSolver, BFSSolver, AStarSolver, BaseSolver
except ImportError as e:
    print(f"[Error] importing utils from 'src/': {e}")
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


class ImgData:
    def __init__(self) -> None:
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0
        self.bpp = 0
        self.iformat = 0


class Main:
    """The main program"""

    def __init__(self) -> None:
        """Every Initialisation starts here"""

        self.config: InputParser.MazeConfig = self.get_input()

        self.color_choices = self.get_colors()

        self.color_choice = random.choice(self.color_choices)

        self.showed_path = 0
        self.showed_visited = 0

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
        self.cell_size, self.width, self.height = self.get_window_size()
        self.win_mlx: Any = self.m.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "A-Maze-Ing!"
        )

        self.backgrounds = self.init_background()
        self.background = self.backgrounds.get(self.color_choice[4], ImgData())

    def init_background(self) -> dict[str, ImgData]:
        backgrounds: dict[str, ImgData] = {}
        for color in self.get_colors():
            backgrounds.update({color[4]: self.set_background(color[4])})
        return backgrounds

    def set_background(self, name: str) -> ImgData:
        background = ImgData()
        path: str = "src/image/" + name + ".xpm"
        tmp = self.m.mlx_xpm_file_to_image(self.mlx_ptr, path)
        if not tmp:
            print("Cannot import background")
            sys.exit(1)
        background.img, background.width, background.height = tmp
        (
            background.data,
            background.bpp,
            background.sl,
            background.iformat,
        ) = self.m.mlx_get_data_addr(background.img)
        return background

    def draw_background(self) -> None:
        for i in range(0, self.width, 512):
            for j in range(0, self.height, 512):
                self.m.mlx_put_image_to_window(
                    self.mlx_ptr, self.win_mlx, self.background.img, i, j
                )

    def get_algorithm(self) -> BaseSolver:
        """Get the algorithm from the settings

        Returns:
            BaseSolver: The class of the solver
        """
        entry_point: tuple[int, int] = (
            self.config["ENTRY"][1],
            self.config["ENTRY"][0],
        )
        exit_point: tuple[int, int] = (
            self.config["EXIT"][1],
            self.config["EXIT"][0],
        )
        if self.config["ALGO"] == "DFS":
            return DFSSolver(self.maze, entry_point, exit_point)
        elif self.config["ALGO"] == "BFS":
            return BFSSolver(self.maze, entry_point, exit_point)
        elif self.config["ALGO"] == "ASTAR":
            return AStarSolver(self.maze, entry_point, exit_point)
        else:
            return AStarSolver(self.maze, entry_point, exit_point)

    def get_window_size(self) -> tuple[int, int, int]:
        """Return the best size of the window

        Returns:
            tuple[int, int]: The width and height of the window
        """
        self.cell_size = 25
        width: int = self.config["WIDTH"] * self.cell_size + 2
        height: int = self.config["HEIGHT"] * self.cell_size + 2
        (_, w, h) = self.m.mlx_get_screen_size(self.mlx_ptr)
        while height > h or width > w:
            self.cell_size -= 1
            width: int = self.config["WIDTH"] * self.cell_size + 2
            height: int = self.config["HEIGHT"] * self.cell_size + 2
        return self.cell_size, width, height

    @staticmethod
    def show_help() -> None:
        """Show help message"""
        print("------------------------------------")
        print("=== Welcome to the world of maze ===")
        print("------------------------------------")
        print("      <<< Instruction: >>>")
        print("S - Show/Hide path")
        print("G - Generate new maze")
        print("O - Write the output in a file")
        print("C - Change the color of the maze")
        print("A - Toggle path animation")
        print("D - Toggle visited cell animation")
        print("------------------------------------")

    def draw(
        self,
        nbr_str: str,
        pos: tuple[int, int],
        color: int = rgba(255, 255, 255),
    ) -> None:
        """Draw a cell on the window

        Args:
            nbr_str (str): the number in hexa to be printed
            pos (tuple[int, int]): the position of the cell
            color (int, optional): the color of the cell
        """
        nbr: int = int(nbr_str, 16)
        i = 0
        while (nbr >> i) != 0:
            if ((nbr >> i) & 1) == 1:
                if i == 0:
                    for x in range(pos[0], pos[0] + self.cell_size + 2):
                        for y in range(2):
                            self.m.mlx_pixel_put(
                                self.mlx_ptr,
                                self.win_mlx,
                                x,
                                pos[1] + y,
                                color,
                            )
                if i == 1:
                    for y in range(pos[1], pos[1] + self.cell_size + 2):
                        for x in range(2):
                            self.m.mlx_pixel_put(
                                self.mlx_ptr,
                                self.win_mlx,
                                pos[0] + self.cell_size + x,
                                y,
                                color,
                            )
                if i == 2:
                    for x in range(pos[0], pos[0] + self.cell_size + 2):
                        for y in range(2):
                            self.m.mlx_pixel_put(
                                self.mlx_ptr,
                                self.win_mlx,
                                x,
                                pos[1] + self.cell_size + y,
                                color,
                            )
                if i == 3:
                    for y in range(pos[1], pos[1] + self.cell_size + 2):
                        for x in range(2):
                            self.m.mlx_pixel_put(
                                self.mlx_ptr,
                                self.win_mlx,
                                pos[0] + x,
                                y,
                                color,
                            )
            i += 1

    def get_input(self) -> InputParser.MazeConfig:
        """Get the input from the config file

        Returns:
            dict: the dictionary that contains every setting
        """
        if len(sys.argv) != 2:
            print("Error: Missing config file argument.")
            print("Usage: python a_maze_ing.py <config_file>")
            sys.exit(1)
        else:
            self.show_help()
            self.input_parsers = InputParser()
            return self.input_parsers.load_config(sys.argv[1])

    def draw_cells(self, maze: list[list[str]], color: int) -> None:
        """Draw every cell on the window

        Args:
            maze (list): the maze you want to draw
            color (int): the color of the cell
        """
        pos: list[int] = [0, 0]
        tmp_pos: tuple[int, int] = (pos[0], pos[1])
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

    def draw_path(self, path: str, color: int) -> None:
        """Draw the path on the window

        Args:
            path (str): the path you want to follow
            color (int): the color of the path
        """
        x: int = self.config["ENTRY"][0] * self.cell_size
        y: int = self.config["ENTRY"][1] * self.cell_size
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
            if self.config["ANIMATION"]:
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

    @staticmethod
    def get_colors() -> list[tuple[int, int, int, int, str]]:
        """Return The list of color in the maze

        Returns:
            list[tuple[int, int, int, int]]: list of 4 color each
        """
        # Mur                  Logo             Path

        return [
            (
                rgba(44, 43, 72),
                rgba(192, 223, 239),
                rgba(32, 43, 122),
                rgba(100, 20, 42, 50),
                "papaya_whip",
            ),
            (
                rgba(78, 110, 88),
                rgba(11, 164, 138),
                rgba(122, 223, 187),
                rgba(166, 236, 224, 50),
                "stone_brown",
            ),
            (
                rgba(143, 57, 133),
                rgba(239, 217, 206),
                rgba(37, 40, 61),
                rgba(166, 117, 161, 175),
                "rosy_taupe",
            ),
        ]

    def draw_thick_segment(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: int,
        thickness: int,
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
            pos[0] + 1,
            pos[0] + self.cell_size,
        ):
            for y in range(pos[1] + 1, pos[1] + self.cell_size):
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
        exit_point = (
            str(self.config["EXIT"][0]) + "," + str(self.config["EXIT"][1])
        )
        with open(file_path or "maze.txt", "w") as f:
            f.write(maze)
            f.write("\n")
            f.write(entry)
            f.write("\n")
            f.write(exit_point)
            f.write("\n")
            f.write(path if path is not None else "No solution")

    def exit_window(self, _: object) -> None:
        """Exit the window

        Args:
            _ (object): Nothing (just to avoid error with mlx)
        """
        self.m.mlx_loop_exit(self.mlx_ptr)

    def new_maze(self) -> None:
        """Generate a new maze and show it in the window"""
        self.maze = self.maze_generator.generate_maze()
        self.maze_solver.set_new_maze(self.maze)
        self.m.mlx_clear_window(self.mlx_ptr, self.win_mlx)
        self.draw_background()
        self.draw_cells(self.maze, self.color_choice[0])
        if self.showed_path:
            self.draw_visited_cells(self.color_choice[3])
        if self.showed_path:
            path = self.maze_solver.solve_as_string()
            self.draw_path(path, self.color_choice[2])

    def hide_path(self) -> None:
        """Hide the path in the window"""
        self.m.mlx_clear_window(self.mlx_ptr, self.win_mlx)
        self.draw_background()

        self.draw_cells(self.maze, self.color_choice[0])

    def give_output_file(self) -> None:
        """Give the output file with the OUTPUT_FILE in the config"""
        self.get_maze_output(self.config["OUTPUT_FILE"])

    def change_color(self) -> None:
        """Change the color of the cell and path"""
        if not self.color_choices:
            self.color_choices = self.get_colors()

        self.color_choice = random.choice(self.color_choices)
        self.color_choices.remove(self.color_choice)

        self.m.mlx_clear_window(self.mlx_ptr, self.win_mlx)
        self.background = self.backgrounds.get(self.color_choice[4], ImgData())

        self.draw_background()

        self.draw_cells(self.maze, self.color_choice[0])

        if self.showed_visited:
            self.draw_visited_cells(self.color_choice[3])
        if self.showed_path:
            path = self.maze_solver.solve_as_string()
            self.draw_path(path, self.color_choice[2])

    def toggle_animation(self) -> None:
        """Toggle animation with on and off"""
        self.config["ANIMATION"] = not self.config["ANIMATION"]
        print(f"Animation {"on" if self.config["ANIMATION"] else "off"}!")

    def toggle_visited_cell(self) -> None:
        self.showed_visited = not self.showed_visited
        print(
            "Visited cell animation turned "
            + f"{"on" if self.showed_visited else "off"}!"
        )

    def draw_visited_cells(self, color: int) -> None:
        visited: list[tuple[int, int]] = self.maze_solver.get_visited_cells()
        for cell in visited:
            tmp: tuple[int, int] = (
                cell[1] * self.cell_size,
                cell[0] * self.cell_size,
            )
            self.color_cell(tmp, color)
            if self.config["ANIMATION"]:
                self.m.mlx_do_sync(self.mlx_ptr)

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
                if self.showed_visited:
                    self.draw_visited_cells(self.color_choice[3])
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
        elif keynum == 100:
            self.toggle_visited_cell()

    def run(self) -> None:
        """Run the program"""
        self.draw_background()
        self.draw_cells(self.maze, self.color_choice[0])
        self.m.mlx_hook(self.win_mlx, 33, 0, self.exit_window, None)
        self.m.mlx_key_hook(self.win_mlx, self.key_pressed, None)
        self.m.mlx_loop(self.mlx_ptr)


def run() -> None:
    Main().run()


if __name__ == "__main__":
    p = multiprocessing.Process(target=run)
    try:
        p.start()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
        print("\n=== Exiting... ===")
