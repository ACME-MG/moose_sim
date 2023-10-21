import sys; sys.path += [".."]
from deer_sim.api import API

api = API("temp", input_path="./data/analysis", output_here=True)
api.analyse_results("results.csv", "x")
