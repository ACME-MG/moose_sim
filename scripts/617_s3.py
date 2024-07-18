"""
 Title:         617_s3
 Description:   Runs the CPFEM model once
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf
from deer_sim.helper.io import csv_to_dict

# Define the mesh and orientations
itf = Interface(input_path="data/617_s3")
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
exp_dict = csv_to_dict("data/617_s3/617_s3_exp.csv")
itf.define_simulation(
    simulation_name = "sim_1to1",
    time_intervals  = exp_dict["time_intervals"],
    end_strain      = exp_dict["strain_intervals"][-1] * 2200 * 5/3
)

# Runs the model and saves results
num_processors = int(sys.argv[1]) if len(sys.argv)>1 else 8
itf.export_params()
itf.simulate("~/moose/deer/deer-opt", num_processors, 100000)
itf.compress_csv(sf=5, exclude=["x", "y", "z"])

# Define grain IDs
# BEST: 16, 21, 37, 46, 76, 82, 87, 99, 101, 110, 137,
#       141, 147, 152, 154, 159, 166, 167, 173, 180
# GOOD: 23, 27, 36, 38, 40, 49, 56, 64, 66, 97, 108,
#       109, 112, 114, 120, 128, 130, 139, 148, 176, 178
