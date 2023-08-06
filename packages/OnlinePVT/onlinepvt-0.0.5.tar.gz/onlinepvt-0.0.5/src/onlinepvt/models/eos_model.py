from enum import Enum


class EosModel(int, Enum):
    PCSAFT = 0
    """0 - PC-SAFT"""
    CO_PCSAFT = 1
    """1 - coPC-SAFT"""

    def __str__(self) -> str:
        return str(self.value)
