from enum import Enum


class PropertiesCalculationType(int, Enum):
    PT = 0
    "0 - Fixed Temperature/Pressure"
    VT = 1
    "1 - Fixed Temperature/Volume"
    PV = 2
    """2 - Fixed Pressure/Volume"""

    def __str__(self) -> str:
        return str(self.value)
