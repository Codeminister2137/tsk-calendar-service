import pytest
from datetime import datetime, timedelta
import random
from calendar_app.models import Category, Status, Task
from calendar_app.use_cases import Calendar

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
    # Setup: Create a new Calendar instance and example tasks list
    calendar = Calendar()
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
    yield calendar, example_tasks
    # Teardown: Clear the tasks list to ensure data is not shared between tests
    del calendar
    del example_tasks


class TestSetupTeardown:
    def test_should_yield_claendar_with_empty_task_list(self, setup_teardown):
        calendar, example_tasks = setup_teardown
        assert len(calendar.tasks) == 0
class TestAddTask:
    def test_should_expand_task_list(self, setup_teardown):
        calendar, example_tasks = setup_teardown
        calendar.add_task(random_task())
        assert len(calendar.tasks) == 1


    def test_should_add_correct_task_to_list(self, setup_teardown):
        calendar, example_tasks = setup_teardown
        task = random_task()
        calendar.add_task(task)
        expected_value = task
        actual_value = calendar.tasks[0]
        assert expected_value == actual_value

class TestModifyTask:
    def test_should_modify_correct_task(self, setup_teardown):
        calendar, example_tasks = setup_teardown
        tasks = calendar.tasks
        for task in example_tasks:
            calendar.add_task(task)
        chosen_task_id = random.randint(0,len(tasks))
        expected_value = calendar.tasks[chosen_task_id].__repr__()
        calendar.modify_task(task_id=chosen_task_id, tasks=tasks, name = random_task().name)
        actual_value = calendar.tasks[chosen_task_id].__repr__()
        assert expected_value != actual_value
class TestGetMostImportantTask:
    def test_get_most_important_task(self, setup_teardown):
        # Placeholder test method
        pass

class TestOrderByAttribute:
    def test_order_by_attribute(self, setup_teardown):
        # Placeholder test method
        pass

class TestGroupByAttribute:
    def test_group_by_attribute(self, setup_teardown):
        # Placeholder test method
        pass

class TestFilterByAttribute:
    def test_filter_by_attribute(self, setup_teardown):
        # Placeholder test method
        pass

def test_group_by_category(setup_teardown):
    calendar, example_tasks = setup_teardown
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
