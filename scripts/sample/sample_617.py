"""
 Title:         Sample 617_s1
 Description:   Runs the CPFEM model many times
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
import itertools
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf

# Define parameter domain
index_1 = int(sys.argv[1])
index_2 = int(sys.argv[2])
all_params_dict = {
    "cp_tau_s":   [100, 200, 400, 800, 1600],
    "cp_b":       [[0.25, 0.5, 1, 2, 4, 8][index_1]],
    "cp_tau_0":   [[100, 200, 400, 800][index_2]],
    "cp_gamma_0": [round_sf(1e-4/3, 4)],
    "cp_n":       [1, 2, 4, 8, 16, 32],
}

# Get all parameter combinations
param_names = list(all_params_dict.keys())
param_values = list(all_params_dict.values())
combinations = list(itertools.product(*param_values))
combinations = [list(c) for c in combinations]

# Iterate through parameter combinations
for i, combination in enumerate(combinations):

    # Initialise
    index_str = str(i+1).zfill(3)
    itf = Interface(
        title       = f"{index_1}_{index_2}_{index_str}",
        input_path  = "../data/ebsd/617_s1_z1_lr",
        output_path = "../results/",
    )

    # Define the mesh and orientations
    itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)

    # Defines the material parameters
    param_dict = dict(zip(param_names, combination))
    itf.define_material(
        material_name   = "mat_1to1",
        material_params = {

            # Crystal Plasticity Parameters
            "cp_tau_s":   param_dict["cp_tau_s"],
            "cp_b":       param_dict["cp_b"],
            "cp_tau_0":   param_dict["cp_tau_0"],
            "cp_gamma_0": round_sf(1e-4/3, 5),
            "cp_n":       param_dict["cp_n"],

            # Viscoplastic Parameters
            "vp_s0":      95.121,
            "vp_R":       559.17,
            "vp_d":       1.3763,
            "vp_n":       4.2967,
            "vp_eta":     2385.9,
        },
        youngs   = 211000.0,
        poissons = 0.30,
    )

    # Defines the simulation parameters
    itf.define_simulation(
        simulation_name = "sim_1to1_simple",
        time_intervals  = [0, 130.75, 261.51, 392.26, 523.01, 653.77, 784.52, 915.27, 1046, 1176.8, 1307.5, 1438.3, 1569, 1699.8],
        end_strain      = 0.189*2300*1.5
    )

    # Runs the model and saves results
    itf.export_params()
    itf.simulate("~/moose/deer/deer-opt", 8, 10000)
