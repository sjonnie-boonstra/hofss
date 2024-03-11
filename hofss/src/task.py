from typing import Iterable
import random
import pandas as pd

from ..data_structures import TaskType, Scenario, FactorLevel


class Task:
    """A task within the design or construction of a structure"""

    def __init__(
        self, name: str, task_type: TaskType, possible_scenarios: list[Scenario],
    ) -> None:
        """
        Args:
            name (str): the name of the task
            assignee (Actor): the actor to which this task is assigned
            task_type (TaskType]): the type of this task
            possible_scenarios (list[Scenario]): the scenarios that may occur after a human error occurs
        """
        self.name = name
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

    def determine_hep(self) -> tuple[float, FactorLevel]:
        """determines the Human Error Probability (HEP) for this task given the task's factors

        Returns:
            float: the probability that this task leads to a human error
        """
        composite_multiplier = 1
        complexity_level = None
        for factor in self.task_type.factors:
            factor_multiplier, factor_level = factor.draw_multiplier()
            composite_multiplier *= factor_multiplier
            if "complexity" in factor.description:
                complexity_level = factor_level
        if complexity_level is None:
            raise RuntimeError("unable to determine complexity level when determining HEP")

        hep = (self.task_type.nhep * composite_multiplier) / (self.task_type.nhep * (composite_multiplier - 1) + 1)
        return hep, complexity_level

    def do_task(self) -> None | Scenario:
        """performs the task: first determines the Human Error Probability (HEP); if an error occurs resolves
        if the error is found and consequently fixed; if the error is not fixed, determines the scenario that
        arises from the human error and returns this scenario

        Returns:
            None | Scenario: the scenario if an error occurs, None if no error occurs or if it is found and corrected
        """
        # determine the HEP
        task_hep, complexity_level = self.determine_hep()

        # determine if human error occurs or not
        if task_hep < random.uniform(0, 1):
            return None  # no human error occurs

        # if this code is reached, a human error occurred
        # determine if a check resolves the error
        human_error_discovered = 0.8 >= random.uniform(0, 1)
        if human_error_discovered:
            human_error_corrected = 0.9 >= random.uniform(0, 1)
            if human_error_corrected:
                return None

        # if this code is reached, the human error was not corrected
        # determine scenario
        Scenario = None

        return Scenario, complexity_level

    @classmethod
    def parse_from_file(cls, task_file_path: str, task_types: list[TaskType], scenarios: list[Scenario]):

        task_data = pd.read_csv(task_file_path, header=0, index_col=0)
        tasks = []
        for index, row in task_data:

            # parse the names and probabilities of the scenarios assigned to this task in case an error occurs
            scenarios_and_probabilities = map(
                lambda x: tuple(x.split("&")),
                row["scenarios_and_probabilities"].strip("[").strip("]").split(";")
            )
            scenario_names, scenario_probabilities = zip(*scenarios_and_probabilities)

            # check if the sum of all scenario probabilities is 1
            if sum(scenario_probabilities) != 1.0:
                raise RuntimeError(
                    f"sum of scenario possibilties for taks '{index}' should be 1, is: {sum(scenario_probabilities)}"
                )

            # find the matching scenario instance with each scenario name
            scenarios = []
            for scenario_name in scenario_names:
                scenario_match = None

                if scenario_match is None:
                    raise RuntimeError(f"unable to find scenario '{scenario_name}' that is defined for task '{index}'")
                scenarios.append(scenario_match)

            tasks.append(cls(
                name=index, task_type=task_types, scenarios=scenarios,
                scenario_probabilities=list(scenario_probabilities)
            ))

        return tasks
