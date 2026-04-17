from pathlib import Path
from typing import TypedDict, TypeGuard
from .parsers import Parser


class InputParser:
    """Basic Input parsers for the maze generator, it is used to parse the
    config file and check if all the config are valid, it also contains
    some useful function to check edge cases and to get the position of the
    '42' pattern in the maze

    Raises:
        ValueError: If the config file is invalid or if there is a missing key
    """
    class PartialMazeConfig(TypedDict, total=False):

        WIDTH: int
        HEIGHT: int
        ENTRY: tuple[int, int]
        EXIT: tuple[int, int]
        OUTPUT_FILE: str
        PERFECT: bool
        SEED: int
        ANIMATION: bool
        ALGO: str

    class MazeConfig(TypedDict):
        """General config type hint
        """

        WIDTH: int
        HEIGHT: int
        ENTRY: tuple[int, int]
        EXIT: tuple[int, int]
        OUTPUT_FILE: str
        PERFECT: bool
        SEED: int
        ANIMATION: bool
        ALGO: str

    def __init__(self) -> None:
        """Everything start here
        """

        self.parsers = Parser()

        self.required_keys = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "SEED",
            "ANIMATION",
            "ALGO",
        }

        self.default_config: InputParser.MazeConfig = {
            "WIDTH": 20,
            "HEIGHT": 20,
            "ENTRY": (0, 0),
            "EXIT": (19, 19),
            "OUTPUT_FILE": "maze_output.txt",
            "PERFECT": True,
            "SEED": 42,
            "ANIMATION": True,
            "ALGO": "AUTO",
        }

    def set_algo(self, algo_name: str) -> None:
        """Set the algorithm to use for solving the maze"""
        if algo_name.upper() in {"DFS", "BFS", "ASTAR", "AUTO"}:
            self.default_config["ALGO"] = algo_name.upper()

    def parse_line(self, line: str, config: PartialMazeConfig) -> None:
        """Check each line and convert them with the available parsers

        Args:
            line (str): The line of the key-value to parse
            config (PartialMazeConfig): the config class

        Raises:
            ValueError: If there is not '=' in the line
            ValueError: if the key is unrecognized
        """
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            return

        if "=" not in stripped:
            raise ValueError(f"Invalid config line (missing '='): {stripped}")

        key, raw_value = (part.strip() for part in stripped.split("=", 1))

        if key == "WIDTH":
            config["WIDTH"] = int(raw_value)
        elif key == "HEIGHT":
            config["HEIGHT"] = int(raw_value)
        elif key == "SEED":
            config["SEED"] = int(raw_value)
        elif key == "ENTRY":
            config["ENTRY"] = self.parsers.parse_point(raw_value)
        elif key == "EXIT":
            config["EXIT"] = self.parsers.parse_point(raw_value)
        elif key == "OUTPUT_FILE":
            config["OUTPUT_FILE"] = raw_value
        elif key == "PERFECT":
            config["PERFECT"] = self.parsers.parse_bool(raw_value)
        elif key == "ANIMATION":
            config["ANIMATION"] = self.parsers.parse_bool(raw_value)
        elif key == "ALGO":
            config["ALGO"] = raw_value.upper()
        else:
            raise ValueError(f"Unrecognized config key: {key}")

    @staticmethod
    def get_forty_two_positions(
        width: int, height: int
    ) -> tuple[tuple[int, int], ...]:
        """Get all the position of the 42 logo in the maze if there is one

        Args:
            width (int): the width of the maze
            height (int): the height of the maze

        Returns:
            tuple[tuple[int, int], ...]: The list of the position of the 42
            logo in the maze, empty if there is no 42 logo
        """
        center_y = width // 2
        center_x = height // 2
        positions: set[tuple[int, int]] = set()
        if width <= 8 or height <= 6:
            return tuple(positions)
        for i in range(3, 0, -1):
            positions.update(
                [
                    (center_x - i + 1, center_y - 3),
                    (center_x - i + 1, center_y + 3),
                    (center_x + i - 1, center_y - 1),
                    (center_x + i - 1, center_y + 1),
                    (center_x, center_y - i),
                    (center_x, center_y + i),
                    (center_x + 2, center_y + i),
                    (center_x - 2, center_y + i),
                ]
            )
        return tuple(positions)

    def validate_config(self, config: MazeConfig) -> None:
        """Validate every setting in the config

        Args:
            config (MazeConfig): The dict that has all the settings

        Raises:
            ValueError: If any of the settings is invalid
        """
        if not (0 < config["WIDTH"] <= 300):
            raise ValueError(
                f"Invalid config value for WIDTH: {config['WIDTH']}"
                )
        if not (0 < config["HEIGHT"] <= 150):
            raise ValueError(
                f"Invalid config value for HEIGHT: {config['HEIGHT']}"
                )
        if not (
            0 <= config["ENTRY"][0] < config["WIDTH"]
            and 0 <= config["ENTRY"][1] < config["HEIGHT"]
        ):
            raise ValueError(
                f"Invalid config value for ENTRY: {config['ENTRY']}"
                )
        if not (
            0 <= config["EXIT"][0] < config["WIDTH"]
            and 0 <= config["EXIT"][1] < config["HEIGHT"]
        ):
            raise ValueError(
                f"Invalid config value for EXIT: {config['EXIT']}"
                )
        if config["ENTRY"] == config["EXIT"]:
            raise ValueError(
                "Invalid config: ENTRY and EXIT cannot be the same"
                )

        if config["WIDTH"] <= 8 or config["HEIGHT"] <= 6:
            print("=== WARNING! ===")
            print(
                "The maze is too small to include the '42' pattern.",
                "ENTRY and EXIT can be anywhere."
                )
        for pos in self.get_forty_two_positions(
                config["WIDTH"], config["HEIGHT"]):
            pos_xy = (pos[1], pos[0])
            if pos_xy == config["ENTRY"] or pos_xy == config["EXIT"]:
                raise ValueError(
                    f"Invalid config: ENTRY and EXIT cannot be at position \
    {pos_xy} reserved for '42'"
                )

    def is_complete_config(
            self, config: PartialMazeConfig
            ) -> TypeGuard[MazeConfig]:
        """Check if every config is in the dictionary

        Args:
            config (PartialMazeConfig): The dictionary of the config

        Returns:
            TypeGuard[MazeConfig]: boolean that indicate if the config is
              complete or not
        """
        return all(key in config for key in self.required_keys)

    def check_missing(self, config: PartialMazeConfig) -> MazeConfig:
        """Check if all the config are in the dictionary

        Args:
            config (PartialMazeConfig): The dictionary of the config

        Raises:
            ValueError: If any required config key is missing
            ValueError: If the config structure is invalid

        Returns:
            MazeConfig: The complete maze configuration
        """
        missing = self.required_keys - set(config)
        if missing:
            missing_keys = ", ".join(sorted(missing))
            raise ValueError(f"Missing required config keys: {missing_keys}")
        if not self.is_complete_config(config):
            raise ValueError("Invalid config structure")
        self.validate_config(config)
        return config

    def load_config(self, path: str) -> MazeConfig:
        """Load the configuration in the path

        Args:
            path (str): The path of the file we want to load the config from

        Returns:
            MazeConfig: The complete maze configuration, set as default
              if there is an error
        """
        config_path = Path(path)
        config: InputParser.PartialMazeConfig = {}

        with config_path.open("r") as file:
            for line in file:
                try:
                    self.parse_line(line, config)
                except ValueError as e:
                    print(f"Error parsing line: {line.strip()}")
                    print(f"Reason: {e}")
                    print("Using default value...")
                    return self.default_config
        try:
            return self.check_missing(config)
        except ValueError as e:
            print("Error validating config:", config)
            print(f"ERROR: {e}")
            print("Using default value...")
            return self.default_config
