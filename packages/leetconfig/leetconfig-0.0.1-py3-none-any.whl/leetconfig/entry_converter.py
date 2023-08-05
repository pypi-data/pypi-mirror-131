from abc import ABCMeta, abstractmethod
from typing import Type, TypeVar, Generic, Any, Dict, List, Optional, Tuple, cast

from enum import Enum

PT = TypeVar("PT")
ET = TypeVar("ET", bound=Enum)
TuplePT = TypeVar("TuplePT", bound=Tuple)


class ConfigValueDeserializationError(Exception):
    pass


class ConfigValueSerializationError(Exception):
    pass


class ConfigEntryConverter(Generic[PT]):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_target_type(self):  # type: () -> str
        raise NotImplementedError()

    @abstractmethod
    def deserialize(self, value):  # type: (Any) -> PT
        raise NotImplementedError()

    @abstractmethod
    def serialize(self, value):  # type: (PT) -> Any
        raise NotImplementedError()


class ArrayConfigEntryConverter(ConfigEntryConverter[List[PT]]):
    def __init__(
        self,
        parser,  # type: ConfigEntryConverter[PT]
    ):
        self.parser = parser

    def get_target_type(self):  # type: () -> str
        return "{}[]".format(self.parser.get_target_type())

    def deserialize(self, raw_values):  # type: (Any) -> List[PT]
        if not isinstance(raw_values, list):
            raise ConfigValueDeserializationError("expected the value to be a list")
        return [self.parser.deserialize(raw_value) for raw_value in raw_values]

    def serialize(self, values):  # type: (List[PT]) -> List[Any]
        if not isinstance(values, list):
            raise ConfigValueSerializationError("expected the value to be a list")
        return [self.parser.serialize(value) for value in values]


class TupleConfigEntryConverter(ConfigEntryConverter[TuplePT]):
    def __init__(
        self,
        *parsers,  # type: ConfigEntryConverter
    ):
        # Unfortunately, Python doesn't currently allow us to define the relationship between
        # TuplePT and the type of `parsers` properly
        self.parsers: Tuple[ConfigEntryConverter, ...] = parsers

    def get_target_type(self):  # type: () -> str
        return "Tuple[{}]".format(
            ", ".join([parser.get_target_type() for parser in self.parsers])
        )

    def deserialize(self, raw_values):  # type: (Any) -> TuplePT
        if not isinstance(raw_values, list):
            raise ConfigValueDeserializationError("expected the value to be a list")
        if len(raw_values) != len(self.parsers):
            raise ConfigValueDeserializationError(
                "expected number of raw values ({}) to match number of parsers ({})".format(
                    len(raw_values), len(self.parsers)
                )
            )
        results = tuple(
            parser.deserialize(raw_value)
            for parser, raw_value in zip(self.parsers, raw_values)
        )
        return cast(TuplePT, results)

    def serialize(self, values):  # type: (TuplePT) -> Tuple[Any, ...]
        if not isinstance(values, tuple):
            raise ConfigValueSerializationError("expected the value to be a tuple")
        if len(values) != len(self.parsers):
            raise ConfigValueDeserializationError(
                "expected number of values ({}) to match number of parsers ({})".format(
                    len(values), len(self.parsers)
                )
            )
        _values = cast(Tuple[Any], values)
        return tuple(
            parser.serialize(value) for parser, value in zip(self.parsers, _values)
        )


class DictConfigEntryConverter(ConfigEntryConverter[Dict[str, PT]]):
    def __init__(
        self, parser  # type: ConfigEntryConverter[PT]
    ):
        self.parser = parser

    def get_target_type(self):  # type: () -> str
        return "Dict[str, {}]".format(self.parser.get_target_type())

    def deserialize(self, value):  # type: (Any) -> Dict[str, PT]
        if not isinstance(value, dict):
            raise ConfigValueDeserializationError(
                "expected the value to be a dictionary"
            )
        return dict([(k, self.parser.deserialize(v)) for k, v in value.items()])

    def serialize(self, value):  # type: (Dict[str, PT]) -> Dict[str, Any]
        if not isinstance(value, dict):
            raise ConfigValueSerializationError("expected the value to be a dict")
        return dict([(k, self.parser.serialize(v)) for k, v in value.items()])


class OptionalConfigEntryConverter(ConfigEntryConverter[Optional[PT]]):
    def __init__(self, parser):
        # type: (ConfigEntryConverter[PT]) -> None
        self.parser = parser

    def get_target_type(self):  # type: () -> str
        return "Optional[{}]".format(self.parser.get_target_type())

    def deserialize(self, value):  # type: (Any) -> Optional[PT]
        return self.parser.deserialize(value) if value is not None else None

    def serialize(self, value):  # type: (Optional[PT]) -> Any
        return self.parser.serialize(value) if value is not None else None


