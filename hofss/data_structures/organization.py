from dataclasses import dataclass, field

from .factor import Factor


@dataclass
class Organization:

    name: str
    factors: list[Factor] = field(default_factory=list)
