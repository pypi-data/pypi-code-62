from toolkit.creation.factory import Factory


class ATest:
    pass


def test_factory():
    Factory.register(product='A', definition={'do_task': lambda: NotImplemented})
    a = Factory.produce('A')
    b = Factory.produce('A')
    Factory.register(product=ATest)
    c = Factory.produce(ATest.__qualname__)
    assert 'A' in Factory.cache
    assert ATest.__qualname__ in Factory.cache
    assert isinstance(a, object)
    assert isinstance(b, object)
    assert isinstance(c, ATest)


