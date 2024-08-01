"""
 Title:         Familiser
 Description:   Contains code for grouping grain orientations into grain families
 References:    http://www.ebsd.info/pdf/TablesOfTextureAnalysis.pdf
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from deer_sim.maths.orientation import deg_to_rad, matrix_to_euler, fix_angle
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

def miller_to_euler(hkl:list, uvw:list) -> list:
    """
    Converts a list of miller indices to their euler-bunge form;
    (plane)[directionn] = (hkl)[uvw] = {hkl}<uvw>

    Parameters:
    * `hkl`: The crystallographic plane
    * `uvw`: The crystallographic direction

    Returns the euler-bunge orientation (rads)
    """
    h, k, l = tuple(hkl)
    u, v, w = tuple(uvw)
    phi_2 = math.atan2(h, k)
    Phi   = math.atan2(k, l*math.cos(phi_2))
    phi_1 = math.atan2(l*w, (k*u-h*v)*math.cos(Phi))
    euler = [fix_angle(phi) for phi in [phi_1, Phi, phi_2]]
    return euler

def miller_to_euler_2(hkl:list, uvw:list) -> list:
    """
    Converts a list of miller indices to their euler-bunge form;
    (plane)[directionn] = (hkl)[uvw] = {hkl}<uvw>

    Parameters:
    * `hkl`: The crystallographic plane
    * `uvw`: The crystallographic direction

    Returns the euler-bunge orientation (rads)
    """
    hkl_mag = get_magnitude(hkl)
    uvw_mag = get_magnitude(uvw)
    n = [i/hkl_mag for i in hkl]
    b = [i/uvw_mag for i in uvw]
    nxb = np.cross(np.array(n), np.array(b))
    nxb_mag = get_magnitude(nxb)
    t = list(nxb/nxb_mag)
    matrix = [
        [b[0], t[0], n[0]],
        [b[1], t[1], n[1]],
        [b[2], t[2], n[2]]
    ]
    euler = matrix_to_euler(matrix)
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
