#!/usr/bin/env python

import pytest
from notion_recurring_tasks.main import main

TEST_TASKS = [
    [],
    [
        {
            "id": "task_id",
            "properties": {
                "Name": {"title": [{"plain_text": "Test Task"}]},
                "Due Date": {"date": None},
                "RecurInterval": {"number": None},
                "RecurUnit": {"select": None},
            },
        },
    ],
    [
        {
            "id": "fail_task_id",
            "properties": {
                "Name": {"title": [{"plain_text": "Failed Task"}]},
                "Due Date": {"date": None},
                "RecurInterval": {"number": None},
                "RecurUnit": {"select": None},
            },
        },
    ],
]


@pytest.mark.parametrize("response_fixture", ["successful"], indirect=True)
@pytest.mark.parametrize("search_return", ["good"], indirect=True)
@pytest.mark.parametrize("db_query_return", [TEST_TASKS[0]], indirect=True)
def test_no_tasks_to_update(response_fixture, search_return, db_query_return, capsys):
    main()
    cap = capsys.readouterr()
    assert cap.out.strip() == "Updated 0 tasks."


@pytest.mark.parametrize("response_fixture", ["successful"], indirect=True)
@pytest.mark.parametrize("search_return", ["good"], indirect=True)
@pytest.mark.parametrize("db_query_return", [TEST_TASKS[1]], indirect=True)
def test_updating_tasks(response_fixture, search_return, db_query_return, capsys):
    main()
    cap = capsys.readouterr()
    assert cap.out.strip() == "Updated 1 tasks."


@pytest.mark.parametrize("response_fixture", ["unsuccessful"], indirect=True)
@pytest.mark.parametrize("search_return", ["good"], indirect=True)
@pytest.mark.parametrize("db_query_return", [TEST_TASKS[2]], indirect=True)
def test_fail_updating_task(response_fixture, search_return, db_query_return, capsys):
    main()
    cap = capsys.readouterr().out.split("\n")
    assert cap[0].strip() == "Failed to update Failed Task."
    assert cap[1].strip() == "Updated 0 tasks."
