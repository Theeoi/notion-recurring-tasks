#!/usr/bin/env python

import os
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
from requests import Response

from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_db_id() -> str:
    SEARCH_PARAMS: dict = {"filter": {"value": "database", "property": "object"}}

    response: Response = requests.post(
        "https://api.notion.com/v1/search", json=SEARCH_PARAMS, headers=HEADERS
    )
    results: list = response.json()["results"]
    if results[0]["object"] != "database":
        # User may have not created the connection in the database
        raise ValueError("Database not found..")

    return results[0]["id"]


def get_tasks_to_recur(db_id: str) -> list:
    SEARCH_PARAMS: dict = {
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

    response = requests.post(
        f"https://api.notion.com/v1/databases/{db_id}/query",
        json=SEARCH_PARAMS,
        headers=HEADERS,
    )
    return response.json()["results"]


def get_task_properties(task: dict) -> dict:
    def get_due_date(prop: dict) -> date | None:
        try:
            return date.fromisoformat(prop["Due Date"]["date"]["start"])
        except TypeError:
            return prop["Due Date"]["date"]

    def get_recur_interval(prop: dict) -> int:
        return prop["RecurInterval"]["number"]

    def get_recur_unit(prop: dict) -> str | None:
        try:
            return prop["RecurUnit"]["select"]["name"]
        except TypeError:
            return prop["RecurUnit"]["select"]

    properties = {}
    prop = task["properties"]

    properties["due_date"] = get_due_date(prop)
    properties["recur_interval"] = get_recur_interval(prop)
    properties["recur_unit"] = get_recur_unit(prop)

    return properties


def update_task_properties(task_id: str, new_due_date: str | None) -> Response:
    NEW_PROPERTIES: dict = {}
    if new_due_date:
        NEW_PROPERTIES["Due Date"] = {
            "date": {
                "start": new_due_date,
            }
        }
    else:
        NEW_PROPERTIES["Due Date"] = {
            "date": None,
        }
    NEW_PROPERTIES["Status"] = {
        "status": {
            "name": "Not started",
        }
    }

    JSON_DATA: dict = {"properties": NEW_PROPERTIES}

    response: Response = requests.patch(
        f"https://api.notion.com/v1/pages/{task_id}",
        json=JSON_DATA,
        headers=HEADERS,
    )

    return response


def main() -> None:
    db_id: str = get_db_id()

    tasks = get_tasks_to_recur(db_id)

    num_updated_tasks = 0
    for task in tasks:
        task_id = task["id"]
        props = get_task_properties(task)

        new_due_date = None
        if props["due_date"]:
            if not props["recur_interval"] or not props["recur_unit"]:
                new_due_date = str(props["due_date"])
            else:
                old_due_date: date = props["due_date"]
                recur_int = props["recur_interval"]
                recur_unit = props["recur_unit"]
                match recur_unit:
                    case "Days":
                        new_due_date = str(
                            old_due_date + relativedelta(days=+recur_int)
                        )
                    case "Weeks":
                        new_due_date = str(
                            old_due_date + relativedelta(weeks=+recur_int)
                        )
                    case "Months":
                        new_due_date = str(
                            old_due_date + relativedelta(months=+recur_int)
                        )
                    case "Years":
                        new_due_date = str(
                            old_due_date + relativedelta(years=+recur_int)
                        )

        response: Response = update_task_properties(task_id, new_due_date)
        if response.status_code == requests.codes.ok:
            num_updated_tasks += 1
        else:
            print(f"Failed to update {task_id=}")

    print(f"Updated {num_updated_tasks} tasks.")


if __name__ == "__main__":
    main()
