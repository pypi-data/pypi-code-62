from .lib import _StoppingProblem
from .schema import validate

"""
Defines the core interface to the library.
"""

import logging


logger = logging.getLogger(__name__)


class StoppingProblem:
    """Wrapper class for a quickest.lib._StoppingProblem object.
    Enables application programmers to get a class from a configuration file,
    or get a configuration, 
    or get the available module options.

    """

    @staticmethod
    def from_config(config={}):
        """Load a stopping problem object from a configuration file

        Args:
            config (dict): Configuration

        """
        logging.debug("Stand-in for validation")
        # TODO SCHEMAS

        errors = validate(config)

        if len(errors) > 0:
            msg = "Invalid config. Errors: "
            for error in errors:
                msg = msg + "\n{}".format(error)
            raise AttributeError(msg)

        return _StoppingProblem(**config)

    @staticmethod
    def get_opts():
        """Get options for a user interface. 
        The choices for each option can be passed to the StoppingProblem constructor.

        Returns:
            [type]: [description]
        """
        options = {}
        for key in _StoppingProblem.modules:
            if len(_StoppingProblem.modules[key].__subclasses__()) > 0:
                options[key] = _StoppingProblem.modules[key].opts()
        return options

    @staticmethod
    def get_config(opts=None):

        if opts == None:
            return dict(_StoppingProblem())
        else:

            # Extract the options not needing iteration over subclasses
            num_states = opts.pop("num_states")
            num_pre_change_states = opts.pop("num_pre_change_states")

            for key in opts:
                opts[key] = {"type": opts[key]}

            
            opts["change_process"] = {
                "num_states": num_states,
                "num_pre_change_states": num_pre_change_states,
            }

            print("Got all opts: {}".format(opts))

            return dict(_StoppingProblem(**opts))


if __name__ == "__main__":
    """Reference usage of the library.
    Shows high-level application code example using default values.
    """
    pass

