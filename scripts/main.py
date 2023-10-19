import sys; sys.path += [".."]
from sim_deer.api import API

api = API("temp", input_path="./data/500/16_s1")
api.define_mesh("mesh.e", "input_orientations.csv")
