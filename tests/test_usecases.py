import random
from datetime import datetime, timedelta

import pytest

from calendar_app.models import Category, Status, Task
from calendar_app.use_cases import Calendar
from tests.test_models import example_task_list, random_task


@pytest.fixture
def setup_teardown():
    # Setup: Create a new Calendar instance and example tasks list
    calendar = Calendar()
    example_tasks = example_task_list
    yield calendar, example_tasks
    # Teardown: Clear the tasks list to ensure data is not shared between tests
    del calendar
    del example_tasks

class TestSetupTeardown:
    def test_should_yield_calendar_with_empty_task_list(self, setup_teardown):
        calendar, example_tasks = setup_teardown
        assert len(calendar.tasks) == 0

class TestAddTask:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown

    def test_should_expand_task_list(self):
        self.calendar.add_task(random_task())
        assert len(self.calendar.tasks) == 1

    def test_should_add_correct_task_to_list(self):
        task = random_task()
        self.calendar.add_task(task)
        expected_value = task
        actual_value = self.calendar.tasks[0]
        assert expected_value == actual_value
    def test_should_add_correct_task_with_correct_data_to_list(self):
        task = random_task()
        self.calendar.add_task(task)
        expected_value = task.__repr__()
        actual_value = self.calendar.tasks[0].__repr__()
        assert expected_value == actual_value

class TestModifyTask:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.tasks = self.calendar.tasks
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.chosen_task_id = random.randint(0, len(self.tasks) - 1)


    def test_should_modify_correct_task(self):
        chosen_task_id = self.chosen_task_id
        expected_value = self.calendar.tasks[chosen_task_id].__repr__()
        self.calendar.modify_task(task_id=chosen_task_id, tasks=self.tasks, updates=random_task().__dict__)
        actual_value = self.calendar.tasks[chosen_task_id].__repr__()
        assert expected_value != actual_value

    def test_should_not_modify_incorrect_task(self):
        task_reproductions = [task.__repr__() for task in self.example_tasks]
        chosen_task_id = self.chosen_task_id
        self.calendar.modify_task(task_id=chosen_task_id, tasks=self.tasks, updates=random_task().__dict__)
        for id in range(len(self.tasks)):
            if id != chosen_task_id:
                assert self.tasks[id].__repr__() in task_reproductions

    def test_should_not_change_amount_of_tasks(self):
        chosen_task_id = self.chosen_task_id
        expected_value = len(self.tasks)
        self.calendar.modify_task(task_id=chosen_task_id, tasks=self.tasks, updates=random_task().__dict__)
        actual_value = len(self.tasks)
        assert expected_value == actual_value

class TestGetMostImportantTask:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.tasks = self.calendar.tasks
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.chosen_task_id = random.randint(0, len(self.tasks) - 1)
        self.tasks[self.chosen_task_id].priority = 10

    def test_should_return_task_with_highest_priority(self, setup_teardown):
        actual_value = self.calendar.get_most_important_task(self.tasks)
        expected_value = self.tasks[self.chosen_task_id]
        assert actual_value == expected_value

    def test_should_return_one_task(self, setup_teardown):
        self.tasks.append(Task(name="example", priority=10))
        actual_value = self.calendar.get_most_important_task(self.tasks)
        assert isinstance(actual_value, Task)


class TestOrderByAttribute:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.tasks = self.calendar.tasks
        for task in self.example_tasks:
            self.calendar.add_task(task)

    def test_should_return_list_ordered_by_name(self, setup_teardown):
        mode = "name"
        actual_value = self.calendar.order_by_attribute(self.example_tasks, mode=mode, reverse=True)
        expected_value = sorted(self.example_tasks, key=lambda task: task.name, reverse=True)
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_expected_duration(self, setup_teardown):
        mode = "expected_duration"
        actual_value = self.calendar.order_by_attribute(self.example_tasks, mode=mode, reverse=True)
        expected_value = sorted(self.example_tasks, key=lambda task: task.expected_duration, reverse=True)
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_actual_duration(self, setup_teardown):
        mode = "actual_duration"
        actual_value = self.calendar.order_by_attribute(self.example_tasks, mode=mode, reverse=True)
        expected_value = sorted(self.example_tasks, key=lambda task: task.actual_duration, reverse=True)
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_deadline(self, setup_teardown):
        mode = "deadline"
        actual_value = self.calendar.order_by_attribute(self.example_tasks, mode=mode, reverse=True)
        expected_value = sorted(self.example_tasks, key=lambda task: task.deadline, reverse=True)
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_priority(self, setup_teardown):
        mode = "priority"
        actual_value = self.calendar.order_by_attribute(self.example_tasks, mode=mode, reverse=True)
        expected_value = sorted(self.example_tasks, key=lambda task: task.priority, reverse=True)
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_status(self, setup_teardown):
        mode = "status"
        actual_value = self.calendar.order_by_attribute(self.example_tasks, mode=mode, reverse=True)
        expected_value = sorted(self.example_tasks, key=lambda task: task.status, reverse=True)
        assert actual_value == expected_value

class TestGroupByAttribute:
    def test_group_by_attribute(self, setup_teardown):
        # Placeholder test method
        pass

class TestFilterByAttribute:
    def test_filter_by_attribute(self, setup_teardown):
        # Placeholder test method
        pass

# def test_group_by_category(setup_teardown):
#     calendar, example_tasks = setup_teardown
#     expected_grouped_tasks = {
#         "boring": [example_tasks[0]],
#         "short": example_tasks[0:2],
#         "fun": [example_tasks[1]],
#         "meeting": [example_tasks[2]],
#     }
#     actual_grouped_tasks = Calendar.group_by_attribute(
#         tasks=example_tasks, mode="category"
#     )
#     assert expected_grouped_tasks == actual_grouped_tasks
