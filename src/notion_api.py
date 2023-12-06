#!/usr/bin/env python
"""notion_api.py

Code related to the interaction with the Notion API.
"""


import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_URL: str = "https://api.notion.com/v1"
HEADERS: dict[str, str] = {
    "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


class Calls:
    """
    Gathers the available API calls. \\
    All methods return the response in json-format and raises an HTTPError if unsuccesful.
    """

    @staticmethod
    def search(params: dict) -> dict:
        """Performs a search query with the given params.

        Args:
            params (dict): Input parameters for the search query.

        Raises:
            HTTPError: If API call is unsuccessful.

        Returns:
            dict: Response data in json format.
        """
        response = requests.post(
            f"{NOTION_API_URL}/search", headers=HEADERS, json=params
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def db_query(db_id: str, params: dict) -> dict:
        """Query a Notion database with a given id.

        Args:
            db_id (str): Notion database id.
            params (dict): Input parameters for the query.

        Raises:
            HTTPError: If API call is unsuccessful.

        Returns:
            dict: Response data in json format.
        """
        response = requests.post(
            f"{NOTION_API_URL}/databases/{db_id}/query", headers=HEADERS, json=params
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def patch_page_properties(page_id: str, new_properties: dict) -> dict:
        """Patch (update) a page with new properties.

        Args:
            page_id (str): Notion page id
            new_properties (dict): New properties to add to page

        Raises:
            HTTPError: If API call is unsuccessful

        Returns:
            dict: Response data in json format
        """
        properties = {"properties": new_properties}
        response = requests.patch(
            f"{NOTION_API_URL}/pages/{page_id}", headers=HEADERS, json=properties
        )
        response.raise_for_status()
        return response.json()


def get_db_id() -> str:
    """Gets id of Tasks database.

    Raises:
        ValueError: If database id was not found.

    Returns:
        str: The database id
    """
    SEARCH_PARAMS: dict = {"filter": {"value": "database", "property": "object"}}

    results: list[dict] = Calls.search(SEARCH_PARAMS)["results"]

    if results[0]["object"] != "database":
        # User may have not created the connection in the database
        raise ValueError("Database not found..")

    return results[0]["id"]


def find_recurrable_tasks(db_id: str) -> list:
    """Finds all tasks that are due to recur from the database.

    Args:
        db_id (str): The id of the database to be queried.

    Returns:
        list: List of all tasks found.
    """
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

    data = Calls.db_query(db_id, TASK_FILTERS)

    return data["results"]


def update_task_properties(task_id: str, new_due_date: str | None) -> None:
    """Reset the task and set a new due date if provided.

    Args:
        task_id (str): The id of the task
        new_due_date (str | None): The new due date to set in ISO-format 'YYYY-MM-DD'
    """
    new_properties: dict = {}

    ## Set due date
    if new_due_date:
        new_properties["Due Date"] = {
            "date": {
                "start": new_due_date,
            }
        }
    else:
        new_properties["Due Date"] = {
            "date": None,
        }

    ## Set status
    new_properties["Status"] = {
        "status": {
            "name": "Not started",
        }
    }

    Calls.patch_page_properties(task_id, new_properties)
