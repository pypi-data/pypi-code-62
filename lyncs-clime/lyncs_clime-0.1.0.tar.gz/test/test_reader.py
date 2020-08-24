import sys
import pytest
from lyncs_clime import Reader
from lyncs_clime.reader import main


def test_reader():
    reader = Reader("test/conf.unity")

    records = tuple(reader)
    assert len(reader) == len(records)
    assert "precision" in str(reader)
    for rec in records:
        if rec["nbytes"] > reader.max_bytes:
            assert "data" not in rec

    reader.max_bytes = max([rec["nbytes"] for rec in records])
    assert all(("data" in rec for rec in reader))
    assert "[Binary data]" in str(reader)

    with reader as fp:
        assert list(fp) == list(reader)

    with pytest.raises(RuntimeError):
        reader.close()
    with pytest.raises(RuntimeError):
        reader.next()


def test_with():
    with Reader("test/conf.unity") as reader:
        list(reader)


def test_main():
    sys.argv = ["foo", "test/conf.unity"]
    assert str(Reader("test/conf.unity")) == main()
