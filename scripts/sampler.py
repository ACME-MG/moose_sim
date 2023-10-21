import sys; sys.path += [".."]
from deer_sim.api import API
import itertools

# Define parameter domains
param_dict = {
    # "tau_s":   [1, 500, 1000, 1500, 2000],
    "tau_s":   [1],
    "b":       [0.1, 1, 10, 100],
    "tau_0":   [100, 200, 300, 400, 500],
    "gamma_0": [round(1e-4/3, 7)],
    "n":       [1, 5, 10, 15, 20],
}

# Get combinations of domains
param_list = list(param_dict.values())
combinations = list(itertools.product(*param_list))
combinations = [list(c) for c in combinations]

# Iterate through the parameters
param_names = list(param_dict.keys())
for i in range(len(combinations)):
    param_dict = dict(zip(param_names, combinations[i]))
    api = API(f"s1_p{i}", input_path="./data/500/16_s1")
    api.define_mesh("mesh.e", "input_orientations.csv")
    api.define_material("vshai", param_dict)
    api.define_simulation("no_czm", {})
    api.simulate("~/moose/deer/deer-opt", 16)
    