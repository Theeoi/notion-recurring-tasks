# Notion Recurring Tasks

![Pytest Status](https://github.com/Theeoi/notion-recurring-tasks/actions/workflows/test.yml/badge.svg?label=Tests)
![Coverage Status](https://coveralls.io/repos/github/Theeoi/notion-recurring-tasks/badge.svg?branch=main)
![Documentation Status](https://readthedocs.org/projects/notion-recurring-tasks/badge/?version=latest)

Using the Notion API to achieve recurring tasks in Notion.

*[Read the full documentation on ReadTheDocs](https://notion-recurring-tasks.readthedocs.io/)*

## General Information

Notion is a great productivity tool for tracking goals, projects and tasks. However, achieving recurring tasks (tasks whos due date repeats at a set interval) is a hassle and requires manual intervention without external tools. Thanks to the Notion API we can access our task data programatically and make specific tasks recur automatically. This software can be connected to a tasks database in Notion and update the Status and Due Date of these tasks accordingly.

### Technologies

- Python =3.12
- Requests >= 2.31
- Dateutil >= 2.8
- Dotenv >= 1.0

### Features

- Connect to a Notion database through a Notion Integration
- Detect recurring tasks in a connected Notion database
- Set new Status and Due Date accoring to task properties
- More features coming! See [Roadmap](#roadmap)..

### Project Layout

    .github/                        # Github Workflows
    
    docs/                           # Documentation Source

    scripts/                        # Helper Scripts

    src/                            # Package Source Code

        notion_recurring_tasks/     # Main Package
        README.md                   # Code Reference README

    tests/                          # Pytest Tests

        functional/                 # Testing if the code does the right things
        unit/                       # Testing if the code does things right
        conftest.py                 # Pytest Configuration

    .gitignore                      # Ignoring unnecessary files
    .readthedocs.yml                # ReadTheDocs Configuration
    mkdocs.yml                      # Documentation Configuration
    pyproject.toml                  # Project Meta Information
    README.md                       # Project README

## Setup

### Usage

To use the package do the following:

1. Clone the repo and open it as the working directory
2. Run `pip install .` to install the script (in a venv if you want)
3. Get a Notion API key and setup your database as required
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

The code has been cleaned up and tests are added. The focus is now on getting this package published and create documentation such that *anyone* can use it.
There are currently no new features planned.

### Roadmap

TODO:

- [x] Implement testing suite
- [x] Refactor script
- [x] Add way to programatically add your own NOTION_KEY
- [ ] Add complete documentation

Room for Improvement:

- Expand testing

## Contact

This code is written and maintained by [Theodor Blom](mailto:me@theodorblom.com).
