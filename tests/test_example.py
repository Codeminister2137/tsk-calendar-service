from tests.conf import EXAMPLE_TASK_LIST, load_file


def test_example():
    load_file()
    print(f"{EXAMPLE_TASK_LIST}")

    assert False
