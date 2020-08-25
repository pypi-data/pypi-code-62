import json

CONFIG = {
    "app_name": "CapBlood-Seq",
    "port": 80,
    "num_threads": 4
}


def load_config(file_path):

    global CONFIG

    with open(file_path) as new_config_file:
        new_config = json.load(new_config_file)

    for key, value in new_config.items():
        CONFIG[key] = value


def get(key):

    return CONFIG[key]
