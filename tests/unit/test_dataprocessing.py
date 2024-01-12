#!/usr/bin/env python

from datetime import date
import pytest
from notion_recurring_tasks import dataprocessing

TEST_PROPERTIES = [
    {
        "input": {"due_date": None, "recur_interval": None, "recur_unit": None},
        "expected": {"due_date": None},
    },
    {
        "input": {
            "due_date": "2024-01-01",
            "recur_interval": None,
            "recur_unit": "Months",
        },
        "expected": {"due_date": "2024-01-01"},
    },
    {
        "input": {
            "due_date": "2024-01-01",
            "recur_interval": 3,
            "recur_unit": None,
        },
        "expected": {"due_date": "2024-01-01"},
    },
    {
        "input": {
            "due_date": "2024-01-01",
            "recur_interval": 4,
            "recur_unit": "Days",
        },
        "expected": {"due_date": "2024-01-05"},
    },
    {
        "input": {
            "due_date": "2024-01-01",
            "recur_interval": 3,
            "recur_unit": "Weeks",
        },
        "expected": {"due_date": "2024-01-22"},
    },
    {
        "input": {
            "due_date": "2024-01-01",
            "recur_interval": 2,
            "recur_unit": "Months",
        },
        "expected": {"due_date": "2024-03-01"},
    },
    {
        "input": {
            "due_date": "2024-01-01",
            "recur_interval": 1,
            "recur_unit": "Years",
        },
        "expected": {"due_date": "2025-01-01"},
    },
]


@pytest.mark.parametrize("task_properties", TEST_PROPERTIES, indirect=True)
def test_get_task_properties(task_properties):
    EXPECTED: dict = task_properties["expected"]["props"]
    if EXPECTED["due_date"] is not None:
        EXPECTED["due_date"] = date.fromisoformat(EXPECTED["due_date"])

    props = dataprocessing.get_task_properties(task_properties)

    assert all([key in props.keys() for key in EXPECTED.keys()])
    assert props["due_date"] == EXPECTED["due_date"]
    assert props["recur_interval"] == EXPECTED["recur_interval"]
    assert props["recur_unit"] == EXPECTED["recur_unit"]


@pytest.mark.parametrize("task_properties", TEST_PROPERTIES, indirect=True)
def test_calc_new_due_date(task_properties):
    new_due_date = dataprocessing.calc_new_due_date(task_properties)
    assert new_due_date == task_properties["expected"]["due_date"]
