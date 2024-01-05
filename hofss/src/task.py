from typing import Iterable

from .structure import Structure
from ..data_structures import Actor, Factor, TaskType, Scenario


class Task:
    """A task within the design or construction of a structure"""

    def __init__(
        self, name: str, factors: list[Factor], assignee: Actor,
        task_type: [str | TaskType], possible_scenarios: list[Scenario],
    ) -> None:
        """_summary_

        Args:
            name (str): the name of the task
            factors (list[Factor]): the task specific factors that affect this task
            assignee (Actor): the actor to which this task is assigned
            task_type (str  |  TaskType]): the type of this task
            possible_scenarios (list[Scenario]): the scenarios that may occur after a human error occurs
        """
        self.name = name
        self.factors = factors
        self.assignee = assignee
        self.type = task_type
        self.possible_scenarios = possible_scenarios
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
    def possible_scenarios(self) -> list[Scenario]:
        """the task specific possible_scenarios that may occur after a human error occurs"""
        return self._possible_scenarios

    @possible_scenarios.setter
    def possible_scenarios(self, values: list[Scenario]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"possible_scenarios should be an iterable and not of type str")
        for i, value in enumerate(values):
            if not isinstance(value, Scenario):
                raise TypeError(f"item at index '{i}' is not of type: Scenario; received: {type(value).__name__}")
        self._possible_scenarios = list(values)
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

    def determine_hep(self, factors: list[Factor], base_hep: float = 1e-3) -> float:
        """determines the Human Error Probability (HEP) for this task given the specified factors

        Args:
            factors (list[Factor]): the factors that affect the HEP

        Returns:
            float: the probability that this task leads to a human error
        """
        hep = base_hep
        for factor in factors:
            # update the hep based on this factor
            pass
        return hep

    def do_task(self) -> None | Scenario:
        """performs the task: first determines the Human Error Probability (HEP); if an error occurs resolves
        if the error is found and consequently fixed; if the error is not fixed, determines the scenario that
        arises from the human error and returns this scenario

        Returns:
            None | Scenario: the scenario if an error occurs, None if no error occurs or if it is found and corrected
        """
        # collect all factors that affect this task
        factors = [
            *self.assignee.factors,
            *self.factors,
            *self.assignee.organization.factors,
        ]
        # determine the HEP
        hep = self.determine_hep(factors)

        # determine if human error occurs or not
        human_error_occurs = False

        if not human_error_occurs:
            return None

        # if this code is reached, a human error occurred
        # determine if a check resolves the error
        human_error_discovered = False
        if human_error_discovered:
            human_error_corrected = False
            if human_error_corrected:
                return None

        # if this code is reached, the human error was not corrected
        # determine scenario
        Scenario = None

        return Scenario
