from dataclasses import dataclass, field

from .factor import Factor


@dataclass
class Organization:
    """an organization to which an Actor may belong
    """

    name: str
    factors: list[Factor] = field(default_factory=list)
