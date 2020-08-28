
#coding:utf-8
'''
# File Name: factors.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
from .utils import FactorApiGenerator

basic = FactorApiGenerator("basic")

class Factor(FactorApiGenerator):
    class Vip(FactorApiGenerator):
        def __init__(self):
            super(Factor.Vip,self).__init__("factor/vip")
            self.std = FactorApiGenerator("factor/vip/standard")

    def __init__(self):
        super(Factor,self).__init__("factor")
        self.std = FactorApiGenerator("factor/standard")
        self.vip = Factor.Vip()

factor = Factor()
