"""
This package implements specialized container data types providing
alternatives to Python's general purpose built-in containers, dict,
list, with signals for state changes.


* List:
    items_added = Signal(items=typing.Tuple[object], pos=Position)
    items_changed = Signal(past_items=typing.Tuple[object], new_items=typing.Tuple[object], pos=Position)
    items_removed = Signal(items=typing.Tuple[object], pos=Position)
    items_cleared = Signal()

    Where Position = t.Union[int, slice]

* Dict:
    key_added = Signal(key=object, item=object)
    key_changed = Signal(key=object, past_item=object, new_item=object)
    key_removed = Signal(key=object)
"""

from ._list import List
from ._dict import Dict
