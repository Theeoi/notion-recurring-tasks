#!/usr/bin/env python

import pytest


@pytest.fixture(scope="function")
def notion_key(monkeypatch):
    TESTING_KEY = "secret_testing_key"
    monkeypatch.setenv("NOTION_KEY", TESTING_KEY)
    return TESTING_KEY
