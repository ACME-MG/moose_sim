
    BEGIN SCULPT

        # Dimensions
        nelx = 8
        nely = 8
        nelz = 8

        # Fixed mesh improvement
        smooth = 2
        pillow_curves = true
        pillow_boundaries = true
        micro_shave = true
        scale = 1

        # Variable mesh improvement
        defeature = 1
        opt_threshold = 0.7
        pillow_curve_layers = 3
        pillow_curve_thresh = 0.3
        
        # Solver
        laplacian_iters = 5
        max_opt_iters = 50
        
        # Output files
        input_spn = ./results/240401131138_8/rve.spn
        exodus_file = ./results/240401131138_8/mesh.e
        
    END SCULPT
    