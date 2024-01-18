#!/usr/bin/env python
"""
The main module of notion-recurring-tasks.
"""

import os
from notion_recurring_tasks import notion_api
from notion_recurring_tasks import dataprocessing

from requests import HTTPError

def check_notion_key(key: str | None) -> bool:
    """Check the validity of the given Notion key.

    Args:
        key (str | None): Notion key

    Raises:
        EnvironmentError: If the given key is not valid.

    Returns:
        bool: True if key is valid. False otherwise.
    """
    try:
        if not key:
            raise EnvironmentError("Missing NOTION_KEY environment variable.")
        elif not key.startswith("secret_"):
            raise EnvironmentError("NOTION_KEY environment variable not correct.")
    except EnvironmentError as e:
        print(f"WARNING: {e}")
        return False

    return True

def set_notion_key(key: str) -> None:
    """Sets the NOTION_KEY environment variable.

    Args:
        key (str): Notion key
    """
    with open('.env', 'w') as f:
        f.write("# Notion Recurring Tasks environment variables\n")
        f.write(f"NOTION_KEY = '{key}'")
    
def get_notion_key() -> None:
    """Gets the Notion key from the user. If valid, sets the environment variable.
    """
    while True:
        key = input("Input your Notion key: ")
        if check_notion_key(key):
            set_notion_key(key)
            break

def script() -> None:
    """The notion-recurring-tasks script.
    """
    db_id: str = notion_api.get_db_id()

    tasks: list = notion_api.find_recurrable_tasks(db_id)

    num_updated_tasks: int = 0
    for task in tasks:
        new_due_date = dataprocessing.calc_new_due_date(task)

        try:
            notion_api.update_task_properties(task["id"], new_due_date)
        except HTTPError:
            print(f"Failed to update {task["properties"]["Name"]["title"][0]["plain_text"]}.")
        else:
            num_updated_tasks += 1

    print(f"Updated {num_updated_tasks} tasks.")

def main() -> None:
    """The main function where the program starts.
    """
    if not check_notion_key(os.getenv("NOTION_KEY")):
        get_notion_key()
        
    script()

if __name__ == "__main__":
    main()
