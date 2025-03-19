from calendar_app.models import Task, Calendar, Category, Status

example_tasks = [Task(name='homework', categories=[Category(name='boring'), Category(name='short')]),
                 Task(name='dogwalk', categories=[Category(name='fun'), Category(name='short')]),
                 Task(name='project meeting', categories=[Category(name='meeting')])]

def test_group_by_category():
    expected_grouped_tasks = {"boring": [example_tasks[0]], "short": example_tasks[0:2], "fun": [example_tasks[1]], "meeting": [example_tasks[2]]}
    actual_grouped_tasks = Calendar.group_by_attribute(tasks=example_tasks, mode='category')
    assert expected_grouped_tasks == actual_grouped_tasks