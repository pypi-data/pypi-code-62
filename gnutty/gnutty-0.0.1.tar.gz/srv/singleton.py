"""!
@author atomicfruitcake

@date 2020

Singleton metaclass to prevent multiple instantiations of the same class
"""

from abc import ABCMeta

class Singleton(type, metaclass=ABCMeta):
    """
    Singleton pattern class. If the class already exists. Return that instead of instantiating a new one
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        If cls object does not exist, instantiate cls object, otherwise return the object that exists
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
