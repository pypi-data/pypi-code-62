from datetime import datetime
from importlib.metadata import version

from click import ParamType

__version__ = version(__package__)


class Date(ParamType):
    """The Date type converts date strings into `datetime.date` objects.

    The format strings which are checked are configurable, but default to some
    common (non-timezone aware) ISO 8601 formats.

    When specifying *Date* formats, you should only pass a list or a tuple.
    Other iterables, like generators, may lead to surprising results.

    The format strings are processed using ``datetime.strptime``, and this
    consequently defines the format strings which are allowed.

    Parsing is tried using each format, in order, and the first format which
    parses successfully is used.

    :param formats: A list or tuple of date format strings, in the order in
                    which they should be tried. Defaults to
                    ``'%Y-%m-%d'``.
    """

    name = "date"

    def __init__(self, formats=None):
        self.formats = formats or [
            "%Y-%m-%d",
        ]

    def to_info_dict(self):
        info_dict = super().to_info_dict()
        info_dict["formats"] = self.formats
        return info_dict

    def get_metavar(self, param):
        return f"[{'|'.join(self.formats)}]"

    def _try_to_convert_date(self, value, format):
        try:
            return datetime.strptime(value, format).date()
        except ValueError:
            return None

    def convert(self, value, param, ctx):
        for format in self.formats:
            date = self._try_to_convert_date(value, format)
            if date:
                return date

        self.fail(
            f"invalid date format: {value}. (choose from {', '.join(self.formats)})"
        )

    def __repr__(self):
        return "Date"
