import argparse
import sys
from typing import Dict, Any, Optional, List

from leetconfig.group import ConfigGroup
from leetconfig.format.abstract_format import ConfigSourceError, ConfigFormat


class DictParser(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(DictParser, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        result = {}
        for item in values:
            parts = item.split(":")
            if len(parts) != 2:
                raise ConfigSourceError(
                    "expected dictionary items to be separated by a single ':'"
                )
            result[parts[0]] = parts[1]
        setattr(namespace, self.dest, result)


class CLIConfigFormat(ConfigFormat):
    def __init__(
        self,
        program,  # type: str
        args=None,  # type: Optional[List[str]]
        serialize_short=False,  # type: bool
    ):
        if args is None:
            args = sys.argv[1:]
        self.help_flag = False
        self.show_config_flag = False
        self.parser = argparse.ArgumentParser(program, add_help=False)
        self.args = args
        self.serialize_short = serialize_short
        super(CLIConfigFormat, self).__init__(
            "CLI",
            "command line arguments",
            "Parse config values from the command line arguments.",
        )

    def _configure_parser(
        self,
        parser,
        entry_group,
        values=None,
    ):  # type: (argparse.ArgumentParser, ConfigGroup, Optional[Dict[str, Any]]) ->  None
        parser.add_argument("--help", "-h", action="store_true")
        parser.add_argument("--show-config", "-sc", action="store_true")
        entry_ids = set()
        for entry in entry_group._get_all_entries():
            names = []
            kwargs: Dict[str, object] = dict()
            if entry._get_namespaced_id() in entry_ids:
                continue
            entry_ids.add(entry._get_namespaced_id())

            required = False
            if (
                values is not None
                and entry._is_required is True
                and entry._default is None
            ):
                required = values.get(entry._get_namespaced_id()) is None
            kwargs["required"] = required

            if entry._is_flag:
                kwargs["action"] = "store_true"
            elif entry._is_dict:
                kwargs["action"] = DictParser
                kwargs["metavar"] = "KEY:VAL"
            else:
                kwargs["metavar"] = "VAL"
                kwargs["type"] = str
            if entry._is_list or entry._is_dict:
                kwargs["nargs"] = "+" if required is True else "*"

            if not entry._is_positional:
                for name in entry._get_names():
                    names.append("--{}".format(name.replace("_", "-")))
                for name in entry._get_short_names():
                    names.append("-{}".format(name))
            else:
                name = entry._get_namespaced_id()
                if not required:
                    if entry._is_list or entry._is_dict:
                        kwargs["nargs"] = "*"
                    else:
                        kwargs["nargs"] = "?"
                del kwargs["required"]
                kwargs["metavar"] = name.upper()
                names.append(name)
            parser.add_argument(*names, **kwargs)  # type: ignore

    def get_usage(self):
        return self.parser.format_usage()

    def get_finalized_usage(
        self, group, values
    ):  # type: (ConfigGroup, Dict[str, Any]) ->  str
        parser = argparse.ArgumentParser(self.parser.prog, add_help=False)
        self._configure_parser(parser, group, values)
        return parser.format_usage()

    def extract_source_args(
        self, sources
    ):  # type: (List[ConfigFormat]) ->  Dict[str, Any]
        entries = []
        for source in sources:
            entries.extend(source.cli_entries)
        group = ConfigGroup(entries=entries)
        parser = argparse.ArgumentParser(self.parser.prog, add_help=False)
        self._configure_parser(parser, group)

        args, _ = parser.parse_known_args(args=self.args)
        return args.__dict__

    def deserialize(self, namespace):  # type: (ConfigGroup) ->  Dict[str, Any]
        self._configure_parser(self.parser, namespace)

        args = self.parser.parse_args(args=self.args)
        self.help_flag = args.help
        self.show_config_flag = args.show_config
        return args.__dict__

    def serialize(self, entry_group):  # type: (ConfigGroup) ->  List[str]
        is_nargs = False
        command = []
        for entry in entry_group._get_all_entries():
            if entry.get_value() == entry._default:
                continue
            serialized_value = entry._get_serialized_value()
            if serialized_value is None:
                continue
            short_id = entry._get_short_namespaced_id()
            if self.serialize_short is True and short_id is not None:
                name = "-{}".format(short_id)
            else:
                name = "--{}".format(entry._get_namespaced_id().replace("_", "-"))
            if entry._is_flag:
                if entry.get_value() is True:
                    command.append(name)
                continue
            if not entry._is_positional:
                command.append(name)
            elif is_nargs:
                command.append("--")
            if isinstance(serialized_value, list):
                command.extend(serialized_value)
            elif isinstance(serialized_value, dict):
                command.extend(
                    ["{}:{}".format(k, v) for k, v in serialized_value.items()]
                )
            else:
                command.append(str(serialized_value))
            is_nargs = entry._is_dict is True or entry._is_list is True
        return command
