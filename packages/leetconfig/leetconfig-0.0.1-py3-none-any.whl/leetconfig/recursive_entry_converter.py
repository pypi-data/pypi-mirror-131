from typing import Any, Dict, Type, TypeVar

from leetconfig.entry_converter import (
    ConfigEntryConverter,
    ConfigValueSerializationError,
)
from leetconfig.format.dictionary import DictConfigFormat
from leetconfig.group import ConfigGroup
from leetconfig.parser import ConfigParser

PT = TypeVar("PT")


class RecursiveConfigEntryConverter(ConfigEntryConverter):
    """
    Allows for nested config types
    """

    def __init__(
        self,
        config_definition_class,  # type: Type[ConfigGroup]
        *args,
        **kwargs,
    ):
        self.config_definition_class = config_definition_class
        self.config_definition_args = args
        self.config_definition_kwargs = kwargs

    def get_target_type(self):  # type: () -> str
        return str(self.config_definition_class)

    def deserialize(self, value):  # type: (Any) -> object
        config_definition = self.config_definition_class(
            *self.config_definition_args, **self.config_definition_kwargs
        )

        if issubclass(type(value), ConfigGroup):
            return value
        elif type(value) is not dict:
            raise TypeError("type(value) required to be dict or ConfigGroup")

        config_aggregator = ConfigParser(
            "",
            "temp",
            groups=[config_definition],
            sources=[
                DictConfigFormat("", "", "", value),
            ],
            force_no_cli=True,
        )
        config_aggregator.extract()
        # TODO: Either fix this typing issue or remove the module if deprecated.
        return config_definition.export()  # type: ignore

    def serialize(self, value):  # type: (PT) -> Dict[str, Any]
        """
        Go from a structured dataclass to a dictionary
        :param value:
        :return:
        """
        if not isinstance(value, ConfigGroup):
            raise ConfigValueSerializationError(
                "expected the value to be a config group, not {}".format(type(value))
            )
        return value.export().__dict__
