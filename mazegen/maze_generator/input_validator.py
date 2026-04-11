from typing import TypedDict


class MazeConfig(TypedDict):
    WIDTH: int
    HEIGHT: int
    PERFECT: bool
    SEED: int


def validate_size(height: int, width: int) -> None:
    """Check the size if it is too big or negative

    Args:
        height (int): the height of the maze
        width (int): the width of the maze

    Raises:
        ValueError: If the size if invalid
    """
    if isinstance(height, int):
        if 0 >= height:
            raise ValueError(
                f"Height {height} can't be negative or 0"
                )
        if 500 < height:
            raise ValueError(
                f"Height {height} can't be too high "
                + "(Generation too long)"
            )
    else:
        raise ValueError("Invalid height value")

    if isinstance(width, int):
        if 0 >= width:
            raise ValueError(
                f"Width {width} can't be negative or 0"
                )
        if 500 < width:
            raise ValueError(
                f"Width {width} can't be too high "
                + "(Generation too long)"
            )
    else:
        raise ValueError("Invalid width value")


def validate_perfect(perfect: bool) -> None:
    """Check if the perfect parameters is a boolean

    Args:
        perfect (bool): The perfect config of the maze

    Raises:
        ValueError: If the parameters is not a boolean
    """
    if isinstance(perfect, bool):
        pass
    else:
        raise ValueError("Invalid perfect value")


def validate_seed(seed: int | None) -> None:
    """Check if the seed parameter is an integer

    Args:
        seed (int): The seed of the maze

    Raises:
        ValueError: If the seed is not an integer
    """
    if isinstance(seed, int) or seed is None:
        pass
    else:
        raise ValueError("Invalid seed value")
