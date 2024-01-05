from dataclasses import dataclass

from .organization import Organization
from .factor import Factor


@dataclass
class Actor:

    name: str
    organization: Organization
    factors: list[Factor]
