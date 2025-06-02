import copy
import random
from collections import defaultdict
from unittest.mock import patch

import pytest

from calendar_app.enums import Priority
from calendar_app.models import Task
from calendar_app.use_cases import Calendar
from tests.conf import EXAMPLE_TASK_LIST, random_task


@pytest.fixture
def setup_teardown():
    # Setup: Create a new Calendar instance and example tasks list
    calendar = Calendar()
    example_tasks = copy.deepcopy(EXAMPLE_TASK_LIST)
    yield calendar, example_tasks
    # Teardown: Clear the tasks list to ensure data is not shared between tests
    calendar.tasks = []


class TestSetupTeardown:
    def test_should_yield_calendar_with_empty_task_list(self, setup_teardown):
        calendar, example_tasks = setup_teardown
        assert len(calendar.tasks) == 0


class TestAddTask:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.calendar.tasks = []

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
        self.calendar.tasks = []
        self.tasks = self.calendar.tasks
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.chosen_task_id = random.randint(0, len(self.tasks) - 1)

    def test_should_modify_correct_task(self):
        chosen_task_id = self.chosen_task_id
        expected_value = self.calendar.tasks[chosen_task_id].__repr__()
        self.calendar.modify_task(
            task_id=chosen_task_id, tasks=self.tasks, updates=random_task().__dict__
        )
        actual_value = self.calendar.tasks[chosen_task_id].__repr__()
        assert expected_value != actual_value

    def test_should_not_modify_incorrect_task(self):
        task_reproductions = [task.__repr__() for task in self.example_tasks]
        chosen_task_id = self.chosen_task_id
        self.calendar.modify_task(
            task_id=chosen_task_id, tasks=self.tasks, updates=random_task().__dict__
        )
        for id in range(len(self.tasks)):
            if id != chosen_task_id:
                assert self.tasks[id].__repr__() in task_reproductions

    def test_should_not_change_amount_of_tasks(self):
        chosen_task_id = self.chosen_task_id
        expected_value = len(self.tasks)
        self.calendar.modify_task(
            task_id=chosen_task_id, tasks=self.tasks, updates=random_task().__dict__
        )
        actual_value = len(self.tasks)
        assert expected_value == actual_value


class TestGetMostImportantTask:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.chosen_task_id = random.randint(0, len(self.calendar.tasks) - 1)
        self.calendar.tasks[self.chosen_task_id].priority = Priority.HIGHEST

    def test_should_return_task_with_highest_priority(self):
        actual_value = self.calendar.get_most_important_task(
            self.calendar.tasks
        ).priority
        expected_value = Priority.HIGHEST
        assert actual_value == expected_value

    def test_should_return_one_task(self):
        self.calendar.tasks.append(Task(name="example", priority=Priority.HIGHEST))
        actual_value = self.calendar.get_most_important_task(self.calendar.tasks)
        assert isinstance(actual_value, Task)


class TestOrderByAttribute:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.tasks = self.calendar.tasks
        for task in self.example_tasks:
            self.calendar.add_task(task)

    def test_should_return_list_ordered_by_name(self):
        mode = "name"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: task.name, reverse=True
        )
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_expected_duration(self):
        mode = "expected_duration"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: task.expected_duration, reverse=True
        )
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_actual_duration(self):
        mode = "actual_duration"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: task.actual_duration, reverse=True
        )
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_deadline(self):
        mode = "deadline"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: task.deadline, reverse=True
        )
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_priority(self):
        mode = "priority"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: task.priority.value, reverse=True
        )
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_status(self):
        mode = "status"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: task.status.value, reverse=True
        )
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_categories_quantity(self):
        mode = "categories_quantity"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: len(task.categories), reverse=True
        )
        assert actual_value == expected_value

    def test_should_return_list_ordered_by_notifications_quantity(self):
        mode = "notifications_quantity"
        actual_value = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected_value = sorted(
            self.example_tasks, key=lambda task: len(task.notifications), reverse=True
        )
        assert actual_value == expected_value

    def test_should_raise_value_error_on_unsupported_mode_with_existing_attribute(self):
        with patch(
            "calendar_app.use_cases.Calendar.excluded_order_modes"
        ) as mock_order_by_attribute:
            mock_order_by_attribute.return_value = ["abc"]
            mode = "abc"
            with pytest.raises(ValueError):
                self.calendar.order_by_attribute(
                    self.example_tasks, mode=mode, reverse=True
                )

    def test_should_raise_value_error_on_unsupported_mode_without_existing_attribute(
        self,
    ):
        random_name = random_task().name
        mode = random_name
        with pytest.raises(ValueError):
            self.calendar.order_by_attribute(
                self.example_tasks, mode=mode, reverse=True
            )


