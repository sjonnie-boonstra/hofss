from hofss import *

hofs = Factor.parse_from_file(r"C:\Users\xinren\Desktop\HOFSS\ABM MODEL\model input\hofs_frequencies_and_multipliers.csv")
task_types = TaskType.parse_from_file(r"C:\Users\xinren\Desktop\HOFSS\ABM MODEL\model input\gtt_nhep_hofs.csv", hofs=hofs)



# task_1 = Task(
#     name="first_task",
#     task_type=task_types[0],
#     possible_scenarios=[Scenario]
# )