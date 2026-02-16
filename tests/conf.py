import json
import random
from datetime import datetime, timedelta

from calendar_app.models import Priority, Status, Task
from calendar_app.serializers import TaskJsonInputSerializer

EXAMPLE_TASK_LIST = []


def load_file() -> None:
    with open("tests/example_task_list.json", "r") as f:
        data = json.load(f)
        global EXAMPLE_TASK_LIST
        for task_data in data:
            serializer = TaskJsonInputSerializer(data=task_data)
            serializer.is_valid(raise_exception=True)
            task = Task(**serializer.validated_data)

            EXAMPLE_TASK_LIST.append(task)


def random_task() -> Task:
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
