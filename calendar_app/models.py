from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .enums import Status


@dataclass
class Category:
    name: str


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
