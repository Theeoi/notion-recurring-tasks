#!/usr/bin/env python

import pytest
import requests
from requests import HTTPError

from notion_recurring_tasks import notion_api


@pytest.fixture(scope="session", autouse=True)
def notion_key(session_mocker):
    TESTING_KEY = "secret_testing_key"
    session_mocker.patch.dict("os.environ", {"NOTION_KEY": TESTING_KEY})
    return TESTING_KEY


@pytest.fixture(scope="function")
def spy_fixture(mocker, request):
    TARGET = {
        "post": requests,
        "patch": requests,
        "search": notion_api.Calls,
        "db_query": notion_api.Calls,
        "patch_page_properties": notion_api.Calls,
    }.get(request.param)
    return mocker.spy(TARGET, request.param)


@pytest.fixture(scope="function")
def response_fixture(mocker, request):
    match request.param:
        case "successful":
            RESPONSE = mocker.Mock(
                name="successful_response",
                **{"status_code": 200, "json.return_value": {}},
            )
        case "unsuccessful":
            RESPONSE = mocker.Mock(
                name="unsuccessful_response",
                **{"status_code": 404, "json.return_value": {}},
                raise_for_status=mocker.Mock(side_effect=HTTPError()),
            )
        case _:
            raise NotImplementedError

    mocker.patch("requests.post", return_value=RESPONSE)
    mocker.patch("requests.patch", return_value=RESPONSE)
    return RESPONSE


@pytest.fixture(scope="function")
def search_return(mocker, request):
    match request.param:
        case "good":
            MOCK_RETURN = {"results": [{"object": "database", "id": "db_id"}]}
        case "bad":
            MOCK_RETURN = {"results": [{"object": "not_database", "id": "db_id"}]}
        case _:
            raise NotImplementedError

    mocker.patch(
        "notion_recurring_tasks.notion_api.Calls.search", return_value=MOCK_RETURN
    )

    return MOCK_RETURN


@pytest.fixture(scope="function")
def db_query_return(mocker, request):
    if hasattr(request, "param"):
        RESULTS = request.param
    else:
        RESULTS = []
    MOCK_RETURN = {"results": RESULTS}
    mocker.patch(
        "notion_recurring_tasks.notion_api.Calls.db_query", return_value=MOCK_RETURN
    )
    return MOCK_RETURN


@pytest.fixture()
def task_properties(request):
    PROPERTIES_STRUCTURE = {
        "properties": {
            "Due Date": {"date": None},
            "RecurInterval": {"number": None},
            "RecurUnit": {"select": None},
        },
        "expected": {
            "props": {
                "due_date": None,
                "recur_interval": None,
                "recur_unit": None,
            },
            "due_date": None,
        },
    }

    INPUT = request.param["input"]
    EXPECTED = request.param["expected"]

    PROPERTIES_STRUCTURE["expected"]["props"].update(INPUT)
    PROPERTIES_STRUCTURE["expected"].update(EXPECTED)

    if INPUT["due_date"]:
        PROPERTIES_STRUCTURE["properties"]["Due Date"]["date"] = {
            "start": INPUT["due_date"]
        }
    if INPUT["recur_interval"]:
        PROPERTIES_STRUCTURE["properties"]["RecurInterval"]["number"] = INPUT[
            "recur_interval"
        ]
    if INPUT["recur_unit"]:
        PROPERTIES_STRUCTURE["properties"]["RecurUnit"]["select"] = {
            "name": INPUT["recur_unit"]
        }

    return PROPERTIES_STRUCTURE
