#!/usr/bin/env python
"""dataprocessing.py

Module for processing task data. 
"""

from datetime import date
from dateutil.relativedelta import relativedelta


def get_task_properties(task: dict) -> dict:
    """Get properties of a task.

    Args:
        task (dict): A task as returned by the Notion API.

    Returns:
        dict: Task properties in a easily parsable format.
    """

    def get_due_date(prop: dict) -> date | None:
        """Get the due date property.

        Args:
            prop (dict): Task property dictionary.

        Returns:
            date | None: Task due date in datetime.date format
        """
        try:
            return date.fromisoformat(prop["Due Date"]["date"]["start"])
        except TypeError:
            return prop["Due Date"]["date"]

    def get_recur_interval(prop: dict) -> int:
        """Get the recur interval property.

        Args:
            prop (dict): Task property dictionary.

        Returns:
            int: Task RecurInterval
        """
        return prop["RecurInterval"]["number"]

    def get_recur_unit(prop: dict) -> str | None:
        """Get the recur interval property.

        Args:
            prop (dict): Task property dictionary.

        Returns:
            str | None: Task RecurUnit
        """
        try:
            return prop["RecurUnit"]["select"]["name"]
        except TypeError:
            return prop["RecurUnit"]["select"]

    properties: dict = {}
    prop: dict = task["properties"]

    properties["due_date"] = get_due_date(prop)
    properties["recur_interval"] = get_recur_interval(prop)
    properties["recur_unit"] = get_recur_unit(prop)

    return properties


def calc_new_due_date(task: dict) -> str | None:
    """Calculate new due date from current task properties.

    Args:
        task (dict): A task as returned by the Notion API.

    Returns:
        str | None: _description_
    """
    props: dict = get_task_properties(task)

    if not props["due_date"]:
        return None
    elif not props["recur_interval"] or not props["recur_unit"]:
        return str(props["due_date"])
    else:
        match props["recur_unit"]:
            case "Days":
                return str(props["due_date"] + relativedelta(days=+props["recur_int"]))
            case "Weeks":
                return str(props["due_date"] + relativedelta(weeks=+props["recur_int"]))
            case "Months":
                return str(
                    props["due_date"] + relativedelta(months=+props["recur_int"])
                )
            case "Years":
                return str(props["due_date"] + relativedelta(years=+props["recur_int"]))
            case _:
                return str(props["due_date"])
