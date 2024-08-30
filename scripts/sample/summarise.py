"""
 Title:         Summarise
 Description:   Summarises the results of the sampled simulations
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
import os, re
from deer_sim.helper.general import round_sf
from deer_sim.helper.io import csv_to_dict, dict_to_csv

# Constants
SIM_PATH = "/mnt/c/Users/z5208868/OneDrive - UNSW/PhD/results/deer_sim/2024-08-25 (617_s3_sm)"
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

def convert_grain_ids(data_dict:dict, grain_map_path:str) -> dict:
    """
    Converts the grain IDs of a dictionary
    
    Parameters:
    * `data_dict`:      The dictionary
    * `grain_map_path`: The path to the grain map
    
    Returns the dictionary with renamed keys
    """
    
    # Initialise conversion
    grain_map = csv_to_dict(grain_map_path)
    new_data_dict = {}
    mesh_to_ebsd = dict(zip(grain_map["mesh_id"], grain_map["ebsd_id"]))

    # Iterate through keys
    for key in data_dict:
        if bool(re.match(r'^g\d+.*$', key)):
            key_list = key.split("_")
            mesh_id = int(key_list[0].replace("g",""))
            new_key = f"g{int(mesh_to_ebsd[mesh_id])}_{'_'.join(key_list[1:])}"
            new_data_dict[new_key] = data_dict[key]
        else:
            new_data_dict[key] = data_dict[key]
    
    # Return
    return new_data_dict

# Read all summary files
dir_path_list = [f"{SIM_PATH}/{dir_path}" for dir_path in os.listdir(SIM_PATH)
            if os.path.exists(f"{SIM_PATH}/{dir_path}/summary.csv")]
summary_path_list = [f"{dir_path}/summary.csv" for dir_path in dir_path_list]
summary_dict_list = [csv_to_dict(summary_path) for summary_path in summary_path_list]
param_dict_list = [get_param_dict(f"{dir_path}/params.txt") for dir_path in dir_path_list]
print(len(param_dict_list))
        
# Initialise a summary dictionary for the summaries
key_list = list(param_dict_list[0].keys()) + list(summary_dict_list[0].keys())
super_summary_dict = dict(zip(key_list, [[] for _ in range(len(key_list))]))
first_key = [list(summary_dict_list[0].keys())][0][0]
num_values = len(summary_dict_list[0][first_key])
print(num_values)

# Iterate through the results
for summary_dict, param_dict in zip(summary_dict_list, param_dict_list):
    for key in param_dict:
        super_summary_dict[key] += [param_dict[key]]*(num_values-1)
    for key in summary_dict:
        super_summary_dict[key] += round_sf(summary_dict[key][1:], 5)

# # Replace grain IDs if necessary
# super_summary_dict = convert_grain_ids(super_summary_dict, "../data/617_s3/grain_map.csv")

# Save the super summary dictionary
dict_to_csv(super_summary_dict, "617_s3_sampled.csv")
