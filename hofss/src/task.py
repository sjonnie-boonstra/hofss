from typing import Iterable

from .structure import Structure
from ..data_structures import Actor, Factor, TaskType, Scenario


class Task:
    """A task within the design or construction of a structure"""

    def __init__(
        self, name: str, factors: list[Factor], assignee: Actor,
        task_type: [str | TaskType], structure: Structure = None
    ) -> None:

        self.name = name
        self.factors = factors
        self.assignee = assignee
        self.type = task_type
        self.structure = structure
        return

    @property
    def name(self) -> str:
        """the name of this task"""
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"name should be of type: str; received: {type(value).__name__}")
        self._name = value
        return

    @property
    def factors(self) -> list[Factor]:
        """the task specific factors that influence this task"""
        return self._factors

    @factors.setter
    def factors(self, values: list[Factor]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"factors should be an iterable and not of type str")
        for i, value in enumerate(values):
            if not isinstance(value, Factor):
                raise TypeError(f"item at index '{i}' is not of type: Factor; received: {type(value).__name__}")
        self._factors = list(values)
        return

    @property
    def assignee(self) -> Actor:
        """the Actor to which this task is assigned"""
        return self._assignee

    @assignee.setter
    def assignee(self, value: Actor):
        if not isinstance(value, Actor):
            raise TypeError(f"assignee should be of type: Actor; received: {type(value).__name__}")
        self._assignee = value
        return

    @property
    def structure(self) -> Structure:
        """the structure for which this task is performed"""
        return self._structure

    @structure.setter
    def structure(self, value: Structure):
        if not isinstance(value, Structure) and value is not None:
            raise TypeError(f"structure should be of type: Structure; received: {type(value).__name__}")
        self._structure = value
        return

    @property
    def task_type(self) -> TaskType:
        """the type of this task"""
        return self._task_type

    @task_type.setter
    def task_type(self, value: TaskType):
        if not isinstance(value, TaskType):
            try:
                value = TaskType.cast(value)
            except Exception as err:
                raise TypeError(f"task_type should be castable to enum: TaskType; received error:\n{repr(err)}")
        self._task_type = value
        return

    def do_task(self) -> None | Scenario:

        return
