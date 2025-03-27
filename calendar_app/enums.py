from enum import Enum


class Status(Enum):
    INIT = 0
    PENDING = 1
    FINISHED = 2
    FAILED = 3
