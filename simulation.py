import time
import random
import re
import pandas as pd
from hofss import *

# seed the global random number generator using the current time
seed = time.time_ns()
random.seed(seed)

# load the factors, tasks, scenarios, and structure
hofs = Factor.parse_from_file("data/hofs_frequencies_and_multipliers.csv")
task_types = TaskType.parse_from_file("data/gtt_nhep_hofs.csv", hofs=hofs)
structure = Structure.parse_from_file("data/structure.csv")
scenarios = Scenario.parse_from_file("data/scenarios.csv")
tasks = Task.parse_from_file("data/tasks.csv", task_types, scenarios)

# # run the simulation
failure_probabilities = structure.calculate_failure_probabilities(number_of_iterations=1e6)
failure_probabily_rows = [failure_probabilities]
for task in tasks:
    task_result = task.do_task()
    task_result["error_magnitude"] = None

    # if no error occured during this task, continue to the next task
    if task_result["scenario"] is not None:
        error_magnitude = structure.update_parameters(task_result)
        task_result["error_magnitude"] = error_magnitude
        failure_probabilities = structure.calculate_failure_probabilities(number_of_iterations=1e6)
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


def sort_key(s):
    re_result = re.match(r"(\D*)(\d*)(\D*)", s)
    if re_result:
        return (re_result.group(1), int(re_result.group(2)), re_result.group(3))
    else:
        return (s, None, None)


sorted_columns.extend(sorted(other_columns, key=sort_key))
collective_df = collective_df[sorted_columns]

# store the dataframe to file
collective_df.to_csv(f"results/sim_{seed}.csv", index=False)
