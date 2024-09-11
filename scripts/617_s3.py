"""
 Title:         617_s3
 Description:   Runs the CPFEM model once
 References:    https://asmedigitalcollection.asme.org/pressurevesseltech/article/135/2/021502/378322/Synchrotron-Radiation-Study-on-Alloy-617-and-Alloy
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf
from deer_sim.helper.io import csv_to_dict

# Define the mesh and orientations
FOLDER = "617_s3_lr"
itf = Interface(input_path=f"data/{FOLDER}")
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)

# Defines the material parameters
itf.define_material(
    material_name   = "cvp_ae_lh",
    material_params = {

        # Crystal Plasticity Parameters
        # "cp_tau_s":   825,
        # "cp_b":       2,#0.3,
        # "cp_tau_0":   112,
        "cp_lh_0":    60,
        "cp_lh_1":    180,
        "cp_tau_0":   60,
        "cp_gamma_0": round_sf(1e-4/3, 5),
        "cp_n":       5,

        # Viscoplastic Parameters
        "vp_s0":      93.655,
        "vp_R":       3957.3,
        "vp_d":       0.5651,
        "vp_n":       7.3648,
        "vp_eta":     721.59,
    },
    c_11     = 250000,
    c_12     = 151000,
    c_44     = 123000,
    youngs   = 211000.0,
    poissons = 0.30,
)

# Defines the simulation parameters
exp_dict = csv_to_dict(f"data/{FOLDER}/617_s3_exp.csv")
itf.define_simulation(
    simulation_name = "1to1_ui",
    end_time        = exp_dict["time_intervals"][-1],
    end_strain      = exp_dict["strain_intervals"][-1] * 2200 * 5/3
)

# Runs the model and saves results
num_processors = int(sys.argv[1]) if len(sys.argv)>1 else 8
itf.export_params()
itf.simulate("~/moose/deer/deer-opt", num_processors, 100000)

# Conduct post processing
itf.compress_csv(sf=5, exclude=["x", "y", "z"])
itf.post_process(grain_map_path="data/617_s3/grain_map.csv")
itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])
