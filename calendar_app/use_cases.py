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
    def modify_task(task_id: int, tasks: List[Task], updates) -> Task:
        """
        Modify a task in the provided list of tasks based on its index and update the provided attributes.

        Args:
            task_id (int): The id of the task to modify.
            tasks (List[Task]): The list of tasks to modify.
            updates (dict): A dictionary of attributes to update.

        Returns:
            Task | Raises ValueError

        Examples:
            >>> task = Task.objects.create(name="Task 1")
            >>> Calendar.modify_task(task.id, tasks, {"name": "Task 2"})
            >>> print(task.name)
            Task 2
        """
        if len(tasks) > task_id:
            task = tasks[task_id]
            task.modify(updates=updates)
            return task
        else:
            raise ValueError("Task not found in list")

    @staticmethod
    def map_mode(mode: str) -> str:
        """
        Map the provided mode to a standardized mode used in ordering or grouping.

        Args:
            mode (str): The input mode to normalize.

        Returns:
            str: The standardized form of the mode.

        Examples:
            >>> Calendar.map_mode("deadline_week")
            'deadline'
            >>> Calendar.map_mode("categories")
            'categories_quantity'
        """
        mapper = {
            "deadline_day": "deadline",
            "deadline_week": "deadline",
            "deadline_month": "deadline",
            "deadline_year": "deadline",
            "notifications": "notifications_quantity",
            "categories": "categories_quantity",
        }
        return mapper[mode] if mode in mapper else mode

    @staticmethod
    def get_most_important_task(tasks: List[Task]) -> Task:
        """
        Retrieve the task with the highest priority value from a list.

        Args:
            tasks (List[Task]): The list of tasks to search.

        Returns:
            Task | None: The task with the highest priority, or None if list is empty.

        Examples:
            >>> task1 = Task.objects.create(name="Low", priority=1)
            >>> task2 = Task.objects.create(name="High", priority=5)
            >>> Calendar.get_most_important_task([task1, task2])
            <Task: High>
        """
        return max(tasks, key=lambda task: task.priority.value, default=None)

    def order_by_attribute(
        self, tasks: List[Task], mode: str, reverse=True
    ) -> List[Task]:
        """
        Order tasks based on a given attribute such as status, priority, or custom fields.

        Args:
            tasks (List[Task]): The list of tasks to sort.
            mode (str): The attribute used to sort tasks.
            reverse (bool): Whether to sort descending. Defaults to True.

        Returns:
            List[Task]: Sorted list of tasks.

        Raises:
            ValueError: If the attribute is not supported or excluded.

        Examples:
            >>> task1 = Task.objects.create(name="Low", priority=1)
            >>> task2 = Task.objects.create(name="High", priority=5)
            >>> calendar = Calendar()
            >>> calendar.order_by_attribute([task1, task2], mode="priority")
            [<Task: High>, <Task: Low>]
        """
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
        """
        Group tasks by a specified mode such as status, priority, or deadline time unit. Groups are then sorted by order_by_attribute method.

        Args:
            tasks (List[Task]): The list of tasks to group.
            mode (str): The attribute or group mode to use.

        Returns:
            Dict[str, List[Task]]: Dictionary of grouped tasks by key.

        Raises:
            ValueError: If the grouping mode is unsupported or excluded.

        Examples:
            >>> task1 = Task.objects.create(name="A", deadline=datetime(2025, 7, 21))
            >>> task2 = Task.objects.create(name="B", deadline=datetime(2025, 7, 22))
            >>> calendar = Calendar()
            >>> calendar.group_by_attribute([task1, task2], "deadline_day")
            {
                '2025-07-21': [<Task: A>],
                '2025-07-22': [<Task: B>]
            }
        """
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
                    if hasattr(task, mode) and mode not in self.excluded_order_modes:
                        grouped[getattr(task, mode)].append(task)
                    elif mode in self.excluded_group_modes:
                        raise ValueError(f"Banned group mode: {mode}")
                    else:
                        raise ValueError(f"Unsupported group mode: {mode}")

        for item in grouped:
            mode = self.map_mode(mode)
            grouped[item] = self.order_by_attribute(grouped[item], mode, reverse=True)

        return grouped

    @staticmethod
    def filter_by_attribute(tasks: List[Task], mode: str, target) -> List[Task]:
        """
        Filter tasks by a given attribute and target value (e.g. category, priority, deadline).

        Args:
            tasks (List[Task]): The list of tasks to filter.
            mode (str): The filtering mode (attribute name or alias).
            target: The value to match against.

        Returns:
            List[Task]: List of tasks matching the filter criteria.

        Raises:
            ValueError: If the mode is unsupported or excluded.

        Examples:
            >>> task1 = Task.objects.create(name="X", deadline=datetime(2025, 7, 21))
            >>> task2 = Task.objects.create(name="Y", deadline=datetime(2025, 7, 25))
            >>> Calendar.filter_by_attribute([task1, task2], "deadline_week", datetime(2025, 7, 21))
            [<Task: X>]
        """

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
