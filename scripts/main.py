import sys; sys.path += [".."]
from deer_sim.api import API

api = API("temp", input_path="./data/500/16_s1")
api.define_mesh("mesh.e", "input_orientations.csv")

api.define_material("vshai", {
    "tau_s":   12,
    "b":       66.67,
    "tau_0":   40,
    "gamma_0": 9.55e-8,
    "n":       12
})

api.define_simulation("cp")

api.simulate("~/moose/deer/deer-opt", 8)
