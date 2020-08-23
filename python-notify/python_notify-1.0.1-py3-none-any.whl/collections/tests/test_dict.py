import pytest
import unittest.mock as mock

from .. import Dict


def _dict_and_signals_catcher():
    def on_key_added(key, item):
        pass

    def on_key_changed(key, past_item, new_item):
        pass

    def on_key_removed(key):
        pass

    mock_manager = mock.Mock()
    mock_manager.attach_mock(mock.create_autospec(on_key_added), 'on_key_added')
    mock_manager.attach_mock(mock.create_autospec(on_key_changed), 'on_key_changed')
    mock_manager.attach_mock(mock.create_autospec(on_key_removed), 'on_key_removed')

    obj = Dict(a=1, b=[2])
    obj.key_added.connect(mock_manager.on_key_added)
    obj.key_changed.connect(mock_manager.on_key_changed)
    obj.key_removed.connect(mock_manager.on_key_removed)

    return obj, mock_manager


@pytest.fixture
def dict_and_signals_catcher():
    return _dict_and_signals_catcher()


@pytest.fixture
def dict_and_signals_catcher_factory():
    return _dict_and_signals_catcher


def test__setitem__notify_key_added(dict_and_signals_catcher):
    """
    Notify key_added when use __setitem__ with missing key.
    """
    obj, signals_catcher = dict_and_signals_catcher

    obj['new'] = 1

    signals_catcher.on_key_added.assert_called_once_with(key='new', item=1)


def test__setitem__notify_key_changed(dict_and_signals_catcher):
    """
    Notify key_changed when use __setitem__ with existing key.
    """
    obj, signals_catcher = dict_and_signals_catcher

    obj['a'] = 'new_value'

    signals_catcher.on_key_changed.assert_called_once_with(key='a', past_item=1, new_item='new_value')


def test__delitem__notify_key_removed(dict_and_signals_catcher):
    """
    Notify key_removed when use __delitem__ with existing key.
    """
    obj, signals_catcher = dict_and_signals_catcher

    del obj['a']

    signals_catcher.on_key_removed.assert_called_once_with(key='a')
