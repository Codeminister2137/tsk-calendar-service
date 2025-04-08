from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Union

from .enums import Status


@dataclass
class Category:
    name: str


@dataclass
class Task:
    name: str
    expected_duration: timedelta | None = None
    actual_duration: timedelta | None = None
    categories: List[Category] | None = None
    deadline: datetime = field(default_factory=lambda: datetime.max)
    priority: int = 5
    notifications: List[datetime] | None = None
    status: Status = Status.INIT


    def __str__(self):
        return self.name

    @classmethod
    def get_attribute_tuple(cls):
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
