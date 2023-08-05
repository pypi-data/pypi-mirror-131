import logging
import sys
from typing import Optional

from leetconfig.group import InvalidConfigGroupError

from leetconfig.definitions.server_client import (
    ServerClientConfigDefinition,
    ServerClientConfig,
)

from leetconfig.parser import ConfigEntry
from leetconfig.entry_converter import StringConfigEntryConverter
from leetconfig.namespace import ConfigNamespace


class SyslogHandlerConfig:
    def __init__(
        self,
        socket_type,  # type: str
        server,  # type: ServerClientConfig
    ):
        self.socket_type = socket_type
        self.server = server


class LoggerConfig:
    def __init__(
        self,
        log_level,  # type: str
        syslog_handler,  # type: Optional[SyslogHandlerConfig]
    ):
        self.log_level = log_level
        self.syslog_handler = syslog_handler

    def get_format(self):
        return "%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(message)s"

    def get_date_format(self):
        return "%m/%d/%Y %H:%M:%S"

    def get_formatter(self) -> logging.Formatter:
        return logging.Formatter(self.get_format(), self.get_date_format())

    def _get_level(self) -> int:
        if self.log_level == "TRACE":
            return 5
        return logging.getLevelName(self.log_level)

    def configure(self, output_stream=sys.stdout):
        logging.addLevelName(5, "TRACE")
        logging.basicConfig(
            level=self._get_level(),
            stream=output_stream,
            format=self.get_format(),
            datefmt=self.get_date_format(),
        )


class SyslogHandlerConfigDefinition(ConfigNamespace):
    def __init__(self):
        self.socket_type = ConfigEntry(
            "socket",
            short_names="l",
            parser=StringConfigEntryConverter(),
            choices=["UDP", "TCP"],
            help="The logging level used in the application",
            default="TCP",
            is_required=True,
        )  # type: ConfigEntry[str]
        self.server = ServerClientConfigDefinition("Syslog", False)

        # TODO: Allow the group to define itself as optional (but not its individual children
        #  entries/groups)
        super(SyslogHandlerConfigDefinition, self).__init__(
            "syslog", "l", [self.socket_type], [self.server]
        )

    def validate(self):
        if not self.server.hostname.get_value() and not self.server.port.get_value():
            return
        if self.server.hostname.get_value() and self.server.port.get_value():
            return
        if not self.server.hostname.get_value():
            raise InvalidConfigGroupError(self, "The entry 'hostname' must be provided")
        if not self.server.port.get_value():
            raise InvalidConfigGroupError(self, "The entry 'port' must be provided")

    def populate(self, config):  # type: (Optional[SyslogHandlerConfig]) -> None
        if config is None:
            return
        self.socket_type.set_value(config.socket_type)
        self.server.populate(config.server)

    def export(self):  # type: () -> Optional[SyslogHandlerConfig]
        server_config = self.server.export()
        if not server_config.hostname or not server_config.port:
            return None
        return SyslogHandlerConfig(self.socket_type.get_value(), server_config)


class LoggerConfigDefinition(ConfigNamespace):
    def __init__(self):
        self.syslog_config = SyslogHandlerConfigDefinition()
        self.log_level = ConfigEntry(
            "level",
            short_names="l",
            parser=StringConfigEntryConverter(),
            choices=["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="The logging level used in the application",
            is_required=True,
        )  # type: ConfigEntry[str]

        super(LoggerConfigDefinition, self).__init__(
            "logger", "l", [self.log_level], [self.syslog_config]
        )

    def populate(self, config):  # type: (LoggerConfig) -> None
        self.log_level.set_value(config.log_level)
        self.syslog_config.populate(config.syslog_handler)

    def export(self):  # type: () -> LoggerConfig
        return LoggerConfig(self.log_level.get_value(), self.syslog_config.export())
