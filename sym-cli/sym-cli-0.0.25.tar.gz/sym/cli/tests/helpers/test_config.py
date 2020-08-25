import json
from uuid import UUID

import pytest

from sym.cli.helpers.config import Config, SymConfigFile
from sym.cli.helpers.contexts import push_env
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def org(sandbox: Sandbox, uuid: UUID) -> str:
    org = uuid.hex
    with sandbox.create_file_with_content(".config/sym/config.yml") as f:
        print(f"org: {org}", file=f)
    return org


def test_get_org_with_xdg_config_home(sandbox: Sandbox, org: str) -> None:
    with push_env("XDG_CONFIG_HOME", str(sandbox.path / ".config")):
        assert Config()["org"] == org


def test_get_org_without_xdg_config_home(sandbox: Sandbox, org: str) -> None:
    with push_env("HOME", str(sandbox.path)):
        assert Config()["org"] == org


def test_sym_config_truncate(sandbox: Sandbox):
    short_json = json.dumps({"hello": "world"})
    long_json = json.dumps({"hello": "world", "foo": "bar"})

    with sandbox.push_xdg_config_home():
        config_file = SymConfigFile(a=1, b=2, file_name="config.json")
        with config_file as f:
            f.write(long_json)
            f.seek(0)
            assert f.read() == long_json
        with config_file as f:
            assert f.read() == long_json
        with config_file as f:
            f.write(short_json)
            f.seek(0)
            assert f.read() == short_json
        with config_file as f:
            assert f.read() == short_json

