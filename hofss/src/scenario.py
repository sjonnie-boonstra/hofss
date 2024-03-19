from __future__ import annotations
import dataclasses
from copy import copy
import pandas as pd
import numpy as np

from ..data_structures import Parameter, FactorLevel


class Scenario:
    """a scenario that is initiated by a human error
    """

    def __init__(
        self, name: str, increasing_parameters: list[str] = [], decreasing_parameters: list[str] = [],
        deviating_parameters: list[str] = [], description: str = ""
    ) -> None:
        self.name = name
        self.description = description
        self.increasing_parameters = increasing_parameters
        self.decreasing_parameters = decreasing_parameters
        self.deviating_parameters = deviating_parameters
        return

    def update_parameters(
        self, initial_parameters: list[Parameter], complexity_level: FactorLevel, rng: np.random.Generator = None
    ) -> tuple[list[Parameter], float]:

        if rng is None:
            rng = np.random.default_rng

        parameters = copy(initial_parameters)

        error_magnitude = rng.lognormal(0, complexity_level.value)
        increasing_multiplier = error_magnitude if error_magnitude > 1 else 1.0 / error_magnitude
        decreasing_multiplier = 1.0 / increasing_multiplier

        for i, parameter in enumerate(parameters):
            error_multiplier = None
            if parameter.name in self.deviating_parameters:
                error_multiplier = error_magnitude
            elif parameter.name in self.increasing_parameters:
                error_multiplier = increasing_multiplier
            elif parameter.name in self.decreasing_parameters:
                error_multiplier = decreasing_multiplier
            else:
                continue

            # update the parameter
            updated_parameter = dataclasses.replace(parameter)
            updated_parameter.value *= error_multiplier
            parameters[i] = updated_parameter
        return parameters, error_magnitude

    @classmethod
    def parse_from_file(cls, scenario_file_path: str) -> list[Scenario]:

        scenario_data = pd.read_csv(scenario_file_path, header=0).fillna("")

        scenarios = []
        for _, row in scenario_data.iterrows():
            scenarios.append(cls(
                name=row["name"], description=row["description"],
                increasing_parameters=row["increasing_parameters"].split(";"),
                decreasing_parameters=row["decreasing_parameters"].split(";"),
                deviating_parameters=row["deviating_parameters"].split(";")
            ))

        return scenarios

    def __str__(self) -> str:
        return self.name
