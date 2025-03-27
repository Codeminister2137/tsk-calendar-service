from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional


@dataclass()
class Category:
    name: str


class Status(Enum):
    INIT = 0
    PENDING = 1
    FINISHED = 2
    FAILED = 3


@dataclass
class Task:
    name: str
    expected_duration: Optional[timedelta] = None
    actual_duration: Optional[timedelta] = None
    categories: Optional[List[Category]] = None
    deadline: datetime = field(default_factory=lambda: datetime.max)
    priority: int = 5
    notifications: Optional[List[datetime]] = None
    status: Status = Status.INIT

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Task({self.name})"

    @classmethod
    def get_attribute_tuple(cls):
        return tuple(
            attribute
            for attribute in dir(cls)
            if not callable(getattr(cls, attribute)) and not attribute.startswith("__")
        )


class Calendar:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task, schedule_for: Optional[datetime] = None):
        if schedule_for:
            task.deadline = schedule_for
        self.tasks.append(task)

    @staticmethod
    def modify_task(task_id: int, tasks: List[Task], **updates):
        """
        Modify a task in the provided list of tasks based on its index and update the provided attributes.

        :param task_id: The index of the task in the tasks list.
        :param tasks: The list of tasks to search within.
        :param updates: Dictionary of attributes to update (e.g., name="New Name", expected_duration=5).
        :return: The updated task object.
        """
        for i, task in enumerate(tasks):
            if id(task) == task_id:
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                    else:
                        raise AttributeError(f"Task has no attribute '{key}'")
                tasks[i] = task
                return task
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
            case _:
                return sorted(
                    tasks, key=lambda task: getattr(task, mode, None), reverse=reverse
                )

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
        match mode:
            case "category":
                return [
                    task
                    for task in tasks
                    if any(cat.name == target for cat in task.categories or [])
                ]
            case "categories_quantity":
                return [task for task in tasks if len(task.categories or []) == target]
            case "notifications_quantity":
                return [
                    task for task in tasks if len(task.notifications or []) == target
                ]
            case "deadline_day":
                return [task for task in tasks if task.deadline.date() == target.date()]
            case "deadline_week":
                return [
                    task
                    for task in tasks
                    if task.deadline.isocalendar()[0] == target.isocalendar()[0]
                    and task.deadline.isocalendar()[1] == target.isocalendar()[1]
                ]
            case "deadline_month":
                return [
                    task
                    for task in tasks
                    if task.deadline.year == target.year
                    and task.deadline.month == target.month
                ]
            case "deadline_year":
                return [task for task in tasks if task.deadline.year == target.year]
            case _:
                # Default case: Check if mode is a valid Task attribute and filter dynamically
                if hasattr(tasks[0], mode):  # Ensure tasks list is not empty
                    attr = getattr(
                        tasks[0], mode
                    )  # Get the first task's attribute to check type
                    if isinstance(
                        attr, datetime
                    ):  # Handle datetime attributes like deadline
                        return [
                            task
                            for task in tasks
                            if getattr(task, mode).date() == target.date()
                        ]
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
        calendar.filter_tasks_by_deadline(
            target=datetime.now(), tasks=calendar.tasks, mode="monthh"
        )
    )
