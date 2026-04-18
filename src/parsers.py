"""Module that contain a basic parser that convert a string into a value."""


class Parser:
    """Basic parsers that use to convert string into an appropriated type.

    Raises:
        ValueError: If the string cannot be converted into the expected type
    """

    @staticmethod
    def parse_bool(value: str) -> bool:
        """Translate a string into a boolean.

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

    @staticmethod
    def parse_point(value: str) -> tuple[int, int]:
        """Take a tuple like string and return its cast value into tuple.

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
            x_str, y_str = cleaned[1:-1].split(",")
        return int(x_str.strip()), int(y_str.strip())
