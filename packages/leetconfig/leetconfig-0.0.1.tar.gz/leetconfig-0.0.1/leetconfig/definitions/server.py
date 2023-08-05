import socket

from leetconfig.entry import ConfigEntry
from leetconfig.entry_converter import (
    IntegerConfigEntryConverter,
    StringConfigEntryConverter,
)
from leetconfig.group import ConfigGroup


class ServerConfig:
    def __init__(
        self,
        ip,  # type: str
        port,  # type: int
    ):
        self.ip = ip
        self.port = port


class ServerConfigDefinition(ConfigGroup):
    def __init__(self, is_required: bool = True):
        self.ip = ConfigEntry(
            "ip",
            parser=StringConfigEntryConverter(),
            help="The ip the server binds to.",
            is_required=is_required,
            choices=["127.0.0.1", "0.0.0.0", socket.gethostname()],
        )  # type: ConfigEntry[str]

        self.port = ConfigEntry(
            "port",
            short_names="p",
            parser=IntegerConfigEntryConverter(),
            help="The port the server binds to.",
            is_required=is_required,
        )  # type: ConfigEntry[int]

        super(ServerConfigDefinition, self).__init__(entries=[self.ip, self.port])

    def populate(self, config):  # type: (ServerConfig) -> None
        self.ip.set_value(config.ip)
        self.port.set_value(config.port)

    def export(self):  # type: () -> ServerConfig
        return ServerConfig(self.ip.get_value(), self.port.get_value())
