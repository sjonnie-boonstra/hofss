from __future__ import annotations
import dataclasses
from copy import copy
import pandas as pd

from ..data_structures import Parameter, FactorLevel


class Scenario:
    """a scenario that is initiated by a human error
    """

    def __init__(self, name: str, affected_parameters: list[str], description: str = "") -> None:
        self.name = name
        self.description = description
        self.affected_parameters = affected_parameters
        return

    def update_parameter(self, initial_parameters: list[Parameter], complexity_level: FactorLevel) -> Parameter:
        parameters = copy(initial_parameters)

        affected_parameters = copy(self.affected_parameters)
        for i, parameter in enumerate(parameters):
            if not parameter.name in affected_parameters:
                continue
            affected_parameters.remove(parameter)

            # determine new value of parameter
            updated_parameter = dataclasses.replace(parameter)
            # >>>>>>>>>>>>>>> MAGIC HERE <<<<<<<<<<<<<<<<<<<<<
            parameters[i] = updated_parameter
        return parameters

    @classmethod
    def parse_from_file(cls, scenario_file_path: str) -> list[Scenario]:

        scenario_data = pd.read_csv(scenario_file_path, header=0, index_col=0)

        scenarios = []
        for index, row in scenario_data.iterrows():
            scenarios.append(cls(
                name=index, description=row["description"],
                affected_parameters=row["affected_parameters"].strip("[").strip("]").split(";")
            ))

        return scenarios
