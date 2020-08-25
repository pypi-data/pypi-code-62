import importlib
import collections
import re
from lib.bric_builder.brics import directories


def get_modules(name, modules):
    # modules[name] = {
    #     'name': name,
    #     'Main': module.Main,
    #     'consts': module.bricConsts(),
    #     'get_params': module.bricParams,
    #     'get_calculations': module.bricCalculations,
    #     'get_modifiers': module.bricModifiers
    # }
    modules[name] = importlib.import_module('brics.{}'.format(name))
    modules[name].name = name

    return modules


# Passing a list of brics will return only the selected brics.
# Not passing a value, or passing 'all' will return all brics.
# placing a double underscore (__) in a bric directory's name will skip the bric
def mold_brics(bric_list='all'):
    brics = {}

    for module in directories:
        if '__' in module:
            pass
        else:
            module = (re.search(r'(?<=\\)(.*?)(?=\\)', module)).group(0)
            if bric_list == 'all' or (isinstance(bric_list, collections.Iterable) and module in bric_list):
                get_modules(module, brics)

    return brics


# TODO - this is a class, because it will be extended
#  Or maybe it'll stop being a class
class BricBuilder:
    def __init__(self, layer):
        self.layer = layer

        self.mold_brics = mold_brics
