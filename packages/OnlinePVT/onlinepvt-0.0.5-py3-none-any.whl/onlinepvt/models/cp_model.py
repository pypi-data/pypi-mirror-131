from enum import Enum


class CpModel(int, Enum):
    POLYNOMIAL = 0
    """0 - Polynomial"""
    DIPPR = 1
    """1 - DIPPR"""

    def __str__(self) -> str:
        return str(self.value)
