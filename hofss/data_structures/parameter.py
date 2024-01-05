from dataclasses import dataclass


@dataclass
class Parameter:
    """a parameter that describes the structural properties and/or integrity of a structure
    """

    name: str
    value: float
    standard_deviation: float
