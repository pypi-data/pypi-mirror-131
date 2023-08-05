from leetconfig.parser import ConfigEntry
from leetconfig.group import ConfigGroup
from leetconfig.entry_converter import (
    StringConfigEntryConverter,
    IntegerConfigEntryConverter,
)


class ServerClientConfig:
    def __init__(
        self,
        hostname,  # type: str
        port,  # type: int
        connect_retries,  # type: int
    ):
        self.hostname = hostname
        self.port = port
        self.connect_retries = connect_retries

    def __eq__(self, other):  # type: (object) -> bool
        if not isinstance(other, ServerClientConfig):
            return NotImplemented
        return (
            self.hostname == other.hostname
            and self.port == other.port
            and self.connect_retries == other.connect_retries
        )

    def __ne__(self, other):  # type: (object) -> bool
        return not self.__eq__(other)


class ServerClientConfigDefinition(ConfigGroup):
    def __init__(
        self,
        server_name,  # type: str
        is_required=True,  # type: bool
    ):
        self.hostname = ConfigEntry(
            "hostname",
            short_names="hn",
            parser=StringConfigEntryConverter(),
            help="The host to connect to the {} server".format(server_name),
            is_required=is_required,
        )  # type: ConfigEntry[str]
        self.port = ConfigEntry(
            "port",
            short_names="p",
            parser=IntegerConfigEntryConverter(),
            help="The port to connect to the {} server".format(server_name),
            is_required=is_required,
        )  # type: ConfigEntry[int]
        self.connect_retries = ConfigEntry(
            "connect_retries",
            short_names="cr",
            parser=IntegerConfigEntryConverter(),
            help="Max retries when attempting to connect to the {} server (default 0)".format(
                server_name
            ),
            is_required=False,
            default=0,
        )  # type: ConfigEntry[int]
        super(ServerClientConfigDefinition, self).__init__(
            entries=[self.hostname, self.port, self.connect_retries],
        )

    def populate(self, config):  # type: (ServerClientConfig) -> None
        self.hostname.set_value(config.hostname)
        self.port.set_value(config.port)
        self.connect_retries.set_value(config.connect_retries)

    def export(self):  # type: () -> ServerClientConfig
        return ServerClientConfig(
            self.hostname.get_value(),
            self.port.get_value(),
            self.connect_retries.get_value(),
        )