class StringConfigEntryConverter(ConfigEntryConverter[str]):
    def get_target_type(self):  # type: () -> str
        return "string"

    def deserialize(self, value):  # type: (Any) -> str
        if not isinstance(value, str):
            raise ConfigValueDeserializationError(
                "expected the value to be a string, not {}".format(type(value))
            )
        return value

    def serialize(self, value):  # type: (str) -> str
        if not isinstance(value, str):
            raise ConfigValueSerializationError(
                "expected the value to be a string, not {}".format(type(value))
            )
        return value


class HexStringConfigEntryConverter(ConfigEntryConverter[bytes]):
    def get_target_type(self):  # type: () -> str
        return "hex string"

    def deserialize(self, value):  # type: (Any) -> bytes
        if not isinstance(value, str):
            raise ConfigValueDeserializationError(
                "expected the value to be a string, not {}".format(type(value))
            )
        return bytes.fromhex(value)

    def serialize(self, value):  # type: (bytes) -> str
        if not isinstance(value, bytes):
            raise ConfigValueSerializationError(
                "expected the value to be bytes, not {}".format(type(value))
            )
        return value.hex()


class BooleanConfigEntryConverter(ConfigEntryConverter[bool]):
    def get_target_type(self):  # type: () -> str
        return "boolean"

    def deserialize(self, value):  # type: (Any) -> bool
        if isinstance(value, bool):
            return value
        if not isinstance(value, str):
            raise ConfigValueDeserializationError(
                "expected the value to either a bool or a string, not {}".format(
                    type(value)
                )
            )
        try:
            if value.lower() in ["true", "1"]:
                return True
            elif value.lower() in ["false", "0"]:
                return False
            else:
                raise ValueError("Invalid value")
        except ValueError:
            raise ConfigValueDeserializationError(
                "the string '{}' should be either 'true' or 'false'".format(value)
            )

    def serialize(self, value):  # type: (bool) -> str
        if not isinstance(value, bool):
            raise ConfigValueSerializationError(
                "expected the value to be a boolean, not {}".format(type(value))
            )
        return str(value)


class IntegerConfigEntryConverter(ConfigEntryConverter[int]):
    def get_target_type(self):  # type: () -> str
        return "integer"

    def deserialize(self, value):  # type: (Any) -> int
        if isinstance(value, int):
            return value
        if not isinstance(value, str):
            raise ConfigValueDeserializationError(
                "expected the value to be either an integer or string, not {}".format(
                    type(value)
                )
            )
        try:
            return int(value, 0)
        except ValueError:
            raise ConfigValueDeserializationError(
                "the string '{}' is not a valid integer representation".format(value)
            )

    def serialize(self, value):  # type: (int) -> int
        if not isinstance(value, int):
            raise ConfigValueSerializationError(
                "expected the value to be an integer, not {}".format(type(value))
            )
        return value


class FloatConfigEntryConverter(ConfigEntryConverter[float]):
    def get_target_type(self):  # type: () -> str
        return "float"

    def deserialize(self, value):  # type: (Any) -> float
        if isinstance(value, float):
            return value
        if not isinstance(value, (str, int)):
            raise ConfigValueDeserializationError(
                "expected the value to be either a float, int, or string, not {}".format(
                    type(value)
                )
            )
        try:
            return float(value)
        except ValueError:
            raise ConfigValueDeserializationError(
                "the string '{}' is not a valid float representation".format(value)
            )

    def serialize(self, value):  # type: (float) -> float
        if not isinstance(value, float):
            raise ConfigValueSerializationError(
                "expected the value to be a float, not {}".format(type(value))
            )
        return value


class EnumConfigEntryConverter(ConfigEntryConverter[ET]):
    def __init__(
        self, enum  # type: Type[ET]
    ):
        self.enum = enum

    def get_target_type(self):  # type: () -> str
        return "string"

    def deserialize(self, value):  # type: (Any) -> ET
        if isinstance(value, self.enum):
            return value
        if not isinstance(value, str):
            raise ConfigValueDeserializationError(
                "expected the value to be a string, not {}".format(type(value))
            )
        try:
            return self.enum[value]
        except KeyError:
            pass
        try:
            return self.enum(value)
        except ValueError:
            allowed_values = []
            for k in self.enum:
                allowed_values.append(k.name)
                allowed_values.append(k.value)
            raise ConfigValueDeserializationError(
                "expected the value to be one of {}".format(", ".join(allowed_values))
            )

    def serialize(self, value):  # type: (ET) -> str
        if value not in self.enum:
            raise ConfigValueSerializationError(
                "expected the value to be in {}, got {}".format(self.enum, value)
            )
        return value.name


class RawConfigEntryConverter(ConfigEntryConverter):
    """
    Returns the raw value without deserializing.
    Used for converting a YAML dict of multiple types.
    """

    def get_target_type(self):  # type: () -> str
        return "Any"

    def deserialize(self, value):  # type: (Any) -> Any
        return value

    def serialize(self, value):  # type: (Any) -> Any
        return value
