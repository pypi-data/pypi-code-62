from sql_query import *

from datesy.database_IO import SQLQueryConstructor


class Test:
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        print("set", type(value))
        print("set", type(self.value))
        if not isinstance(value, type(self.value)):
            raise ValueError("unequal")
        self.value = value


class Values:
    t = Test(3)


class OrderTest:
    def p(self, p):
        print(p)
        return self


class TestTable:
    query = SQLQueryConstructor("depot_bco", "__attributes_sandbox")


if __name__ == "__main__":
    t = TestTable()
    q = t.query
    # print(t.query)
    # t.query.limit(3, 5)
    # print(t.query)
    # print(q)
    # q.order("updated_at", False)
    # q.add_desired_columns("name", "updated_at").add_where_statements(("attribute_group_id", "<>", 69)).limit(5)
    # print(q)
    # print(q.order('first_id', foreign_table="__HauptfaserMapHinweis").add_join(('__attributes_sandbox', 'id'), ('__HauptfaserMapHinweis', 'first_id')))
    print(q.add_where_statements(column="ids", command="in", value=(1, 2, 3)))
    q.add_where_statements(column="ids", command="in", value=(1, 2, 3), OR=True)
    q.add_where_statements(("col", "=", "value"))
    print(q)
    q.add_where_statements(("col", "=", "value"), ("co1l", "!=", "value2"), OR=True)
    print(q)
