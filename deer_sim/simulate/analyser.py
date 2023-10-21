"""
 Title:         Analyser
 Description:   For analysing the results of the simulation
 Author:        Janzen Choi

"""

# Libraries
import matplotlib.pyplot as plt

def plot_creep(csv_path:str, output_path:str, direction:str) -> None:
    """
    Plots creep curves from the simulation results

    Parameters:
    * `csv_path`:    Path to the CSV file
    * `output_path`: Path to the output file
    * `direction`:   The direction (x, y, z)
    """

    # Define the directions
    direction_map = {"x": "xx", "y": "yy", "z": "zz"}
    direction = direction_map[direction]

    # Prepare plot
    plt.figure(figsize=(5,5))
    plt.title(f"Strain {direction} against Time")
    plt.xlabel("Time (s)")
    plt.ylabel(f"Strain {direction}")

    # Reads the contents of the file
    with open(csv_path, "r") as fh:
        all_lines = fh.readlines()
    headers = all_lines[0].replace("\n","").split(",")
    time_index = headers.index("time")
    strain_index = headers.index(f"mTE_{direction}")

    # Extract data
    time_list, strain_list = [], []
    for line in all_lines[1:]:
        line = line.replace("\n", "").split(",")
        time_list.append(float(line[time_index]))
        strain_list.append(float(line[strain_index]))

    # Plot data and save
    plt.scatter(time_list, strain_list, marker="o", linewidth=1)
    plt.savefig(output_path)
