from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Union

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .enums import Priority, Status


class Task(models.Model):
    """
    Represents a task with metadata such as name, durations, categories, deadlines, priority, and status.

    Fields:
        name (str): Required. A short descriptive name for the task (max 120 characters).
        expected_duration (timedelta): Optional. Estimated time expected to complete the task.
        actual_duration (timedelta): Optional. Actual time spent on the task.
        categories (List[str]): Optional. Tags or labels associated with the task.
        deadline (datetime): Optional. Deadline by which the task should be completed. Defaults to datetime.max.
        priority (str): Optional. One of the enum values from `Priority` (e.g., "HIGH", "LOW").
        notifications (List[datetime]): Optional. List of datetime objects when notifications should be triggered.
        status (str): Optional. Current state of the task (e.g., "INIT", "TODO", "DONE") from `Status` enum.

    Methods:
        modify(updates: Dict[str, any]) -> None:
            Update one or more attributes of the task instance.
        get_attribute_tuple() -> Tuple[str, ...]:
            Return a tuple of non-callable class-level attribute names.

    Examples:
        >>> task = Task.objects.create(
        ...     name="Write documentation",
        ...     expected_duration=timedelta(hours=2),
        ...     categories=["writing", "work"],
        ...     deadline=datetime(2025, 7, 22, 12, 0),
        ...     priority="HIGH",
        ...     notifications=[datetime(2025, 7, 22, 10, 0)],
        ...     status="TODO"
        ... )
        >>> task.modify({"name": "Write final report", "priority": "MEDIUM"})
        >>> print(task.name)
        Write final report
    """

    name = models.CharField(max_length=120)
    expected_duration = models.DurationField(default=timedelta(minutes=0))
    actual_duration = models.DurationField(default=timedelta(minutes=0))
    categories = ArrayField(models.CharField(max_length=60), blank=True, default=list)
    deadline: datetime = field(
        default_factory=lambda: datetime.max.replace(tzinfo=timezone.utc)
    )
    priority = models.CharField(
        max_length=20,
        choices=[(priority.value, priority.name.title()) for priority in Priority],
        default=Priority.MEDIUM.value,
    )
    notifications = ArrayField(models.DateTimeField(), blank=True, default=list)
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name.title()) for status in Status],
        default=Status.INIT.value,
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_attribute_tuple(cls):
        """
        Return a tuple of class-level attributes.

        Returns:
            Tuple[str, ...]: A tuple of attribute names.

        Examples:
            >>> Task.get_attribute_tuple()
            ('actual_duration', 'categories', 'deadline', 'expected_duration', 'name', ...)
        """
        return tuple(
            attribute
            for attribute in dir(cls)
            if not callable(getattr(cls, attribute)) and not attribute.startswith("__")
        )

    def modify(self, updates: Dict[str, any]) -> None:
        """
        Modify the task instance by updating one or more attributes dynamically.

        Args:
            updates (Dict[str, any]): A dictionary where each key is a Task field name
                                      and each value is the new value to set.

        Raises:
            AttributeError: If any of the provided keys do not match existing Task attributes.

        Examples:
            >>> task = Task.objects.create(name="Old Name", priority="LOW")
            >>> task.modify({"name": "New Name", "priority": "HIGH"})
            >>> print(task.name)
            New Name
            >>> print(task.priority)
            HIGH
        """
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Task has no attribute '{key}'")
