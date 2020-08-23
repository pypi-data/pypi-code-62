from pathlib import Path

from console_tea.config import Config as TeaConfig, ConfigField


class Config(TeaConfig):
    ENTRIES = {
        **TeaConfig.ENTRIES,
        "server_host": ConfigField(section="server", option="host"),
        "server_port": ConfigField(section="server", option="port", type=int),
        "token": ConfigField(section="auth", option="token"),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()

        # Server
        self.server_host = "127.0.0.1"
        self.server_port = 8080
        self.token = None

        super().__init__(config_file=self.config_dir / "traktor-client.ini")
        # Load the values from configuration file

    @property
    def server_url(self):
        if self.server_port == 80:
            return f"http://{self.server_host}"
        elif self.server_port == 443:
            return f"https://{self.server_host}"
        else:
            return f"http://{self.server_host}:{self.server_port}"


config = Config()
