from enum import Enum


class FactorLevel(Enum):
    """the level of a factor, can be used to assess the conditions with respect to a factor
    """

    OBVIOUS = "obvious"  # easy conditions
    NOMINAL = "nominal"  # normal conditions
    MODERATE = "moderate"  # moderate conditions
    HIGH = "high"  # difficult conditions
