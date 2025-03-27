from datetime import datetime, timedelta

import pytest

from calendar_app.models import Calendar, Category, Status, Task


@pytest.fixture
def sample_task():
    return Task(
        name="Sample Task",
        expected_duration=timedelta(hours=2),
        actual_duration=timedelta(hours=1),
        categories=[Category(name="Work"), Category(name="Urgent")],
        deadline=datetime(2025, 3, 30),
        priority=3,
        notifications=[datetime(2025, 3, 28), datetime(2025, 3, 29)],
        status=Status.PENDING,
    )


example_tasks = [
    Task(
        name="homework",
        expected_duration=timedelta(hours=1),
        deadline=datetime(2025, 4, 25),
        priority=2,
        status=Status.INIT,
        categories=[Category(name="boring"), Category(name="short")],
    ),
    Task(
        name="dogwalk",
        expected_duration=timedelta(hours=2),
        deadline=datetime(2025, 3, 30),
        priority=3,
        status=Status.PENDING,
        categories=[Category(name="fun"), Category(name="short")],
    ),
    Task(
        name="project meeting",
        expected_duration=timedelta(hours=3),
        deadline=datetime(2025, 3, 27),
        priority=1,
        status=Status.FINISHED,
        categories=[Category(name="meeting")],
    ),
]


def test_group_by_category():
    expected_grouped_tasks = {
        "boring": [example_tasks[0]],
        "short": example_tasks[0:2],
        "fun": [example_tasks[1]],
        "meeting": [example_tasks[2]],
    }
    actual_grouped_tasks = Calendar.group_by_attribute(
        tasks=example_tasks, mode="category"
    )
    assert expected_grouped_tasks == actual_grouped_tasks
