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
itf = Interface(input_path=f"data/617_s3_z1/40um")
itf.define_mesh("mesh.e", "element_stats.csv", degrees=False, active=False)
itf.define_material(material_name="test_neml2", material_ext="i")
itf.define_simulation("test_neml2")
itf.simulate("~/moose/moose/modules/solid_mechanics/solid_mechanics-opt", 4, 100)
