from hofss import *

hofs = Factor.parse_from_file("data/hofs_frequencies_and_multipliers.csv")
task_types = TaskType.parse_from_file("data/gtt_nhep_hofs.csv", hofs=hofs)


# task_1 = Task(
#     name="first_task",
#     task_type=task_types[0],
#     possible_scenarios=[Scenario]
# )
