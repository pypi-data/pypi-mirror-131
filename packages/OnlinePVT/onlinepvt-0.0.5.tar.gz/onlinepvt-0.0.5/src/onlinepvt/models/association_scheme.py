from enum import Enum


class AssociationScheme(int, Enum):
    NONE = 0
    """0 - None"""
    USER = 1
    """1 - User"""
    AS_1A = 2
    """2 - 1A"""
    AS_1C = 3
    """3 - 1C"""
    AS_1D = 4
    """4 - 1D"""
    AS_2A = 5
    """5 - 2A"""
    AS_2B = 6
    """6 - 2B"""
    AS_2C = 7
    """7 - 2C"""
    AS_2D = 8
    """8 - 2D"""
    AS_3A = 9
    """9 - 3A"""
    AS_3B = 10
    """10 - 3B"""
    AS_4A = 11
    """11 - 4A"""
    AS_4B = 12
    """12 - 4B"""
    AS_4C = 13
    """13 - 4C"""

    def __str__(self) -> str:
        return str(self.value)
