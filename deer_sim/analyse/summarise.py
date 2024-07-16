"""
 Title:         Summarise
 Description:   Analysis functions for simulation results
 Author:        Janzen Choi

"""

# Libraries
import os
from deer_sim.helper.io import csv_to_dict

def get_csv_results(results_path:str, include:str=None, exclude:str=None) -> list:
    """
    Gets the results

    Parameters:
    * `results_path`: Path to the results
    * `include`:      Keyword to identify files to include
    * `exclude`:      Keyword to identify files to exclude

    Returns the results as a list of dictionaries
    """
    csv_file_list  = [csv_file for csv_file in os.listdir(results_path)
                      if csv_file.endswith(".csv") and (include == None or include in csv_file)
                      and (include == None or not exclude in csv_file)]
    data_dict_list = [csv_to_dict(f"{results_path}/{csv_file}") for csv_file in csv_file_list]
    return data_dict_list

def get_map(data_dict:dict, grain_id_field:str, target_field:str, target_type:type) -> dict:
    """
    Maps the grain IDs to a field

    Parameters:
    * `data_dict`:      The dictionary of the data
    * `grain_id_field`: The field for the grain IDs
    * `target_field`:   The field to conduct the mapping to

    Returns the mapping as a dictionary of lists
    """

    # Check input parameters
    if not target_field in data_dict.keys():
        raise ValueError(f"The '{target_field}' field does not exist in the dictionary")
    
    # Initialise mapping
    grain_ids = [int(grain_id) for grain_id in list(set(data_dict[grain_id_field]))]
    map_dict = dict(zip(grain_ids, [[] for _ in range(len(grain_ids))]))

    # Conduct mapping
    for i, grain_id in enumerate(data_dict[grain_id_field]):
        target_value = target_type(data_dict[target_field][i])
        map_dict[grain_id].append(target_value)

    # Return mapping
    return map_dict
