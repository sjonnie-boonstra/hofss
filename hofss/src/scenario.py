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
        self.possible_parameter_mutation = [
            *[("increase", parameter) for parameter in increasing_parameters],
            *[("decrease", parameter) for parameter in decreasing_parameters],
            *[("", parameter) for parameter in deviating_parameters],
        ]
        return

    def update_parameters(
        self, initial_parameters: list[Parameter], complexity_level: FactorLevel, rng: np.random.Generator = None
    ) -> tuple[list[Parameter], float]:

        if rng is None:
            rng = np.random.default_rng

        parameters = copy(initial_parameters)

        error_magnitude = rng.lognormal(0, complexity_level.value)
        mutation, mutated_parameter = rng.choice(self.possible_parameter_mutation)
        if mutation == "increase" and error_magnitude < 1.0:
            error_magnitude = 1 / error_magnitude
        elif mutation == "decrase" and error_magnitude > 1.0:
            error_magnitude = 1 / error_magnitude

        for i, parameter in enumerate(parameters):
            if parameter.name != mutated_parameter:
                continue

            # update the parameter
            updated_parameter = dataclasses.replace(parameter)
            updated_parameter.value *= error_magnitude
            parameters[i] = updated_parameter
            break
        return parameters, mutated_parameter, error_magnitude

    @classmethod
    def parse_from_file(cls, scenario_file_path: str) -> list[Scenario]:

        scenario_data = pd.read_csv(scenario_file_path, header=0).fillna("")

        scenarios = []
        for _, row in scenario_data.iterrows():
            increasing_parameters = [p for p in row["increasing_parameters"].split(";") if p.strip() != ""]
            decreasing_parameters = [p for p in row["decreasing_parameters"].split(";") if p.strip() != ""]
            deviating_parameters = [p for p in row["deviating_parameters"].split(";") if p.strip() != ""]
            scenarios.append(cls(
                name=row["name"], description=row["description"],
                increasing_parameters=increasing_parameters,
                decreasing_parameters=decreasing_parameters,
                deviating_parameters=deviating_parameters
            ))

        return scenarios

    def __str__(self) -> str:
        return self.name
