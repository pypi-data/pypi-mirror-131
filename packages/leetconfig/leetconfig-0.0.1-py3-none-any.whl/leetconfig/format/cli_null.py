from typing import Optional, List, Dict, Any

from leetconfig.group import ConfigGroup
from leetconfig.format.abstract_format import ConfigFormat
from leetconfig.format.cli import CLIConfigFormat


class NullCLIConfigFormat(CLIConfigFormat):
    def __init__(
        self,
        program,  # type: str
        args=None,  # type: Optional[List[str]]
        serialize_short=False,  # type: bool
    ):
        super(NullCLIConfigFormat, self).__init__(program, args, serialize_short)

    def get_finalized_usage(
        self, group, values
    ):  # type: (ConfigGroup, Dict[str, Any]) ->  str
        return "Placeholder usage"

    def extract_source_args(
        self, sources
    ):  # type: (List[ConfigFormat]) ->  Dict[str, Any]
        return dict()

    def deserialize(self, namespace):  # type: (ConfigGroup) ->  Dict[str, Any]
        return dict()

    def serialize(self, entry_group):  # type: (ConfigGroup) ->  List[str]
        return []
