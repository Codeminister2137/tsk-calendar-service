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
    calendar = Calendar()
    example_tasks = copy.deepcopy(EXAMPLE_TASK_LIST)
    yield calendar, example_tasks
    calendar.tasks = []


class TestSetupTeardown:
    def test_should_yield_calendar_with_empty_task_list(self, setup_teardown):
        calendar, _ = setup_teardown
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
        assert task == self.calendar.tasks[0]

    def test_should_add_correct_task_with_correct_data_to_list(self):
        task = random_task()
        self.calendar.add_task(task)
        assert task.__repr__() == self.calendar.tasks[0].__repr__()


class TestModifyTask:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        self.calendar.tasks = []
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.chosen_task_id = random.randint(0, len(self.calendar.tasks) - 1)

    def test_should_modify_correct_task(self):
        task_id = self.chosen_task_id
        before = self.calendar.tasks[task_id].__repr__()
        self.calendar.modify_task(
            task_id=task_id, tasks=self.calendar.tasks, updates=random_task().__dict__
        )
        after = self.calendar.tasks[task_id].__repr__()
        assert before != after

    def test_should_not_modify_incorrect_task(self):
        before = [task.__repr__() for task in self.calendar.tasks]
        self.calendar.modify_task(
            task_id=self.chosen_task_id,
            tasks=self.calendar.tasks,
            updates=random_task().__dict__,
        )
        for i, task in enumerate(self.calendar.tasks):
            if i != self.chosen_task_id:
                assert task.__repr__() == before[i]

    def test_should_not_change_amount_of_tasks(self):
        before = len(self.calendar.tasks)
        self.calendar.modify_task(
            task_id=self.chosen_task_id,
            tasks=self.calendar.tasks,
            updates=random_task().__dict__,
        )
        after = len(self.calendar.tasks)
        assert before == after


class TestGetMostImportantTask:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.chosen_task_id = random.randint(0, len(self.calendar.tasks) - 1)
        self.calendar.tasks[self.chosen_task_id].priority = Priority.HIGHEST

    def test_should_return_task_with_highest_priority(self):
        task = self.calendar.get_most_important_task(self.calendar.tasks)
        assert task.priority == Priority.HIGHEST

    def test_should_return_one_task(self):
        self.calendar.tasks.append(Task(name="example", priority=Priority.HIGHEST))
        task = self.calendar.get_most_important_task(self.calendar.tasks)
        assert isinstance(task, Task)


class TestOrderByAttribute:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        for task in self.example_tasks:
            self.calendar.add_task(task)

    @pytest.mark.parametrize(
        "mode, key",
        [
            ("name", lambda t: t.name),
            ("expected_duration", lambda t: t.expected_duration),
            ("actual_duration", lambda t: t.actual_duration),
            ("deadline", lambda t: t.deadline),
            ("priority", lambda t: t.priority.value),
            ("status", lambda t: t.status.value),
            ("categories_quantity", lambda t: len(t.categories)),
            ("notifications_quantity", lambda t: len(t.notifications)),
        ],
    )
    def test_should_return_list_ordered_by_attribute(self, mode, key):
        actual = self.calendar.order_by_attribute(
            self.example_tasks, mode=mode, reverse=True
        )
        expected = sorted(self.example_tasks, key=key, reverse=True)
        assert actual == expected

    def test_should_raise_value_error_on_unsupported_mode_with_existing_attribute(self):
        with patch(
            "calendar_app.use_cases.Calendar.excluded_order_modes", return_value=["abc"]
        ):
            with pytest.raises(ValueError):
                self.calendar.order_by_attribute(
                    self.example_tasks, mode="abc", reverse=True
                )

    def test_should_raise_value_error_on_unsupported_mode_without_existing_attribute(
        self,
    ):
        mode = random_task().name
        with pytest.raises(ValueError):
            self.calendar.order_by_attribute(
                self.example_tasks, mode=mode, reverse=True
            )


