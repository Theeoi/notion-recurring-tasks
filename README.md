# Notion Recurring Tasks

![Run Pytest](https://github.com/Theeoi/notion-recurring-tasks/actions/workflows/test.yml/badge.svg?label=Tests)

Using the Notion API to achieve recurring tasks in Notion.

## General Information

Notion is a great productivity tool for tracking goals, projects and tasks. However, achieving recurring tasks (tasks that reappear at a set interval) is a hassle and requires manual intervention.
Thanks to the Notion API this changes as we can access our task data programatically and make specific tasks recurring. This script can be connected to a tasks database in Notion and update the Status and Due Date of tasks when they are completed.

### Technologies

- Python =3.12
- Requests >= 2.31
- Dateutil >= 2.8
- Dotenv >= 1.0

### Features

- Detect recurring tasks in the Notion database
- Set new Status and Due Date accoring to task properties
- More features coming! See [Roadmap](#roadmap)..

## Setup

### Usage

To use the package do the following:

1. Clone the repo and open it as the working directory
2. Create a `.env` file containing your NOTION_KEY
```
# the .env file

NOTION_KEY = "[secret_string]"
```
3. Run `pip install .` to install the script (in a venv if you want)
4. Run `notion-recurring-tasks` to run the script
5. [Optional] Set up a cronjob to run the script once per day

### Contributing

To develop this code you should do the following:

1. Follow the steps outlined in [Usage](#usage) to get the package running
2. Create a Python virtual environment using your prefered program
3. Activate the virtual environment and run `pip install .[dev]` to install the development dependancies
4. Run the tests using `pytest`
5. Make your pull-requests to the `dev` branch

## Project Status

The first version of this script was hastely put together to get recurring tasks to work. Sporadic work is being done to improve the code.
There are currently no new features planned.

### Roadmap

TODO:

- [ ] Implement testing suite
- [ ] Refactor script

Room for Improvement:

- Update this README to allow non-tech users to add this to their Notion

## Contact

This code is written and maintained by [Theodor Blom](mailto:me@theodorblom.com).