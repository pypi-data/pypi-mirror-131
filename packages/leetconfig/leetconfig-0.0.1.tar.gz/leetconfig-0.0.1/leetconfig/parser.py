import os
import sys
import textwrap
from typing import List, Optional, Dict, Any

from leetconfig.entry import ConfigEntry, InvalidConfigValueError
from leetconfig.entry_converter import ConfigValueDeserializationError
from leetconfig.group import ConfigGroup, InvalidConfigGroupError
from leetconfig.namespace import ConfigNamespace
from leetconfig.format.abstract_format import ConfigSourceError, ConfigFormat
from leetconfig.format.cli import CLIConfigFormat


class ConfigParser:
    def __init__(
        self,
        program,  # type: str
        description,  # type: str
        sources=None,  # type: List[ConfigFormat]
        groups=None,  # type: Optional[List[ConfigGroup]]
        entries=None,  # type: List[ConfigEntry]
        args=None,  # type: Optional[List[str]]
        force_no_cli=False,  # type: bool
    ):
        if args is None:
            args = sys.argv[1:]
        self.cli_source = CLIConfigFormat(program, args)
        self.description = description

        try:
            self.line_width = int(os.environ["COLUMNS"])
        except (KeyError, ValueError):
            self.line_width = 80
        self.line_width -= 2

        self.sources = (
            sources if sources is not None else []
        )  # type: List[ConfigFormat]
        if not force_no_cli:
            self.sources.insert(0, self.cli_source)

        all_entries = []
        if entries is not None:
            all_entries.extend(entries)
        source_entries = []
        for source in self.sources:
            source_entries.extend(source.cli_entries)
        all_entries.extend(source_entries)

        self.entry_group = ConfigGroup(all_entries, groups)
        merged_values = self.cli_source.extract_source_args(self.sources)
        self._update_entries(source_entries, merged_values, dict())

        config_entry_names = dict()  # type: Dict[str, ConfigEntry]
        for child_entry in self.entry_group._get_all_entries():
            child_names = []
            child_names.extend(child_entry._get_names())
            child_names.extend(child_entry._get_short_names())
            for name in child_names:
                config_entry = config_entry_names.get(name)
                if config_entry is None:
                    config_entry_names[name] = child_entry
                    continue
                if (
                    config_entry._get_names() == child_entry._get_names()
                    and config_entry._get_short_names()
                    == child_entry._get_short_names()
                ):
                    break
                print(
                    "The config entry name {} ({}) is already used by the config "
                    "entry {}".format(
                        name,
                        child_entry._get_namespaced_id(),
                        config_entry._get_namespaced_id(),
                    )
                )
                sys.exit(1)

    def _print_help_line(self, line, indent):  # type: (str, int) -> None
        lines = textwrap.wrap(line, self.line_width - 2 * indent)
        for i, line in enumerate(lines):
            if i == 0:
                print(" " * (indent * 2) + line)
            else:
                print(" " * ((indent + 1) * 2) + line)

    def print_usage_help(self, values=None):  # type: (Optional[Dict[str, Any]]) -> None
        if values is not None:
            print(self.cli_source.get_finalized_usage(self.entry_group, values))
        else:
            print(self.cli_source.get_usage())

    def _format_entry_type(
        self,
        entry,
    ):  # type: (ConfigEntry) -> str
        entry_type = entry._converter.get_target_type()
        if not entry._is_required:
            entry_type = "[{}]".format(entry_type)
        return entry_type

    def print_entry_help(
        self,
        entry,  # type: ConfigEntry
        depth,  # type: int
    ):
        names = []
        names.append(entry._get_id())
        names.extend([n for n in entry._get_names() if n != entry._get_id()])
        names.extend(entry._get_short_names())
        default_value = ""
        if entry._default is not None:
            default_value = " (default: {})".format(entry._default)
        line = "{}: {}".format(
            ", ".join(names),
            self._format_entry_type(entry),
        )
        self._print_help_line(line, depth)

        self._print_help_line("{}{}".format(entry._help, default_value), depth + 2)

    def print_sources_help(self):
        print("Configuration sources (ordered by priority):")
        for source in self.sources:
            self._print_help_line("{}:".format(source.id), 1)
            self._print_help_line("{}".format(source.help), 2)

    def print_namespace_help(
        self,
        entry_group,  # type: ConfigGroup
        depth,  # type: int
    ):
        if isinstance(entry_group, ConfigNamespace):
            self._print_help_line("{}:".format(entry_group._get_name()), depth)
        else:
            depth -= 1

        child_entries = entry_group._get_direct_entries()
        if len(child_entries) > 0:
            for child_entry in child_entries:
                self.print_entry_help(child_entry, depth + 1)

        child_groups = entry_group._get_direct_groups()
        for child_group in child_groups:
            if len(child_entries) > 0 and isinstance(child_group, ConfigNamespace):
                print("")
            self.print_namespace_help(child_group, depth + 1)

    def print_help(self, values=None):  # type: (Optional[Dict[str, Any]]) -> None
        self.print_usage_help(values)
        self._print_help_line(self.description, 0)
        print("")
        self.print_sources_help()
        print("")
        self._print_help_line("Configuration options:", 0)
        self.print_namespace_help(self.entry_group, 1)

    def print_entry_config(
        self,
        entry,  # type: ConfigEntry
        value_sources,  # type: Dict[str, ConfigFormat]
        depth,  # type: int
    ):
        source = value_sources.get(entry._get_namespaced_id())
        if source is not None:
            source_id = source.id
        else:
            source_id = "DEFAULT"
        line = "{}: {} = {} [from {}]".format(
            entry._get_id(), self._format_entry_type(entry), entry._value, source_id
        )
        self._print_help_line(line, depth)

    def print_namespace_config(
        self,
        entry_group,  # type: ConfigGroup
        value_sources,  # type: Dict[str, ConfigFormat]
        depth,  # type: int
    ):
        if isinstance(entry_group, ConfigNamespace):
            self._print_help_line("{}:".format(entry_group._get_name()), depth)
        else:
            depth -= 1

        child_entries = entry_group._get_direct_entries()
        if len(child_entries) > 0:
            for child_entry in child_entries:
                self.print_entry_config(child_entry, value_sources, depth + 1)

        child_groups = entry_group._get_direct_groups()
        for child_group in child_groups:
            if len(child_entries) > 0 and isinstance(child_group, ConfigNamespace):
                print("")
            self.print_namespace_config(child_group, value_sources, depth + 1)

    def print_config(
        self,
        value_sources,  # type: Dict[str, ConfigFormat]
    ):
        self._print_help_line("Configuration: ", 0)
        self.print_namespace_config(self.entry_group, value_sources, 1)

    def _update_entries(
        self,
        entries,  # type: List[ConfigEntry]
        merged_values,  # type: Dict[str, Any]
        merged_values_sources,  # type: Dict[str, ConfigFormat]
    ):
        for entry in entries:
            raw_value = merged_values.get(entry._get_namespaced_id())
            source = merged_values_sources.get(entry._get_namespaced_id())
            try:
                entry.set_value(raw_value)
            except ConfigValueDeserializationError as err:
                self.print_usage_help(merged_values)
                if source is not None:
                    self._print_help_line(
                        "Failed to parse the '{}' config value from {}: {}".format(
                            entry._get_namespaced_id(), source.name, str(err)
                        ),
                        0,
                    )
                else:
                    self._print_help_line(
                        "Failed to parse the '{}' config value: {}".format(
                            entry._get_namespaced_id(), str(err)
                        ),
                        0,
                    )
                sys.exit(1)

    def _handle_config_entry_error(
        self,
        err,  # type: InvalidConfigValueError
        merged_values,  # type: Dict[str, Any]
        merged_values_sources,  # type: Dict[str, ConfigFormat]
    ):
        source = merged_values_sources.get(err.entry._get_namespaced_id())
        self.print_usage_help(merged_values)
        if source is not None:
            self._print_help_line(
                "Invalid '{}' config value from {}: {}".format(
                    err.entry._get_namespaced_id(), source.name, str(err)
                ),
                0,
            )
        else:
            self._print_help_line(
                "Invalid '{}' config value: {}".format(
                    err.entry._get_namespaced_id(), str(err)
                ),
                0,
            )
        sys.exit(1)

    def _handle_config_group_error(
        self,
        err,  # type: InvalidConfigGroupError
        merged_values,  # type: Dict[str, Any]
    ):
        self.print_usage_help(merged_values)
        if isinstance(err.group, ConfigNamespace):
            self._print_help_line(
                "Invalid {} namespace config: {}".format(
                    err.group._get_name().lower(), str(err)
                ),
                0,
            )
        else:
            self._print_help_line("Invalid namespace config: {}".format(str(err)), 0)
        sys.exit(1)

    def extract(self):
        merged_values = dict()  # type: Dict[str, Any]
        merged_values_sources = dict()  # type: Dict[str, ConfigFormat]
        for source in reversed(self.sources):
            try:
                values = source.deserialize(self.entry_group)
                if source == self.cli_source and self.cli_source.help_flag is True:
                    self.print_help(merged_values)
                    sys.exit(0)
                for key, value in values.items():
                    if value is not None:
                        merged_values[key] = value
                        merged_values_sources[key] = source
            except ConfigSourceError as err:
                self.print_usage_help()
                self.print_sources_help()
                print("")
                self._print_help_line(
                    "Failed to populate config from {}: {}".format(
                        source.name, str(err)
                    ),
                    0,
                )
                sys.exit(1)

        self._update_entries(
            self.entry_group._get_all_entries(), merged_values, merged_values_sources
        )

        if self.cli_source.show_config_flag:
            self.print_config(merged_values_sources)
            sys.exit(0)

        for entry in self.entry_group._get_direct_entries():
            try:
                entry.validate()
            except InvalidConfigValueError as err:
                self._handle_config_entry_error(
                    err, merged_values, merged_values_sources
                )

        for group in self.entry_group._get_direct_groups():
            try:
                group.validate()
            except InvalidConfigGroupError as err:
                self._handle_config_group_error(err, merged_values)
            except InvalidConfigValueError as err:
                self._handle_config_entry_error(
                    err, merged_values, merged_values_sources
                )
