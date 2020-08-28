#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Date   : 2020/8/18
# @Author : Bruce Liu /Lin Luo
# @Mail   : 15869300264@163.com
class CadException(BaseException):
    def __init__(self, ak):
        self._msg = f'the ak: {ak} is not found'

    def __str__(self):
        return self._msg
