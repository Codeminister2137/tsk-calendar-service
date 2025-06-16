from enum import Enum


class Status(Enum):
    INIT = 0
    PENDING = 1
    FINISHED = 2
    FAILED = -1


class Priority(Enum):
    UNIMPORTANT = 0
    LOWEST = 1
    LOWER = 2
    LOW = 3
    MEDIUM = 4
    HIGH = 5
    HIGHER = 6
    HIGHEST = 7
