from enum import Enum


class FactorLevel(Enum):
    """the level of a factor, can be used to assess the conditions with respect to a factor
    """

    OBVIOUS = 0.1  # easy conditions
    NOMINAL = 0.2  # normal conditions
    MODERATE = 0.3  # moderate conditions
    HIGH = 0.4  # difficult conditions

    def __str__(self) -> str:
        return self.name.lower()
