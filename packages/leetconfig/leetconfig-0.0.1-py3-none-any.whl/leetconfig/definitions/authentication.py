from leetconfig.parser import ConfigEntry
from leetconfig.group import ConfigGroup
from leetconfig.entry_converter import StringConfigEntryConverter


class PasswordAuthenticationConfig:
    def __init__(
        self,
        username,  # type: str
        password,  # type: str
    ):
        self.username = username
        self.password = password

    def __eq__(self, other):  # type: (object) -> bool
        if not isinstance(other, PasswordAuthenticationConfig):
            return NotImplemented
        return self.username == other.username and self.password == other.password

    def __ne__(self, other):  # type: (object) -> bool
        return not self.__ne__(other)


class PasswordAuthenticationConfigDefinition(ConfigGroup):
    def __init__(
        self,
        service_name,  # type: str
        is_required=False,  # type: bool
    ):
        self.username = ConfigEntry(
            "username",
            short_names="u",
            parser=StringConfigEntryConverter(),
            help="The username to authenticate with the {} service".format(
                service_name
            ),
            is_required=is_required,
        )  # type: ConfigEntry[str]
        self.password = ConfigEntry(
            "password",
            short_names="pw",
            parser=StringConfigEntryConverter(),
            help="The password to authenticate with the {} service".format(
                service_name
            ),
            is_required=is_required,
        )  # type: ConfigEntry[str]
        super(PasswordAuthenticationConfigDefinition, self).__init__(
            entries=[self.username, self.password],
        )

    def populate(self, config):  # type: (PasswordAuthenticationConfig) -> None
        self.username.set_value(config.username)
        self.password.set_value(config.password)

    def export(self):  # type: () -> PasswordAuthenticationConfig
        return PasswordAuthenticationConfig(
            self.username.get_value(),
            self.password.get_value(),
        )
