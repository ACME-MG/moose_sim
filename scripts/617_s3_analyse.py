"""
 Title:         Analyse
 Description:   Analyses the simulation results
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.helper.io import csv_to_dict
from deer_sim.analyse.element import get_exp_trajectories, get_data_dict_list, get_sim_trajectories
from deer_sim.analyse.element import get_trajectory_dict, get_grain_ids, get_sim_stress
from deer_sim.analyse.plotter import Plotter, save_plot
from deer_sim.analyse.pole_figure import quick_ipf

# Constants
EXP_PATH = "data/617_s3/617_s3_exp.csv"
MAP_PATH = "data/617_s3/grain_map.csv"
SIM_PATH = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/deer_sim/2024-07-08 (617_s3)"

# Get grain ID mapping
grain_id_dict = get_grain_ids(
    exp_path  = EXP_PATH,
    mesh_path = MAP_PATH
)

# Define grain IDs
# BEST: 16, 21, 37, 46, 76, 82, 87, 99, 101, 110, 137,
#       141, 147, 152, 154, 159, 166, 167, 173, 180
# GOOD: 23, 27, 36, 38, 40, 49, 56, 64, 66, 97, 108,
#       109, 112, 114, 120, 128, 130, 139, 148, 176, 178
exp_grain_ids  = [16, 21, 37, 46, 76]
sim_grain_ids  = [grain_id_dict[exp_grain_id] for exp_grain_id in exp_grain_ids]
for exp, sim in zip(exp_grain_ids, sim_grain_ids):
    print(f" exp: {exp}\t sim: {sim}")

# Get experimental and simulated data
exp_dict      = csv_to_dict(EXP_PATH)
sim_dict_list = get_data_dict_list(SIM_PATH)

# Plot stress-strain curves
exp_ss = {"strain": exp_dict["strain"], "stress": exp_dict["stress"]}
sim_ss = {"strain": exp_dict["strain_intervals"], "stress": get_sim_stress(sim_dict_list)}
plotter_ss = Plotter("strain", "stress")
plotter_ss.prep_plot()
plotter_ss.scat_plot(exp_ss, colour="darkgray")
plotter_ss.line_plot(sim_ss, colour="red")
plotter_ss.define_legend(["darkgray", "red"], ["Experimental", "CPFEM"], [7, 2], ["scatter", "line"])
save_plot("plot_ss.png")

# Plot trajectories on IPF
exp_trajectories = get_exp_trajectories(exp_dict, exp_grain_ids)
sim_trajectories = get_sim_trajectories(sim_dict_list, sim_grain_ids)
quick_ipf(
    exp_trajectories = exp_trajectories,
    sim_trajectories = sim_trajectories,
    file_path        = "plot_phi.png",
    structure        = "fcc",
    direction        = [1,0,0],
    # initial_only     = True,
    grain_ids        = exp_grain_ids,
)

# Save simulated data
# sim_dict = get_trajectory_dict(sim_trajectories, sim_grain_ids)
