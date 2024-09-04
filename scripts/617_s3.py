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
FOLDER = "617_s3"
itf = Interface(input_path=f"data/{FOLDER}")
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)

# Defines the material parameters
itf.define_material(
    material_name   = "mat_1to1_ae",
    material_params = {

        # Crystal Plasticity Parameters
        "cp_tau_s":   825,
        "cp_b":       2,#0.3,
        "cp_tau_0":   112,
        "cp_gamma_0": round_sf(1e-4/3, 5),
        "cp_n":       15,

        # Viscoplastic Parameters
        "vp_s0":      93.655,
        "vp_R":       3957.3,
        "vp_d":       0.5651,
        "vp_n":       7.3648,
        "vp_eta":     721.59,
    },
    c_11     = 205000,
    c_12     = 138000,
    c_44     = 126000,
    youngs   = 211000.0,
    poissons = 0.30,
)

# Read experimental data
exp_dict = csv_to_dict(f"data/{FOLDER}/617_s3_exp.csv")
# time_intervals = exp_dict["time_intervals"]
time_intervals = sorted(list(exp_dict["time_intervals"] + [2**i for i in range(10)]))
end_strain = exp_dict["strain_intervals"][-1] * 2200 * 5/3

# Defines the simulation parameters
itf.define_simulation(
    simulation_name = "sim_1to1_vb",
    time_intervals  = time_intervals,
    end_strain      = end_strain,
)

# Runs the model and saves results
num_processors = int(sys.argv[1]) if len(sys.argv)>1 else 8
itf.export_params()
itf.simulate("~/moose/deer/deer-opt", num_processors, 100000)

# Conduct post processing
itf.compress_csv(sf=5, exclude=["x", "y", "z"])
itf.post_process(grain_map_path="data/617_s3/grain_map.csv")
itf.remove_files(["mesh.e", "element_stats.csv", "results", "simulation_out_cp"])
