from dataclasses import dataclass


@dataclass
class Factor:
    """a factor that influences the Human Error Probability of a task
    """

    name: str
    value: float
