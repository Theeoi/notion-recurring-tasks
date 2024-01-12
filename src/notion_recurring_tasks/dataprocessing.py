#!/usr/bin/env python
"""
Module for processing task data. 
"""

from datetime import date
from typing import Optional
from dateutil.relativedelta import relativedelta


def get_task_properties(task: dict) -> dict[str, Optional[str | int | date]]:
    """Get properties of a task.

    Args:
        task (dict): A task as returned by the Notion API.

    Returns:
        dict: Task properties in a easily parsable format.
    """

    def get_due_date(prop: dict) -> Optional[date]:
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

    def get_recur_interval(prop: dict) -> Optional[int]:
        """Get the recur interval property.

        Args:
            prop (dict): Task property dictionary.

        Returns:
            int: Task RecurInterval
        """
        return prop["RecurInterval"]["number"]

    def get_recur_unit(prop: dict) -> Optional[str]:
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

    properties: dict[str, Optional[str | int | date]] = {}
    prop: dict = task["properties"]

    properties["due_date"] = get_due_date(prop)
    properties["recur_interval"] = get_recur_interval(prop)
    properties["recur_unit"] = get_recur_unit(prop)

    return properties


def calc_new_due_date(task: dict) -> Optional[str]:
    """Calculate new due date from current task properties.

    Args:
        task (dict): A task as returned by the Notion API.

    Returns:
        str | None: New due date. None if not set.
    """
    props: dict = get_task_properties(task)

    if not props["due_date"]:
        return None
    elif not props["recur_interval"] or not props["recur_unit"]:
        return str(props["due_date"])
    else:
        match props["recur_unit"]:
            case "Days":
                return str(
                    props["due_date"] + relativedelta(days=+props["recur_interval"])
                )
            case "Weeks":
                return str(
                    props["due_date"] + relativedelta(weeks=+props["recur_interval"])
                )
            case "Months":
                return str(
                    props["due_date"] + relativedelta(months=+props["recur_interval"])
                )
            case "Years":
                return str(
                    props["due_date"] + relativedelta(years=+props["recur_interval"])
                )
            case _:
                return str(props["due_date"])
