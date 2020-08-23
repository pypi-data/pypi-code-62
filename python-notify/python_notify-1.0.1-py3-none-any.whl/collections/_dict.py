import collections

from notify.signal import Signal


class Dict(collections.UserDict):
    """
    Dict is container like collections.UserDict but provides
    signals of adding value by key, changing value by key and removing key.
    """
    key_added = Signal(key=object, item=object)
    key_changed = Signal(key=object, past_item=object, new_item=object)
    key_removed = Signal(key=object)

    def __setitem__(self, key, item):
        signal, kwargs = self.key_added, {'key': key, 'item': item}
        try:
            past_tem = self[key]
        except KeyError:
            pass
        else:
            signal, kwargs = self.key_changed, {'key': key, 'past_item': past_tem, 'new_item': item}

        self.data[key] = item
        signal.notify(**kwargs)

    def __delitem__(self, key):
        del self.data[key]
        self.key_removed.notify(key=key)
