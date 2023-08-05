from leetconfig.definitions.authentication import (
    PasswordAuthenticationConfig,
    PasswordAuthenticationConfigDefinition,
)
from leetconfig.definitions.server_client import (
    ServerClientConfig,
    ServerClientConfigDefinition,
)
from leetconfig.namespace import ConfigNamespace


class TelnetConfig:
    def __init__(
        self,
        server,  # type: ServerClientConfig
        authentication,  # type: PasswordAuthenticationConfig
    ):
        self.server = server
        self.authentication = authentication


class TelnetConfigDefinition(ConfigNamespace):
    def __init__(self):
        self.server = ServerClientConfigDefinition("Telnet")
        self.authentication = PasswordAuthenticationConfigDefinition("Telnet")
        super(TelnetConfigDefinition, self).__init__(
            "telnet",
            "t",
            groups=[self.server, self.authentication],
        )

    def populate(self, config):  # type: (TelnetConfig) -> None
        self.server.populate(config.server)
        self.authentication.populate(config.authentication)

    def export(self):  # type: () -> TelnetConfig
        return TelnetConfig(
            self.server.export(),
            self.authentication.export(),
        )
