import sys; sys.path += [".."]
from deer_sim.interface import Interface

itf = Interface("temp", input_path="./data/analysis", output_here=True)
itf.analyse_results("results.csv", "x")
