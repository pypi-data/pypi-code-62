from ast import literal_eval
import datesy
import asyncio


class Item:
    """
    Representation of a database entry
    """

    def __init__(self, data):
        row, column, table, value = data
        self.__value = value
        self.__row = row
        self.__column = column
        self._table = table
        self.__python_type = type(self.__value)

    def print_stupid(self):
        print("Stuüopd")

    @property
    def column(self):
        return self.__column

    # @property
    # def table(self):
    #     return self.__table

    @property
    def database(self):
        return self._table

    def _where_reference_to_row(self, with_own_column=True):
        """
        Create a query reference to the belonging row

        """
        if with_own_column:
            self.table.query.add_desired_columns(self.column)

        if self.table.primary:
            primary_value = self.__row[self.table.primary]
            self.table.query.add_where_statement(**{self.table.primary: primary_value})
        else:
            self.table.query.add_where_statement(**self.__row.__dict__())
            self.table.query.limit(1)

    def sync(self):
        self._where_reference_to_row()
        self.__value = self.table.run_query()
        print(self.__value)

    def __set__(self, instance, value):
        if not isinstance(value, self.__python_type):
            raise TypeError(f"expected {self.__python_type}, got {type(value)}")
        # ToDo schema validation
        self._where_reference_to_row(with_own_column=False)
        self.table.query.add_new_values(**{self.column: value})

        self.sync()

    def __delete__(self, instance):
        self.table.query.delete_request()
        self._where_reference_to_row()

        self.sync()


class Test(object):
    async def __aenter__(self):
        print("in aenter")

    def __enter__(self):
        print("in enter")
        return self

    def __init__(self, value):
        print("in init")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("in exit")
        if exc_type is not None:
            print(1, exc_type)
            print(2, exc_val)
            print(3, exc_tb)
            raise exc_type(exc_val)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await print("in aexit")

    def print(self, value):
        print(value)


async def main():
    async with Test("host") as t2:
        await t2


if __name__ == "__main__":
    try:
        with Test("host") as t:
            t.print("a")
            raise SystemExit("abc")
            pass
    except SystemExit as e:
        print(e)
        print(e.__traceback__)

    # main()
    # s = str()
    t1 = Test("abc")
    t1.print("b")
