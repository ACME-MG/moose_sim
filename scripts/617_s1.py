import sys; sys.path += [".."]
from deer_sim.interface import Interface
from deer_sim.helper.general import round_sf

# DATA_FOLDER = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/ebsd_mesher/240612151644_617_s1_lr"
DATA_FOLDER = "/mnt/c/Users/Janzen/OneDrive - UNSW/PhD/results/ebsd_mesher/240612152121_617_s1_unfixed"
itf = Interface(input_path=DATA_FOLDER)
itf.define_mesh("mesh.e", "element_stats.csv")

itf.define_material(
    material_name   = "mat_1to1",
    material_params = {

        # # Crystal Plasticity Parameters
        # "cp_tau_s":   200,
        # "cp_b":       2,
        # "cp_tau_0":   400,
        # "cp_gamma_0": round_sf(1e-4/3, 5),
        # "cp_n":       4,

        # # Viscoplastic Parameters
        # "vp_s0":      95.121,
        # "vp_R":       559.17,
        # "vp_d":       1.3763,
        # "vp_n":       4.2967,
        # "vp_eta":     2385.9,

        "cp_tau_s":   1250,
        "cp_b":       0.25,
        "cp_tau_0":   107,
        "cp_gamma_0": round_sf(1e-4/3, 5),
        "cp_n":       4.5,
        "vp_s0":      107,
        "vp_R":       8600,
        "vp_d":       0.25,
        "vp_n":       4.5,
        "vp_eta":     1450,
    },
    youngs          = 211000.0,
    poissons        = 0.30,
)

itf.define_simulation(
    simulation_name = "sim_1to1",
    # time_intervals  = [0, 130.75, 261.51, 392.26, 523.01, 653.77, 784.52, 915.27, 1046, 1176.8, 1307.5, 1438.3, 1569, 1699.8],
    # end_strain      = 0.189*2300*1.5
    time_intervals  = [0.0,12.6,25.2,37.8,50.4,63.0,75.6,88.2,100.8,113.4,126.0,252.0,378.0,504.0,630.0,756.0,882.0,1008.0,1134.0,1260.0,1386.0,1512.0,1638.0,1764.0,1890.0,2016.0,2142.0,2268.0,2394.0,2520.0,2646.0,2772.0,2898.0,3024.0,3150.0,3276.0,3402.0,3528.0,3654.0,3780.0,3906.0,4032.0,4158.0,4284.0,4410.0,4536.0,4662.0,4788.0,4914.0,5040.0,5166.0,5292.0,5418.0,5544.0,5670.0,5796.0,5922.0,6048.0,6174.0,6300.0],
    end_strain      = 2173.5
)

itf.export_params()
itf.simulate("~/moose/deer/deer-opt", int(sys.argv[1]), 10000)
itf.remove_artifacts()
