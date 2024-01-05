from dataclasses import dataclass


@dataclass
class Project:
    """a project within which the design and construction of a structure is performed
    """

    name: str
    time_budget: str
    monetary_budget: str
