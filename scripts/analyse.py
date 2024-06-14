"""
 Title:         Analyser
 Description:   Analyses the results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
import os
from deer_sim.helper.general import transpose, round_sf
from deer_sim.helper.io import csv_to_dict, dict_to_csv
from deer_sim.maths.orientation import get_average_quat
from deer_sim.maths.neml import deer_quat_to_euler

# Constants
GRAIN_FIELD   = "block_id"
ELEMENT_FIELD = "id"
QUAT_FIELDS   = ["orientation_q1", "orientation_q2", "orientation_q3", "orientation_q4"]
RESULTS_PATH  = "results/240614222935_617_s1"

def get_data_dict_list(results_path:str) -> list:
    """
    Gets the list of data dictionaries

    Parameters:
    * `results_path`: Path to the results

    Returns the data dictionary list
    """
    csv_file_list = [csv_file for csv_file in os.listdir(results_path) if csv_file.endswith(".csv")]
    data_dict_list = [csv_to_dict(f"{results_path}/{csv_file}") for csv_file in csv_file_list]
    data_dict_list = [data_dict for data_dict in data_dict_list if GRAIN_FIELD in data_dict.keys()]
    return data_dict_list

def get_grain_map(data_dict:dict) -> dict:
    """
    Gets the mapping from grain ID to element IDs

    Parameters:
    * `data_dict`: The dictionary containing the element information

    Returns the mapping as a dictionary
    """
    grain_ids = list(set(data_dict[GRAIN_FIELD]))
    grain_map = dict(zip(grain_ids, [[] for _ in range(len(grain_ids))]))
    for i, grain_id in enumerate(data_dict[GRAIN_FIELD]):
        grain_map[grain_id].append(data_dict[ELEMENT_FIELD][i])
    return grain_map

def get_average_orientations(data_dict_list:list, grain_map:dict) -> dict:
    """
    Gets the changes in the average orientations

    Parameters:
    * `data_dict_list`: The list of data dictionaries
    * `grain_map`:      The mapping from grain ID to element IDs

    Returns a dictionary that maps the grain IDs to the list of
    average orientations
    """

    # Initialise mapping from grain id to average orientation
    grain_ids = list(grain_map.keys())
    average_dict = dict(zip(grain_ids, [[] for _ in range(len(grain_ids))]))

    # Extract orientation data from each result file
    for i, data_dict in enumerate(data_dict_list):
        
        # Get all quaternions
        all_quat_list = [data_dict[field] for field in QUAT_FIELDS]
        all_quat_list = transpose(all_quat_list)

        # Calculate average quaternion
        for grain_id in grain_ids:
            quat_list = [all_quat_list[j] for j in range(len(all_quat_list)) if j in grain_map[grain_id]]
            average_quat = get_average_quat(quat_list)
            average_euler = deer_quat_to_euler(average_quat, reorient=True, offset=(i==0))
            average_dict[grain_id].append(average_euler)
    
    # Return
    return average_dict

def save_average_orientations(average_dict:dict, file_path:str) -> None:
    """
    Saves the average orientations

    Parameters:
    * `average_dict`: The dictionary of average orientations
    * `file_path`:    The path to save the file
    """
    trajectories = {}
    for grain_id in average_dict.keys():
        for i, phi in enumerate(["phi_1", "Phi", "phi_2"]):
            trajectory = [round_sf(average_euler[i], 5) for average_euler in average_dict[grain_id]]
            trajectories[f"g{int(grain_id)}_{phi}"] = trajectory
    dict_to_csv(trajectories, file_path)

# Save orientation trajectories
data_dict_list = get_data_dict_list(RESULTS_PATH)
grain_map = get_grain_map(data_dict_list[-1])
average_dict = get_average_orientations(data_dict_list, grain_map)
save_average_orientations(average_dict, "trajectories.csv")
