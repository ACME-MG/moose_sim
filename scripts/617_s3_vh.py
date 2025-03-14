"""
 Title:         617_s3 Voce Hardening
 Description:   Runs the CPFEM model once with the Voce hardening model
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
# MESH_PATH = "data/617_s3/10um"
EXP_PATH  = "data/617_s3/617_s3_exp.csv"

# Define the mesh and orientations
itf = Interface(input_path=MESH_PATH)
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
dimensions = itf.get_dimensions()

# Define crystal plasticity parameters
param_names  = ["cp_tau_s", "cp_b", "cp_tau_0", "cp_n", "cp_gamma_0"]
param_values = [1589.8, 0.1672, 127.47, 3.8933, 3.25e-05]
cp_params = dict(zip(param_names, param_values))

# Defines the material parameters
itf.define_material(
    material_path   = "deer/cpvh_ae",
    material_params = cp_params,
    c_11            = 250000,
    c_12            = 151000,
    c_44            = 123000/2,
)

# Defines the simulation parameters
exp_dict = csv_to_dict(EXP_PATH)
eng_strain = math.exp(exp_dict["strain_intervals"][-1])-1
itf.define_simulation(
    simulation_path = "deer/1to1_ui_cp_pin",
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
