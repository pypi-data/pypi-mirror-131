from typing import Any, Dict

from leetconfig.group import ConfigGroup


from leetconfig.format.abstract_format import ConfigFormat


class DictConfigFormat(ConfigFormat):
    def __init__(
        self,
        id,  # type: str
        name,  # type: str
        help,  # type: str
        dict_entries,  # type: Dict[Any, Any]
    ):
        super(DictConfigFormat, self).__init__(id, name, help)
        self._dict_entries = dict_entries

    def deserialize(self, entry_group):  # type: (ConfigGroup) ->  Dict[str, Any]
        return self._dict_entries

    def serialize(self, entry_group):  # type: (ConfigGroup) ->  Any
        return self._dict_entries
