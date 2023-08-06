from enum import Enum


class ApiCallResult(int, Enum):
    SUCCESS = 0
    """0 - Success"""
    FAILED = 1
    """1 - Failed"""

    def __str__(self) -> str:
        return str(self.value)
