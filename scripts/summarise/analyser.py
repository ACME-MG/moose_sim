"""
 Title:         Analyser
 Description:   Analyses the summarised results
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
from deer_sim.helper.io import csv_to_dict
from deer_sim.analyse.plotter import save_plot, Plotter
from deer_sim.analyse.pole_figure import IPF, get_lattice

# Constants
SAMPLE_PATH = "617_s3_sampled.csv"
GRAIN_IDS = [164, 173, 265, 213, 207]
NUM_DATA = 23 # per simulation

# Read sampled data
sample_dict = csv_to_dict("617_s3_sampled.csv")
total_data = len(list(sample_dict.values())[0])
num_simulations = total_data//NUM_DATA
indexes_list = [list(range(total_data))[i:i+NUM_DATA] for i in range(0, total_data, NUM_DATA)]

# Initialise IPF
ipf = IPF(get_lattice("fcc"))
direction = [1,0,0]
colour_list = ["red", "blue", "green", "orange", "purple"]*10

# Iterate through grains
for j, index_list in enumerate(indexes_list):
    for grain_id, colour in zip(GRAIN_IDS, colour_list):
        trajectory = [[sample_dict[f"g{grain_id}_{phi}"][i] for phi in ["phi_1", "Phi", "phi_2"]] for i in index_list]
        ipf.plot_ipf_trajectory([trajectory], direction, "plot", {"color": colour, "linewidth": 2})
        ipf.plot_ipf_trajectory([trajectory], direction, "arrow", {"color": colour, "head_width": 0.01, "head_length": 0.015})
        ipf.plot_ipf_trajectory([[trajectory[0]]], direction, "scatter", {"color": colour, "s": 8**2})
    # save_plot(f"plot_rt_{j}.png")
save_plot("plot_rt.png")

# Plot stress-strain response
plotter = Plotter("strain", "stress", "mm/mm", "MPa")
plotter.prep_plot()
for index_list, colour in zip(indexes_list, colour_list):
    strain_list = [sample_dict["average_strain"][i] for i in index_list]
    stress_list = [sample_dict["average_stress"][i] for i in index_list]
    plotter.line_plot({"strain": [0]+strain_list, "stress": [0]+stress_list}, colour)
save_plot("plot_ss.png")
