# -*- coding: utf-8 -*-
# author:Yaphp
# time:2020-08-22
# email:yaphp960907@gmail.com

import re, time
import datetime
import calendar

'''
    Whether the variable exists
'''
def isset(variable):
    return variable in locals() or variable in globals()


'''
    Is there a key in the dictionary
'''
def is_key_exsit(dictVar=None, keyVar=''):
    if dictVar is None:
        dictVar = {}
    try:
        if dictVar[keyVar]:
            val = True
        else:
            val = False
        return val
    except KeyError:
        val = False
    return val

'''
    Is there a key in the dictionary
'''
def is_numeric(var):
    try:
        float(var)
        return True
    except ValueError:
        return False

'''
    Is there a key in the dictionary
'''
def pdo_quote(string):
    return "'" + re.sub(r'(?<=[^\\])([\'\"])', r'\\\1', str(string)) + "'"

'''
    Gets the current date quickly. You can specify the format
'''
def date(format="%Y-%m-%d"):
    return time.strftime(format, time.localtime(time.time()))

'''
    Returns a millisecond or microsecond timestamp
'''
def time(isMicro = False):
    if isMicro:
        return calendar.timegm(time.gmtime())
    return datetime.datetime.now().timestamp()
