from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .enums import Priority, Status


class Task(models.Model):
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
    def get_attribute_tuple(cls) -> Tuple:
        return tuple(
            attribute
            for attribute in dir(cls)
            if not callable(getattr(cls, attribute)) and not attribute.startswith("__")
        )

    def modify(self, updates: Dict[str, any]) -> None:
        """
        Modify the task instance by updating its attributes based on the provided dictionary of new values.

        :param updates: Dictionary of attributes to update (e.g., {"name": "New Name", "priority": 1}).
        """
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Task has no attribute '{key}'")
