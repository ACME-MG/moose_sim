"""
 Title:         Analyse SS
 Description:   Analyses the stress-strain results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
import numpy as np
from deer_sim.helper.io import csv_to_dict
from deer_sim.simulate.analyser import get_data_dict_list
from deer_sim.simulate.plotter import Plotter, save_plot, ALL_COLOURS

# Constants
EXP_PATH = "data/ebsd/617_s1_exp.csv"
STRESS_FIELD = "cauchy_stress_xx"
SIM_PATHS = [
    # "240616162353_617_s1_ztest_z1",
    # "240616163252_617_s1_ztest_z2",
    # "240616171015_617_s1_ztest_z3",
    # "240616180216_617_s1_ztest_z4",
    # "240616190907_617_s1_ztest_z5",
    # "240616203250_617_s1_ztest_z6",
    # "240616221245_617_s1_ztest_z7",
    # "240617001130_617_s1_ztest_z8",
    "240617101222_617_s1_ztest_d5",
    "240617125904_617_s1_ztest_d6",
    "240617154545_617_s1_ztest_d7",
    "240617174625_617_s1_ztest_d8",
    "240617192420_617_s1_ztest_d9",
    "240617204427_617_s1_ztest_d10",
]

# Plot experimental stress-strain data
exp_dict = csv_to_dict(EXP_PATH)
# plotter = Plotter("strain", "stress")
# plotter.scat_plot(exp_dict, colour="darkgray")
# strain_list = list(exp_dict["strain"][:14])



# Plot all simulated data
for sim_path, colour in zip(SIM_PATHS, ALL_COLOURS):
    sim_dict_list = get_data_dict_list(f"results/{sim_path}")
    stress_list = [np.average(sim_dict[STRESS_FIELD]) for sim_dict in sim_dict_list]
    sim_sum_dict = {"strain": strain_list[:len(stress_list)], "stress": stress_list}
    plotter.line_plot(sim_sum_dict, colour=colour)

# Save the plot
plotter.define_legend(["darkgray", "black"], ["Experimental", "CPFEM"], [7, 2], ["scatter", "line"])
save_plot("plot_ss.png")
