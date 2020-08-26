from toolkit.behaviour.command import Command


def do_task():
    return NotImplemented


def test_command():
    command = Command(cmd=do_task, rank=1, group='Test', label='TestCommand')
    assert command.rank == 1
    assert command.group == 'Test'
    assert command.cmd == do_task
    assert command.label == 'TestCommand'
    assert callable(command)
    assert command() == NotImplemented
