from enum import Enum


class DistributionModel(int, Enum):
    GAMMA = 0
    """0 - Gamma"""
    LN_NORMAL = 1
    """1 - LnNormal"""
    BETA = 2
    """2 - Beta"""
    CHI_SQUARE = 3
    """3 - ChiSquare"""

    def __str__(self) -> str:
        return str(self.value)
