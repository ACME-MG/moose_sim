import sys; sys.path += [".."]
from deer_sim.interface import Interface

itf = Interface(input_path="./data/ebsd/617_s1_gs")
itf.define_mesh("mesh.e", "grain_stats.csv")

itf.define_material("gripped", {
    "cp_tau_s":   200,
    "cp_b":       2,
    "cp_tau_0":   400,
    "cp_gamma_0": round(1e-4/3, 4),
    "cp_n":       4,
    "vp_s0":      0,
    "vp_R":       0,
    "vp_d":       0,
    "vp_n":       0,
    "vp_eta":     0,
})

itf.define_simulation("cp_tensile")

itf.export_params()

itf.simulate("~/moose/deer/deer-opt", 8, 1000)
itf.remove_artifacts()
