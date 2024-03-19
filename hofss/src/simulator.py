from __future__ import annotations
import os
import re
import numpy as np
import pandas as pd
from copy import copy

from .task import Task
from .structure import Structure
from .scenario import Scenario
from ..data_structures import Factor, TaskType


class Simulator:

    def __init__(self, structure: Structure, tasks: list[Task]) -> None:

        self.tasks = tasks
        self.structure = structure

        return

    @staticmethod
    def _data_column_sort_key(s):
        re_result = re.match(r"(\D*)(\d*)(\D*)", s)
        if re_result:
            return (re_result.group(1), int(re_result.group(2)), re_result.group(3))
        else:
            return (s, None, None)

    def simulate(self, seed: int, number_of_parameter_draws: int = 1e8) -> pd.Dataframe:

        # create a random number generator
        rng = np.random.default_rng(seed)

        # make a copy of self.structure, such that the initial values remain
        structure_copy = self.structure.make_copy(rng)

        # run the simulation
        failure_probabilities = structure_copy.calculate_failure_probabilities(
            number_of_iterations=number_of_parameter_draws
        )
        failure_probabily_rows = [failure_probabilities]
        for task in self.tasks:
            task_result = task.do_task(rng=rng)
            task_result["error_magnitude"] = None

            # if no error occured during this task, continue to the next task
            if task_result["scenario"] is not None:
                error_magnitude = structure_copy.update_parameters(task_result, rng)
                task_result["error_magnitude"] = error_magnitude
                failure_probabilities = structure_copy.calculate_failure_probabilities(
                    number_of_iterations=number_of_parameter_draws
                )
                task_result["scenario"] = task_result["scenario"].name
            failure_probabily_rows.append(pd.concat([task_result, failure_probabilities]))

        # combine the failure probability results of each task in one dataframe
        collective_df = pd.concat(failure_probabily_rows, axis=1).T

        # sort the columns in a way that is more convenient to read
        sorted_columns = [
            "task", "human_error_occured", "error_discovered", "error_corrected", "scenario",
            "complexity_level", "error_magnitude", "hep", "bendingMomentULS", "total"
        ]
        other_columns = []
        for column in collective_df.columns:
            if column in sorted_columns:
                continue
            other_columns.append(column)

        sorted_columns.extend(sorted(other_columns, key=self._data_column_sort_key))
        collective_df = collective_df[sorted_columns]

        return collective_df

    @classmethod
    def parse_from_directory(
        cls, directory: str, hofs_filename: str = "hofs_frequencies_and_multipliers.csv",
        task_types_filename: str = "gtt_nhep_hofs.csv", structure_filename: str = "structure.csv",
        scenarios_filename: str = "scenarios.csv", tasks_filename: str = "tasks.csv"
    ) -> Simulator:

        # load the factors, tasks, scenarios, and structure
        hofs = Factor.parse_from_file(os.path.join(directory, hofs_filename))
        task_types = TaskType.parse_from_file(os.path.join(directory, task_types_filename), hofs=hofs)
        structure = Structure.parse_from_file(os.path.join(directory, structure_filename))
        scenarios = Scenario.parse_from_file(os.path.join(directory, scenarios_filename))
        tasks = Task.parse_from_file(os.path.join(directory, tasks_filename), task_types, scenarios)
        return cls(structure, tasks)
