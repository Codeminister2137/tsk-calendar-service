import copy

import pytest

from tests.conf import EXAMPLE_TASK_LIST, random_task


@pytest.fixture
def setup_teardown():
    example_tasks = copy.deepcopy(EXAMPLE_TASK_LIST)
    yield example_tasks
    del example_tasks


class TestModifyTask:
    @pytest.mark.parametrize(
        "attribute",
        [
            "name",
            "priority",
            "status",
            "expected_duration",
            "actual_duration",
            "categories",
            "deadline",
            "notifications",
        ],
    )
    def test_modify_task_attribute(self, setup_teardown, attribute):
        task = random_task()
        new_task = random_task()
        updates = {attribute: getattr(new_task, attribute)}
        task.modify(updates)

        # Use `.name` for enum-like objects (e.g. priority), otherwise raw value
        expected = getattr(new_task, attribute)
        actual = getattr(task, attribute)

        if hasattr(expected, "name") and hasattr(actual, "name"):
            assert actual.name == expected.name
        else:
            assert actual == expected

    def test_modify_whole_task(self, setup_teardown):
        task = random_task()
        new_task = random_task()
        updates = new_task.__dict__
        before = task.__repr__()
        task.modify(updates)
        after = task.__repr__()
        assert before != after

    def test_modify_task_invalid_attribute(self, setup_teardown):
        task = random_task()
        updates = {"invalid_attr": "value"}
        with pytest.raises(AttributeError):
            task.modify(updates)
