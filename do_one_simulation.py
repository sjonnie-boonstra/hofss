import os
import pandas as pd

from hofss import Simulator


# input
input_directory = "data"
output_directory = "/home/boonstra/test"
number_of_parameter_draws = 5e6
parameter_draw_batch_size = 5e6

# preparation
simulator = Simulator.parse_from_directory(input_directory, include_check=False)

initial_failure_probabilities = simulator.structure.calculate_failure_probabilities(1e6, 1e6)

simulation_data: pd.DataFrame = simulator.simulate(
    2, number_of_parameter_draws, parameter_draw_batch_size, initial_failure_probabilities
)
simulation_data.to_csv("test.csv", index=False)
