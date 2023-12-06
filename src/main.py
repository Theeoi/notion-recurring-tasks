#!/usr/bin/env python
"""main.py

The main module of notion-recurring-tasks.
"""

import dataprocessing
import notion_api
from requests import HTTPError


def main() -> None:
    """The main function where the program starts.
    """
    db_id: str = notion_api.get_db_id()

    tasks: list = notion_api.find_recurrable_tasks(db_id)

    num_updated_tasks: int = 0
    for task in tasks:
        new_due_date = dataprocessing.calc_new_due_date(task)

        try:
            notion_api.update_task_properties(task["id"], new_due_date)
        except HTTPError:
            print(f"Failed to update {task["properties"]["Name"]["title"][0]["plain_text"]}")
        else:
            num_updated_tasks += 1

    print(f"Updated {num_updated_tasks} tasks.")


if __name__ == "__main__":
    main()
