"""
 Title:         Summarise
 Description:   Summarises the results of the sampled simulations
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
import math, numpy as np, os, re
from scipy.interpolate import splev, splrep, splder
from moose_sim.helper.general import transpose, round_sf, get_thinned_list
from moose_sim.helper.io import csv_to_dict, dict_to_csv
from moose_sim.analyse.plotter import Plotter, save_plot

# Constants
SIM_PATH = "/mnt/c/Users/z5208868/OneDrive - UNSW/PhD/results/moose_sim/2024-09-17 (617_s3_10u_z1_sm)"
PARAMS = ["cp_tau_s", "cp_b", "cp_tau_0", "cp_n"]
NUM_STRAINS = 32

# The Interpolator Class
class Interpolator:

    def __init__(self, x_list:list, y_list:list, resolution:int=50, smooth:bool=False):
        """
        Class for interpolating two lists of values

        Parameters:
        * `x_list`:     List of x values
        * `y_list`:     List of y values
        * `resolution`: The resolution used for the interpolation
        * `smooth`:     Whether to smooth the interpolation
        """
        x_list, indices = np.unique(np.array(x_list), return_index=True)
        y_list = np.array(y_list)[indices]
        if len(x_list) > resolution:
            x_list = get_thinned_list(list(x_list), resolution)
            y_list = get_thinned_list(list(y_list), resolution)
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(x_list, y_list, s=smooth_amount)
    
    def differentiate(self) -> None:
        """
        Differentiate the interpolator
        """
        self.spl = splder(self.spl)

    def evaluate(self, x_list:list) -> list:
        """
        Run the interpolator for specific values

        Parameters
        * `x_list`: The list of x values

        Returns the evaluated values
        """
        return list(splev(x_list, self.spl))

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

def get_trajectories(data_dict:dict) -> dict:
    """
    Gets the reorientation trajectories

    Parameters:
    * `data_dict`: The data dictionary
    
    Return trajectories as a dictoinary of lists of euler angles
    """
    grain_ids = [int(key.replace("g","").replace("_phi_1","")) for key in data_dict.keys() if "_phi_1" in key]
    trajectories = {}
    for grain_id in grain_ids:
        trajectory = [data_dict[f"g{grain_id}_{phi}"] for phi in ["phi_1", "Phi", "phi_2"]]
        trajectory = transpose(trajectory)
        trajectories[grain_id] = trajectory
    return trajectories

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

def fix_angle(angle:float, l_bound:float=0.0, u_bound:float=2*math.pi) -> float:
    """
    Fixes an angle between two bounds
    
    Parameters:
    * `angle`: The angle (rads)

    Returns the fixed angle
    """
    if abs(angle-l_bound) < 1e-4 or abs(angle-u_bound) < 1e-4:
        return angle
    range = u_bound - l_bound
    if l_bound < angle and angle < u_bound:
        return angle
    elif angle < l_bound:
        return fix_angle(angle+range, l_bound, u_bound)
    else:
        return fix_angle(angle-range, l_bound, u_bound)

def process_data_dict(data_dict:dict) -> dict:
    """
    Processes the data in the data dictionary;
    normalises strain difference
    
    Parameters:
    * `data_dict`: The dictionary of data
    
    Returns the processed dictionary
    """
    
    # Prepare old and new strain values
    strain_list = data_dict["average_strain"]
    new_strain_list = list(np.linspace(0,data_dict["average_strain"][-1],NUM_STRAINS+1)[1:])
    
    # Prepare fields
    grain_ids = [int(key.replace("g","").replace("_phi_1","")) for key in data_dict.keys() if "_phi_1" in key]
    euler_fields = [f"g{grain_id}_{field}" for grain_id in grain_ids for field in ["phi_1", "Phi", "phi_2"]]
    field_list = ["average_stress"] + euler_fields
    
    # Interpolate for each field and return
    processed_dict = {"average_strain": new_strain_list}
    for field in field_list:
        field_itp = Interpolator(strain_list, data_dict[field], len(strain_list))
        new_list = field_itp.evaluate(new_strain_list)
        processed_dict[field] = new_list
    
    # Fix the domain of the euler-bunge angles
    # for field in euler_fields:
    #     processed_dict[field] = [fix_angle(phi) for phi in processed_dict[field]]
    
    # Return processed dictionary
    return processed_dict

# Read all summary files
dir_path_list = [f"{SIM_PATH}/{dir_path}" for dir_path in os.listdir(SIM_PATH)
                 if os.path.exists(f"{SIM_PATH}/{dir_path}/summary.csv")]
summary_path_list = [f"{dir_path}/summary.csv" for dir_path in dir_path_list]
summary_dict_list = [csv_to_dict(summary_path) for summary_path in summary_path_list]
param_dict_list = [get_param_dict(f"{dir_path}/params.txt") for dir_path in dir_path_list]
print(len(param_dict_list))

# Process the dictionaries
processed_dict_list = [process_data_dict(summary_dict) for summary_dict in summary_dict_list]
key_list = list(param_dict_list[0].keys()) + list(processed_dict_list[0].keys())
super_processed_dict = dict(zip(key_list, [[] for _ in range(len(key_list))]))
first_key = [list(processed_dict_list[0].keys())][0][0]

# Initialise plotter
plotter = Plotter("average_strain", "average_stress", "mm/mm", "MPa")
plotter.prep_plot()

# Iterate through the results
super_summary_dict = {}
for summary_dict, processed_dict, param_dict in zip(summary_dict_list, processed_dict_list, param_dict_list):
    
    # Plot unprocessed and processed data
    plotter.scat_plot(summary_dict, colour="silver")
    plotter.line_plot(processed_dict, colour="red")
    
    # Save to super dictionary 
    num_values = len(list(processed_dict.values())[0])
    for key in param_dict:
        super_processed_dict[key] += [param_dict[key]]*num_values
    for key in processed_dict:
        super_processed_dict[key] += round_sf(processed_dict[key], 5)

# Save the plot and super summary dictionary
save_plot("plot_ss.png")
super_processed_dict = convert_grain_ids(super_processed_dict, "../data/617_s3_z1/10um/grain_map.csv")
dict_to_csv(super_processed_dict, "617_s3_sampled_2.csv")
