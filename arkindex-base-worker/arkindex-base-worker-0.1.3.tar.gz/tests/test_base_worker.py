# -*- coding: utf-8 -*-
import logging
import os
import sys
from pathlib import Path

import pytest

from arkindex_worker import logger
from arkindex_worker.worker import BaseWorker


def test_init_default_local_share():
    worker = BaseWorker()

    assert worker.work_dir == os.path.expanduser("~/.local/share/arkindex")
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_default_xdg_data_home(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("XDG_DATA_HOME", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/arkindex"
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_var_ponos_data_given(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("PONOS_DATA", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/current"
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_var_worker_version_id_missing(monkeypatch):
    monkeypatch.delenv("WORKER_VERSION_ID")
    with pytest.raises(Exception) as e:
        BaseWorker()
    assert (
        str(e.value)
        == "Missing WORKER_VERSION_ID environment variable to start the Worker"
    )


def test_cli_default(mocker):
    worker = BaseWorker()
    spy = mocker.spy(worker, "add_arguments")
    assert not spy.called
    assert logger.level == logging.NOTSET
    assert not hasattr(worker, "api_client")
    worker.configure()

    assert spy.called
    assert spy.call_count == 1
    assert not worker.args.verbose
    assert logger.level == logging.NOTSET
    assert worker.api_client

    logger.setLevel(logging.NOTSET)


def test_cli_arg_verbose_given(mocker):
    worker = BaseWorker()
    spy = mocker.spy(worker, "add_arguments")
    assert not spy.called
    assert logger.level == logging.NOTSET
    assert not hasattr(worker, "api_client")

    mocker.patch.object(sys, "argv", ["worker", "-v"])
    worker.configure()

    assert spy.called
    assert spy.call_count == 1
    assert worker.args.verbose
    assert logger.level == logging.DEBUG
    assert worker.api_client

    logger.setLevel(logging.NOTSET)
