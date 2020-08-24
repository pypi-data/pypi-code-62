"""
tests the clickRepl.py file
"""
import click
from game_hub.clickRepl import ClickCompleter
from prompt_toolkit.document import Document


def test_one() -> None:
    """filler"""
    @click.group()
    def root_command() -> None:
        """filler"""
        pass

    @root_command.command()
    @click.argument("handler", type=click.Choice(["foo", "bar"]))
    def arg_cmd() -> None:
        """filler"""
        pass

    c = ClickCompleter(root_command)
    completions = list(c.get_completions(Document(u"arg_cmd ")))

    assert set(x.text for x in completions) == {u"arg-cmd"}


def test_two() -> None:
    """filler"""
    @click.group()
    def root_command() -> None:
        """filler"""
        pass

    @root_command.group()
    def first_level_command() -> None:
        """filler"""
        pass

    @first_level_command.command()
    def second_level_command_one() -> None:
        """filler"""
        pass

    @first_level_command.command()
    def second_level_command_two() -> None:
        """filler"""
        pass

    c = ClickCompleter(root_command)
    completions = list(c.get_completions(Document(u"first_level_command ")))

    assert set(x.text for x in completions) == {'first-level-command'}


def test_three() -> None:
    """filler"""
    @click.group()
    def foo_group() -> None:
        """filler"""
        pass

    @foo_group.command()
    def foo_cmd() -> None:
        """filler"""
        pass

    @click.group()
    def foobar_group() -> None:
        """filler"""
        pass

    @foobar_group.command()
    def foobar_cmd() -> None:
        """filler"""
        pass

    c = ClickCompleter(click.CommandCollection(sources=[foo_group, foobar_group]))
    completions = list(c.get_completions(Document(u"foo")))

    assert set(x.text for x in completions) == {'foobar-cmd', 'foo-cmd'}
