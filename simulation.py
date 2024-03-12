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
failure_probabily_dataframes = []
for task in tasks:
    scenario, complexity_level = task.do_task()
    structure.update_parameters(scenario, complexity_level)
    failure_probabilities = structure.calculate_failure_probabilities(number_of_iterations=1e6)

# store the result
collective_df = pd.concat(failure_probabily_dataframes)
collective_df.to_csv(f"results/sim_{seed}.csv")
