"""
 Title:         Analyse SS
 Description:   Analyses the stress-strain results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.helper.io import csv_to_dict
from deer_sim.helper.general import transpose
from deer_sim.simulate.analyser import get_data_dict_list, get_grain_map, get_average_orientations
from deer_sim.simulate.pole_figure import IPF, get_lattice
from deer_sim.simulate.plotter import save_plot, ALL_COLOURS

# Get ID mapping (exp -> mesh)
def get_exp_to_mesh(ebsd_to_mesh:dict, exp_dict:dict) -> dict:
    exp_to_mesh = {}
    exp_ids = [int(key.replace("_phi_1","").replace("g","")) for key in exp_dict.keys() if "_phi_1" in key]
    for exp_id in exp_ids:
        if exp_id in ebsd_to_mesh["ebsd_id"]:
            index = ebsd_to_mesh["ebsd_id"].index(exp_id)
            mesh_id = ebsd_to_mesh["mesh_id"][index]
            exp_to_mesh[exp_id] = int(mesh_id)
    return exp_to_mesh

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
GRAIN_MAP_DIR = "/mnt/c/Users/Janzen/Desktop/code/ebsd_mesher/scripts/results"
GRAIN_MAP_PATHS = [
    # "240616155850_617_s1_d10_z1",
    # "240616160156_617_s1_d10_z2",
    # "240616160439_617_s1_d10_z3",
    # "240616160557_617_s1_d10_z4",
    # "240616160650_617_s1_d10_z5",
    # "240616160751_617_s1_d10_z6",
    # "240616160858_617_s1_d10_z7",
    # "240616161014_617_s1_d10_z8",
    "240617094525_617_s1_d5_z4",
    "240617094822_617_s1_d6_z4",
    "240617095022_617_s1_d7_z4",
    "240617095151_617_s1_d8_z4",
    "240617095306_617_s1_d9_z4",
    "240617095409_617_s1_d10_z4",
]

# Initialise IPF plot
lattice = get_lattice("fcc")
direction=[1,0,0]
ipf = IPF(lattice)

# Plot experimental trajectories
exp_dict = csv_to_dict(EXP_PATH)
exp_grain_ids = [45, 56, 135, 213, 346, 768]
exp_trajectories = []
for grain_id in exp_grain_ids:
    exp_trajectory = [exp_dict[f"g{grain_id}_{phi}"] for phi in ["phi_1", "Phi", "phi_2"]]
    exp_trajectory = transpose(exp_trajectory)
    exp_trajectories.append(exp_trajectory)
ipf.plot_ipf_trajectory(exp_trajectories, direction, "plot", {"color": "darkgray", "linewidth": 2})
ipf.plot_ipf_trajectory(exp_trajectories, direction, "arrow", {"color": "darkgray", "head_width": 0.01, "head_length": 0.015})
ipf.plot_ipf_trajectory([[et[0]] for et in exp_trajectories], direction, "scatter", {"color": "darkgray", "s": 8**2})
for i, et in enumerate(exp_trajectories):
    ipf.plot_ipf_trajectory([[et[0]]], direction, "text", {"color": "black", "fontsize": 8, "s": exp_grain_ids[i]})

# Iterate through simulation results
for sim_path, grain_map_path, colour in zip(SIM_PATHS, GRAIN_MAP_PATHS, ALL_COLOURS):
    print(sim_path)

    # Extract simulation results
    sim_dict_list = get_data_dict_list(f"results/{sim_path}")
    grain_map = get_grain_map(sim_dict_list[-1])
    average_dict = get_average_orientations(sim_dict_list, grain_map)
    
    # Get simulated trajectories
    ebsd_to_mesh = csv_to_dict(f"{GRAIN_MAP_DIR}/{grain_map_path}/grain_map.csv")
    exp_to_mesh = get_exp_to_mesh(ebsd_to_mesh, exp_dict)
    sim_grain_ids = [exp_to_mesh[id] for id in exp_grain_ids]
    sim_trajectories = [average_dict[grain_id] for grain_id in sim_grain_ids if grain_id in average_dict.keys()]

    # Plot simulated trajectories
    ipf.plot_ipf_trajectory(sim_trajectories, direction, "plot", {"color": colour, "linewidth": 1, "zorder": 3})
    ipf.plot_ipf_trajectory(sim_trajectories, direction, "arrow", {"color": colour, "head_width": 0.0075, "head_length": 0.0075*1.5, "zorder": 3})
    ipf.plot_ipf_trajectory([[st[0]] for st in sim_trajectories], direction, "scatter", {"color": colour, "s": 6**2, "zorder": 3})

# Save the plot
save_plot("plot_phi2.png")
