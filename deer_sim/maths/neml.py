"""
 Title:         NEML
 Description:   Helper functions that use NEML
 Author:        Janzen Choi

"""

# Libraries
import math
from deer_sim.maths.orientation import fix_angle
from neml.math import rotations

def deer_quat_to_euler(quat:list, reorient:bool=False, offset:bool=False) -> list:
    """
    Converts the quaternion outputted by deer into euler-bunge angles

    Parameters:
    * `quat`:     The quaternion
    * `offset`:   Whether to add an offset to phi_1
    * `reorient`: Whether to invert the angle

    Returns the euler-bunge angle (rads)
    """
    euler = rotations.Orientation(quat).to_euler(angle_type="radians", convention="bunge")
    if reorient:
        euler = reorient_euler(euler)
    if offset:
        euler[0] += math.pi
    euler = [fix_angle(e) for e in euler]
    return euler

def reorient_euler(euler:list) -> list:
    """
    Inverts the euler angle from passive/active to active/passive

    Parameters:
    * `euler`: The euler angle (rads)

    Returns the inverted euler angle
    """
    orientation = rotations.CrystalOrientation(euler[0], euler[1], euler[2], angle_type="radians", convention="bunge")
    inverse = orientation.inverse()
    new_euler = inverse.to_euler(angle_type="radians", convention="bunge")
    return list(new_euler)
