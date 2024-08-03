"""
 Title:         617_s3
 Description:   Runs a mini CPFEM model once
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf

# Define the mesh and orientations
itf = Interface(input_path="data/mini")
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)

# Defines the material parameters
itf.define_material(
    material_name   = "mat_1to1",
    material_params = {

        # Crystal Plasticity Parameters
        "cp_tau_s":   1250,
        "cp_b":       0.25,
        "cp_tau_0":   107,
        "cp_gamma_0": round_sf(1e-4/3, 5),
        "cp_n":       4.5,

        # Viscoplastic Parameters
        "vp_s0":      95.121,
        "vp_R":       559.17,
        "vp_d":       1.3763,
        "vp_n":       4.2967,
        "vp_eta":     2385.9,
    },
    youngs          = 211000.0,
    poissons        = 0.30,
)

# Defines the simulation parameters
itf.define_simulation(
    simulation_name = "sim_1to1",
    time_intervals  = [0.0, 1, 2, 4],
    end_strain      = 4,
)

# Runs the model and saves results
num_processors = int(sys.argv[1]) if len(sys.argv)>1 else 8
itf.export_params()
itf.simulate("~/moose/deer/deer-opt", num_processors, 100000)

# Conduct post processing
itf.compress_csv(sf=5, exclude=["x", "y", "z"])
itf.post_process()
# itf.remove_files(["mesh.e", "element_stats.csv", "results"])
