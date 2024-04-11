import numpy as np
import os
import time
import logging
import threading
import queue
from traceback import format_exc

from hofss import Simulator
logging.basicConfig(level=logging.INFO)


# input
input_directory = "data"
output_directory = "/home/boonstra/24_04_11_with_checks"
number_of_simulations = int(1e5)
number_of_parameter_draws = 5e6
parameter_draw_batch_size = 5e6
number_of_threads = 5

# preparation
simulator = Simulator.parse_from_directory(input_directory, include_check=True)
os.makedirs(output_directory, exist_ok=True)

start = time.time()
initial_failure_probabilities = simulator.structure.calculate_failure_probabilities(
    1e8, 1e7
)
end = time.time()
logging.info(f"determined initial failure probabilities ({end-start} seconds)\n:{initial_failure_probabilities}")


start = time.time()
# function that each worker will call to do a simulation


def do_simulation(worker_id, queue):
    while True:  # keep doing this until the thread is killed
        seed, output_file = queue.get()

        try:
            logging.info(f"worker: '{worker_id}' attempting to simulate seed: {seed}")
            simulation_data = simulator.simulate(
                seed, number_of_parameter_draws, parameter_draw_batch_size,
                initial_failure_probabilities
            )
            simulation_data.to_csv(output_file, index=False)
        except Exception as err:
            error_file = os.path.join(output_directory, f"{seed}.log")
            logging.warning(f"worker: '{worker_id}' failure on seed: {seed}. Check: {error_file}")
            with open(error_file, "w") as err_f:
                err_f.write(format_exc())
        else:
            logging.info(f"worker: '{worker_id}' success on seed: {seed}")

        queue.task_done()
    return True


# make a list of sseds and output files, these represent each unique simulation
seeds = list(range(1, number_of_simulations+1))
output_files = [os.path.join(output_directory, f"{seed}.csv") for seed in seeds]

# initialize the queue
input_queue = queue.Queue()
for seed, output_file in zip(seeds, output_files):
    if os.path.exists(output_file):
        continue  # if an output file already exists, skip it
    input_queue.put((seed, output_file))  # add the seeds and output file to the queue

# do the tasks using multithreading
for worker_id in range(1, number_of_threads+1):
    threading.Thread(target=do_simulation, daemon=True, args=(worker_id, input_queue)).start()

# Block until all tasks are done
input_queue.join()  # kills all thread when the queue is empty

end = time.time()
print(f"time: {end-start} seconds")
