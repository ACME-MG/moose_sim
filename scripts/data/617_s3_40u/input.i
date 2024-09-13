
BEGIN SCULPT
    
    # Dimensions
    nelx = 85
    nely = 39
    nelz = 1
    scale = 40
    
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
    input_spn = ./results/240823140420_617_s3/voxels.spn
    exodus_file = ./results/240823140420_617_s3/mesh.e

END SCULPT