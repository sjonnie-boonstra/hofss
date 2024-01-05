from abc import ABCMeta, abstractmethod  # Abstract Base Class (ABC)

from ..data_structures import Parameter


class FailureMode(ABCMeta):
    """Abstract class to define failure modes with"""

    def __init__(self, name: str) -> None:
        """Args:
            name (str): the name of this failure mode
        """
        self.name = name
        return

    @property
    def name(self) -> str:
        """the name of this failure mode"""
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"name should be of type: str; received: {type(value).__name__}")
        self._name = value
        return

    @abstractmethod
    def calculate_failure_criterion(self, parameters: list[Parameter]) -> float:
        """determines the failure criterion Z (Capacity / Acting force) for
        this failure mode. If Z < 0, failure occurs.

        Args:
            parameters (list[Parameter]): the parameters required to calculate the failure criterion

        Returns:
            float: the failure criterion for this failure mode
        """
        return None  # this method is abstract, meaning without it being overridden the class remains abstract
