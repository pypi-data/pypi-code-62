import argparse, logging, json, os, appdirs
from datetime import datetime

APP_NAME = 'quickest'


def get_parser(application_options=None, backend_options=None):

    parser = argparse.ArgumentParser(
        description="Quickest Change Application entry point"
    )
    parser.add_argument(
        "application",
        type=str,
        nargs="?",
        choices=application_options,
        help="Experiment to run",
    )

    for key in backend_options:
        opts = backend_options[key]
        for opt in opts:
            parser.add_argument("--" + opt['kwarg'], help=opt['description'])

    parser.add_argument("--conf", type=str, help="Absolute path to config file")

    parser.add_argument("--steps", type=int, help="Number of steps to run optimiser for")

    parser.add_argument("--lr", type=float, help="Initial learning rate")
    parser.add_argument("--decay", type=float, help="Exponential learning decay constant")

    return parser


def get_logger():

    USER_LOG_DIR = appdirs.user_log_dir(APP_NAME)

    if not os.path.isdir(USER_LOG_DIR):
        os.makedirs(USER_LOG_DIR)

    LOG_LOCATION = os.path.join(USER_LOG_DIR, "{}.log".format(datetime.now().strftime("%Y_%m_%d")))

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d %(name)-16s %(levelname)-8s %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
        filename=LOG_LOCATION,
        filemode="a",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    logger = logging.getLogger(APP_NAME)
    return logger


def load_config(CONFIGFILE):
    with open(CONFIGFILE) as f:
        config = json.load(f)
    # TODO VALIDATION

    return config

