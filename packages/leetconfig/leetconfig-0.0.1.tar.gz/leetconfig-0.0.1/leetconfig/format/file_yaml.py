import os
from typing import List, Dict, Any, Union

import yaml

from leetconfig.group import ConfigGroup
from leetconfig.entry import ConfigEntry
from leetconfig.entry_converter import (
    ArrayConfigEntryConverter,
    StringConfigEntryConverter,
)
from leetconfig.namespace import ConfigNamespace
from leetconfig.format.abstract_format import ConfigSourceError, ConfigFormat

LEETCONFIG_DIR = "/etc/leetconfig"


class YAMLConfigFormat(ConfigFormat):
    def __init__(
        self,
        config_name,  # type: Union[str, List[str]]
        config_directories=None,  # type: Union[str, List[str]]
    ):
        if config_directories is None:
            config_directories = [LEETCONFIG_DIR, os.getcwd()]
        self.config_directories = (
            config_directories
            if isinstance(config_directories, list)
            else [config_directories]
        )
        self.config_file_names = (
            config_name if isinstance(config_name, list) else [config_name]
        )

        self.config_path_cli_entry = ConfigEntry(
            "yaml_config_path",
            short_names="ycp",
            parser=ArrayConfigEntryConverter(StringConfigEntryConverter()),
            help="The path to the yaml config file.",
            is_required=False,
            is_list=True,
            default=[],
        )  # type: ConfigEntry[List[str]]
        super(YAMLConfigFormat, self).__init__(
            "YAML",
            "yaml config file",
            "Parse config values from file(s) named {} in the current working directory.".format(
                ", ".join(self.config_file_names),
            ),
            cli_entries=[self.config_path_cli_entry],
        )

    def _extract_from_group(
        self,
        group,
        group_values,
    ):  # type: (ConfigGroup, Dict[str, Any]) ->  Dict[str, Any]
        values = {}
        if group_values is None:
            return values
        for child_entry in group._get_direct_entries():
            value = group_values.get(child_entry._get_id())
            if value is not None:
                values[child_entry._get_namespaced_id()] = value
        for child_group in group._get_direct_groups():
            if isinstance(child_group, ConfigNamespace):
                child_group_values = group_values.get(child_group._get_name())
                if isinstance(child_group_values, dict):
                    child_group_values = {
                        k: v
                        for k, v in child_group_values.items()
                        if isinstance(k, str)
                    }
                    values.update(
                        self._extract_from_group(child_group, child_group_values)
                    )
            else:
                values.update(self._extract_from_group(child_group, group_values))
        return values

    def _extract_from_file(
        self,
        file_path,
        group,
    ):  # type: (str, ConfigGroup) -> Dict[str, Any]
        values: Dict[str, Any] = {}
        try:
            if not os.path.exists(file_path):
                return values
            with open(file_path, "r") as f:
                group_values = yaml.load(f.read(), Loader=yaml.Loader)
                values.update(self._extract_from_group(group, group_values))
            return values
        except Exception as err:
            raise ConfigSourceError(
                "the file '{}' is not a valid yaml file: {}".format(file_path, err)
            )

    def deserialize(self, group):  # type: (ConfigGroup) ->  Dict[str, Any]
        values = dict()
        if not isinstance(group, ConfigGroup):
            raise ValueError("The root group should be an instance of ConfigGroup")

        # Load the default file config
        for config_filename in self.config_file_names:
            for config_directory in self.config_directories:
                config_path = os.path.join(config_directory, config_filename)
                values.update(self._extract_from_file(config_path, group))
        # Load the file config provided by the user
        for file_path in self.config_path_cli_entry.get_value():
            if not os.path.isfile(file_path):
                raise ConfigSourceError(
                    "The provided config path {} does not exist".format(file_path)
                )
            values.update(self._extract_from_file(file_path, group))
        return values

    def _serialize_from_group(
        self,
        group,
        group_values,
    ):  # type: (ConfigGroup, Dict[str, Any]) ->  Dict[str, Any]
        for entry in group._get_direct_entries():
            value = entry._get_serialized_value()
            if value is not None:
                group_values[entry._get_id()] = value
        for child_group in group._get_direct_groups():
            child_group_values = self._serialize_from_group(child_group, dict())
            if isinstance(child_group, ConfigNamespace):
                group_values[child_group._get_name()] = child_group_values
            else:
                group_values.update(child_group_values)
        return group_values

    def _serialize_from_namespace(
        self,
        namespace,  # type: ConfigNamespace
        namespace_values,  # type: Dict[str, Any]
    ):
        # type: (...) -> Dict[str, Any]
        group_values = self._serialize_from_group(namespace, dict())
        namespace_values[namespace._get_name()] = group_values
        return namespace_values

    def serialize(
        self, group_or_namespace
    ):  # type: (Union[ConfigGroup, ConfigNamespace]) ->  str
        if not isinstance(group_or_namespace, ConfigGroup):
            raise ValueError("The root group should be an instance of ConfigGroup")
        if isinstance(group_or_namespace, ConfigNamespace):
            values = self._serialize_from_namespace(group_or_namespace, dict())
        else:
            values = self._serialize_from_group(group_or_namespace, dict())
        return yaml.dump(values, Dumper=yaml.Dumper, default_flow_style=False)
