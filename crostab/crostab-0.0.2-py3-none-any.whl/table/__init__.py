from veho.columns import column
from veho.matrix import shallow, size, transpose

from crostab.enum.keys import HEAD, ROWS, TITLE, TYPES
from crostab.types import Matrix


class Table:
    head: list
    rows: Matrix
    title: str
    types: list

    __slots__ = (HEAD, ROWS, TITLE, TYPES)

    def __init__(self, head: list, rows: list, title: str = None, types: list = None):
        self.title = title if title is not None else ''
        self.rows = rows
        self.head = head
        self.types = types

    @staticmethod
    def from_json(json_ob, title, types):
        j = json_ob.loads(json_ob)
        return Table(j.head, j.rows, title, types)

    @staticmethod
    def from_dict(dict_ob):
        head = dict_ob[HEAD] if HEAD in dict_ob else None
        rows = dict_ob[ROWS] if ROWS in dict_ob else None
        title = dict_ob[TITLE] if TITLE in dict_ob else None
        types = dict_ob[TYPES] if TYPES in dict_ob else None
        return Table(head, rows, title, types)

    @property
    def size(self): return size(self.rows)

    @property
    def height(self): return len(self.rows)

    @property
    def width(self): return len(self.head)

    @property
    def columns(self): return transpose(self.rows)

    def cell(self, x, y): return self.rows[x][y]

    def coin(self, field):
        try: return field if isinstance(field, int) else self.head.index(field)
        except ValueError: return -1

    def column_indexes(self, fields):
        return [self.coin(field) for field in fields]

    def column(self, field):
        return column(self.rows, y) if (y := self.coin(field)) >= 0 else None

    def set_column(self, field, new_column):
        if (y := self.coin(field)) < 0: return self
        for i, row in enumerate(self.rows): row[y] = new_column[i]
        return self

    def set_column_by(self, field, mapper):
        if (y := self.coin(field)) < 0: return self
        for i, row in enumerate(self.rows): row[y] = mapper(row[i])
        return self

    def boot(self, head=None, rows=None, title=None, types=None, mutate=True):
        if not mutate: return self.copy(head, rows, title, types)
        if head: self.head = head
        if rows: self.rows = rows
        if title: self.title = title
        if types: self.types = types
        return self

    def copy(self, head=None, rows=None, title=None, types=None):
        if not head: head = self.head[:]
        if not rows: rows = shallow(self.rows)
        if not title: title = self.title
        if not types: types = self.types
        return Table(head, rows, title, types)
