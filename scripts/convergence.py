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
MAX_STRAIN     = 0.05

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
    {'cp_lh_0': 46.18, 'cp_lh_1': 105.2, 'cp_tau_0': 134.7, 'cp_n': 3.356, 'cp_gamma_0': 3.333e-05},
    {'cp_lh_0': 177.1, 'cp_lh_1': 170.3, 'cp_tau_0': 116.4, 'cp_n': 7.784, 'cp_gamma_0': 3.333e-05},
    {'cp_lh_0': 80.4, 'cp_lh_1': 43.3, 'cp_tau_0': 191.6, 'cp_n': 15.4, 'cp_gamma_0': 3.333e-05},
    {'cp_lh_0': 16.17, 'cp_lh_1': 89.04, 'cp_tau_0': 172.6, 'cp_n': 2.06, 'cp_gamma_0': 3.333e-05},
    {'cp_lh_0': 165.3, 'cp_lh_1': 197.1, 'cp_tau_0': 45.9, 'cp_n': 11.09, 'cp_gamma_0': 3.333e-05},
    {'cp_lh_0': 74.59, 'cp_lh_1': 138.1, 'cp_tau_0': 86.06, 'cp_n': 10.32, 'cp_gamma_0': 3.333e-05},
    {'cp_lh_0': 130.3, 'cp_lh_1': 1.487, 'cp_tau_0': 74.26, 'cp_n': 13.04, 'cp_gamma_0': 3.333e-05},
    {'cp_lh_0': 100.7, 'cp_lh_1': 53.8, 'cp_tau_0': 20.87, 'cp_n': 5.818, 'cp_gamma_0': 3.333e-05},
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
            material_name   = "cvp_ae",
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
            simulation_name = "1to1_ui",
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
