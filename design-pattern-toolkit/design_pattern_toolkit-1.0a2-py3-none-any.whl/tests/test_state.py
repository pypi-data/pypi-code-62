from toolkit.behaviour.state import State, Context, DeterministicContext


class StateOne(State):

    def handle_request(self, *args, **kwargs):
        return self.__class__.__qualname__


class StateTwo(State):

    def handle_request(self, *args, **kwargs):
        return self.__class__.__qualname__


class StateThree(State):

    def handle_request(self, *args, **kwargs):
        return self.__class__.__qualname__


def test_state():
    def change_state():
        return True

    state_a = StateOne()
    state_b = StateTwo()
    state_c = StateThree()
    a = Context(state=state_a)
    assert a.state == state_a
    assert a.request() == state_a.__class__.__qualname__
    a.state = state_b
    a.request()
    assert a.state == state_b
    assert a.request() == state_b.__class__.__qualname__
    a.state = state_c
    a.request()
    assert a.state == state_c
    assert a.request() == state_c.__class__.__qualname__
    b = DeterministicContext(state_a)
    b.change_state(state_b, change_state)
    assert b.state == state_b
    b.change_state(state_c, change_state)
    assert b.state == state_c
