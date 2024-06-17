"""
 Title:         617_s1
 Description:   Runs the CPFEM model once
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf

# Define paths
parent_path = "/mnt/c/Users/Janzen/Desktop/code/ebsd_mesher/scripts/results"
path_list = [
    "240617094525_617_s1_d5_z4",
    "240617094822_617_s1_d6_z4",
    "240617095022_617_s1_d7_z4",
    "240617095151_617_s1_d8_z4",
    "240617095306_617_s1_d9_z4",
    "240617095409_617_s1_d10_z4",
]

# Iterate through paths
for path in path_list:

    # Define the mesh and orientations
    decrease = path.split("_")[-2]
    itf = Interface(title=f"617_s1_ztest_{decrease}", input_path=f"{parent_path}/{path}")
    itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)

    # Defines the material parameters
    itf.define_material(
        material_name   = "mat_1to1",
        material_params = {

            # Crystal Plasticity Parameters
            "cp_tau_s":   1250,
            "cp_b":       0.25,
            "cp_tau_0":   107,
            "cp_gamma_0": round_sf(1e-4/3, 5),
            "cp_n":       4.5,

            # Viscoplastic Parameters
            "vp_s0":      95.121,
            "vp_R":       559.17,
            "vp_d":       1.3763,
            "vp_n":       4.2967,
            "vp_eta":     2385.9,
        },
        youngs          = 211000.0,
        poissons        = 0.30,
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
    # itf.remove_artifacts()
