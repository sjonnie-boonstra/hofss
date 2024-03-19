import time
from hofss import Simulator

# seed the global random number generator using the current time
seed = time.time_ns()

simulator = Simulator.parse_from_directory("data")
data_1 = simulator.simulate(seed, 1e6)
data_2 = simulator.simulate(seed, 1e6)

# store the dataframe to file
data_1.to_csv(f"results/sim1_{seed}.csv", index=False)
data_2.to_csv(f"results/sim2_{seed}.csv", index=False)
