import os

from hofss import Simulator


# input
input_directory = "data"
output_directory = "/home/boonstra/xin_results_23_3"
number_of_parameter_draws = 1e6
parameter_draw_batch_size = 1e6

# preparation
simulator = Simulator.parse_from_directory(input_directory)
os.makedirs(output_directory, exist_ok=True)

initial_failure_probabilities = simulator.structure.calculate_failure_probabilities(
    number_of_parameter_draws, parameter_draw_batch_size
)

simulation_data = simulator.simulate(
    86, number_of_parameter_draws, parameter_draw_batch_size, initial_failure_probabilities
)

print(simulation_data)
