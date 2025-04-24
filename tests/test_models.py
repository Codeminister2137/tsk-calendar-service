import copy

import pytest

from tests.conf import example_task_list, random_task


@pytest.fixture
def setup_teardown():
    # Setup: Create a new example tasks list
    example_tasks = copy.deepcopy(example_task_list)
    yield example_tasks
    # Teardown: Clear the tasks list to ensure data is not shared between tests
    del example_tasks


class TestModifyTask:
    def test_modify_task_name(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"name": new_task.name}
        task.modify(updates)
        assert task.name == new_task.name

    def test_modify_task_priority(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"priority": new_task.priority}
        task.modify(updates)
        assert task.priority == new_task.priority

    def test_modify_task_status(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"status": new_task.status}
        task.modify(updates)
        assert task.status == new_task.status

    def test_modify_task_expected_duration(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"expected_duration": new_task.expected_duration}
        task.modify(updates)
        assert task.expected_duration == new_task.expected_duration

    def test_modify_task_actual_duration(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"actual_duration": new_task.actual_duration}
        task.modify(updates)
        assert task.actual_duration == new_task.actual_duration

    def test_modify_task_categories(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"categories": new_task.categories}
        task.modify(updates)
        assert task.categories == new_task.categories

    def test_modify_task_deadline(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"deadline": new_task.deadline}
        task.modify(updates)
        assert task.deadline == new_task.deadline

    def test_modify_task_notifications(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = {"notifications": new_task.notifications}
        task.modify(updates)
        assert task.notifications == new_task.notifications

    def test_modify_whole_task(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = new_task.__dict__
        expected_value = task.__repr__()
        task.modify(updates)
        actual_value = task.__repr__()
        assert expected_value != actual_value

    def test_modify_task_invalid_attribute(self, setup_teardown):
        task = random_task()
        updates = {"invalid_attr": "value"}
        with pytest.raises(AttributeError):
            task.modify(updates)
