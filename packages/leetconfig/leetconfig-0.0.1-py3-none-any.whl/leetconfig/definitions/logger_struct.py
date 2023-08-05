import logging
import logging.handlers
import socket
import sys
from typing import Optional

import structlog

from leetconfig.definitions.logger import (
    LoggerConfig,
    LoggerConfigDefinition,
    SyslogHandlerConfig,
)
from leetconfig.entry import ConfigEntry
from leetconfig.entry_converter import BooleanConfigEntryConverter


class StructLoggerConfig(LoggerConfig):
    def __init__(
        self,
        log_level,  # type: str
        syslog_handler,  # type: Optional[SyslogHandlerConfig]
        log_machine,  # type: bool
        log_colors,  # type: bool
    ):
        LoggerConfig.__init__(self, log_level, syslog_handler)
        self.log_machine = log_machine
        self.log_colors = log_colors

    def configure(self, output_stream=sys.stdout, processors=None):
        logging.addLevelName(5, "TRACE")
        shared_processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt=self.get_date_format()),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]
        if processors is not None:
            shared_processors = processors + shared_processors
        if self.log_machine:
            renderer = structlog.processors.JSONRenderer()
        else:
            styles = structlog.dev.ConsoleRenderer.get_default_level_styles(
                self.log_colors
            )
            styles["trace"] = styles["debug"]
            renderer = structlog.dev.ConsoleRenderer(
                colors=self.log_colors, level_styles=styles
            )
        formatter = structlog.stdlib.ProcessorFormatter(
            processor=renderer,
            foreign_pre_chain=shared_processors,
        )
        handler = logging.StreamHandler(stream=output_stream)
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)

        if self.syslog_handler is not None:
            formatter = structlog.stdlib.ProcessorFormatter(
                processor=structlog.processors.JSONRenderer(),
                foreign_pre_chain=shared_processors,
            )
            handler = logging.handlers.SysLogHandler(
                address=(
                    self.syslog_handler.server.hostname,
                    self.syslog_handler.server.port,
                ),
                facility=logging.handlers.SysLogHandler.LOG_DAEMON,
                socktype=socket.SOCK_DGRAM
                if self.syslog_handler.socket_type == "UDP"
                else socket.SOCK_STREAM,
            )
            handler.setFormatter(formatter)
            logging.root.addHandler(handler)

        logging.root.setLevel(self._get_level())
        structlog.configure(
            processors=shared_processors
            + [
                structlog.processors.UnicodeDecoder(),
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            context_class=dict,
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_date_format(self):
        return "%m/%d/%Y %H:%M:%S.%f"


class StructLoggerConfigDefinition(LoggerConfigDefinition):
    def __init__(self):
        LoggerConfigDefinition.__init__(self)
        self.log_machine = ConfigEntry(
            "machine",
            short_names="m",
            parser=BooleanConfigEntryConverter(),
            help="If set, the logs are printed in a machine friendly format",
            is_flag=True,
        )  # type: ConfigEntry[bool]
        self.log_colors = ConfigEntry(
            "colors",
            short_names="c",
            parser=BooleanConfigEntryConverter(),
            help="If set, the logs are displayed with colors",
            is_flag=True,
        )  # type: ConfigEntry[bool]
        self.add_entry(self.log_machine)
        self.add_entry(self.log_colors)

    def export(self):  # type: () -> StructLoggerConfig
        return StructLoggerConfig(
            self.log_level.get_value(),
            self.syslog_config.export(),
            self.log_machine.get_value(),
            self.log_colors.get_value(),
        )
