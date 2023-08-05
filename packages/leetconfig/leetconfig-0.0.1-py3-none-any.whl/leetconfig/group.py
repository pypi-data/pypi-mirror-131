from typing import Optional, List, Any

from leetconfig import InvalidUsageError
from leetconfig.entry import ConfigEntry


class InvalidConfigGroupError(Exception):
    def __init__(self, group, message):
        super(InvalidConfigGroupError, self).__init__(message)
        self.group = group


class ConfigGroup(object):
    """
    Group config entries together so they can be registered all at once in the ConfigParser. It
    supports nesting so that groups can be added to other groups, creating a tree structure.
    """

    def __init__(
        self,
        entries=None,  # type: Optional[List[ConfigEntry]]
        groups=None,  # type: Optional[List[ConfigGroup]]
    ):
        if entries is None and groups is None:
            raise InvalidUsageError(
                "Either (or both) entries/groups must be provided when instantiating a config "
                "group"
            )

        self._entries = entries if entries is not None else []
        self._entry_groups = groups if groups is not None else []

    def add_entry(
        self,
        entry,  # type: ConfigEntry
    ):
        """
        Add ConfigEntry to the group.

        :param entry:
        :return:
        """
        self._entries.append(entry)

    def add_group(
        self,
        group,  # type: ConfigGroup
    ):
        """
        Add a ConfigGroup to the group
        :param group:
        :return:
        """
        self._entry_groups.append(group)

    def _get_direct_groups(self):  # type: () -> List[ConfigGroup]
        """
        Get the groups directly registered to the group. In the context of a tree data structure,
        this is equivalent to getting a node's children and filtering on ConfigGroup instances.
        :return:
        """
        return self._entry_groups

    def _get_all_groups(self):  # type: () -> List[ConfigGroup]
        """
        Recursively get the groups registered on the groups. In the context of a tree data
        structure, this is equivalent to getting a node's descendants and filtering on ConfigGroup
        instances.
        :return:
        """
        groups = []
        for child_group in self._entry_groups:
            groups.extend(child_group._get_all_groups())
        groups.extend(self._entry_groups)
        return groups

    def _get_direct_entries(self):  # type: () -> List[ConfigEntry]
        """
        Get the entries directly registered to the group. In the context of a tree data structure,
        this is equivalent to getting a node's children and filtering on ConfigEntry instances.
        :return:
        """
        return [entry for entry in self._entries if entry._is_disabled is False]

    def _get_all_entries(self):  # type: () -> List[ConfigEntry]
        """
        Recursively get the groups registered on the groups. In the context of a tree data
        structure, this is equivalent to getting a node's descendants and filtering on ConfigEntry
        instances.
        :return:
        """
        entries = []
        for child_group in self._entry_groups:
            entries.extend(child_group._get_all_entries())
        entries.extend(self._get_direct_entries())
        return entries

    def validate(self):
        """
        Recursively validate the config entries/groups contained in the group. Overriding this
        method the recommended way of performing validation on a combination of values.
        :return:
        """
        for child_group in self._entry_groups:
            child_group.validate()
        for child_entry in self._get_direct_entries():
            child_entry.validate()

    def export(self):  # type: () -> Any
        """
        Export a config entry to another data structure containing the information. A common
        pattern is a data class for a config, and a corresponding config entry definition
        defining how to parse the fields of that config.
        :return:
        """
        return None
