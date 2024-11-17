"""
 Title:         Generate LHS
 Description:   For generating parameter values using LHS
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
from moose_sim.helper.sampler import get_lhs
from moose_sim.helper.general import round_sf
from moose_sim.helper.io import dict_to_csv

# Constants
OUTPUT_PATH = "params.csv"

# Get parameters for LH6
bounds_dict = {
    "cp_lh_0":    (0, 400),
    "cp_lh_1":    (0, 400),
    # "cp_lh_2":    (0, 400),
    # "cp_lh_3":    (0, 400),
    # "cp_lh_4":    (0, 400),
    # "cp_lh_5":    (0, 400),
    "cp_tau_0":   (0, 200),
    "cp_n":       (1, 16),
    "cp_gamma_0": (round_sf(1e-4/3, 4), round_sf(1e-4/3, 4)),
}
param_dict_list = get_lhs(bounds_dict, 16)

# # Get parameters for non-LH
# bounds_dict = {
#     "cp_tau_s":   (100, 1600),
#     "cp_b":       (0.5, 8),
#     "cp_tau_0":   (50, 400), # 800
#     "cp_n":       (1, 16),
#     "cp_gamma_0": (round_sf(1e-4/3, 4), round_sf(1e-4/3, 4)),
# }
# param_dict_list = get_lhs(bounds_dict, 4)

# Format parameters and save
params_dict = {k: [d[k] for d in param_dict_list] for k in param_dict_list[0]}
dict_to_csv(params_dict, OUTPUT_PATH)
