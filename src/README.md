# Code Reference

This part of the documentation explores the source code and acts like a reference for other parts of the documentation.

## General Information

The Notion Recurring Tasks project only contains one package with the same name. This package encapsuled a script which uses a couple of different modules to work.

### File Overview

    notion_recurring_tasks/     # Directory for the notion_recurring_tasks package.

        __init__.py             # Initializes the package (empty).
        dataprocessing.py       # Processes task data to update the due date accordingly.
        main.py                 # Start of execution. Checks for NOTION_KEY and runs the script.
        notion_api.py           # Communicates with the Notion API.

## Notion Recurring Tasks

The notion_recurring_tasks package contains the script for fetching the recurring tasks through the Notion API and updating their due date and status according to the task properties. It requires a Notion API key set in an environment variable 'NOTION_KEY'. If the script can not find such an environment variable it will prompt you for one and save it in a `.env` file.

The script works like this:

1. Check if "NOTION_KEY" environement variable is available
    1. If not, prompt the user for the key and save it in a `.env` file
1. Find the database id of your connected tasks database
2. Find all tasks that should recur in that database
3. For every task found:
    1. Calculate the new due date according to the task properties
    2. Try to update the task with the new due date and reset the status
4. Print the number of tasks successfully updated
