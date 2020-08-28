import logging
import re
from datetime import datetime

import clock


def get_human_time(numeric_time=None):
    """
    Handles http request to GET /humantime endpoint and returns the human time.
    :param numeric_time: The numeric time to convert, from the http request parameter
    :return: a tuple containing the response body and http status
    """
    logging.info("Received request GET /humantime, converting numeric time to human time...")

    if not numeric_time:
        numeric_time = datetime.now().strftime("%H:%M")
        logging.debug("No numeric time provided, using current time of {}".format(numeric_time))
    elif re.search('[a-zA-Z]', numeric_time):
        msg = "Provided time [{}] contains non numeric characters".format(numeric_time)
        logging.error(msg)
        return {"errorMessage": msg}, 400

    try:
        human_time = clock.talk(numeric_time)
    except ValueError as e:
        msg = "Numeric time [{}] is not in a valid format".format(numeric_time)
        logging.error(msg)
        return {"errorMessage": msg}, 400

    logging.info("Successfully converted numeric time [{}] to human time [{}]".format(numeric_time, human_time))
    return {"humanTime": human_time}, 200
