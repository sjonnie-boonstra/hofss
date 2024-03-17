import time
import random
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
    # if no error occured during this task, continue to the next task
    if task_result["scenario"] is not None:
        structure.update_parameters(task_result)
        failure_probabilities = structure.calculate_failure_probabilities(number_of_iterations=1e6)
        task_result["scenario"] = task_result["scenario"].name
    failure_probabily_rows.append(pd.concat([task_result, failure_probabilities]))

# store the result
collective_df = pd.concat(failure_probabily_rows, axis=1).T
collective_df.to_csv(f"results/sim_{seed}.csv", index=False)
