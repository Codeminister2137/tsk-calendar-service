import pytest
from datetime import datetime, timedelta
import random
from calendar_app.models import Category, Status, Task

def random_task():
    name = f"Task {random.randint(1, 100)}"
    expected_duration = timedelta(hours=random.randint(1, 10))
    actual_duration = timedelta(hours=random.randint(1, 10))
    categories = [Category(name=random.choice(["Work", "Urgent", "Personal", "Other"]))]
    deadline = datetime.now() + timedelta(days=random.randint(1, 365))
    priority = random.randint(1, 10)
    notifications = [datetime.now() + timedelta(days=random.randint(1, 365)) for _ in range(random.randint(1, 5))]
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

@pytest.fixture
def setup_teardown():
    # Setup: Create a new example tasks list
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
    yield example_tasks
    # Teardown: Clear the tasks list to ensure data is not shared between tests
    del example_tasks



class TestModifyTask:
    def test_modify_task_name(self, setup_teardown):
        example_tasks = setup_teardown
        task = example_tasks[0]
        updates = {"name": "Updated Task"}
        task.modify(updates)
        assert task.name == "Updated Task"

    def test_modify_task_priority(self, setup_teardown):
        example_tasks = setup_teardown
        task = example_tasks[1]
        updates = {"priority": 1}
        task.modify(updates)
        assert task.priority == 1

    def test_modify_task_status(self, setup_teardown):
        example_tasks = setup_teardown
        task = example_tasks[2]
        updates = {"status": Status.FAILED}
        task.modify(updates)
        assert task.status == Status.FAILED

    def test_modify_task_invalid_attribute(self, setup_teardown):
        example_tasks = setup_teardown
        task = example_tasks[0]
        updates = {"invalid_attr": "value"}
        with pytest.raises(AttributeError):
            task.modify(updates)



