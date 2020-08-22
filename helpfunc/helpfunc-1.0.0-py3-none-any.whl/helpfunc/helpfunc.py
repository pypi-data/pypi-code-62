import re,time
import datetime
import calendar

def isset(variable):
    return variable in locals() or variable in globals()

def is_key_exsit(dictVar = {},keyVar = ''):
    try:
        if dictVar[keyVar]:
            val = True
        else:
            val = False
        return val
    except KeyError:
        val = False
    return val

def is_numeric(var):
    try:
        float(var)
        return True
    except ValueError:
        return False

def pdo_quote(string):
    return "'" + re.sub(r'(?<=[^\\])([\'\"])', r'\\\1', str(string)) + "'"

def date(format = "%Y-%m-%d"):
    return time.strftime(format,time.localtime(time.time()))

def time(isMircro = False):
    if isMircro:
        return calendar.timegm(time.gmtime())
    return datetime.datetime.now().timestamp()
