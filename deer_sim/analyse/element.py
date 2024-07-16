"""
 Title:         Element
 Description:   Analysis functions for element tracked simulation results
 Author:        Janzen Choi

"""

# Libraries
import os, numpy as np
from deer_sim.helper.general import transpose, round_sf, remove_consecutive_duplicates
from deer_sim.helper.io import csv_to_dict
from deer_sim.maths.orientation import get_average_quat
from deer_sim.maths.neml import deer_quat_to_euler

# Constants
GRAIN_FIELD   = "block_id"
ELEMENT_FIELD = "id"
STRESS_FIELD  = "cauchy_stress_xx"
QUAT_FIELDS   = ["orientation_q1", "orientation_q2", "orientation_q3", "orientation_q4"]

def get_data_dict_list(results_path:str) -> list:
    """
    Gets the list of data dictionaries

    Parameters:
    * `results_path`: Path to the results

    Returns the data dictionary list
    """
    csv_file_list  = [csv_file for csv_file in os.listdir(results_path) if csv_file.endswith(".csv")]
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
    grain_ids = [int(grain_id) for grain_id in grain_ids]
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

def get_exp_trajectories(exp_dict:dict, grain_ids:list=None) -> list:
    """
    Gets the experimental reorientation trajectories

    Parameters:
    * `exp_dict`:  The experimental data dictionary
    * `grain_ids`: List of grain IDs to include;
                   uses all grain IDs if parameter unspecified
    
    Return experimental trajectories as a list of lists of euler angles
    """

    # Read experimental data and specify grain IDs if defined
    exp_grain_ids = [int(key.replace("g","").replace("_phi_1","")) for key in exp_dict.keys() if "_phi_1" in key]
    if grain_ids != None:
        exp_grain_ids = [grain_id for grain_id in exp_grain_ids if grain_id in grain_ids]

    # Get experimental trajectories
    exp_trajectories = []
    for grain_id in exp_grain_ids:
        exp_trajectory = [exp_dict[f"g{grain_id}_{phi}"] for phi in ["phi_1", "Phi", "phi_2"]]
        exp_trajectory = transpose(exp_trajectory)
        exp_trajectory = remove_consecutive_duplicates(exp_trajectory)
        exp_trajectories.append(exp_trajectory)

    # Return experimental trajectories
    return exp_trajectories

def get_sim_trajectories(sim_dict_list:list, grain_ids:list=None) -> list:
    """
    Gets the simulated reorientation trajectories

    Parameters:
    * `sim_dict_list`: List of simulated data dictionaries
    * `grain_ids`:     List of grain IDs to include;
                       uses all grain IDs if parameter unspecified
    
    Return experimental trajectories as a list of lists of euler angles
    """

    # Read simulated data and specify grain IDs if defined
    grain_map = get_grain_map(sim_dict_list[-1])
    if grain_ids != None:
        new_grain_map = {}
        for grain_id in grain_map.keys():
            if grain_id in grain_ids:
                new_grain_map[grain_id] = grain_map[grain_id]
        grain_map = new_grain_map
    
    # Calculate average grain reorientations
    average_dict = get_average_orientations(sim_dict_list, grain_map)
    sim_trajectories = [average_dict[key] for key in average_dict.keys()]
    
    # Return simulated trajectories
    return sim_trajectories

def get_sim_stress(sim_dict_list:list, stress_field:str=STRESS_FIELD) -> list:
    """
    Gets the simulated stress values

    Parameters:
    * `sim_dict_list`: List of simulated data dictionaries
    * `stress_field`:  The field name for the stress values
    
    Return a list of stress values
    """
    stress_list = []
    for sim_dict in sim_dict_list:
        average_stress = np.average(sim_dict[stress_field])
        stress_list.append(average_stress)
    return stress_list

