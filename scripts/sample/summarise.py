"""
 Title:         Summarise
 Description:   Summarises the results of the sampled simulations
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
import os
from deer_sim.helper.io import csv_to_dict, dict_to_csv

# Constants
SIM_PATH = "/mnt/c/Users/z5208868/OneDrive - UNSW/PhD/results/deer_sim/2024-07-29 (617_s3_failed)"
PARAMS = ["cp_tau_s", "cp_b", "cp_tau_0", "cp_n"]

def get_param_dict(params_path:str) -> dict:
    """
    Gets the parameters from a file
    
    Parameters:
    * `params_path`: The path to the parameters file
    
    Returns a dictionary of the parameter values
    """
    with open(params_path, "r") as fh:
        line_list = [line.replace("\n", "").replace(":", "") for line in fh.readlines()]
        param_dict = {line.split(" ")[0]: float(line.split(" ")[1]) for line in line_list
                      if line.split(" ")[0] in PARAMS}
        return param_dict

# Read all summary files
dir_path_list = [f"{SIM_PATH}/{dir_path}" for dir_path in os.listdir(SIM_PATH)
            if os.path.exists(f"{SIM_PATH}/{dir_path}/summary.csv")]
summary_path_list = [f"{dir_path}/summary.csv" for dir_path in dir_path_list]
summary_dict_list = [csv_to_dict(summary_path) for summary_path in summary_path_list]
param_dict_list = [get_param_dict(f"{dir_path}/params.txt") for dir_path in dir_path_list]

# Initialise a summary dictionary for the summaries
key_list = list(param_dict_list[0].keys()) + list(summary_dict_list[0].keys())
super_summary_dict = dict(zip(key_list, [[] for _ in range(len(key_list))]))
first_key = [list(summary_dict_list[0].keys())][0][0]
num_values = len(summary_dict_list[0][first_key])
print(num_values)

# Iterate through the results
for summary_dict, param_dict in zip(summary_dict_list, param_dict_list):
    for key in param_dict:
        super_summary_dict[key] += [param_dict[key]]*num_values
    for key in summary_dict:
        super_summary_dict[key] += summary_dict[key]
         
# Save the super summary dictionary
dict_to_csv(super_summary_dict, "super_summary.csv")
