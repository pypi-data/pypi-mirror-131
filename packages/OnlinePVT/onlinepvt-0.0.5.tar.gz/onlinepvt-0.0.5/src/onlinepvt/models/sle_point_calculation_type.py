from enum import Enum


class SlePointCalculationType(int, Enum):
    FIXED_PRESSURE = 0
    """0 - Fixed Pressure"""
    FIXED_TP = 1
    """1 - Fixed Temperature/Pressure"""

    def __str__(self) -> str:
        return str(self.value)
