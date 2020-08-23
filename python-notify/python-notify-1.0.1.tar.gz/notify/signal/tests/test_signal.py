import pytest
import unittest.mock as mock

from notify.signal.signal import Signal
from notify.signal.tests.conftest import wrong_signature_slots, no_args_slot, correct_names_and_args_slot
from notify.exceptions import WrongSignalNotifyArgs, InvalidSlotSignature, CantConnectSameCallbackTwice


class SignalsKeeper:
    no_args_signal = Signal()
    args_signal = Signal(arg_1=int, arg_2=int)


def test_call_slots_in_connection_order():
    """
    The slots are called in the order in which the connection occurred earlier.
    """
    obj = SignalsKeeper()
    signal = obj.no_args_signal

    mock_manager = mock.Mock()
    mock_manager.attach_mock(mock.create_autospec(no_args_slot), 'slot_1')
    mock_manager.attach_mock(mock.create_autospec(no_args_slot), 'slot_2')
    signal.connect(mock_manager.slot_1)
    signal.connect(mock_manager.slot_2)

    signal.notify()

    expected_calls = [mock.call.slot_1(), mock.call.slot_2()]
    assert mock_manager.method_calls == expected_calls


def test_dispatch_connections_between_objects():
    """
    Connections from one object do not affect the connections of another and are processed in isolation.
    """
    obj_1 = SignalsKeeper()
    obj_2 = SignalsKeeper()
    slot_1 = mock.create_autospec(no_args_slot)
    slot_2 = mock.create_autospec(no_args_slot)
    obj_1.no_args_signal.connect(slot_1)
    obj_2.no_args_signal.connect(slot_2)

    obj_1.no_args_signal.notify()
    slot_1.assert_called_once()
    slot_2.assert_not_called()

    slot_1.reset_mock()
    slot_2.reset_mock()

    obj_2.no_args_signal.notify()
    slot_1.assert_not_called()
    slot_2.assert_called_once()


def test_connection_does_not_make_slot_owner_alive():
    """
    Storing a slot does not increase the reference count of the associated object,
    thus, the object will not remain in memory just because its slot is subscribed to some signal."""
    obj = SignalsKeeper()
    slot_obj = mock.Mock()
    mock_1 = mock.Mock()
    slot_obj.slot = lambda: mock_1()
    obj.no_args_signal.connect(slot_obj.slot)

    del slot_obj
    obj.no_args_signal.notify()

    mock_1.assert_not_called()


def test_unnamed_unsaved_function():
    """
    connect() lambda to signal does not increase the reference count to it and if at the time of calling notify()
    no one else refers to it; it will not be called. it has already been destroyed by the garbage collector.
    """
    obj = SignalsKeeper()
    mock_1 = mock.Mock()
    obj.no_args_signal.connect(lambda: mock_1())

    obj.no_args_signal.notify()

    mock_1.assert_not_called()


def test_can_disconnect_via_connection():
    """
    connect() returns connection object with able to disconnect using them.
    """
    obj = SignalsKeeper()
    mock_1 = mock.create_autospec(no_args_slot)
    connection = obj.no_args_signal.connect(mock_1)

    connection.disconnect()
    obj.no_args_signal.notify()

    mock_1.assert_not_called()


def test_disconnect_all():
    """
    Disconnect all slots using one call.
    """
    obj = SignalsKeeper()
    slot_1 = mock.create_autospec(no_args_slot)
    slot_2 = mock.create_autospec(no_args_slot)
    obj.no_args_signal.connect(slot_1)
    obj.no_args_signal.connect(slot_2)

    obj.no_args_signal.disconnect_all()
    obj.no_args_signal.notify()

    slot_1.assert_not_called()
    slot_2.assert_not_called()


def test_disconnect_explicit_slot():
    """
    Disconnecting one slot does not affect calls to others.
    """
    obj = SignalsKeeper()
    slot_1 = mock.create_autospec(no_args_slot)
    slot_2 = mock.create_autospec(no_args_slot)
    obj.no_args_signal.connect(slot_1)
    obj.no_args_signal.connect(slot_2)

    obj.no_args_signal.disconnect(slot_1)
    obj.no_args_signal.notify()

    slot_1.assert_not_called()
    slot_2.assert_called_once()


