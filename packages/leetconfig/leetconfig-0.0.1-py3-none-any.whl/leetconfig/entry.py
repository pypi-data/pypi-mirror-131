import re
from typing import Any, Generic, List, Optional, TypeVar, Union

from leetconfig import InvalidUsageError
from leetconfig.entry_converter import ConfigEntryConverter

LONG_NAME_REGEX = re.compile("^[a-z0-9_]+$")
SHORT_NAME_REGEX = re.compile("^[a-z0-9]+$")

T = TypeVar("T")


class ConfigEntry(Generic[T]):
    def __init__(
        self,
        names,  # type: Union[str, List[str]]
        parser,  # type: ConfigEntryConverter[T]
        help,  # type: str
        short_names=None,  # type: Optional[Union[str, List[str]]]
        is_flag=False,  # type: bool
        is_list=False,  # type: bool
        is_dict=False,  # type: bool
        is_required=False,  # type: bool
        is_positional=False,  # type: bool
        choices=None,  # type: Optional[List[T]]
        default=None,  # type: Optional[T]
    ):
        self._names = []  # type: List[str]
        if isinstance(names, str):
            self._names.append(names)
        else:
            self._names.extend(names)
        for name in self._names:
            if LONG_NAME_REGEX.match(name) is None:
                raise InvalidUsageError(
                    "The config entry name can only contain lower case characters, numbers "
                    "and underscores."
                )
        self._id = self._names[0]

        self._short_names = []  # type: List[str]
        if short_names is not None:
            if isinstance(short_names, str):
                self._short_names.append(short_names)
            else:
                self._short_names.extend(short_names)
        for name in self._short_names:
            if SHORT_NAME_REGEX.match(name) is None:
                raise InvalidUsageError(
                    "The config entry short name must can only contain lower case characters and"
                    "numbers."
                )
        self._short_id = self._short_names[0] if len(self._short_names) > 0 else None

        self._converter = parser
        self._help = help
        self._is_list = is_list
        self._is_dict = is_dict
        self._is_flag = is_flag
        self._is_required = is_required
        self._is_positional = is_positional
        self._is_disabled = False
        self._choices = choices
        self._default = default  # type: Optional[T]
        self._value = default  # type: Optional[T]
        self._namespaces = []  # type: List[str]
        self._short_namespaces = []  # type: List[str]

    def set_value(
        self,
        value,  # type: Any
    ):
        if value is not None:
            self._value = self._converter.deserialize(value)

    def set_default(
        self,
        value,  # type: T
    ):
        self._default = value
        self._value = value

    def set_required(
        self,
        is_required,  # type: bool
    ):
        self._is_required = is_required

    def set_disabled(
        self,
        is_disabled,  # type: bool
    ):
        """
        When a config entry is disabled, it is ignored by the format parser; they behave as if the
        entry did not exist. It can be useful when reusing config group/namespaces but some entries
        are to be populated programmatically.
        :param is_disabled:
        :return:
        """
        self._is_disabled = is_disabled

    def add_namespace(
        self,
        name,  # type: str
        short_name,  # type: str
    ):
        self._namespaces.insert(0, name)
        self._short_namespaces.insert(0, short_name)

    def _get_id(self):
        return self._id

    def _get_namespaced_id(self):  # type: () -> str
        parts = self._namespaces[:]
        parts.append(self._id)
        return "_".join(parts)

    def _get_short_namespaced_id(self):  # type: () -> Optional[str]
        if self._short_id is None:
            return None
        parts = self._short_namespaces[:]
        parts.append(self._short_id)
        return "".join(parts)

    def _get_names(self):  # type: () -> List[str]
        names = []
        for name in self._names:
            parts = self._namespaces[:]
            parts.append(name)
            names.append("_".join(parts))
        return names

    def _get_short_names(self):  # type: () -> List[str]
        short_names = []
        for name in self._short_names:
            parts = self._short_namespaces[:]
            parts.append(name)
            short_names.append("".join(parts))
        return short_names

    def get_value(self):  # type: () -> T
        # TODO: This used to return an Optional[T] like get_optional, but we changed it. We should
        # update all consumers of this library to call either get_value or get_optional as is
        # appropriate and add a runtime assertion instead of ignored the type checker.
        return self._value  # type: ignore

    def get_optional(self):  # type: () -> Optional[T]
        return self._value

    def _get_serialized_value(self):  # type: () -> Any
        if self._value is None:
            return None
        return self._converter.serialize(self._value)

    def validate(self):
        if self._is_required and self._value is None:
            raise InvalidConfigValueError(self, "the value is required")

        if self._value is None:
            return
        if self._choices is not None:
            if (
                (self._is_list is False and self._value not in self._choices)
                or self._is_list is True
                and any([v not in self._choices for v in self._value])
            ):
                raise InvalidConfigValueError(
                    self,
                    "the value must be one of {}, not {}".format(
                        ", ".join([str(c) for c in self._choices]), self._value
                    ),
                )


class InvalidConfigValueError(Exception):
    def __init__(self, entry, message):
        super(InvalidConfigValueError, self).__init__(message)
        self.entry = entry
