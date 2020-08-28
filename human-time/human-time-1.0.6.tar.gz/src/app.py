import os

import connexion
import logging
from flask import redirect
from flask.helpers import get_debug_flag


def start():
    debug = get_debug_flag()
    log_level = "DEBUG" if debug else "INFO"
    logging.basicConfig(format="[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s", level=log_level)
    app = connexion.FlaskApp(__name__, specification_dir=".")
    app.add_api("humantime.yaml", strict_validation=True, validate_responses=True)

    @app.route("/")
    def root():
        return redirect("/api/ui")

    logging.info("Running humantime service...")
    port = os.getenv("HUMANTIME_PORT", 5000)
    app.run(port=port, debug=debug)


if __name__ == "__main__":
    start()
