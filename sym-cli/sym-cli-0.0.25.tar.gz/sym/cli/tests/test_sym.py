from contextlib import contextmanager

import pytest

from sym.cli.helpers.config import Config
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.sandbox import Sandbox


def test_login(click_setup):
    with click_setup(set_org=False) as runner:
        result = runner.invoke(
            click_command, ["login", "--org", "sym", "--email", "y@symops.io"]
        )
        assert result.exit_code == 0
        assert result.output == "Sym successfully initalized!\n"


def test_resources(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["resources"])
        assert result.exit_code == 0
        assert result.output == "test (Test)\n"


def test_ssh(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["exec", "test", "--", "aws"])
        assert result.exit_code == 0
