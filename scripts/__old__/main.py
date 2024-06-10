import sys; sys.path += [".."]
from deer_sim.interface import Interface

itf = Interface("temp", input_path="./ebsd/617_s1_small")
itf.define_mesh("mesh.e", "input_orientations.csv")

itf.define_material("vshai", {"tau_sat": 108.35, "b": 0.5840, "tau_0": 120.21, "gamma_0": round(1e-4/3, 4), "n": 2.5832})

itf.define_simulation("cp_simple")

itf.export_params()

itf.simulate("~/moose/deer/deer-opt", 8, 100)
itf.remove_artifacts()
itf.analyse_results()
