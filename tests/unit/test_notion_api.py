#!/usr/bin/env python


import os
from notion_recurring_tasks import notion_api


def test_set_notion_key(notion_key):
    env_key = os.getenv("NOTION_KEY")
    assert env_key == notion_key


def test_headers(notion_key):
    headers = notion_api.get_headers()
    assert headers["Authorization"] == f"Bearer {notion_key}"
    assert headers["Content-Type"] == "application/json"
    assert headers["Notion-Version"] == "2022-06-28"
