q = [0.458918505, -0.729728245, -0.229312538, 0.452002494]
import sys; sys.path += [".."]
from deer_sim.maths.neml import deer_quat_to_euler
print(deer_quat_to_euler(q, True, True))
# print(deer_quat_to_euler(q, False, True))
q = [0.452997275, -0.229247374, 0.729653314, -0.45808842]
print(deer_quat_to_euler(q, True, False))
# print(deer_quat_to_euler(q, False, False))