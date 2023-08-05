import os
from typing import Dict, Any

from leetconfig.group import ConfigGroup
from leetconfig.format.abstract_format import ConfigFormat


class EnvironmentConfigFormat(ConfigFormat):
    def __init__(self):
        super(EnvironmentConfigFormat, self).__init__(
            "ENV",
            "environmental variables",
            "Parse config values from environmental variables. The lower case and upper case "
            "version of the config entry name are tried.",
        )

    def deserialize(self, group):  # type: (ConfigGroup) ->  Dict[str, Any]
        values = {}
        for entry in group._get_all_entries():
            for name in entry._get_names():
                value = os.environ.get(name)
                if value is None:
                    value = os.environ.get(name.upper())
                values[name] = value
        return values

    def serialize(self, group):  # type: (ConfigGroup) -> Any
        raise NotImplementedError()
