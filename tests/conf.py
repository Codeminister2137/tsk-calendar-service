import json
import random
from datetime import datetime, timedelta

from calendar_app.models import Priority, Status, Task
from calendar_app.serializers import TaskJsonInputSerializer

EXAMPLE_TASK_LIST = []


def load_file():
    with open("tests/example_task_list.json", "r") as f:
        data = json.load(f)
        global EXAMPLE_TASK_LIST
        for task in data:
            new_task = TaskJsonInputSerializer(data=task)
            new_task.is_valid(raise_exception=True)
            validated_data = new_task.validated_data
            EXAMPLE_TASK_LIST.append(
                Task(status=Status(validated_data["status"][0]), **validated_data)
            )


def random_task():
    name = f"Task {random.randint(1, 100)}"
    expected_duration = timedelta(hours=random.randint(1, 10))
    actual_duration = timedelta(hours=random.randint(1, 10))
    categories = [random.choice(["Work", "Urgent", "Personal", "Other"])]
    deadline = datetime.now() + timedelta(days=random.randint(1, 365))
    priority = random.choice(list(Priority))
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


if __name__ == "__main__":
    load_file()
