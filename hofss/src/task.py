from __future__ import annotations
from typing import Iterable
import random
import pandas as pd

from .scenario import Scenario
from ..data_structures import TaskType, FactorLevel


class Task:
    """A task within the design or construction of a structure"""

    def __init__(
        self, name: str, task_type: TaskType, scenarios: list[Scenario], scenario_probabilities: list[float]
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
        self.scenarios = scenarios
        self.scenario_probabilities = scenario_probabilities
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

    @property
    def scenarios(self) -> list[Scenario]:
        """the task specific scenarios that may occur after a human error occurs"""
        return self._scenarios

    @scenarios.setter
    def scenarios(self, values: list[Scenario]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"scenarios should be an iterable and not of type {type(values).__name__}")
        for i, value in enumerate(values):
            if not isinstance(value, Scenario):
                raise TypeError(f"item at index '{i}' is not of type: Scenario; received: {type(value).__name__}")
        self._scenarios = list(values)
        return

    @property
    def scenario_possibilities(self) -> list[float]:
        """the possibilites of each respective scenario"""
        return self._scenario_possibilities

    @scenario_possibilities.setter
    def scenario_possibilities(self, values: list[float]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"scenario_probabilities should be an iterable and not of type {type(values).__name__}")
        scenario_probabilities = []
        for i, value in enumerate(values):
            try:
                scenario_probabilities.append(float(value))
            except:
                raise TypeError(f"item at index '{i}' can't be cast to a float; received type: {type(value).__name__}")
        self._scenarios = scenario_probabilities
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
    def parse_from_file(
        cls, task_file_path: str, project_task_types: list[TaskType], project_scenarios: list[Scenario]
    ) -> list[Task]:

        task_data = pd.read_csv(task_file_path, header=0, index_col=0)
        tasks = []
        for index, row in task_data.iterrows():

            # find the instance of the task type from the specified list of task types
            task_type_name = row["task_type"]
            task_type = None
            for project_task_type in project_task_types:
                if project_task_type.name == task_type_name:
                    task_type = project_task_type
                    break

            if task_type is None:
                raise ValueError(f"unable to find task type: '{task_type_name}' specified for task '{index}'")

            # parse the names and probabilities of the scenarios assigned to this task in case an error occurs
            scenarios_and_probabilities = map(
                lambda x: tuple(x.split("&")),
                row["scenarios_and_probabilities"].strip("[").strip("]").split(";")
            )
            scenario_names, scenario_probabilities = zip(*scenarios_and_probabilities)

            scenario_probabilities = [float(p) for p in scenario_probabilities]

            # check if the sum of all scenario probabilities is 1
            if sum(scenario_probabilities) != 1.0:
                raise RuntimeError(
                    f"sum of scenario possibilties for taks '{index}' should be 1, is: {sum(scenario_probabilities)}"
                )

            # find the matching scenario instance with each scenario name
            scenarios = []
            for scenario_name in scenario_names:
                scenario_match = None

                for project_scenario in project_scenarios:
                    if project_scenario.name == scenario_name:
                        scenario_match = project_scenario
                        break
                if scenario_match is None:
                    raise RuntimeError(f"unable to find scenario '{scenario_name}' that is defined for task '{index}'")
                scenarios.append(scenario_match)

            tasks.append(cls(
                name=index, task_type=task_type, scenarios=scenarios,
                scenario_probabilities=list(scenario_probabilities)
            ))

        return tasks
