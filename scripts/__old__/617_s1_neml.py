import sys; sys.path += [".."]
from deer_sim.interface import Interface

itf = Interface(input_path="./data/ebsd/617_s1_llr")
itf.define_mesh("mesh.e", "orientations.csv")

itf.define_material("vshai", {"tau_s": 200, "b": 2, "tau_0": 400, "gamma_0": round(1e-4/3, 4), "n": 4})

itf.define_simulation("cp_tensile")

itf.export_params()

itf.simulate("~/moose/deer/deer-opt", 8, 1000)
itf.remove_artifacts()
