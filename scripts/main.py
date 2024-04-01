import sys; sys.path += [".."]
from deer_sim.interface import Interface

itf = Interface("temp", input_path="./data/500/4_s1")
itf.define_mesh("mesh.e", "input_orientations.csv")

# itf.define_material("vshai", {
#     "tau_s":   12,
#     "b":       66.67,
#     "tau_0":   40,
#     "gamma_0": 9.55e-8,
#     "n":       12
# })
itf.define_material("vshai", {
    "tau_s":   200,
    "b":       200,
    "tau_0":   300,
    "gamma_0": round(1e-4/3, 7),
    "n":       5,
})

itf.define_simulation("cp_simple")

itf.export_params()

itf.simulate("~/moose/deer/deer-opt", 8)
itf.remove_artifacts()
itf.analyse_results()
