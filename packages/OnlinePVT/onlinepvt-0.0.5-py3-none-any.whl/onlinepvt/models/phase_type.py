from enum import Enum


class PhaseType(int, Enum):
    RESULT = 0
    """0 - Result"""
    FEED = 1
    """1 - Feed"""
    SYSTEM = 2
    """2 - System"""
    ZERO_PHASE = 3
    """3 - ZeroPhase"""

    def __str__(self) -> str:
        return str(self.value)
