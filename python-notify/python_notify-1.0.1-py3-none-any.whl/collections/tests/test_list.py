import pytest
import unittest.mock as mock

from .. import List


def _list_and_signals_catcher():
    def on_items_added(items, pos):
        pass

    def on_items_changed(past_items, new_items, pos):
        pass

    def on_items_removed(items, pos):
        pass

    def on_items_cleared():
        pass

    mock_manager = mock.Mock()
    mock_manager.attach_mock(mock.create_autospec(on_items_added), 'on_items_added')
    mock_manager.attach_mock(mock.create_autospec(on_items_changed), 'on_items_changed')
    mock_manager.attach_mock(mock.create_autospec(on_items_removed), 'on_items_removed')
    mock_manager.attach_mock(mock.create_autospec(on_items_cleared), 'on_items_cleared')

    obj = List((0, 1, [2], 3, [4]))
    obj.items_added.connect(mock_manager.on_items_added)
    obj.items_changed.connect(mock_manager.on_items_changed)
    obj.items_removed.connect(mock_manager.on_items_removed)
    obj.items_cleared.connect(mock_manager.on_items_cleared)

    return obj, mock_manager


@pytest.fixture
def list_and_signals_catcher():
    return _list_and_signals_catcher()


@pytest.fixture
def list_and_signals_catcher_factory():
    return _list_and_signals_catcher


def test__setitem__notify_item_changed_or_items_added(list_and_signals_catcher_factory):
    obj, signals_catcher = list_and_signals_catcher_factory()
    obj[1] = 11
    signals_catcher.on_items_changed.assert_called_once_with(past_items=(1,), new_items=(11,),
                                                             pos=1)

    obj, signals_catcher = list_and_signals_catcher_factory()
    obj[1] = [11, 11]
    signals_catcher.on_items_changed.assert_called_once_with(past_items=(1,), new_items=([11, 11],),
                                                             pos=1)

    obj, signals_catcher = list_and_signals_catcher_factory()
    obj[2] = 22
    signals_catcher.on_items_changed.assert_called_once_with(past_items=([2],), new_items=(22,),
                                                             pos=2)

    obj, signals_catcher = list_and_signals_catcher_factory()
    obj[2] = [22, 22]
    signals_catcher.on_items_changed.assert_called_once_with(past_items=([2],), new_items=([22, 22],),
                                                             pos=2)

    obj, signals_catcher = list_and_signals_catcher_factory()
    obj[1:3] = [22, [22]]
    signals_catcher.on_items_changed.assert_called_once_with(past_items=(1, [2],), new_items=(22, [22],),
                                                             pos=slice(1, 3, None))

    obj, signals_catcher = list_and_signals_catcher_factory()
    obj[100:102] = [100, 101]
    signals_catcher.on_items_added.assert_called_once_with(items=(100, 101,), pos=5)


def test__delitem__notify_item_removed_or_nothing(list_and_signals_catcher_factory):
    obj, signals_catcher = list_and_signals_catcher_factory()
    del obj[1]
    signals_catcher.on_items_removed.assert_called_once_with(items=(1,), pos=1)

    obj, signals_catcher = list_and_signals_catcher_factory()
    del obj[2]
    signals_catcher.on_items_removed.assert_called_once_with(items=([2],), pos=2)

    obj, signals_catcher = list_and_signals_catcher_factory()
    del obj[1:3]
    signals_catcher.on_items_removed.assert_called_once_with(items=(1, [2],), pos=slice(1, 3, None))

    obj, signals_catcher = list_and_signals_catcher_factory()
    del obj[10:12]
    signals_catcher.on_items_removed.assert_not_called()


def test__iadd__notify_items_added(list_and_signals_catcher):
    obj, signals_catcher = list_and_signals_catcher

    obj += []
    signals_catcher.on_items_added.assert_not_called()

    obj += [5, [6]]
    signals_catcher.on_items_added.assert_called_once_with(items=(5, [6]), pos=5)


def test__imul__notify_items_added(list_and_signals_catcher_factory):
    obj, signals_catcher = list_and_signals_catcher_factory()
    obj *= 0
    signals_catcher.on_items_removed.assert_called_once_with(items=(0, 1, [2], 3, [4]), pos=0)
    signals_catcher.on_items_added.assert_not_called()

    obj, signals_catcher = list_and_signals_catcher_factory()
    obj *= 2
    signals_catcher.on_items_added.assert_called_once_with(items=(0, 1, [2], 3, [4]), pos=5)
    signals_catcher.on_items_removed.assert_not_called()


def test__append__notify_items_added(list_and_signals_catcher):
    obj, signals_catcher = list_and_signals_catcher

    obj.append(4)

    signals_catcher.on_items_added.assert_called_once_with(items=(4,), pos=5)


def test__insert__notify_items_added(list_and_signals_catcher):
    obj, signals_catcher = list_and_signals_catcher

    obj.insert(1, 11)

    signals_catcher.on_items_added.assert_called_once_with(items=(11,), pos=1)


def test__pop__notify_items_removed(list_and_signals_catcher):
    obj, signals_catcher = list_and_signals_catcher

    obj.pop(2)

    signals_catcher.on_items_removed.assert_called_once_with(items=([2],), pos=2)


def test__remove__notify_items_removed(list_and_signals_catcher):
    obj, signals_catcher = list_and_signals_catcher

    obj.remove([2])

    signals_catcher.on_items_removed.assert_called_once_with(items=([2],), pos=2)


def test__clear__notify_items_cleared(list_and_signals_catcher):
    obj, signals_catcher = list_and_signals_catcher

    obj.clear()

    signals_catcher.on_items_cleared.assert_called_once()


def test__extend__notify_items_added(list_and_signals_catcher):
    obj, signals_catcher = list_and_signals_catcher

    obj.extend([1, [1]])

    signals_catcher.on_items_added.assert_called_once_with(items=(1, [1]), pos=5)
