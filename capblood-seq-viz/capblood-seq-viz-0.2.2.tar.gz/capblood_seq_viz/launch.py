import argparse
import subprocess
import sys

import capblood_seq

try:
    from .common import resources
    from . import config
except:
    sys.path.append(".")
    from capblood_seq_viz.common import resources
    from capblood_seq_viz import config


def launch_server():

    # Load the default config file
    config_file_path = resources.get_resource_path(config, "default.json")
    config.load_config(config_file_path)

    # Check for config file argument passing
    arg_parser = argparse.ArgumentParser(
        description="Launch the capblood-seq-viz server")
    arg_parser.add_argument(
        "--config_path",
        help="Path to the capblood-seq-viz config file",
        default=None
    )
    arg_parser.add_argument(
        "--dataset_config_path",
        help="Path to the capblood-seq config file",
        default=None
    )
    arg_parser.add_argument(
        "--data_directory",
        help="Path to the capblood-seq data directory",
        default=None
    )

    args, _ = arg_parser.parse_known_args()

    # If the user passed a config file, load it
    if args.config_path is not None:
        config.load_config(args.config_path)

    port = config.get("port")
    num_threads = config.get("num_threads")

    app_path = "capblood_seq_viz.server:server("

    arg_list = []
    if args.data_directory is not None:
        arg_list.append("data_directory=\"%s\"" % args.data_directory)
    if args.config_path is not None:
        arg_list.append("config_path=\"%s\"" % args.config_path)
    if args.dataset_config_path is not None:
        arg_list.append("dataset_config_path=\"%s\"" % args.dataset_config_path)
    app_path += ",".join(arg_list) + ")"

    try:
        subprocess.call(
            [
                "gunicorn",
                "-w", "%i" % num_threads,
                "-b", "127.0.0.1:%i" % port,
                app_path
            ]
        )
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    launch_server()
