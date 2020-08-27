import win32ui
from .stock import StockQuote


def window_exists(classname):
    try:
        win32ui.FindWindow(classname, None)
    except win32ui.error:
        return False
    else:
        return True