"""
 Title:         Elastic
 Description:   Plots the elastic strain
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += ["../.."]
import cv2, numpy as np
import matplotlib.pyplot as plt
from deer_sim.helper.general import flatten
from deer_sim.helper.io import csv_to_dict
from deer_sim.analyse.plotter import save_plot
from deer_sim.analyse.pole_figure import IPF, get_lattice, get_colour_map
from neml.math import rotations, tensors
from neml.cp import crystallography

# Constants
SUMMARY_PATH = "data/sim_data.csv"
KEYWORD      = "_stress"

def get_lattice(structure:str="fcc"):
    """
    Gets the lattice object

    Parameters:
    * `structure`: The crystal structure

    Returns the lattice object
    """
    lattice = crystallography.CubicLattice(1.0)
    if structure == "fcc":
        lattice.add_slip_system([1,1,0], [1,1,1])
    elif structure == "bcc":
        lattice.add_slip_system([1,1,1], [1,1,0])
        lattice.add_slip_system([1,1,1], [1,2,3])
        lattice.add_slip_system([1,1,1], [1,1,2])
    else:
        raise ValueError(f"Crystal structure '{structure}' unsupported!")
    return lattice

# Extract initialisation information
summary_dict = csv_to_dict(SUMMARY_PATH)
grain_ids = [int(key.replace("_phi_1","").replace("g","")) for key in summary_dict.keys() if "_phi_1" in key]
orientation_keys = [[f"g{grain_id}_{phi}" for phi in ["phi_1", "Phi", "phi_2"]] for grain_id in grain_ids]
num_states = len(summary_dict[orientation_keys[0][0]])

# Get orientations (euler-bunge, passive, rads) and grain stress for each state
orientation_history = [[[summary_dict[key][i] for key in keys] for keys in orientation_keys]
                       for i in range(num_states)]
stress_history = [[summary_dict[key][i] for key in summary_dict.keys()
                   if key.startswith("g") and KEYWORD in key] for i in range(num_states)]
volume_history = [[summary_dict[key][i] for key in summary_dict.keys()
                   if key.startswith("g") and "volume" in key] for i in range(num_states)]
all_volumes = flatten(volume_history)

# Calculate schmidt factor history
lattice = get_lattice("fcc")
schmidt_history = []
for orientation_list, stress_list in zip(orientation_history, stress_history):
    schmidt_list = []
    for orientation, stress in zip(orientation_list, stress_list):
        co = rotations.CrystalOrientation(*orientation, angle_type="radians", convention="bunge")
        matrix_list = [lattice.M(0,i,co) for i in range(12)]
        schmidt = np.average([stress*matrix.data[0] for matrix in matrix_list])
        schmidt_list.append(schmidt)
    schmidt_history.append(schmidt_list)
all_schmidts = flatten(schmidt_history)

# Initialise video writer
frame_rate = 3
frame_size = (640, 480)
fourcc = cv2.VideoWriter_fourcc(*"mp4v") # codec for mp4
video_writer = cv2.VideoWriter("stresses.mp4", fourcc, frame_rate, frame_size)

# Record stress distribution
ipf = IPF(
    lattice = get_lattice("fcc"),
    # colour_limits = (min(all_schmidts), max(all_schmidts)),
    # size_limits = (min(all_volumes), max(all_volumes)),
)
sample_direction = [1,0,0]
for i, (orientations, schmidts, volumes) in enumerate(zip(orientation_history, schmidt_history, volume_history)):
    
    # Ignore initial (zero stress)
    if i == 0:
        continue
    print(f"Adding frame {i}")
    
    # Otherwise, draw the IPF
    # ipf.plot_ipf(orientations, sample_direction, schmidts, volumes)
    ipf.plot_ipf(orientations, sample_direction, schmidts)
    figure = plt.gcf()
    figure.canvas.draw()
    
    # Convert drawing to video frame
    image = np.frombuffer(figure.canvas.tostring_rgb(), dtype=np.uint8)
    image = image.reshape(figure.canvas.get_width_height()[::-1] + (3,))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    video_writer.write(image)
    plt.close(figure)
    
# Release writer
video_writer.release()

get_colour_map(all_schmidts, orientation="vertical")
save_plot("cm.png")
