"""
 Title:         Sample 617_s3
 Description:   Runs the CPFEM model using CCD
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf
from deer_sim.helper.sampler import get_lhs
from deer_sim.helper.io import csv_to_dict

# Constants
NUM_PARALLEL   = 4
NUM_PROCESSORS = 48

# Define VP material parameters
vp_param_dict = {
    "vp_s0":  93.655,
    "vp_R":   3957.3,
    "vp_d":   0.5651,
    "vp_n":   7.3648,
    "vp_eta": 721.59,
}

# Get CP parameter combinations
bounds_dict = {
    "cp_lh_0":    (0, 200),
    "cp_lh_1":    (0, 200),
    "cp_tau_0":   (0, 200),
    "cp_n":       (1, 16),
    "cp_gamma_0": (round_sf(1e-4/3, 4), round_sf(1e-4/3, 4)),
}
param_dict_list = get_lhs(bounds_dict, 32)
# for param_dict in param_dict_list:
#     print(param_dict)
# exit()

# Section CP parameter list for script
sim_id     = int(sys.argv[1])
num_sims   = int(len(param_dict_list)/NUM_PARALLEL)
index_list = list(range(32))[sim_id*num_sims:(sim_id+1)*num_sims]
param_dict_list = [param_dict_list[i] for i in index_list]

# Iterate through CP parameter list
for i, cp_param_dict in enumerate(param_dict_list):

    # Initialise
    index_str = str(i+1).zfill(2)
    itf = Interface(
        title       = f"{sim_id}_{index_str}",
        input_path  = "../data/617_s3/10u",
        output_path = "../results/",
    )

    # Define the mesh
    itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
    dimensions = itf.get_dimensions()

    # Defines the material parameters
    itf.define_material(
        material_name   = "cvp_ae_lh",
        material_params = {**cp_param_dict, **vp_param_dict},
        c_11            = 250000,
        c_12            = 151000,
        c_44            = 123000,
        youngs          = 211000.0,
        poissons        = 0.30,
    )

    # Defines the simulation parameters
    exp_dict = csv_to_dict(f"../data/617_s3/617_s3_exp.csv")
    itf.define_simulation(
        simulation_name = "1to1_ui",
        end_time        = exp_dict["time_intervals"][-1],
        end_strain      = exp_dict["strain_intervals"][-1] * dimensions["x"]
    )

    # Runs the model and saves results
    itf.export_params()
    itf.simulate("~/moose/deer/deer-opt", NUM_PROCESSORS, 100000)

    # Conduct post processing
    itf.compress_csv(sf=5, exclude=["x", "y", "z"])
    itf.post_process()
    itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])
