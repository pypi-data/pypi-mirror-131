from abc import ABCMeta, abstractmethod

from typing import Optional, List, Dict, Any

from leetconfig.entry import ConfigEntry
from leetconfig.group import ConfigGroup


class ConfigSourceError(RuntimeError):
    pass


class ConfigFormat:
    __metaclass__ = ABCMeta

    def __init__(
        self,
        id,  # type: str
        name,  # type: str
        help,  # type: str
        cli_entries=None,  # type: Optional[List[ConfigEntry]]
    ):
        self.id = id
        self.name = name
        self.help = help
        self.cli_entries = cli_entries if cli_entries is not None else []

    @abstractmethod
    def deserialize(self, entry_group):  # type: (ConfigGroup) ->  Dict[str, Any]
        raise NotImplementedError()

    @abstractmethod
    def serialize(self, entry_group):  # type: (ConfigGroup) ->  Any
        raise NotImplementedError()
