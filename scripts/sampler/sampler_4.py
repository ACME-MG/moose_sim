import sys; sys.path += ["../.."]
from deer_sim.interface import Interface
import itertools
from constants import *

# Define parameter domains
param_dict = {
    "tau_s":   [PARAM_DICT["tau_s"][3]],
    "b":       PARAM_DICT["b"],
    "tau_0":   PARAM_DICT["tau_0"],
    "gamma_0": PARAM_DICT["gamma_0"],
    "n":       PARAM_DICT["n"],
}

# Get combinations of domains
param_list = list(param_dict.values())
combinations = list(itertools.product(*param_list))
combinations = [list(c) for c in combinations]

# Iterate through the parameters
param_names = list(param_dict.keys())
for i in range(len(combinations)):
    param_dict = dict(zip(param_names, combinations[i]))
    itf = Interface(f"s4_p{i}", input_path=f"../data/500/{MESH_PATH}", output_path="../results")
    itf.define_mesh("mesh.e", "input_orientations.csv")
    itf.define_material("vshai", param_dict)
    itf.define_simulation("cp_simple", {})
    itf.export_params()
    itf.simulate("~/moose/deer/deer-opt", NUM_CORES, TIMEOUT)
    itf.remove_artifacts()
    itf.analyse_results()
