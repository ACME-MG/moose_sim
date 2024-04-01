import sys; sys.path += ["../.."]
from deer_sim.interface import Interface

param_dict = {
    "tau_s":   100,
    "b":       100,
    "tau_0":   300,
    "gamma_0": round(1e-4/3, 7),
    "n":       5,
}

itf = Interface(f"test_1", input_path="../data/500/16_s1", output_path="../results")
itf.define_mesh("mesh.e", "input_orientations.csv")
itf.define_material("vshai", param_dict)
itf.define_simulation("cp_simple", {})
itf.export_params()
itf.simulate("~/moose/deer/deer-opt", 32)
itf.remove_artifacts()
itf.analyse_results()
