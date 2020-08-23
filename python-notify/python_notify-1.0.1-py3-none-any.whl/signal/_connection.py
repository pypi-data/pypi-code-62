import weakref


class Connection:
    """
    Represents connection object with able to disconnect using them.
    """
    def __init__(self, signal_backend, slot: weakref.ReferenceType):
        self._signal = weakref.ref(signal_backend)
        self._slot = slot

    def disconnect(self):
        if signal := self._signal():
            if slot := self._slot():
                signal.disconnect(slot)
