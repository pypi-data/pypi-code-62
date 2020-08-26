import js2py
from .ASLMutation import var, ASLMutation

__all__ = map(lambda i: i.to_py(), var.get('__all__').to_list())

for key in __all__:
  locals()[key] = getattr(ASLMutation, key)
