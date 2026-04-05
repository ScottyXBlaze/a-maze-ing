from pathlib import Path
from typing import TypedDict, TypeGuard

REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
    "SEED",
    "ANIMATION"
}


class MazeConfig(TypedDict):
    """General config type hint

    Args:
        TypedDict (class): Base class for hinting with dict
    """
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int
    ANIMATION: bool


class PartialMazeConfig(TypedDict, total=False):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int
    ANIMATION: bool


DEFAULT_CONFIG: MazeConfig = {
    "WIDTH": 20,
    "HEIGHT": 20,
    "ENTRY": (0, 0),
    "EXIT": (19, 19),
    "OUTPUT_FILE": "maze_output.txt",
    "PERFECT": True,
    "SEED": 42,
    "ANIMATION": True
}


def parse_bool(value: str) -> bool:
    """Translate a string into a boolean

    Args:
        value (str): string like TRUE, 1, YES, Y

    Raises:
        ValueError: if the string cannot be translated into a boolean

    Returns:
        bool: the translated value of the string
    """
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def parse_point(value: str) -> tuple[int, int]:
    """Take a tuple like string and return its casted value into tuple

    Args:
        value (str): the tuple in string we want to convert

    Raises:
        ValueError: if the format is not like (x, y)

    Returns:
        tuple[int, int]: the tuple in (x, y) form
    """
    cleaned = value.strip()
    if not (cleaned.startswith("(") and cleaned.endswith(")")):
        x_str, y_str = cleaned.split(",")
    else:
        x_str, y_str = cleaned[1:-1:1].split(",")
    return int(x_str.strip()), int(y_str.strip())


def parse_line(
        line: str,
        config: PartialMazeConfig
        ) -> None:
    """Take all the string to convert them into key/value with a dictionnary

    Args:
        line (str): the string we want to convert
        config (MazeConfig): the dictionary we want to put the config

    Raises:
        ValueError: if the format is invalid (no '=')
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
        config["ENTRY"] = parse_point(raw_value)
    elif key == "EXIT":
        config["EXIT"] = parse_point(raw_value)
    elif key == "OUTPUT_FILE":
        config["OUTPUT_FILE"] = raw_value
    elif key == "PERFECT":
        config["PERFECT"] = parse_bool(raw_value)
    elif key == "ANIMATION":
        config["ANIMATION"] = parse_bool(raw_value)
    else:
        raise ValueError(f"Unrecognized config key: {key}")


def get_forty_two_positions(
        width: int, height: int
        ) -> tuple[tuple[int, int], ...]:
    center_y = width // 2
    center_x = height // 2
    positions: list[tuple[int, int]] = []
    if width <= 8 or height <= 6:
        return tuple(positions)
    for i in range(3, 0, -1):
        positions.extend(
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


def validate_config(config: MazeConfig) -> None:
    if not (0 < config["WIDTH"] <= 100):
        raise ValueError(f"Invalid config value for WIDTH: {config['WIDTH']}")
    if not (0 < config["HEIGHT"] <= 50):
        raise ValueError(
            f"Invalid config value for HEIGHT: {config['HEIGHT']}"
            )
    if not (
        0 <= config["ENTRY"][0] < config["WIDTH"]
        and 0 <= config["ENTRY"][1] < config["HEIGHT"]
    ):
        raise ValueError(f"Invalid config value for ENTRY: {config['ENTRY']}")
    if not (
        0 <= config["EXIT"][0] < config["WIDTH"]
        and 0 <= config["EXIT"][1] < config["HEIGHT"]
    ):
        raise ValueError(f"Invalid config value for EXIT: {config['EXIT']}")
    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("Invalid config: ENTRY and EXIT cannot be the same")
    for pos in get_forty_two_positions(config["WIDTH"], config["HEIGHT"]):
        # pos is (row, col), convert to (x, y) for comparison
        pos_xy = (pos[1], pos[0])
        if pos_xy == config["ENTRY"] or pos_xy == config["EXIT"]:
            raise ValueError(
                f"Invalid config: ENTRY and EXIT cannot be at position \
{pos_xy} reserved for '42'"
            )


def is_complete_config(config: PartialMazeConfig) -> TypeGuard[MazeConfig]:
    return all(key in config for key in REQUIRED_KEYS)


def check_missing(config: PartialMazeConfig) -> MazeConfig:
    missing = REQUIRED_KEYS - set(config)
    if missing:
        missing_keys = ", ".join(sorted(missing))
        raise ValueError(f"Missing required config keys: {missing_keys}")
    if not is_complete_config(config):
        # Defensive guard for static typing.
        raise ValueError("Invalid config structure")
    validate_config(config)
    return config


def load_config(path: str) -> MazeConfig:
    config_path = Path(path)
    config: PartialMazeConfig = {}

    with config_path.open("r") as file:
        for line in file:
            try:
                parse_line(line, config)
            except ValueError as e:
                print(f"Error parsing line: {line.strip()}")
                print(f"Reason: {e}")
                print("Using default value...")
                return DEFAULT_CONFIG
    try:
        return check_missing(config)
    except ValueError as e:
        print("Error validating config:", config)
        print(f"ERROR: {e}")
        print("Using default value...")
        return DEFAULT_CONFIG
