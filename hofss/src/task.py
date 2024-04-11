from __future__ import annotations
from typing import Iterable
import random
import pandas as pd
import numpy as np

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
        self.task_type = task_type
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

    def determine_hep(self, rng: np.random.Generator = None) -> pd.Series:
        """determines the Human Error Probability (HEP) for this task given the task's factors

        Returns:
            float: the probability that this task leads to a human error
        """

        if rng is None:
            rng = np.random.default_rng()

        hep_data = {}
        multiplier_values = []
        complexity_level = None
        for factor in self.task_type.factors:
            factor_multiplier, factor_level = factor.draw_multiplier(rng)
            hep_data[f"{factor.name}_multiplier"] = factor_multiplier
            multiplier_values.append(factor_multiplier)
            if "complexity" in factor.description:
                complexity_level = factor_level

        if complexity_level is None:
            raise RuntimeError("unable to determine complexity level when determining HEP")
        hep_data["complexity_level"] = complexity_level

        multiplier_values = np.array(multiplier_values)
        composite_multiplier = multiplier_values.prod()**(1.0/len(multiplier_values))
        hep = composite_multiplier * self.task_type.nhep
        # hep = (self.task_type.nhep * composite_multiplier) / (self.task_type.nhep * (composite_multiplier - 1) + 1)

        # hep = min(multiplier_values) * max(multiplier_values) * self.task_type.nhep
        # hep = np.product(multiplier_values) * self.task_type.nhep / float(len(multiplier_values))
        # hep = np.product(multiplier_values) * self.task_type.nhep

        hep_data["hep"] = hep
        return hep_data

    def do_task(self, rng: np.random.Generator = None) -> pd.Series:
        """performs the task: first determines the Human Error Probability (HEP); if an error occurs resolves
        if the error is found and consequently fixed; if the error is not fixed, determines the scenario that
        arises from the human error and returns this scenario

        Returns:
            None | Scenario: the scenario if an error occurs, None if no error occurs or if it is found and corrected
        """

        if rng is None:
            rng = np.random.default_rng()

        # initiate task result dict with default values
        task_result = {"task": self.name, "scenario": None}

        # determine the HEP
        hep_data = self.determine_hep(rng=rng)
        task_hep = hep_data["hep"]
        task_result.update(hep_data)

        # determine if human error occurs or not
        if task_hep < rng.uniform(0, 1):
            return pd.Series(task_result)  # no human error occurs

        # if this code is reached, the human error has occured, determin scenario
        scenario_draw = rng.uniform(0, 1)
        probability_sum = 0
        scenario = None
        for scenario, probability in zip(self.scenarios, self.scenario_probabilities):
            probability_sum += probability
            if scenario_draw < probability_sum:
                break

        task_result["scenario"] = scenario
        return pd.Series(task_result)

    @classmethod
    def parse_from_file(
        cls, task_file_path: str, project_task_types: list[TaskType], project_scenarios: list[Scenario]
    ) -> list[Task]:

        task_data = pd.read_csv(task_file_path, header=0, index_col=0).fillna("")
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
            scenario_names, scenario_probabilities = [], []
            for field in row["scenarios_and_probabilities"].split(";"):
                if field == "":
                    continue
                scenario_name, scenario_probability = field.split("&")
                scenario_names.append(scenario_name)
                scenario_probabilities.append(float(scenario_probability))

            # check if the sum of all scenario probabilities is 1
            if round(sum(scenario_probabilities), 3) != 1.0 and len(scenario_probabilities) != 0:
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
