
# Libraries
import sys; sys.path += [".."]
import os
from deer_sim.helper.general import transpose, round_sf
from deer_sim.helper.io import csv_to_dict, dict_to_csv
from deer_sim.maths.orientation import get_average_quat, quat_to_euler

# Constants
QUAT_FIELDS = ["orientation_q1", "orientation_q2", "orientation_q3", "orientation_q4"]
RESULTS_DIR = "results/240613124605_617_s1_lr/"

# Get results
csv_file_list = [csv_file for csv_file in os.listdir(RESULTS_DIR) if csv_file.endswith(".csv")]
data_dict_list = [csv_to_dict(f"{RESULTS_DIR}/{csv_file}") for csv_file in csv_file_list]
data_dict_list = [data_dict for data_dict in data_dict_list if "block_id" in data_dict.keys()]

# Get grain mapping from last dictionary
last_data_dict = data_dict_list[-1]
grain_ids = list(set(last_data_dict["block_id"]))
grain_dict = dict(zip(grain_ids, [[] for _ in range(len(grain_ids))]))
for i, grain_id in enumerate(last_data_dict["block_id"]):
    grain_dict[grain_id].append(last_data_dict["id"][i])

# Initialise orientation averages
average_dict = dict(zip(grain_ids, [[] for _ in range(len(grain_ids))]))

# Extract orientation data from each result file
for data_dict in data_dict_list:
    
    # Get all quaternions
    all_quat_list = [data_dict[field] for field in QUAT_FIELDS]
    all_quat_list = transpose(all_quat_list)

    # Store average orientation for grain
    for grain_id in grain_ids:
        quat_list = [all_quat_list[i] for i in range(len(all_quat_list)) if i in grain_dict[grain_id]]
        average_quat = get_average_quat(quat_list)
        average_euler = quat_to_euler(average_quat)
        average_dict[grain_id].append(average_euler)

# Save the orientation trajectories
trajectories = {}
for grain_id in grain_ids:
    for i, phi in enumerate(["phi_1", "Phi", "phi_2"]):
        trajectory = [round_sf(average_euler[i], 5) for average_euler in average_dict[grain_id]]
        trajectories[f"g{int(grain_id)}_{phi}"] = trajectory
dict_to_csv(trajectories, "orientation_history.csv")
