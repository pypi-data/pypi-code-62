# -*- coding: utf-8 -*-
import os

import pytest


@pytest.fixture(autouse=True)
def pass_schema(responses):
    schema_url = os.environ.get("ARKINDEX_API_SCHEMA_URL")
    responses.add_passthru(schema_url)


@pytest.fixture(autouse=True)
def give_worker_version_id_env_variable(monkeypatch):
    monkeypatch.setenv("WORKER_VERSION_ID", "12341234-1234-1234-1234-123412341234")
