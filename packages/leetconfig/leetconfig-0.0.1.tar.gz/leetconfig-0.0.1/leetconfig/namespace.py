from typing import List, Optional

from leetconfig import InvalidUsageError
from leetconfig.entry import ConfigEntry
from leetconfig.group import ConfigGroup


class ConfigNamespace(ConfigGroup):
    """
    Group config entries together so they can be registered all at once in the ConfigParser. Each
    config entry's id is modified to contain the name of the namespace. For example, if a config
    entry named `hostname` is added to the namespace named `redis`, the config entry's value can be
    set by referring to `redis_hostname`. The ConfigNamespace supports nesting so that
    namespaces/groups can be added to other namespaces, creating a tree structure.
    """

    def __init__(
        self,
        name,  # type: str
        short_name,  # type: str
        entries=None,  # type: Optional[List[ConfigEntry]]
        groups=None,  # type: Optional[List[ConfigGroup]]
    ):
        if name is None or short_name is None:
            raise InvalidUsageError(
                "Both the name and short name must be provided when instantiating a config "
                "namespace."
            )
        self._name = name
        self._short_name = short_name

        super(ConfigNamespace, self).__init__(entries, groups)
        for child_group in self._entry_groups:
            for entry in child_group._get_all_entries():
                entry.add_namespace(name, short_name)

        for entry in self._entries:
            entry.add_namespace(name, short_name)

    def add_entry(
        self,
        entry,  # type: ConfigEntry
    ):
        super(ConfigNamespace, self).add_entry(entry)
        entry.add_namespace(self._name, self._short_name)

    def add_group(
        self,
        group,  # type: ConfigGroup
    ):
        super(ConfigNamespace, self).add_group(group)
        for entry in group._get_all_entries():
            entry.add_namespace(self._name, self._short_name)

    def _get_name(self):
        # type: () -> str
        return self._name
