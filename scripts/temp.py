import numpy as np
from neml.math import tensors, rotations
import sys; sys.path += [".."]
from deer_sim.maths.neml import get_cubic_misorientation
from deer_sim.maths.orientation import euler_to_quat

hkl = [1,0,0] # plane
uvw = [1,0,0] # direction

hkl_vector = tensors.Vector(np.array([float(i) for i in hkl])).normalize()
uvw_vector = tensors.Vector(np.array([float(i) for i in uvw])).normalize()

quaternion = rotations.rotate_to(hkl_vector, uvw_vector)
euler = quaternion.to_euler(angle_type="radians", convention="bunge")

my_euler = [0.32469, 2.2967, 3.4113]
mori = get_cubic_misorientation(my_euler, [0,0,0])

print(euler_to_quat(my_euler))

# print(mori)
