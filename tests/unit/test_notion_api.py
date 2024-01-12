#!/usr/bin/env python


import pytest
import os

from requests import HTTPError
from notion_recurring_tasks import notion_api
from notion_recurring_tasks.notion_api import NOTION_API_URL


def test_set_notion_key(notion_key):
    env_key = os.getenv("NOTION_KEY")
    assert env_key == notion_key


def test_headers(notion_key):
    headers = notion_api.get_headers()
    assert headers["Authorization"] == f"Bearer {notion_key}"
    assert headers["Content-Type"] == "application/json"
    assert headers["Notion-Version"] == "2022-06-28"


@pytest.mark.parametrize("response_fixture", ["successful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["post"], indirect=True)
def test_successful_search(response_fixture, spy_fixture):
    PARAMS = {}
    data = notion_api.Calls.search(PARAMS)
    assert data == response_fixture.json.return_value
    spy_fixture.assert_called_once_with(
        f"{NOTION_API_URL}/search", headers=notion_api.get_headers(), json=PARAMS
    )


@pytest.mark.parametrize("response_fixture", ["successful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["post"], indirect=True)
def test_successful_db_query(response_fixture, spy_fixture):
    PARAMS = {}
    data = notion_api.Calls.db_query("db_id", PARAMS)
    assert data == response_fixture.json.return_value
    spy_fixture.assert_called_once_with(
        f"{NOTION_API_URL}/databases/db_id/query",
        headers=notion_api.get_headers(),
        json=PARAMS,
    )


@pytest.mark.parametrize("response_fixture", ["successful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["patch"], indirect=True)
def test_successful_patch_page_properties(response_fixture, spy_fixture):
    PARAMS = {}
    data = notion_api.Calls.patch_page_properties("task_id", PARAMS)
    assert data == response_fixture.json.return_value
    spy_fixture.assert_called_once_with(
        f"{NOTION_API_URL}/pages/task_id",
        headers=notion_api.get_headers(),
        json={"properties": PARAMS},
    )


@pytest.mark.parametrize("response_fixture", ["unsuccessful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["post"], indirect=True)
def test_unsuccessful_search(response_fixture, spy_fixture):
    PARAMS = {}
    with pytest.raises(HTTPError):
        notion_api.Calls.search(PARAMS)
    spy_fixture.assert_called_once()


@pytest.mark.parametrize("response_fixture", ["unsuccessful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["post"], indirect=True)
def test_unsuccessful_db_query(response_fixture, spy_fixture):
    PARAMS = {}
    with pytest.raises(HTTPError):
        notion_api.Calls.db_query("db_id", PARAMS)
    spy_fixture.assert_called_once()


@pytest.mark.parametrize("response_fixture", ["unsuccessful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["patch"], indirect=True)
def test_unsuccessful_patch_page_properties(response_fixture, spy_fixture):
    PARAMS = {}
    with pytest.raises(HTTPError):
        notion_api.Calls.patch_page_properties("task_id", PARAMS)
    spy_fixture.assert_called_once()


@pytest.mark.parametrize("search_return", ["good"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["search"], indirect=True)
def test_get_db_id_success(search_return, spy_fixture):
    SEARCH_PARAMS: dict = {"filter": {"value": "database", "property": "object"}}
    id = notion_api.get_db_id()
    spy_fixture.assert_called_with(SEARCH_PARAMS)
    assert id == search_return["results"][0]["id"]


@pytest.mark.parametrize("search_return", ["bad"], indirect=True)
def test_get_db_id_fail(search_return):
    with pytest.raises(ValueError):
        notion_api.get_db_id()


@pytest.mark.parametrize("spy_fixture", ["db_query"], indirect=True)
def test_find_recurrable_tasks(db_query_return, spy_fixture):
    TASK_FILTERS: dict = {
        "filter": {
            "and": [
                {
                    "property": "Recurring",
                    "checkbox": {"equals": True},
                },
                {
                    "property": "Status",
                    "status": {"equals": "Done"},
                },
                {
                    "property": "Archived",
                    "checkbox": {"equals": False},
                },
            ]
        },
    }
    tasks = notion_api.find_recurrable_tasks("db_id")
    spy_fixture.assert_called_once_with("db_id", TASK_FILTERS)
    assert isinstance(tasks, list)


@pytest.mark.parametrize("response_fixture", ["successful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["patch_page_properties"], indirect=True)
def test_update_task_properties_no_due(response_fixture, spy_fixture):
    notion_api.update_task_properties("task_id", None)
    NEW_PROPERTIES = {
        "Due Date": {"date": None},
        "Status": {"status": {"name": "Not started"}},
    }
    spy_fixture.assert_called_once_with("task_id", NEW_PROPERTIES)


@pytest.mark.parametrize("response_fixture", ["successful"], indirect=True)
@pytest.mark.parametrize("spy_fixture", ["patch_page_properties"], indirect=True)
def test_update_task_properties_new_due(response_fixture, spy_fixture):
    notion_api.update_task_properties("task_id", "2024-01-01")
    NEW_PROPERTIES = {
        "Due Date": {"date": {"start": "2024-01-01"}},
        "Status": {"status": {"name": "Not started"}},
    }
    spy_fixture.assert_called_once_with("task_id", NEW_PROPERTIES)
