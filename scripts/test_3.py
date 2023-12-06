import sys; sys.path += [".."]
from deer_sim.api import API

param_dict = {
    "tau_s":   200,
    "b":       200,
    "tau_0":   100,
    "gamma_0": round(1e-4/3, 7),
    "n":       10,
}

api = API(f"test_3", input_path="./data/500/16_s1")
api.define_mesh("mesh.e", "input_orientations.csv")
api.define_material("vshai", param_dict)
api.define_simulation("cp_simple", {})
api.export_params()
api.simulate("~/moose/deer/deer-opt", 32)
api.remove_artifacts()
api.analyse_results()