def get_trajectory_dict(trajectories:list, grain_ids:list) -> dict:
    """
    Reformats the reorientation trajectories into a dictionary

    Parameters:
    * `trajectories`: The list of reorientation trajectories
    * `grain_ids`:    List of grain IDs to include

    Returns the dictionary of reorientation trajectories
    """
    trajectory_dict = {}
    for grain_id, trajectory in zip(grain_ids, trajectories):
        for i, phi in enumerate(["phi_1", "Phi", "phi_2"]):
            phi_list = [round_sf(average_euler[i], 5) for average_euler in trajectory]
            trajectory_dict[f"g{int(grain_id)}_{phi}"] = phi_list
    return trajectory_dict

def get_grain_ids(exp_path:str, mesh_path:str) -> dict:
    """
    Gets the mappable grain IDs
    
    Parameters:
    * `exp_path`:  Path to the experimental data
    * `mesh_path`: Path to the mesh CSV map

    Returns a dictionary mapping the experimental grain IDs to the mesh grain IDs
    """

    # Read files
    exp_dict  = csv_to_dict(exp_path)  # exp
    mesh_dict = csv_to_dict(mesh_path) # exp : mesh
    exp_grain_ids = [int(key.replace("_phi_1","").replace("g","")) for key in exp_dict.keys() if "_phi_1" in key]
    
    # Map experimental grain IDs to mesh grain IDs
    exp_to_mesh = {}
    for exp_grain_id in exp_grain_ids:
        if exp_grain_id in mesh_dict["ebsd_id"]:
            ebsd_index = mesh_dict["ebsd_id"].index(exp_grain_id)
            exp_to_mesh[exp_grain_id] = int(mesh_dict["mesh_id"][ebsd_index])

    # Return mapping
    return exp_to_mesh

def get_mappable_grain_ids(exp_path:str, ebsd_path:str, mesh_path:str) -> dict:
    """
    Gets the mappable grain IDs
    
    Parameters:
    * `exp_path`:  Path to the experimental data
    * `ebsd_path`: Path to the EBSD CSV map ("ebsd_1": exp, "ebsd_2": ebsd)
    * `mesh_path`: Path to the mesh CSV map ("ebsd_id": ebsd, "mesh_id": mesh)

    Returns a dictionary with a list of experimental, EBSD, and simulated grain IDs;
    {"exp": [...], "ebsd": [...], "mesh": [...]}
    """

    # Read all files
    exp_dict  = csv_to_dict(exp_path)  # exp
    ebsd_dict = csv_to_dict(ebsd_path) # exp : ebsd
    mesh_dict = csv_to_dict(mesh_path) # ebsd : mesh

    # Get grain mapping from experimental trajectories (exp) to EBSD mesh map (ebsd)
    exp_grain_ids = [int(key.replace("_phi_1","").replace("g","")) for key in exp_dict.keys() if "_phi_1" in key]
    exp_to_ebsd = {}
    for exp_grain_id in exp_grain_ids:
        if exp_grain_id in ebsd_dict["ebsd_1"]:
            exp_index = ebsd_dict["ebsd_1"].index(exp_grain_id)
            exp_to_ebsd[exp_grain_id] = int(ebsd_dict["ebsd_2"][exp_index])
    
    # Get grain mapping from experimental trajectories (exp) to simulated trajectories (mesh)
    exp_to_mesh = {}
    for exp_grain_id in exp_to_ebsd.keys():
        ebsd_grain_id = exp_to_ebsd[exp_grain_id]
        if ebsd_grain_id in mesh_dict["ebsd_id"]:
            ebsd_index = mesh_dict["ebsd_id"].index(ebsd_grain_id)
            exp_to_mesh[exp_grain_id] = int(mesh_dict["mesh_id"][ebsd_index])

    # Return a dictionary of grain IDs
    grain_id_dict = {
        "exp":  list(exp_to_mesh.keys()),
        "ebsd": [exp_to_ebsd[key] for key in exp_to_mesh.keys()],
        "mesh": list(exp_to_mesh.values())
    }
    return grain_id_dict
