""" apu.dp: anton python utils design pattern module """

__version__ = (0, 0, 0)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.dp.null import Null
from apu.dp.blackboard import Blackboard, MetaInfo

__all__ = ['Null', "Blackboard", "MetaInfo"]
