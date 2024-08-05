"""
 Title:         Familiser
 Description:   Contains code for grouping grain orientations into grain families
 References:    http://www.ebsd.info/pdf/TablesOfTextureAnalysis.pdf
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from neml.math import rotations, tensors
from neml.cp import crystallography
from deer_sim.maths.orientation import deg_to_rad, fix_angle

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

def get_grain_family(orientations:list, plane:list, direction:list, threshold:float=10.0) -> list:
    """
    Groups a list of orientations to a family

    Parameters:
    * `orientations`: The list of euler-bunge angles (rads)
    * `plane`:        The plane (or the crystal direction)
    * `direction`:    The direction (or the sample direction)
    * `threshold`:    The misorientation threshold for being part of a family (deg)

    Returns the indices of the grain family
    """
    
    # Initialise
    lattice = crystallography.CubicLattice(1.0)
    plane = tensors.Vector(np.array([float(p) for p in plane])).normalize()
    direction = tensors.Vector(np.array([float(d) for d in direction])).normalize()
    rad_threshold = deg_to_rad(threshold)
    
    # Iterate through grains and add to family
    family_indices = []
    for i, orientation in enumerate(orientations):
        quat = rotations.Orientation(*orientation, convention="bunge")
        quat = quat.apply(direction)
        misorientations = [np.arccos(np.abs(plane.dot(sop.apply(quat)))) for sop in lattice.symmetry.ops]
        misorientation = np.min(misorientations)
        if misorientation < rad_threshold:
            family_indices.append(i)
            
    # Return indices
    return family_indices