class TestGroupByAttribute:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.tasks = self.calendar.tasks
        for task in self.example_tasks:
            self.calendar.add_task(task)

    def test_should_return_dictionary_grouped_by_name(self):
        mode = "name"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[task.name].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_expected_duration(self):
        mode = "expected_duration"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[task.expected_duration].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_actual_duration(self):
        mode = "actual_duration"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[task.actual_duration].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_deadline_year(self):
        mode = "deadline_year"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[str(task.deadline.year)].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_deadline_month(self):
        mode = "deadline_month"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[f"{task.deadline.year}-{task.deadline.month}"].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_deadline_week(self):
        mode = "deadline_week"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[str(task.deadline.isocalendar()[:2])].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_deadline_day(self):
        mode = "deadline_day"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[str(task.deadline.date())].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_priority(self):
        mode = "priority"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[task.priority.name].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_status(self):
        mode = "status"
        actual_value = self.calendar.group_by_attribute(
            tasks=self.calendar.tasks, mode=mode
        )
        expected_value = defaultdict(list)
        for task in self.calendar.tasks:
            expected_value[task.status.name].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_category(self):
        mode = "category"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            for category in task.categories:
                expected_value[category].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_categories_quantity(self):
        mode = "categories_quantity"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[len(task.categories)].append(task)

        assert actual_value == expected_value

    def test_should_return_dictionary_grouped_by_notifications_quantity(self):
        mode = "notifications_quantity"
        actual_value = self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)
        expected_value = defaultdict(list)
        for task in self.tasks:
            expected_value[len(task.notifications)].append(task)

        assert actual_value == expected_value

    def test_should_raise_value_error_on_unsupported_mode_with_existing_attribute(self):
        for mode in Calendar.excluded_group_modes:
            with pytest.raises(ValueError):
                self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)

    def test_should_raise_value_error_on_unsupported_mode_without_existing_attribute(
        self,
    ):
        random_name = random_task().name
        mode = random_name
        with pytest.raises(ValueError):
            self.calendar.group_by_attribute(tasks=self.tasks, mode=mode)


class TestFilterByAttribute:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.tasks = self.calendar.tasks
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.target_task = random_task()
        self.calendar.add_task(self.target_task)

    def test_should_return_list_filtered_by_name(self):
        mode = "name"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.name
        )
        for task in actual_value:
            assert task.name == self.target_task.name

    def test_should_return_list_filtered_by_expected_duration(self):
        mode = "expected_duration"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.expected_duration
        )
        for task in actual_value:
            assert task.expected_duration == self.target_task.expected_duration

    def test_should_return_list_filtered_by_actual_duration(self):
        mode = "actual_duration"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.actual_duration
        )
        for task in actual_value:
            assert task.actual_duration == self.target_task.actual_duration

    def test_should_return_list_filtered_by_category(self):
        mode = "category"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.categories[0]
        )
        for task in actual_value:
            assert self.target_task.categories[0] in task.categories

    def test_should_return_list_filtered_by_deadline_year(self):
        mode = "deadline_year"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.deadline
        )
        for task in actual_value:
            assert task.deadline.year == self.target_task.deadline.year

    def test_should_return_list_filtered_by_deadline_month(self):
        mode = "deadline_month"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.deadline
        )
        for task in actual_value:
            assert (
                task.deadline.year == self.target_task.deadline.year
                and task.deadline.month == self.target_task.deadline.month
            )

    def test_should_return_list_filtered_by_deadline_week(self):
        mode = "deadline_week"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.deadline
        )
        for task in actual_value:
            assert (
                task.deadline.isocalendar()[:2]
                == self.target_task.deadline.isocalendar()[:2]
            )

    def test_should_return_list_filtered_by_deadline_day(self):
        mode = "deadline_day"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.deadline
        )
        for task in actual_value:
            assert task.deadline.date() == self.target_task.deadline.date()

    def test_should_return_list_filtered_by_priority(self):
        mode = "priority"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.priority.name
        )
        for task in actual_value:
            assert task.priority.name == self.target_task.priority.name

    def test_should_return_list_filtered_by_status(self):
        mode = "status"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=self.target_task.status.name
        )
        for task in actual_value:
            assert task.status.name == self.target_task.status.name

    def test_should_return_list_filtered_by_notifications_quantity(self):
        mode = "notifications_quantity"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=len(self.target_task.notifications)
        )
        for task in actual_value:
            assert len(task.notifications) == len(self.target_task.notifications)

    def test_should_return_list_filtered_by_categories_quantity(self):
        mode = "categories_quantity"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target=len(self.target_task.categories)
        )
        for task in actual_value:
            assert len(task.categories) == len(self.target_task.categories)

    def test_should_raise_value_error_on_unsupported_mode_with_existing_attribute(self):
        mode = "notifications"
        with pytest.raises(ValueError):
            self.calendar.filter_by_attribute(
                tasks=self.tasks, mode=mode, target=len(self.target_task.notifications)
            )
        mode = "categories"
        with pytest.raises(ValueError):
            self.calendar.filter_by_attribute(
                tasks=self.tasks, mode=mode, target=len(self.target_task.notifications)
            )

    def test_should_raise_value_error_on_unsupported_mode_without_existing_attribute(
        self,
    ):
        mode = "wrong mode"
        with pytest.raises(ValueError):
            self.calendar.filter_by_attribute(
                tasks=self.tasks, mode=mode, target=len(self.target_task.notifications)
            )

    def test_should_return_empty_list_when_filtering_by_non_matching_target(self):
        mode = "name"
        actual_value = self.calendar.filter_by_attribute(
            tasks=self.tasks, mode=mode, target="Absolutely nonexistant target"
        )
        assert len(actual_value) == 0
        assert isinstance(actual_value, list)
