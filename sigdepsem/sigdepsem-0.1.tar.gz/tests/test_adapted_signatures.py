import pytest


@pytest.fixture
def C_class(decorator, meta):
    @decorator
    class C(metaclass=meta):
        def __init__(self, name):
            self.name = name
        def __getitem__(self, x, y, z):
            return f"{x, y, z}"
        def __setitem__(self, value, x, y, z):
            self.set = f"{self.name}[{x, y, z}] = {value}"
        def __delitem__(self, x, y, z):
            self.del_ = f"del {self.name}[{x, y, z}]"
    return C


@pytest.fixture
def c(C_class):
    return C_class("c")


@pytest.fixture
def args():
    return 1,2,3


@pytest.fixture
def value():
    return "foo"


@pytest.fixture
def c_set(c, args, value):
    c[args] = value
    return c


@pytest.fixture
def c_del(c, args):
    del c[args]
    return c


def test_getitem(c, args):
    assert c[args] == f"{(*args,)}"


def test_setitem(c_set, args, value):
    assert c_set.set == f"{c_set.name}[{(*args,)}] = {value}"


def test_delitem(c_del, args):
    assert c_del.del_ == f"del {c_del.name}[{(*args,)}]"
