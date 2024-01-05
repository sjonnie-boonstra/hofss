from dataclasses import dataclass


@dataclass
class Scenario:
    """a scenario that may happen after a human error occurs.
    A scenario defines how certain parameters may be affected
    """

    name: str
    description: str