class TestGroupByAttribute:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        for task in self.example_tasks:
            self.calendar.add_task(task)

    @pytest.mark.parametrize(
        "mode, group_key",
        [
            ("name", lambda t: t.name),
            ("expected_duration", lambda t: t.expected_duration),
            ("actual_duration", lambda t: t.actual_duration),
            ("deadline_year", lambda t: str(t.deadline.year)),
            ("deadline_month", lambda t: f"{t.deadline.year}-{t.deadline.month}"),
            ("deadline_week", lambda t: str(t.deadline.isocalendar()[:2])),
            ("deadline_day", lambda t: str(t.deadline.date())),
            ("priority", lambda t: t.priority.name),
            ("status", lambda t: t.status.name),
            ("categories_quantity", lambda t: len(t.categories)),
            ("notifications_quantity", lambda t: len(t.notifications)),
        ],
    )
    def test_should_group_by_attribute(self, mode, group_key):
        result = self.calendar.group_by_attribute(self.calendar.tasks, mode=mode)
        expected = defaultdict(list)
        for task in self.calendar.tasks:
            expected[group_key(task)].append(task)
        assert result == expected

    def test_should_group_by_category(self):
        result = self.calendar.group_by_attribute(self.calendar.tasks, mode="category")
        expected = defaultdict(list)
        for task in self.calendar.tasks:
            for category in task.categories:
                expected[category].append(task)
        assert result == expected

    def test_should_raise_value_error_on_unsupported_modes(self):
        for mode in Calendar.excluded_group_modes:
            with pytest.raises(ValueError):
                self.calendar.group_by_attribute(self.calendar.tasks, mode=mode)
        with pytest.raises(ValueError):
            self.calendar.group_by_attribute(self.calendar.tasks, mode="nonexistent")


class TestFilterByAttribute:
    @pytest.fixture(autouse=True)
    def class_setup(self, setup_teardown):
        self.calendar, self.example_tasks = setup_teardown
        for task in self.example_tasks:
            self.calendar.add_task(task)
        self.target_task = random_task()
        self.calendar.add_task(self.target_task)

    @pytest.mark.parametrize(
        "mode, attr",
        [
            ("name", lambda t: t.name),
            ("expected_duration", lambda t: t.expected_duration),
            ("actual_duration", lambda t: t.actual_duration),
            ("deadline_year", lambda t: t.deadline),
            ("deadline_month", lambda t: t.deadline),
            ("deadline_week", lambda t: t.deadline),
            ("deadline_day", lambda t: t.deadline),
            ("priority", lambda t: t.priority.name),
            ("status", lambda t: t.status.name),
            ("notifications_quantity", lambda t: len(t.notifications)),
            ("categories_quantity", lambda t: len(t.categories)),
        ],
    )
    def test_should_filter_by_attribute(self, mode, attr):
        target = attr(self.target_task)
        results = self.calendar.filter_by_attribute(
            self.calendar.tasks, mode=mode, target=target
        )
        for task in results:
            if mode.startswith("deadline"):
                if mode == "deadline_year":
                    assert task.deadline.year == self.target_task.deadline.year
                elif mode == "deadline_month":
                    assert (
                        task.deadline.year == self.target_task.deadline.year
                        and task.deadline.month == self.target_task.deadline.month
                    )
                elif mode == "deadline_week":
                    assert (
                        task.deadline.isocalendar()[:2]
                        == self.target_task.deadline.isocalendar()[:2]
                    )
                elif mode == "deadline_day":
                    assert task.deadline.date() == self.target_task.deadline.date()
            else:
                assert attr(task) == target

    def test_should_filter_by_category(self):
        category = self.target_task.categories[0]
        results = self.calendar.filter_by_attribute(
            self.calendar.tasks, mode="category", target=category
        )
        for task in results:
            assert category in task.categories

    def test_should_raise_value_error_on_unsupported_modes(self):
        with pytest.raises(ValueError):
            self.calendar.filter_by_attribute(
                self.calendar.tasks, mode="notifications", target=0
            )
        with pytest.raises(ValueError):
            self.calendar.filter_by_attribute(
                self.calendar.tasks, mode="categories", target=0
            )
        with pytest.raises(ValueError):
            self.calendar.filter_by_attribute(
                self.calendar.tasks, mode="invalid_mode", target=0
            )

    def test_should_return_empty_list_when_no_match(self):
        result = self.calendar.filter_by_attribute(
            self.calendar.tasks, mode="name", target="Nonexistent Name"
        )
        assert result == []
