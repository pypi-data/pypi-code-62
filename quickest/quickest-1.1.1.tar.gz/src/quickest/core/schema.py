from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Range

import numpy as np

from .lib import (
    Module,
    ChangeProcess,
    Threshold,
    _StoppingProblem,
    AugmentedHMM,
)

# TODO MOVE LOGIC IN HERE!
json_safe_types = [
    dict,
    list,
    tuple,
    str,
    int,
    float,
    bool,
    None,
    np.float64,
    np.float32,
]


def adapt_module(module):
    """The adapter for change experiment module types. 
    An adapter prepares objects for serialisation by converting them to
    a dictionary.

    Args:
        module (quickest.core.lib.Module): A subclass of Module

    Returns:
        [dict]: Object in dictionary format ready for serialisation
    """

    if isinstance(module, ChangeProcess):
        return dict(module)
    elif isinstance(module, Threshold):
        return dict(module)
    elif isinstance(module, AugmentedHMM):
        return dict(module)
    else:
        raise AttributeError(
            "Type {} is not a subclass of quickest.core.lib.Module".format(type(module))
        )


class Adapter:

    @classmethod
    def jsonify(cls, data):

        if isinstance(data, dict):
            out_data = {}
            for key in data:
                out_data[key] = cls.jsonify(data[key])

        elif type(data) in Module.__subclasses__():
            out_data = adapt_module(data)

        elif isinstance(data, np.ndarray):
            out_data = data.tolist()

        elif type(data) in json_safe_types:
            out_data = data
        else:

            raise ValueError("No adapter found for data of type {}".format(type(data)))
        return out_data

# TODO 
def validate(config):
    return []


class ExperimentSchema(Schema):
    """Validation schema for experimental results. 
    This Schema includes all the information necessary for loading serialised data,
    making meaningful comparisons, plots, etc.

    """
    cost = fields.Float() 
    filter_history = fields.List(fields.List(fields.Float()))
    observation_history = fields.List(fields.Float())
    state_history = fields.List(fields.Integer())
    change_point = fields.Integer(missing=None)
    pre_change_states = fields.List(fields.Integer())
    post_change_states = fields.List(fields.Integer())
    timestamp = fields.String()


# class OptimiserSchema(Schema):
#     # A schema that records the information about a particular optimisation.
#     param_history = fields.List(fields.List(fields.Float()))




