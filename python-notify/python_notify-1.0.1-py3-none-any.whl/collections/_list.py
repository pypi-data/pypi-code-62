import typing as t
import collections

from notify.signal import Signal


Position = t.Union[int, slice]


class List(collections.UserList):
    """
    List is container like collections.UserList but provides
    signals of adding items, changing items, removing items and clearing all.
    """
    items_added = Signal(items=t.Tuple[object], pos=Position)
    items_changed = Signal(past_items=t.Tuple[object], new_items=t.Tuple[object], pos=Position)
    items_removed = Signal(items=t.Tuple[object], pos=Position)
    items_cleared = Signal()

    def __setitem__(self, i, item):
        past_len = len(self)
        if isinstance(i, slice):
            past_item = tuple(self[i])
            super().__setitem__(i, item)
            item = tuple(item)
        else:
            past_item = (self[i],)
            super().__setitem__(i, item)
            item = (item,)

        if past_item:
            signal, kwargs = self.items_changed, {'past_items': past_item, 'new_items': item, 'pos': i}
        else:
            signal, kwargs = self.items_added, {'items': item, 'pos': past_len}
        signal.notify(**kwargs)

    def __delitem__(self, i):
        item = tuple(self[i]) if isinstance(i, slice) else (self[i],)
        super().__delitem__(i)

        if item:
            self.items_removed.notify(items=item, pos=i)

    def __iadd__(self, other):
        start_len = len(self)
        result = super().__iadd__(other)

        if added := tuple(self[start_len: len(self)]):
            self.items_added.notify(items=added, pos=start_len)
        return result

    def __imul__(self, n):
        start_len = len(self)
        if n <= 0:
            start_items = tuple(self[:])
            result = super().__imul__(n)
            self.items_removed.notify(items=start_items, pos=0)
            return result

        result = super().__imul__(n)
        if added := tuple(result[start_len:]):
            self.items_added.notify(items=added, pos=start_len)
        return result

    def append(self, item):
        super().append(item)
        self.items_added.notify(items=(item,), pos=len(self) - 1)

    def insert(self, i, item):
        super().insert(i, item)
        self.items_added.notify(items=(item,), pos=i)

    def pop(self, i=-1):
        result = super().pop(i)
        self.items_removed.notify(items=(result,), pos=i)
        return result

    def remove(self, item):
        try:
            item_index = self.index(item)
        except ValueError:
            self.data.remove(item)
        else:
            self.data.remove(item)
            self.items_removed.notify(items=(item,), pos=item_index)

    def clear(self):
        super().clear()
        self.items_cleared.notify()

    def extend(self, other):
        if new_items := tuple(other):
            start_pos = len(self)
            super().extend(other)
            self.items_added.notify(items=new_items, pos=start_pos)
