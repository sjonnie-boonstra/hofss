from enum import Enum


class FactorLevel(Enum):
    """the level of a factor, can be used to assess the conditions with respect to a factor
    """

    OBVIOUS = 0.2980  # easy conditions
    NOMINAL = 0.4219  # normal conditions
    MODERATE = 0.5409  # moderate conditions
    HIGH = 0.6688  # difficult conditions

    def __str__(self) -> str:
        return self.name.lower()
