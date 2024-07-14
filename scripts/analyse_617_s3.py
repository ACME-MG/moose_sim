"""
 Title:         Analyse Phi
 Description:   Analyses the orientation results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.helper.io import csv_to_dict
from deer_sim.analyse.element import get_exp_trajectories, get_data_dict_list, get_sim_trajectories
from deer_sim.analyse.element import get_trajectory_dict, get_mappable_grain_ids
from deer_sim.analyse.pole_figure import quick_ipf

# Get grain ID mapping
grain_id_dict = get_mappable_grain_ids(
    exp_path  = "data/617_s3/exp.csv",
    ebsd_path = "data/617_s3/ebsd/grain_map.csv",
    mesh_path = "data/617_s3/mesh/grain_map.csv"
)

# Define grain IDs
# exp_grain_ids = list(grain_id_dict.keys())[:5]
exp_grain_ids = [44, 45, 47, 48, 51]#, 79, 90, 95, 96, 110, 113, 117]
sim_grain_ids = [grain_id_dict[exp_grain_id] for exp_grain_id in exp_grain_ids]
for exp, sim in zip(exp_grain_ids, sim_grain_ids):
    print(f" E: {exp}\tS: {sim}")

# Get trajectories
exp_dict         = csv_to_dict("data/617_s3/exp.csv")
sim_dict_list    = get_data_dict_list("/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/deer_sim/2024-07-08 (617_s3)")
exp_trajectories = get_exp_trajectories(exp_dict, exp_grain_ids)
sim_trajectories = get_sim_trajectories(sim_dict_list, sim_grain_ids)
# sim_dict = get_trajectory_dict(sim_trajectories, sim_grain_ids)

# Plot IPF
quick_ipf(
    exp_trajectories = exp_trajectories,
    sim_trajectories = sim_trajectories,
    file_path        = "plot.png",
    structure        = "fcc",
    direction        = [1,0,0],
    initial_only     = True,
    grain_ids        = exp_grain_ids,
)
