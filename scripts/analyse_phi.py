"""
 Title:         Analyse Phi
 Description:   Analyses the orientation results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.helper.io import csv_to_dict
from deer_sim.helper.general import transpose, round_sf
from deer_sim.maths.orientation import rad_to_deg
from deer_sim.simulate.analyser import get_data_dict_list, get_grain_map, get_average_orientations
from deer_sim.simulate.pole_figure import IPF, get_lattice
from deer_sim.simulate.plotter import save_plot

# Constants
EXP_PATH = "data/ebsd/617_s1_exp.csv"
SIM_PATH = "results/240615154703_617_s1"
EXP_TO_MESH_PATH = "data/ebsd/617_s1_z1_lr/grain_map.csv"

# Get all grain ID maps
ebsd_to_mesh = csv_to_dict(EXP_TO_MESH_PATH) # exp -> mesh
exp_dict     = csv_to_dict(EXP_PATH)         # exp (mappable)

# Getting ID mapping (exp -> mesh)
exp_to_mesh = {}
exp_ids = [int(key.replace("_phi_1","").replace("g","")) for key in exp_dict.keys() if "_phi_1" in key]
for exp_id in exp_ids:
    if exp_id in ebsd_to_mesh["ebsd_id"]:
        index = ebsd_to_mesh["ebsd_id"].index(exp_id)
        mesh_id = ebsd_to_mesh["mesh_id"][index]
        exp_to_mesh[exp_id] = int(mesh_id)

# Define grain IDs
exp_grain_ids = list(exp_to_mesh.keys())
# exp_grain_ids = [45, 56, 135, 213, 346, 768]
sim_grain_ids = [exp_to_mesh[id] for id in exp_grain_ids]

# Get experimental trajectories
exp_trajectories = []
for grain_id in exp_grain_ids:
    exp_trajectory = [exp_dict[f"g{grain_id}_{phi}"] for phi in ["phi_1", "Phi", "phi_2"]]
    exp_trajectory = transpose(exp_trajectory)
    exp_trajectories.append(exp_trajectory)

# Get simulated trajectories
sim_dict_list = get_data_dict_list(SIM_PATH)
grain_map = get_grain_map(sim_dict_list[-1])
average_dict = get_average_orientations(sim_dict_list, grain_map)
sim_trajectories = [average_dict[grain_id] for grain_id in sim_grain_ids]

# Print out initial comparison
for i in range(len(exp_trajectories)):
    exp_ori = rad_to_deg(exp_trajectories[i][0])
    sim_ori = rad_to_deg(sim_trajectories[i][0])
    exp_ori = [round_sf(e, 5) for e in exp_ori]
    sim_ori = [round_sf(s, 5) for s in sim_ori]
    print(f"{sim_grain_ids[i]},{exp_grain_ids[i]}:\t{exp_ori}, {sim_ori}")

# Initialise IPF plot
lattice = get_lattice("fcc")
direction=[1,0,0]
ipf = IPF(lattice)

# Plot experimental trajectories
ipf.plot_ipf_trajectory(exp_trajectories, direction, "plot", {"color": "darkgray", "linewidth": 2})
ipf.plot_ipf_trajectory(exp_trajectories, direction, "arrow", {"color": "darkgray", "head_width": 0.01, "head_length": 0.015})
ipf.plot_ipf_trajectory([[et[0]] for et in exp_trajectories], direction, "scatter", {"color": "darkgray", "s": 8**2})
for i, et in enumerate(exp_trajectories):
    ipf.plot_ipf_trajectory([[et[0]]], direction, "text", {"color": "black", "fontsize": 8, "s": exp_grain_ids[i]})

# Plot simulated trajectories
ipf.plot_ipf_trajectory(sim_trajectories, direction, "plot", {"color": "green", "linewidth": 1, "zorder": 3})
ipf.plot_ipf_trajectory(sim_trajectories, direction, "arrow", {"color": "green", "head_width": 0.0075, "head_length": 0.0075*1.5, "zorder": 3})
ipf.plot_ipf_trajectory([[st[0]] for st in sim_trajectories], direction, "scatter", {"color": "green", "s": 6**2, "zorder": 3})

# Save the plot
save_plot("plot.png")
