"""
 Title:         617_s3
 Description:   Runs the CPFEM model once
 References:    https://asmedigitalcollection.asme.org/pressurevesseltech/article/135/2/021502/378322/Synchrotron-Radiation-Study-on-Alloy-617-and-Alloy
 Author:        Janzen Choi

"""

# Libraries
import sys; sys.path += [".."]
from moose_sim.interface import Interface

# Run
itf = Interface(input_path=f"data/test/minimal")
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
dimensions = itf.get_dimensions()
itf.define_material(
    material_path   = "neml2/ie",
    # material_params = {
    #     "cp_tau_0":   50,
    #     "cp_tau_sat": 50,
    #     "cp_n":       8,
    #     "cp_gamma_0": 0.20,
    #     "cp_slope":   500,
    # },
    material_ext    = "i",
    youngs          = 211000,
    poissons        = 0.30
)
itf.define_simulation(
    simulation_path = "neml2/1to1",
    simulation_ext  = "i",
    end_time        = 100,
    end_strain      = dimensions["x"]*0.1,
)
itf.simulate("~/moose/moose/modules/solid_mechanics/solid_mechanics-opt", 4, 100)
