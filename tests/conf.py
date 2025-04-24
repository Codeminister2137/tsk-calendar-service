import random
from datetime import datetime, timedelta

from calendar_app.models import Status, Task

example_task_list = [
    Task(
        name="homework",
        expected_duration=timedelta(hours=1),
        actual_duration=timedelta(hours=2),
        deadline=datetime(2025, 4, 25),
        priority=2,
        status=Status.INIT,
        categories=["boring", "short"],
        notifications=[datetime(2025, 4, 25, 18, 30), datetime(2025, 4, 24, 19, 30)],
    ),
    Task(
        name="dogwalk",
        expected_duration=timedelta(hours=2),
        actual_duration=timedelta(hours=2),
        deadline=datetime(2025, 3, 30),
        priority=3,
        status=Status.PENDING,
        categories=["fun", "short"],
        notifications=[datetime(2025, 2, 25, 18, 30)],
    ),
    Task(
        name="project meeting",
        expected_duration=timedelta(hours=3),
        actual_duration=timedelta(hours=2, minutes=15),
        deadline=datetime(2025, 3, 27),
        priority=1,
        status=Status.FINISHED,
        categories=["meeting"],
        notifications=[
            datetime(2025, 2, 20, 18, 30),
            datetime(2025, 2, 20, 18, 35),
            datetime(2025, 2, 25, 18, 40),
        ],
    ),
    Task(
        name="Empty task",
    ),
]


def random_task():
    name = f"Task {random.randint(1, 100)}"
    expected_duration = timedelta(hours=random.randint(1, 10))
    actual_duration = timedelta(hours=random.randint(1, 10))
    categories = [random.choice(["Work", "Urgent", "Personal", "Other"])]
    deadline = datetime.now() + timedelta(days=random.randint(1, 365))
    priority = random.randint(1, 10)
    notifications = [
        datetime.now() + timedelta(days=random.randint(1, 365))
        for _ in range(random.randint(1, 5))
    ]
    status = random.choice(list(Status))

    return Task(
        name=name,
        expected_duration=expected_duration,
        actual_duration=actual_duration,
        categories=categories,
        deadline=deadline,
        priority=priority,
        notifications=notifications,
        status=status,
    )
