"""
 Title:         Sample 617_s3
 Description:   Runs the CPFEM model using CCD
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
from moose_sim.interface import Interface
from moose_sim.helper.io import csv_to_dict
from moose_sim.helper.interpolator import intervaluate

# Constants
NUM_PARALLEL   = 4
NUM_PROCESSORS = 48
MAX_DURATION   = 200000
MAX_STRAIN     = 0.10
TARGET_DIR     = "../data/617_s3_z1/5um"
PARAMS_PATH    = "params.csv"

# Define VP material parameters
vp_param_dict = {
    "vp_s0":  93.655,
    "vp_R":   3957.3,
    "vp_d":   0.5651,
    "vp_n":   7.3648,
    "vp_eta": 721.59,
}

# Get CP parameters
params_dict = csv_to_dict(PARAMS_PATH)
param_dict_list = [dict(zip(params_dict.keys(), values)) for values in zip(*params_dict.values())]

# Section CP parameter list for script
sim_id     = int(sys.argv[1])
num_sims   = int(len(param_dict_list)/NUM_PARALLEL)
index_list = list(range(len(param_dict_list)))[sim_id*num_sims:(sim_id+1)*num_sims]
param_dict_list = [param_dict_list[i] for i in index_list]

# Iterate through CP parameter list
for i, param_dict in enumerate(param_dict_list):

    # Initialise
    index_str = str(i+1).zfill(2)
    itf = Interface(
        title       = f"{sim_id}_{index_str}",
        input_path  = TARGET_DIR,
        output_path = "../results/",
    )

    # Define the mesh
    itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
    dimensions = itf.get_dimensions()
    
    # Defines the material parameters
    itf.define_material(
        material_path   = "deer/cvp_ae",
        material_params = {**param_dict, **vp_param_dict},
        c_11            = 250000,
        c_12            = 151000,
        c_44            = 123000,
        youngs          = 211000.0,
        poissons        = 0.30,
    )

    # Define end time and strain
    exp_dict = csv_to_dict("../data/617_s3_z1/617_s3_exp.csv")
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
    itf.simulate("~/moose/deer/deer-opt", NUM_PROCESSORS, 300000)

    # Conduct post processing
    itf.compress_csv(sf=5, exclude=["x", "y", "z"])
    itf.post_process(grain_map_path=f"{TARGET_DIR}/grain_map.csv")
    itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])
