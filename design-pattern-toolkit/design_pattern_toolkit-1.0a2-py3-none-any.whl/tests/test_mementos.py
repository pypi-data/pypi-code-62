from toolkit.behaviour.mementos import OriginatorMixin, AppStateManager


class A:

    def __init__(self):
        self.name = 'TestClass'


def test_mementos():
    origin_1 = OriginatorMixin()
    origin_2 = OriginatorMixin()
    AppStateManager.stash(origin_1.state)
    AppStateManager.stash(origin_2.state)
    b = AppStateManager.get(origin_1.state)
    c = AppStateManager.get(origin_2.state)
    assert b
    assert c
    origin_1.commit(label='Modified_state', message='Testing the modified state')
    AppStateManager.stash(origin_1.state)
    assert AppStateManager.history()
    d = AppStateManager.get(origin_1.state)
    assert d
    assert d != b
    origin_1.commit(label='Yet_Another_Change')
    AppStateManager.stash(origin_1.state)
    e = AppStateManager.get(origin_1.state)
    assert e
    assert e != d
    history = list(e)
    _, third_capture = history[2]
    # restore history to third memento captured
    origin_1.restore(third_capture)
    AppStateManager.stash(origin_1.state)
    f = AppStateManager.get(origin_1.state)
    assert list(f) == list(d)
