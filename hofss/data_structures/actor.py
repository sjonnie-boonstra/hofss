from dataclasses import dataclass

from .factor import Factor


@dataclass
class Actor:

    name: str
    factors: list[Factor]
