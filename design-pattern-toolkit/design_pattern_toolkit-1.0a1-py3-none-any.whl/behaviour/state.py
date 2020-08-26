from abc import ABC, abstractmethod
from typing import Sequence, Callable, Any


class State(ABC):

    @abstractmethod
    def handle_request(self, *args, **kwargs):
        pass


class Context:

    def __init__(self, state: State = None) -> None:
        self._state = state if isinstance(state, State) else None

    def request(self, *args, **kwargs):
        if self._state:
            return self._state.handle_request(*args, **kwargs)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        # Change in state is determined by the client object which instantiate context and
        # can manage state transition by setting this property
        if isinstance(value, State):
            self._state = value
        else:
            raise ValueError('Invalid state object provided')


class DeterministicContext(Context):
    # Enforce change of state only by defined rule which can passed as callable or lambda

    def change_state(self, state: State, rule: Callable = None, params: Any = None):
        if not isinstance(state, State):
            raise RuntimeError('Invalid state object provided. Expected type State, '
                               'got %s instead' % type(state))
        if callable(rule):
            if params:
                if isinstance(params, dict):
                    outcome = rule(**params)
                    if outcome:
                        self._state = state
                elif isinstance(params, Sequence):
                    outcome = rule(*params)
                    if outcome:
                        self._state = state
            else:
                outcome = rule()
                if outcome:
                    self._state = state

    @property
    def state(self):
        return super(DeterministicContext, self).state

    @state.setter
    def state(self, value):
        raise RuntimeError('Class state attribute should not be modified without defined rule')
