from enum import Enum


class ComponentType(int, Enum):
    STANDARD = 0
    """0 - Standard"""
    POLYMER = 1
    """1 - Polymer"""
    CO_POLYMER = 2
    """2 - coPolymer"""

    def __str__(self) -> str:
        return str(self.value)
