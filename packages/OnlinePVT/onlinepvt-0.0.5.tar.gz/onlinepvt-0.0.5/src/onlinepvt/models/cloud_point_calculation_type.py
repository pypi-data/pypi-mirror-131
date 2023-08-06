from enum import Enum


class CloudPointCalculationType(int, Enum):
    FIXED_TEMPERATURE = 0
    """0 - Fixed Temperature"""
    FIXED_PRESSURE = 1
    """1 - Fixed Pressure"""

    def __str__(self) -> str:
        return str(self.value)
