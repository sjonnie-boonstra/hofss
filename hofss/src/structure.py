from __future__ import annotations
import os
from typing import Iterable, Callable
import numpy as np
import pandas as pd

from .scenario import Scenario
from ..data_structures import Parameter, FactorLevel
from ..failure_modes import failure_mode_functions


class Structure:

    def __init__(self, name: str, parameters: list[Parameter], failure_modes: list[callable]) -> None:
        self.name = name
        self.parameters = parameters
        self.failure_modes = failure_modes
        return

    @property
    def name(self) -> str:
        """name of this structure"""
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"name should be of type: str; received: {type(value).__name__}")
        self._name = value
        return

    @property
    def parameters(self) -> list[Parameter]:
        """the parameters that define the structural properties and integrity of this structure"""
        return self._parameters

    @parameters.setter
    def parameters(self, values: list[Parameter]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"parameters should be an iterable and not of type str")
        for i, value in enumerate(values):
            if not isinstance(value, Parameter):
                raise TypeError(f"item at index '{i}' is not of type: Parameter; received: {type(value).__name__}")
        self._parameters = list(values)
        return

    @property
    def failure_modes(self) -> list[callable]:
        """the failure modes that affect this structure"""
        return self._failure_modes

    @failure_modes.setter
    def failure_modes(self, values: list[callable]):
        if not isinstance(values, Iterable) or isinstance(values, str):
            raise TypeError(f"failure_modes should be an iterable and not of type str")
        for i, value in enumerate(values):
            if not isinstance(value, Callable):
                raise TypeError(f"item at index '{i}' is not callable; received type: {type(value).__name__}")
        self._failure_modes = list(values)
        return

    def update_parameters(self, task_result: pd.Series) -> tuple[float, None]:
        """updates the parameters according to the provided scnario

        Args:
            scenario (Scenario): the scenario that happened after a human error has occured
        """
        scenario: Scenario = task_result["scenario"]
        if task_result["scenario"] is None:
            return None

        complexity_level: FactorLevel = task_result["complexity_level"]

        # use the scenario to update this structure's prameters
        self.parameters, error_magnitude = scenario.update_parameters(self.parameters, complexity_level)
        return error_magnitude

    def draw_parameter_values(self, n: int = 1) -> dict[str, list[float]]:
        """draws parameter values for this structures from this structure's
        parameter definitions using

        Args:
            n (int): number of draws per parameter.

        Returns:
            dict[str, np.array[float]]: a dictionary with a numpy array of values (size = n)
            by their respective parameter's names
        """
        return {p.name: p.draw(n) for p in self.parameters}

    def calculate_failure_probabilities(self, number_of_iterations: int = 1e6) -> dict[str, float]:
        """calculates the failure probabilities for each failure mode through a Monte Carlo simulation

        Args:
            number_of_iterations (int, optional): the number of iterations in the
            Monte Carlo simulation. Defaults to 1e6.
            monte_carlo_seed (int, optional): the seed that is used to create the randomness
            in the Monte Carlos simulation. Defaults to None.

        Returns:
            dict[str, float]: a dictionary with the failure probability per failure mode
        """

        # draw the parameter values
        parameter_values = self.draw_parameter_values(number_of_iterations)

        # determine if failure occured per iteration and per failure mode, and calculate the
        # failure probability per mode and for the total
        failures_by_mode = {}
        total_failure = None
        for failure_mode in self.failure_modes:
            failure_criteria = failure_mode(**parameter_values)
            failure_occured = failure_criteria < 0
            failures_by_mode[failure_mode.__name__] = np.sum(failure_occured, axis=0)
            if total_failure is None:
                total_failure = failure_occured
            else:
                total_failure = np.logical_or(total_failure, failure_occured)

        failures_by_mode["total"] = np.sum(total_failure, axis=0)
        failure_probability_by_mode = {k: v / number_of_iterations for k, v in failures_by_mode.items()}

        return pd.Series(failure_probability_by_mode)

    @classmethod
    def parse_from_file(
        cls, structure_file_path: str, failure_functions: list[callable] = failure_mode_functions
    ) -> Structure:
        """parses a structure from a file.

        The data file should be comma separated (.CSV) and have the following header:

            `parameter,failure_mechanisms,mean,standard_deviation,distribution_type`

        Args:
            structure_file_path (str): the path to the file containing the structure data.
            failure_functions (list[callable], optional): a list of the failure mode functions that may be.
            assigned in the structure (as specified by the structure file). Defaults to the failure mode
            functions defined within this library.

        Raises:
            RuntimeError: if a failure mode specified in the structucture file cannot
            be found among the failure functions.

        Returns:
            Structure: the structure that was parsed from the structure file.
        """
        structure_data = pd.read_csv(structure_file_path, header=0, index_col=0)
        parameters = []
        structure_failure_modes = {}
        for index, row in structure_data.iterrows():
            failure_mechanisms = row["failure_mechanisms"].strip("[").strip("]").split(";")
            for failure_mechanism in failure_mechanisms:
                failure_mechanism = failure_mechanism.strip()
                if failure_mechanism in structure_failure_modes:
                    continue
                failure_mode_function = None
                for function in failure_functions:
                    if function.__name__.strip() == failure_mechanism:
                        failure_mode_function = function
                        break

                if failure_mode_function is None:
                    raise RuntimeError(f"unable to find function for failure mechanism: {failure_mechanism}")
                structure_failure_modes[failure_mechanism] = failure_mode_function
            parameters.append(Parameter(
                name=index, value=row["mean"], standard_deviation=row["standard_deviation"],
                distribution_function=getattr(np.random, row["distribution_type"])
            ))

        structure = cls(
            name=os.path.splitext(os.path.basename(structure_file_path))[0],
            parameters=parameters, failure_modes=list(structure_failure_modes.values())
        )
        return structure
