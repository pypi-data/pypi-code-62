from .app.io import get_parser
from .app.lib import get_app_list, launch

from .backend import Backend


import sys, os



def main():

    application_types = get_app_list()
    backend_types = Backend.get_opts()

    parser = get_parser(
        application_options=application_types, backend_options=backend_types
    )
    args = parser.parse_args()

    return launch(args)


if __name__ == "__main__":
    main()
