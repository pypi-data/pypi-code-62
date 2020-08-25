import sys

import dash
import dash_bootstrap_components as dbc
import capblood_seq

from .layouts import index as index_layout
from .functions import index as index_functions
from .functions import summary as summary_functions
from .functions import diurnality as diurnality_functions
from .functions import individuality as individuality_functions

import argparse

try:
    from .common import resources
    from . import config
except:
    sys.path.append(".")
    from capblood_seq_viz.common import resources
    from capblood_seq_viz import config


def server(**kwargs):

    for k in kwargs:
        sys.argv.append("--" + k)
        sys.argv.append(kwargs[k])

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

    if args.data_directory is not None:
        capblood_seq.init_dataset(
            data_directory=args.data_directory,
            config_file_path=args.dataset_config_path
        )
    else:
        capblood_seq.init_dataset(
            config_file_path=args.dataset_config_path
        )

    # Initialize the app
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.JOURNAL]
    )

    app.title = config.get("app_name")

    # Load the layout of the home page
    app.layout = index_layout.get_layout()

    # Add navbar collapse functionality
    index_functions.add_navbar_collapse(app)

    # Add tab switching functionality
    index_functions.add_tab_switching(app)

    summary_functions.add_projection_coloring(app)

    diurnality_functions.add_gene_click_listener(app)
    diurnality_functions.add_gene_selected_listener(app)

    individuality_functions.add_gene_click_listener(app)
    individuality_functions.add_gene_selected_listener(app)

    return app.server