def test_disconnect_during_notify():
    """
    Disconnecting any of the slots during the notification process will trigger that slot,
    but it will not called in the next notification processes.
    """
    obj = SignalsKeeper()
    mock_1 = mock.Mock()
    mock_2 = mock.Mock()
    mock_3 = mock.Mock()

    def slot_2():
        mock_2('slot_2')

    def slot_1():
        mock_1('slot_1')
        obj.no_args_signal.disconnect(slot_2)

    def slot_3():
        mock_3('slot_3')

    obj.no_args_signal.connect(slot_1)
    obj.no_args_signal.connect(slot_2)
    obj.no_args_signal.connect(slot_3)

    obj.no_args_signal.notify()

    mock_1.assert_called_once_with('slot_1')
    mock_2.assert_called_once_with('slot_2')
    mock_3.assert_called_once_with('slot_3')

    mock_1.reset_mock(), mock_2.reset_mock(), mock_3.reset_mock()

    obj.no_args_signal.notify()

    mock_1.assert_called_once_with('slot_1')
    mock_2.assert_not_called()
    mock_3.assert_called_once_with('slot_3')


def test_cant_call_notify_with_wrong_args():
    """
    The arguments passed to notify should match signal signature.
    """
    obj = SignalsKeeper()

    with pytest.raises(WrongSignalNotifyArgs):
        obj.no_args_signal.notify(1)

    with pytest.raises(WrongSignalNotifyArgs):
        obj.args_signal.notify()
    with pytest.raises(WrongSignalNotifyArgs):
        obj.args_signal.notify(1)
    with pytest.raises(WrongSignalNotifyArgs):
        obj.args_signal.notify(1, 2, 3)
    with pytest.raises(WrongSignalNotifyArgs):
        obj.args_signal.notify(arg_1=1, unexpected=2)


def test_connect_match_signature():
    """
    A successful connection requires matching names and transfer method pos or keyword.
    """
    obj = SignalsKeeper()

    assert obj.no_args_signal.connect(no_args_slot)
    assert obj.args_signal.connect(correct_names_and_args_slot)

    def correct_arg_slot_with_different_type_hints(arg_1: str, arg_2: str):
        pass
    assert obj.args_signal.connect(correct_arg_slot_with_different_type_hints)

    def correct_arg_slot_without_type_hints(arg_1, arg_2):
        pass
    assert obj.args_signal.connect(correct_arg_slot_without_type_hints)


def test_connect_cant_connect_same_callback_twice():
    """
    Can not connect same slot twice.
    """
    obj = SignalsKeeper()
    mock_1 = mock.Mock()

    def slot():
        mock_1('slot')
    obj.no_args_signal.connect(slot)

    with pytest.raises(CantConnectSameCallbackTwice):
        obj.no_args_signal.connect(slot)

    obj.no_args_signal.notify()
    mock_1.assert_called_once_with('slot')


def test_connect_slot_connected_during_notify_handling_will_not_receive_current_notify():
    """
    Connecting any of the slots during the notification process will not trigger that slot,
    but it will called in the next notification processes.
    """
    obj = SignalsKeeper()
    mock_1 = mock.Mock()
    mock_2 = mock.Mock()
    mock_3 = mock.Mock()

    is_first_time = True

    def slot_1():
        mock_1('slot_1')
        nonlocal is_first_time
        if is_first_time:
            obj.no_args_signal.connect(slot_2)
            is_first_time = False

    def slot_2():
        mock_2('slot_2')

    def slot_3():
        mock_3('slot_3')

    obj.no_args_signal.connect(slot_1)
    obj.no_args_signal.connect(slot_3)

    obj.no_args_signal.notify()
    mock_1.assert_called_once_with('slot_1')
    mock_2.assert_not_called()
    mock_3.assert_called_once_with('slot_3')

    mock_1.reset_mock(), mock_2.reset_mock(), mock_3.reset_mock()

    obj.no_args_signal.notify()
    mock_1.assert_called_once_with('slot_1')
    mock_2.assert_called_once_with('slot_2')
    mock_3.assert_called_once_with('slot_3')


@pytest.mark.parametrize('slot', wrong_signature_slots())
@pytest.mark.parametrize('signal', (SignalsKeeper().no_args_signal, SignalsKeeper().args_signal))
def test_check_slot_args_signature(signal, slot):
    """
    raise InvalidSlotSignature if slot signal does not match signals'.
    """
    with pytest.raises(InvalidSlotSignature):
        signal.connect(slot)
