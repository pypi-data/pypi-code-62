from pathlib import Path

from tea_console.config import Config as TeaConfig, ConfigField


class Config(TeaConfig):
    ENTRIES = {
        **TeaConfig.ENTRIES,
        "server_url": ConfigField(section="server", option="url"),
        "token": ConfigField(section="auth", option="token"),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()

        # Server
        self.server_url = "http://127.0.0.1:8080"
        self.token = None

        super().__init__(config_file=self.config_dir / "traktor-client.ini")


config = Config()
