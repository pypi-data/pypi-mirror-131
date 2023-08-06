from enum import Enum


class FlashCalculationType(int, Enum):
    PT = 0
    """Fixed Temperature/Pressure"""
    PH = 1
    """Fixed Temperature/Enthalpy"""
    PS = 2
    """Fixed Temperature/Entropy"""

    def __str__(self) -> str:
        return str(self.value)
