# Code Reference

This part of the documentation explores the source code and acts like a reference for other parts of the documentation.

## General Information

The Notion Recurring Tasks project only contains one package with the same name. This package encapsuled a script which uses a couple of different modules to work.

### File Overview

    notion_recurring_tasks/     # Directory for the notion_recurring_tasks package.

        __init__.py             # Initializes the package (empty).
        dataprocessing.py       # Processes task data to update the due date accordingly.
        main.py                 # Start of execution. Runs the script.
        notion_api.py           # Communicates with the Notion API.

## Notion Recurring Tasks

The notion_recurring_tasks package contains the script for fetching the recurring tasks through the Notion API and updating their due date and status according to the task properties. The script does this in this order:

1. Finds the database id of your connected tasks database
2. Finds all tasks that should recur in that database
3. For every task found it:
    1. Calculates the new due date according to the task properties
    2. Tries to update the task with the new due date and resets the status
4. Prints the number of tasks it successfully updated
