"""
 Title:         617_s3
 Description:   Runs the CPFEM model once
 References:    https://asmedigitalcollection.asme.org/pressurevesseltech/article/135/2/021502/378322/Synchrotron-Radiation-Study-on-Alloy-617-and-Alloy
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from moose_sim.interface import Interface
from moose_sim.helper.io import csv_to_dict
from moose_sim.helper.interpolator import intervaluate

# Constants
NUM_PROCESSORS = 190
MAX_DURATION   = 200000
MAX_STRAIN     = 0.10

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
    {"cp_tau_s": 142.7, "cp_b": 6.624, "cp_tau_0": 322.3, "cp_n": 11.7, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 1375.0, "cp_b": 7.959, "cp_tau_0": 297.0, "cp_n": 10.11, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 1006.0, "cp_b": 5.22, "cp_tau_0": 66.99, "cp_n": 5.635, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 460.8, "cp_b": 2.267, "cp_tau_0": 396.9, "cp_n": 2.282, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 1127.0, "cp_b": 3.319, "cp_tau_0": 169.5, "cp_n": 7.952, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 555.9, "cp_b": 1.195, "cp_tau_0": 185.7, "cp_n": 4.67, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 838.3, "cp_b": 4.467, "cp_tau_0": 120.9, "cp_n": 15.72, "cp_gamma_0": 3.333e-05},
    {"cp_tau_s": 1540.0, "cp_b": 2.585, "cp_tau_0": 261.7, "cp_n": 13.6, "cp_gamma_0": 3.333e-05},
]

# Iterate through resolutions and crystal plasticity params
for resolution in ["5um", "10um", "15um", "20um", "25um", "30um", "35um", "40um", "45um", "50um"]:
    for i, cp_params in enumerate(cp_params_list):
        
        # Define input path
        input_path = f"data/617_s3_z1/{resolution}"
        
        # Define the mesh and orientations
        itf = Interface(
            title      = f"{resolution}_p{i}",
            input_path = input_path
        )
        itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
        dimensions = itf.get_dimensions()

        # Defines the material parameters
        itf.define_material(
            material_path   = "deer/cvp_ae",
            material_params = {**cp_params, **vp_params},
            c_11            = 250000,
            c_12            = 151000,
            c_44            = 123000,
            youngs          = 211000.0,
            poissons        = 0.30,
        )

        # Define end time and strain
        exp_dict = csv_to_dict(f"data/617_s3_z1/617_s3_exp.csv")
        end_time = intervaluate(exp_dict["strain_intervals"], exp_dict["time_intervals"], MAX_STRAIN)
        end_strain = MAX_STRAIN*dimensions["x"]
        
        # Defines the simulation parameters
        itf.define_simulation(
            simulation_path = "deer/1to1_ui",
            end_time        = end_time,
            end_strain      = end_strain
        )

        # Runs the model and saves results
        itf.export_params()
        itf.simulate("~/moose/deer/deer-opt", NUM_PROCESSORS, MAX_DURATION)

        # Conduct post processing
        itf.compress_csv(sf=5, exclude=["x", "y", "z"])
        itf.post_process(grain_map_path=f"{input_path}/grain_map.csv")
        itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])
