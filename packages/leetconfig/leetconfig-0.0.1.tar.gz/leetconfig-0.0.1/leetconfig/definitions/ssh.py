from leetconfig.definitions.authentication import (
    PasswordAuthenticationConfigDefinition,
    PasswordAuthenticationConfig,
)
from leetconfig.definitions.server_client import (
    ServerClientConfig,
    ServerClientConfigDefinition,
)
from leetconfig.namespace import ConfigNamespace


class SSHConfig:
    def __init__(
        self,
        server,  # type: ServerClientConfig
        authentication,  # type: PasswordAuthenticationConfig
    ):
        self.server = server
        self.authentication = authentication


class SSHConfigDefinition(ConfigNamespace):
    def __init__(self):
        self.server = ServerClientConfigDefinition("SSH")
        self.authentication = PasswordAuthenticationConfigDefinition("SSH")
        super(SSHConfigDefinition, self).__init__(
            "ssh",
            "s",
            groups=[self.server, self.authentication],
        )

    def populate(self, config):  # type: (SSHConfig) -> None
        self.server.populate(config.server)
        self.authentication.populate(config.authentication)

    def export(self):  # type: () -> SSHConfig
        return SSHConfig(
            self.server.export(),
            self.authentication.export(),
        )
