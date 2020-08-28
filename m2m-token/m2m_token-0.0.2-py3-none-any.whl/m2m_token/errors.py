class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class ConfigError(Error):
    config_name: str
    message: str
    error: str

    def __init__(self, config_name, error):
        self.config_name = config_name
        self.error = error
        self.message = f'The following error occurred for the config [{config_name}] : {error}'
