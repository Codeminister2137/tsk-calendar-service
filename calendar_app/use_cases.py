from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from calendar_app.models import Task


class Calendar:
    tasks = []
    excluded_order_modes = frozenset([])
    excluded_group_modes = frozenset(["deadline"])

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Calendar, cls).__new__(cls)
        return cls.instance

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
            task.modify(updates=updates)
            return task
        else:
            raise ValueError("Task not found in list")

    @staticmethod
    def map_mode(mode: str) -> str:
        mapper = {
            "deadline_day": "deadline",
            "deadline_week": "deadline",
            "deadline_month": "deadline",
            "deadline_year": "deadline",
            "notifications": "notifications_quantity",
            "categories": "categories_quantity",
            "category": "name",
        }
        return mapper[mode] if mode in mapper else mode

    @staticmethod
    def get_most_important_task(tasks: List[Task]) -> Task:
        return max(tasks, key=lambda task: task.priority.value, default=None)

    def order_by_attribute(
        self, tasks: List[Task], mode: str, reverse=True
    ) -> List[Task]:
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
            case "priority":
                return sorted(
                    tasks, key=lambda task: task.priority.value, reverse=reverse
                )
            case _:
                if hasattr(tasks[0], mode) and mode not in self.excluded_order_modes:
                    return sorted(
                        tasks,
                        key=lambda task: getattr(task, mode, None),
                        reverse=reverse,
                    )
                elif mode in self.excluded_order_modes:
                    raise ValueError(f"Banned order mode: {mode}")
                else:
                    raise ValueError(f"Unsupported order mode: {mode}")

    def group_by_attribute(self, tasks: List[Task], mode: str) -> Dict[str, List[Task]]:
        grouped = defaultdict(list)

        def match_deadline(date: datetime, mode: str) -> str:
            match mode:
                case "year":
                    return str(date.year)
                case "month":
                    return f"{date.year}-{date.month}"
                case "week":
                    return str(date.isocalendar()[:2])
                case "day":
                    return str(date.date())
                case _:
                    raise ValueError(f"Unsupported mode: {mode}")

        for task in tasks:
            match mode:
                case "category":
                    for category in task.categories or []:
                        grouped[category].append(task)
                case "status":
                    grouped[task.status.name].append(task)
                case "priority":
                    grouped[task.priority.name].append(task)
                case (
                    "deadline_day"
                    | "deadline_week"
                    | "deadline_month"
                    | "deadline_year"
                ):
                    deadline_mode = mode.split("_")[-1]
                    grouped[match_deadline(task.deadline, deadline_mode)].append(task)
                case "categories_quantity":
                    grouped[len(task.categories or [])].append(task)
                case "notifications_quantity":
                    grouped[len(task.notifications or [])].append(task)
                case _:
                    # Default case: Attempt to group by any valid task attribute
                    if mode in self.excluded_group_modes:
                        raise ValueError(f"Banned group mode: {mode}")
                    elif hasattr(task, mode) and mode not in self.excluded_order_modes:
                        grouped[getattr(task, mode)].append(task)
                    else:
                        raise ValueError(f"Unsupported group mode: {mode}")

        for item in grouped:
            mode = self.map_mode(mode)
            grouped[item] = self.order_by_attribute(grouped[item], mode, reverse=True)

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
                    if any(category == target for category in task.categories)
                ]
            case "categories_quantity" | "notifications_quantity":
                return [
                    task
                    for task in tasks
                    if len(getattr(task, mode.split("_")[0])) == target
                ]
            case "deadline_day" | "deadline_week" | "deadline_month" | "deadline_year":
                deadline_mode = mode.split("_")[-1]

                return [
                    task
                    for task in tasks
                    if match_deadline(
                        date=task.deadline, mode=deadline_mode, target=target
                    )
                ]
            case "categories" | "notifications" | "deadline":
                raise ValueError(f"Unsupported group mode: {mode}")
            case _:
                # Default case: Check if mode is a valid Task attribute and filter dynamically
                if hasattr(tasks[0], mode):  # Ensure tasks list is not empty
                    attr = getattr(
                        tasks[0], mode
                    )  # Get the first task's attribute to check type
                    return [task for task in tasks if getattr(task, mode) == target]
                else:
                    raise ValueError(f"Unsupported filter mode: {mode}")
