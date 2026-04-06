import abc
from typing import Any


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.name = ""
        self._data: list[Any] = []
        self._output_value = 0
        self.total_data = 0

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        return True

    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        try:
            value = self._data.pop(0)
            self._output_value += 1
            return (self._output_value - 1, value)
        except IndexError:
            raise Exception("No data left in the processor")


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Numeric Processor"

    def _validate_one(self, data: Any) -> bool:
        return isinstance(data, float | int)

    def _validate_list(self, data: list[Any]) -> bool:
        if isinstance(data, list):
            for num in data:
                if not self._validate_one(num):
                    return False
            return True
        else:
            return False

    def validate(self, data: Any) -> bool:
        if not self._validate_one(data):
            if not self._validate_list(data):
                return False
            else:
                return True
        return True

    def ingest(self, data: list[int | float] | int | float) -> None:
        if self._validate_one(data):
            self._data.append(str(data))
            self.total_data += 1
        elif isinstance(data, list) and self._validate_list(data):
            for num in data:
                self._data.append(str(num))
                self.total_data += 1
        else:
            raise Exception("Invalid numeric data")


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Text Processor"

    def _validate_one(self, data: Any) -> bool:
        return isinstance(data, str)

    def _validate_list(self, data: Any) -> bool:
        if isinstance(data, list):
            for num in data:
                if not self._validate_one(num):
                    return False
            return True
        else:
            return False

    def validate(self, data: Any) -> bool:
        if not self._validate_one(data):
            if self._validate_list(data):
                return True
            else:
                return False
        else:
            return True

    def ingest(self, data: str | list[str]) -> None:
        if self._validate_one(data):
            self._data.append(data)
            self.total_data += 1
        elif self._validate_list(data):
            for num in data:
                self._data.append(num)
                self.total_data += 1
        else:
            raise Exception("Invalid string data")


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Log Processor"

    def _validate_one(self, data: Any) -> bool:
        if isinstance(data, dict):
            if set(data.keys()) == {"log_level", "log_message"}:
                for value in data.values():
                    if isinstance(value, str):
                        continue
                    else:
                        return False
                return True
        return False

    def _validate_list(self, data: Any) -> bool:
        if isinstance(data, list):
            for num in data:
                if not self._validate_one(num):
                    return False
            return True
        else:
            return False

    def validate(self, data: Any) -> bool:
        if not self._validate_one(data):
            if not self._validate_list(data):
                return False
            else:
                return True
        else:
            return True

    def join_values(self, level: str, message: str) -> str:
        return level + ": " + message

    def ingest(self, data: list[dict[str, str]] | dict[str, str]) -> None:
        if self._validate_list(data) and isinstance(data, list):
            for dictionnary in data:
                self._data.append(
                    self.join_values(*dictionnary.values())
                )
                self.total_data += 1
        elif self._validate_one(data) and isinstance(data, dict):
            self._data.append(
                self.join_values(*data.values())
            )
            self.total_data += 1
        else:
            raise Exception("Invalid log data")


def test_processor(
    proc: DataProcessor,
    test_validation: list[Any],
    invalid_test: list[Any],
    data: Any,
    output: int,
) -> None:
    """Test Processor

    Args:
        proc (DataProcessor): The processor you want to test
        test_validation (list[Any]): The list of validation test
          you want to make
        invalid_test (list[Any]): if you want to try to ingest invalid
          data in the processor
        data (list[Any]): The data you want to ingest in the processor
        output (int): the number of output you want to show
    """
    processor = None
    if isinstance(proc, DataProcessor):
        processor = proc
    else:
        print("Invalid Processor, try again :<")
        return

    if not isinstance(test_validation, list):
        print("Invalid test is not a list: try again :<")
        return

    for test in test_validation:
        print(
            f" Trying to validate input '{test}':",
            f"{processor.validate(test)}"
        )

    if not isinstance(invalid_test, list):
        print("Invalid test is not a list: try again :<")
        return

    for test in invalid_test:
        print(
            f" Test invalid ingestion of data '{test}'",
            "without prior validation:"
        )
        try:
            processor.ingest(test)
        except Exception as e:
            print("\n === ERROR ===")
            print(f" Got exception: {e}\n")

    print(f" Processing data: {data}")
    try:
        processor.ingest(data)
    except Exception as e:
        print("\n === ERROR ===")
        print(f" Caught Exception: {e}\n")

    if not isinstance(output, int) or output < 0:
        print("Invalid number of output. Try again :<")
        return
    print(f" Extracting {output} values...")
    for _ in range(output):
        try:
            index, value = proc.output()
            print(f" Numeric value {index}: {value}")
        except Exception as e:
            print(f"Caught Error: {e}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    test_processor(
        NumericProcessor(),
        [42, "hello", [10, 11]],
        ["foo"],
        [1.0, 2, 3, 4, 5],
        3
    )
    print("\nTesting Text Processor...")
    test_processor(
        TextProcessor(),
        [42, "hello", ["answer", "yeah"]],
        [42],
        ["Hello", "Nexus", "World"],
        2,
    )
    print("\nTesting Log Processor...")
    test_processor(
        LogProcessor(),
        ["Hello"],
        ["hey"],
        [
            {"log_level": "NOTICE", "log_message": "Connection to server"},
            {"log_level": "ERROR", "log_message": "Unauthorized acess!!"},
            {"log_level": "WARNING", "log_message": "The API is out of date!"},
        ],
        2,
    )
