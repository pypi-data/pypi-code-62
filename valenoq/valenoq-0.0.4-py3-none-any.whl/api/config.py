import os
import json
from pdb import set_trace as stop

CONFIG_DIR = ".valenoq"
CONFIG_FILE_NAME = "api.config"


class ValenoqIllegalConfigParam(Exception):
    pass

class ValenoqConfigCannotBeCreated(Exception):
    pass

class ValenoqConfigFileDoesNotExist(Exception):
    pass


def set(*args, **kwargs):
    """
    Storing configuration data into a local config file (~/.valenoq/api.config)

    Parameters
    ------------
    api_key: str
    The API key (available upon registration at https://valenoq.com)

    Examples
    --------
    Setting api_key globally:

    >>> config.set(api_key="yourApiKey")
    """
    api_key = kwargs.get("api_key")
    if api_key:
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, CONFIG_DIR)
        if not os.path.isdir(config_dir):
            # create dir first
            try:
                os.mkdir(config_dir)
            except PermissionError:
                raise ValenoqConfigCannotBeCreated("Permission denied to create a folder %s. Please create manually or change permissions" %config_dir)

        config_file = os.path.join(config_dir, CONFIG_FILE_NAME)
        with open(config_file, "w") as ifile:
            ifile.write(json.dumps({"api_key": api_key}))
    else:
        raise ValenoqIllegalConfigParam("The only supported configuration parameter is api_key. The value of the api_key cannot be empty")

def get(config_item):
    """
    Getting configuration data from a local config file (~/.valenoq/api.config)

    Parameters
    ------------
    config_item: string
    The configuration item to be retrieved from config file

    Examples
    --------
    Getting current api_key:

    >>> config.get("api_key")
    """

    config_file_path = os.path.join(os.path.expanduser("~"), CONFIG_DIR, CONFIG_FILE_NAME)
    if not os.path.isfile(config_file_path):
        raise ValenoqConfigFileDoesNotExist(
            "configuration file (config_file_path) does not exist. Please run config.set(`your_api_key`) first")

    with open(config_file_path) as config_file:
        config = json.load(config_file)

    if config_item == "api_key":
        return config.get("api_key")
