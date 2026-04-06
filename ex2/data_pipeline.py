import abc
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def __init__(self) -> None:
        super().__init__()

    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CSVPlugin(ExportPlugin):
    def __init__(self) -> None:
        super().__init__()

    def process_output(self, data: list[tuple[int, str]]) -> None:
        tmp = ""
        starting = True
        for output in data:
            if starting:
                tmp += output[1]
                starting = False
            else:
                tmp += "," + output[1]
        print("CSV Output:")
        print(tmp)


class JSONPlugin(ExportPlugin):
    def __init__(self) -> None:
        super().__init__()

    def process_output(self, data: list[tuple[int, str]]) -> None:
        result = {}
        for output in data:
            tmp_key = "item_" + str(output[0])
            result.update({tmp_key: output[1]})
        print("CSV Output:")
        print(result)


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            if self.validate(proc):
                self.processors.append(proc)
            else:
                print(
                    "ERROR: Processor of type",
                    f"'{type(proc).__name__}' already exist"
                )

    def validate(self, proc: DataProcessor) -> bool:
        for processor in self.processors:
            if type(proc) is type(processor):
                return False
        return True

    def insert_data(self, data: Any) -> None:
        for processor in self.processors:
            if processor.validate(data):
                processor.ingest(data)
                return
        print(f"DataStream Error - Can't process element in stream: {data}")

    def process_stream(self, stream: list[Any]) -> None:
        if isinstance(stream, list):
            for data in stream:
                self.insert_data(data)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if self.processors == []:
            print("No processor found, no data")
        for processor in self.processors:
            print(
                f"{processor.name}: Total {processor.total_data}",
                f"items proceed, remaining {len(processor._data)} on processor"
            )

    def consume_data(self, name: str) -> tuple[int, str]:
        for processor in self.processors:
            if name == processor.name:
                try:
                    return processor.output()
                except Exception as e:
                    print(f"Caught Error: {e}")
        return (-1, "")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self.processors:
            tmp = []
            for _ in range(nb):
                try:
                    tmp.append(processor.output())
                except Exception:
                    pass
            plugin.process_output(tmp)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors...\n")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]

    print(f"Send first batch of data on stream: {data}")
    stream.process_stream(data)
    print()
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVPlugin())
    print()
    stream.print_processors_stats()

    data2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash"
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days"
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {data2}")
    stream.process_stream(data2)
    print()
    stream.print_processors_stats()

    processed_num = 5
    print(
        f"\nSend {processed_num} processed",
        "data from each processor to a JSON plugin:"
    )
    stream.output_pipeline(processed_num, JSONPlugin())
    print()
    stream.print_processors_stats()
