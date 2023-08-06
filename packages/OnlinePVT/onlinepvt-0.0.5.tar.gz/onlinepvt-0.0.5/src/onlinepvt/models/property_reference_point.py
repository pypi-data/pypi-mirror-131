from enum import Enum


class PropertyReferencePoint(int, Enum):
    ORIGINAL = 0
    """0 - Original"""
    IDEAL_GAS = 1
    """1 - Ideal Gas"""
    STANDARD_STATE = 2
    """2 - Standard State"""

    def __str__(self) -> str:
        return str(self.value)
