"""
 Title:         Analyse Phi
 Description:   Analyses the orientation results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.helper.io import csv_to_dict
from deer_sim.helper.general import transpose, remove_consecutive_duplicates
from deer_sim.simulate.pole_figure import IPF, get_lattice
from deer_sim.simulate.plotter import save_plot

# Constants
EXP_PATH = "data/ebsd/617_s3_exp.csv"

# Read experimental data
exp_dict = csv_to_dict(EXP_PATH)
exp_grain_ids = [int(key.replace("g","").replace("_phi_1","")) for key in exp_dict.keys() if "_phi_1" in key]
exp_grain_ids = exp_grain_ids[:4]
print(exp_grain_ids)

# Get experimental trajectories
exp_trajectories = []
for grain_id in exp_grain_ids:
    exp_trajectory = [exp_dict[f"g{grain_id}_{phi}"] for phi in ["phi_1", "Phi", "phi_2"]]
    exp_trajectory = transpose(exp_trajectory)
    exp_trajectory = remove_consecutive_duplicates(exp_trajectory)
    exp_trajectories.append(exp_trajectory)

# Initialise IPF plot
lattice = get_lattice("fcc")
direction = [1,0,0]
ipf = IPF(lattice)

# Plot experimental trajectories
ipf.plot_ipf_trajectory(exp_trajectories, direction, "plot", {"color": "darkgray", "linewidth": 2})
ipf.plot_ipf_trajectory(exp_trajectories, direction, "arrow", {"color": "darkgray", "head_width": 0.01, "head_length": 0.015})
ipf.plot_ipf_trajectory([[et[0]] for et in exp_trajectories], direction, "scatter", {"color": "darkgray", "s": 8**2})
for i, et in enumerate(exp_trajectories):
    ipf.plot_ipf_trajectory([[et[0]]], direction, "text", {"color": "black", "fontsize": 8, "s": exp_grain_ids[i]})

# Save the plot
save_plot("plot.png")
