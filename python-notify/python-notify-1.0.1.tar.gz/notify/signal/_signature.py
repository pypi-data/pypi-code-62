import inspect
import typing


class PosOrKeywordSignalSignature(inspect.Signature):
    """
    Treats passed arguments as pos or keyword argument.
    """
    def __init__(self, **kwargs: typing.Type):
        params = tuple(self._create_args(kwargs))
        super().__init__(params)

    @staticmethod
    def _create_args(kwargs):
        for name, type_ in kwargs.items():
            yield inspect.Parameter(name=name, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=type_)
