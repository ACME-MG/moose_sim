# Libraries
import sys; sys.path += [".."]
from deer_sim.analyse.plotter import save_plot
from deer_sim.analyse.pole_figure import IPF, get_lattice
from deer_sim.helper.general import transpose, remove_consecutive_duplicates
from deer_sim.helper.io import csv_to_dict
from deer_sim.maths.familiser import get_cubic_family

# Constants
EXP_PATH = "data/617_s3/617_s3_exp.csv"
MAP_PATH = "data/617_s3/grain_map.csv"
# SIM_PATH = "results/240718160621_mini/summary.csv"
SIM_PATH = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/deer_sim/2024-07-24 (617_s3)/summary.csv"

def get_trajectories(data_dict:dict, include:list=None) -> list:
    """
    Gets the reorientation trajectories

    Parameters:
    * `data_dict`: The data dictionary
    * `include`:   List of grain IDs to include;
                   uses all grain IDs if parameter unspecified
    
    Return trajectories as a list of lists of euler angles
    """

    # Read data and specify grain IDs if defined
    grain_ids = [int(key.replace("g","").replace("_phi_1","")) for key in data_dict.keys() if "_phi_1" in key]
    if include != None:
        grain_ids = [grain_id for grain_id in grain_ids if grain_id in include]

    # Get trajectories
    trajectories = []
    for grain_id in grain_ids:
        trajectory = [data_dict[f"g{grain_id}_{phi}"] for phi in ["phi_1", "Phi", "phi_2"]]
        trajectory = transpose(trajectory)
        trajectory = remove_consecutive_duplicates(trajectory)
        trajectories.append(trajectory)

    # Return trajectories
    return trajectories

# Initialise IPF plotter
ipf = IPF(get_lattice("fcc"))
direction = [1,0,0]

# Get experimental orientations
exp_dict = csv_to_dict(EXP_PATH)
exp_orientations = [trajectory[0] for trajectory in get_trajectories(exp_dict)]

# Get orientations belonging to family
plane = [1,1,1]
family_indices = get_cubic_family(exp_orientations, plane, direction, 15)
exp_orientations = [exp_orientations[i] for i in family_indices]

# Plot initial orientations on IPF
ipf.plot_ipf_trajectory([[eo] for eo in exp_orientations], direction, "scatter", {"color": "darkgray", "s": 8**2})
save_plot("family.png")
