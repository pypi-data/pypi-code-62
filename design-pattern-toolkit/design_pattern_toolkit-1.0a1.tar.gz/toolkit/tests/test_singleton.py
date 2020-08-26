from toolkit.creation.singleton import Singleton


class A(metaclass=Singleton):
    pass


def test_singleton():
    a = A()
    b = A()
    assert a is b
    assert id(a) == id(b)
