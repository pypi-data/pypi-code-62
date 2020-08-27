#from toolsbyerazhan import *#无效
#from toolsbyerazhan import timetools,gpu4tftools#有效

#可直接用timetools.py和gputools.py文件中的所有函数
#from .timetools import *
#from .gputools import *

from . import gputools,ostools,timetools,tensorflowtools,transformers
from .quicktools import whether_to_transfer

