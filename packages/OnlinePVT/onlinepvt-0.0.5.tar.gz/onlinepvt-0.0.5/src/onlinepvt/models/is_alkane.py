from enum import Enum


class IsAlkane(int, Enum):
    NO = 0
    """0 - No"""
    YES = 1
    """1 - Yes"""

    def __str__(self) -> str:
        return str(self.value)
