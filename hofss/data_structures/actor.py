from dataclasses import dataclass

from .organization import Organization
from .factor import Factor


@dataclass
class Actor:
    """an actor within the structural design of a structure (e.g. an engineer or a contractor)
    """

    name: str
    organization: Organization
    factors: list[Factor]
