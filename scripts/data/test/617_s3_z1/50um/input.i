
BEGIN SCULPT
    
    # Dimensions
    nelx = 56
    nely = 32
    nelz = 1
    scale = 50.0
    
    # Fixed mesh improvement
    smooth = 3
    defeature = 1
    pillow_curves = true
    pillow_boundaries = true
    micro_shave = true
    
    # Variable mesh improvement
    opt_threshold = 0.7
    pillow_curve_layers = 3
    pillow_curve_thresh = 0.3

    # Solver
    laplacian_iters = 5
    max_opt_iters = 50
    
    # Output
    input_spn = ./results/240919144206_res/voxels.spn
    exodus_file = ./results/240919144206_res/mesh.e

END SCULPT
