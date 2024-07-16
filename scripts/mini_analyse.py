"""
 Title:         Analyse
 Description:   Analyses the simulation results
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.analyse.summarise import get_csv_results, get_map

# Constants
SIM_PATH = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/deer_sim/2024-07-16 (mini)"

sim_dict_list = get_csv_results(SIM_PATH, "results_element", "time")
element_map = get_map(sim_dict_list[-1], "block_id", "id", int)

print(element_map)
