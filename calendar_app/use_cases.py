from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from calendar_app.models import Task


class Calendar:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    @staticmethod
    def modify_task(task_id: int, tasks: List[Task], updates):
        """
        Modify a task in the provided list of tasks based on its index and update the provided attributes.

        :param task_id: The index of the task in the tasks list.
        :param tasks: The list of tasks to search within.
        :param updates: Dictionary of attributes to update (e.g., name="New Name", expected_duration=5).
        :return: The updated task object.
        """
        if len(tasks) > task_id:
            task = tasks[task_id]
            task.modify(updates = updates)
            return task
        else:
            raise ValueError("Task not found in list")

    @staticmethod
    def get_most_important_task(tasks: List[Task]) -> Task:
        return max(tasks, key=lambda task: task.priority, default=None)

    @staticmethod
    def order_by_attribute(tasks: List[Task], mode: str, reverse=True) -> List[Task]:
        match mode:
            case "categories_quantity":
                return sorted(
                    tasks, key=lambda task: len(task.categories), reverse=reverse
                )
            case "notifications_quantity":
                return sorted(
                    tasks, key=lambda task: len(task.notifications), reverse=reverse
                )
            case "status":
                return sorted(
                    tasks, key=lambda task: task.status.value, reverse=reverse
                )
            case "categories" | "notifications":
                raise ValueError(f"Unsupported order mode: {mode}")
            case _:
                if hasattr(tasks[0], mode):
                    return sorted(
                        tasks, key=lambda task: getattr(task, mode, None), reverse=reverse
                    )
                else:
                    raise ValueError(f"Unsupported order mode: {mode}")

    @staticmethod
    def group_by_attribute(tasks: List[Task], mode: str) -> Dict[str, List[Task]]:
        grouped = defaultdict(list)

        for task in tasks:
            match mode:
                case "category":
                    for category in task.categories or []:
                        grouped[category.name].append(task)
                case "status":
                    grouped[task.status.name].append(task)
                case "priority":
                    grouped[task.priority].append(task)
                case "deadline":
                    grouped[task.deadline.date()].append(task)
                case "categories_quantity":
                    grouped[len(task.categories or [])].append(task)
                case "notifications_quantity":
                    grouped[len(task.notifications or [])].append(task)
                case _:
                    # Default case: Attempt to group by any valid task attribute
                    if hasattr(task, mode):
                        grouped[getattr(task, mode)].append(task)
                    else:
                        raise ValueError(f"Unsupported group mode: {mode}")

        return grouped

    @staticmethod
    def filter_by_attribute(tasks: List[Task], mode: str, target) -> List[Task]:

        def match_deadline(date: datetime, mode: str, target: datetime) -> bool:
            match mode:
                case "year":
                    return date.year == target.year
                case "month":
                    return date.year == target.year and date.month == target.month
                case "week":
                    return date.isocalendar()[:2] == target.isocalendar()[:2]
                case "day":
                    return date.date() == target.date()
                case _:
                    raise ValueError(f"Unsupported mode: {mode}")


        match mode:
            case "category":
                return [
                    task
                    for task in tasks
                    if any(cat.name == target for cat in task.categories)
                ]
            case "categories_quantity" | "notifications_quantity":
                return [task for task in tasks if len(getattr(task, mode.split("_")[0])) == target]
            case "deadline_day" | "deadline_week" | "deadline_month" | "deadline_year":
                deadline_mode = mode.split("_")[-1]

                return [
                    task
                    for task in tasks
                    if match_deadline(date=task.deadline, mode=deadline_mode, target=target)

                ]
            case _:
                # Default case: Check if mode is a valid Task attribute and filter dynamically
                if hasattr(tasks[0], mode):  # Ensure tasks list is not empty
                    attr = getattr(
                        tasks[0], mode
                    )  # Get the first task's attribute to check type
                    return [task for task in tasks if getattr(task, mode) == target]
                else:
                    raise ValueError(f"Unsupported filter mode: {mode}")


if __name__ == "__main__":
    calendar = Calendar()
    task1 = Task(
        name="Task 1", expected_duration=timedelta(hours=1), deadline=datetime.now()
    )
    task2 = Task(
        name="Task 2",
        expected_duration=timedelta(hours=2),
        deadline=datetime(2025, 3, 31),
    )
    calendar.add_task(task1)
    calendar.add_task(task2)
    print(
        calendar.filter_by_attribute(
            target=datetime.now(), tasks=calendar.tasks, mode="deadline_month"
        )
    )
