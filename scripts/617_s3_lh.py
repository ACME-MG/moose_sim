"""
 Title:         617_s3
 Description:   Runs the CPFEM model once
 References:    https://asmedigitalcollection.asme.org/pressurevesseltech/article/135/2/021502/378322/Synchrotron-Radiation-Study-on-Alloy-617-and-Alloy
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
import math
from moose_sim.interface import Interface
from moose_sim.helper.io import csv_to_dict

# Define paths
MESH_PATH = "data/617_s3/40um"
EXP_PATH  = "data/617_s3/617_s3_exp.csv"

# Define the mesh and orientations
itf = Interface(input_path=MESH_PATH)
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
dimensions = itf.get_dimensions()

# Define viscoplastic parameters
vp_params = {
    "vp_s0":  93.655,
    "vp_R":   3957.3,
    "vp_d":   0.5651,
    "vp_n":   7.3648,
    "vp_eta": 721.59,
}

# Define crystal plasticity parameters
PARAM_NAMES  = [f"cp_lh_{i}" for i in range(2)] + ["cp_tau_0", "cp_n", "cp_gamma_0"]
PARAM_VALUES = [197.89, 372.47, 97.494, 4.6058] + [3.333e-05]
cp_params = dict(zip(PARAM_NAMES, PARAM_VALUES))
# cp_params = {"cp_lh_0": 129.25, "cp_lh_1": 147.54, "cp_tau_0": 84.481, "cp_n": 9.6705, "cp_gamma_0": 3.333e-05}

# Defines the material parameters
itf.define_material(
    material_path   = "deer/cvp_ae_lh",
    material_params = {**cp_params, **vp_params},
    c_11            = 250000,
    c_12            = 151000,
    c_44            = 123000,
    youngs          = 211000.0,
    poissons        = 0.30,
)

# Defines the simulation parameters
exp_dict = csv_to_dict(EXP_PATH)
eng_strain = math.exp(exp_dict["strain_intervals"][-1])-1
itf.define_simulation(
    simulation_path = "deer/1to1_ui",
    end_time        = exp_dict["time_intervals"][-1],
    end_strain      = eng_strain*dimensions["x"]
)

# Runs the model and saves results
num_processors = int(sys.argv[1]) if len(sys.argv)>1 else 8
itf.export_params()
itf.simulate("~/moose/deer/deer-opt", num_processors, 100000)

# Conduct post processing
itf.compress_csv(sf=5, exclude=["x", "y", "z"])
itf.post_process(grain_map_path=f"{MESH_PATH}/grain_map.csv")
itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])
