"""
 Title:         Familiser
 Description:   Contains code for grouping grain orientations into grain families
 References:    http://www.ebsd.info/pdf/TablesOfTextureAnalysis.pdf
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from neml.math import rotations, tensors
from deer_sim.maths.orientation import deg_to_rad, fix_angle
from deer_sim.maths.neml import get_cubic_misorientation

def get_magnitude(vector:list) -> float:
    """
    Calculates the magnitude of a vector

    Parameters:
    * `vector`: The vector

    Returns the magnitude
    """
    square_sum = sum([math.pow(v, 2) for v in vector])
    magnitude = math.sqrt(square_sum)
    return magnitude

def is_equal(list_1:list, list_2:list) -> bool:
    """
    Checks whether the elements of two lists are the same
    
    Parameters:
    * `list_1`: The first list
    * `list_2`: The second list
    
    Returns the equality
    """
    if len(list_1) != len(list_2):
        return False
    for e_1, e_2 in zip(list_1, list_2):
        if e_1 != e_2:
            return False
    return True

def miller_to_euler(hkl:list, uvw:list) -> list:
    """
    Converts a list of miller indices to their euler-bunge form;
    (plane)[directionn] = (hkl)[uvw] = {hkl}<uvw>

    Parameters:
    * `hkl`: The crystallographic plane
    * `uvw`: The crystallographic direction

    Returns the euler-bunge orientation (rads)
    """
    if is_equal(hkl, uvw):
        return [0,0,0]
    hkl_vector = tensors.Vector(np.array([float(i) for i in hkl])).normalize()
    uvw_vector = tensors.Vector(np.array([float(i) for i in uvw])).normalize()
    quaternion = rotations.rotate_to(hkl_vector, uvw_vector)
    euler = quaternion.to_euler(angle_type="radians", convention="bunge")
    euler = [fix_angle(e) for e in euler]
    return euler

def get_cubic_family(orientations:list, plane:list, direction:list, threshold:float=10.0) -> list:
    """
    Groups a list of orientations to a family

    Parameters:
    * `orientations`: The list of euler-bunge angles (rads)
    * `plane`:        The plane
    * `direction`:    The direction
    * `threshold`:    The misorientation threshold for being part of a family (deg)

    Returns the indices of the grain family
    """
    
    # Calculate the miller orientation and convert threshold
    pd_orientation = miller_to_euler(plane, direction)
    rad_threshold = deg_to_rad(threshold)
    
    # Iterate through grains and add to family
    family_indices = []
    for i, orientation in enumerate(orientations):
        misorientation = get_cubic_misorientation(orientation, pd_orientation)
        misorientation = min([misorientation, abs(misorientation-math.pi)])
        if misorientation < rad_threshold:
            family_indices.append(i)
    return family_indices

def get_grain_family(orientations:list, plane:list, direction:list, type:str="cubic",
                     threshold:float=10.0) -> list:
    """
    Groups a list of orientations to a family

    Parameters:
    * `orientations`: The list of orientations (neml.math.rotations.Orientation)
    * `plane`:        The plane
    * `direction`:    The direction
    * `type`:         The type of crystal structure
    * `threshold`:    The misorientation threshold for being part of a family (deg)

    Returns the indices of the grain family
    """
    
    # Calculate the miller orientation and convert threshold
    pd_orientation = miller_to_euler(plane, direction)
    rad_threshold = deg_to_rad(threshold)
    
    # Iterate through grains and add to family
    family_indices = []
    for i in range(len(orientations)):
        orientation = orientations[i].to_euler(angle_type="radians", convention="bunge")
        misorientation = get_cubic_misorientation(orientation, pd_orientation, type)
        if misorientation < rad_threshold:
            family_indices.append(i)
    return family_indices

# Testing
# hkl_uvw = [
#     [[0,0,1],  [1,0,0]],   # [0,0,90]
#     [[0,2,1],  [1,0,0]],   # [0,26,90]
#     [[0,1,1],  [1,0,0]],   # [0,45,90]
#     [[0,1,1],  [2,1,1]],   # [35,45,90]
#     [[1,2,3],  [6,3,4]],   # [59,37,63]
#     [[1,1,2],  [1,1,1]],   # [90,35,45]
#     [[4,4,11], [11,11,8]], # [90,27,45]
# ]
# from orientation import rad_to_deg
# for pd in hkl_uvw:
#     print(rad_to_deg(miller_to_euler(pd[0], pd[1])))
#     print("================")
