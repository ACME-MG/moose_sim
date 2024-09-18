"""
 Title:         617_s3
 Description:   Runs the CPFEM model once
 References:    https://asmedigitalcollection.asme.org/pressurevesseltech/article/135/2/021502/378322/Synchrotron-Radiation-Study-on-Alloy-617-and-Alloy
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.interface import Interface
from deer_sim.helper.io import csv_to_dict

# Constants
NUM_PROCESSORS = 190
MAX_TIME       = 200000

# Define viscoplastic parameters
vp_params = {
    "vp_s0":  93.655,
    "vp_R":   3957.3,
    "vp_d":   0.5651,
    "vp_n":   7.3648,
    "vp_eta": 721.59,
}

# Define crystal plasticity parameters
cp_params_list = [
    {"cp_tau_s": 1418.4, "cp_b": 7.9848, "cp_tau_0": 235.75, "cp_n": 2.2160, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 875.29, "cp_b": 4.8956, "cp_tau_0": 340.67, "cp_n": 4.8973, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 792.57, "cp_b": 1.7664, "cp_tau_0": 86.088, "cp_n": 13.686, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 447.05, "cp_b": 3.0622, "cp_tau_0": 145.20, "cp_n": 11.825, "cp_gamma_0": 3.333e-05}
]

# Iterate through resolutions and crystal plasticity params
for resolution in ["5um", "10um", "15um", "20um", "30um", "40um"]:
    for i, cp_params in enumerate(cp_params_list):
        
        # Define the mesh and orientations
        itf = Interface(
            title      = f"{resolution}_{i}",
            input_path = f"data/617_s3/{resolution}"
        )
        itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
        dimensions = itf.get_dimensions()

        # Defines the material parameters
        itf.define_material(
            material_name   = "cvp_ae",
            material_params = {**cp_params, **vp_params},
            c_11            = 250000,
            c_12            = 151000,
            c_44            = 123000,
            youngs          = 211000.0,
            poissons        = 0.30,
        )

        # Defines the simulation parameters
        exp_dict = csv_to_dict(f"data/617_s3/617_s3_exp.csv")
        itf.define_simulation(
            simulation_name = "1to1_ui",
            end_time        = exp_dict["time_intervals"][-1],
            end_strain      = exp_dict["strain_intervals"][-1] * dimensions["x"]
        )

        # Runs the model and saves results
        itf.export_params()
        itf.simulate("~/moose/deer/deer-opt", NUM_PROCESSORS, MAX_TIME)

        # Conduct post processing
        itf.compress_csv(sf=5, exclude=["x", "y", "z"])
        itf.post_process(grain_map_path="data/617_s3/grain_map.csv")
        itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])
