
    BEGIN SCULPT

        # Dimensions
        nelx = 4
        nely = 4
        nelz = 4

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
        input_spn = ./results/240401131410_4/rve.spn
        exodus_file = ./results/240401131410_4/mesh.e
        
    END SCULPT
    