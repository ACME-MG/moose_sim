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
from deer_sim.simulate.plotter import Plotter, save_plot

# Constants
EXP_PATH = "data/ebsd/617_s1_exp.csv"
SIM_PATH = "results/240615154703_617_s1"
STRESS_FIELD = "cauchy_stress_xx"

# Get experimental stress-strain data
exp_dict = csv_to_dict(EXP_PATH)

# Initialise simulation data
sim_sum_dict = {"strain": list(exp_dict["strain"][:14]), "stress": []}

# Get simulated stress-strain data
sim_dict_list = get_data_dict_list(SIM_PATH)
for sim_dict in sim_dict_list:
    stress = np.average(sim_dict[STRESS_FIELD])
    sim_sum_dict["stress"].append(stress)

# Create plots
plotter = Plotter("strain", "stress")
plotter.scat_plot(exp_dict, colour="darkgray")
plotter.line_plot(sim_sum_dict, colour="red")
plotter.define_legend(["darkgray", "red"], ["Experimental", "CPFEM"], [7, 2], ["scatter", "line"])
save_plot("plot_ss.png")
