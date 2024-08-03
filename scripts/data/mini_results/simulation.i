
# ==================================================
# Define global parameters
# ==================================================

[GlobalParams]
  displacements = 'disp_x disp_y disp_z'
[]

# ==================================================
# Define Mesh
# ==================================================

[Mesh]
  use_displaced_mesh = false
  [./mesh_input]
    type         = FileMeshGenerator
    file         = 'mesh.e'
  [../]
  [./add_side_sets]
    input        = mesh_input
    type         = SideSetsFromNormalsGenerator
    fixed_normal = true
    new_boundary = 'x0 x1'
    normals      = '-1 0 0 1 0 0'
  [../]
  [./add_subdomain_ids]
    type         = SubdomainExtraElementIDGenerator
    input        = add_side_sets
    subdomains   = '1 2 3 4'
    extra_element_id_names = 'block_id'
    extra_element_ids = '1 2 3 4'
  [../]
  [./add_z_hold_side_set]
    input        = add_subdomain_ids
    type         = SideSetsAroundSubdomainGenerator
    new_boundary = 'z0'
    fixed_normal = true
    normal       = '0 0 -1'
    block        = '3 4'
  [../]
  [./add_y_hold_side_set]
    input        = add_z_hold_side_set
    type         = SideSetsAroundSubdomainGenerator
    new_boundary = 'y0'
    fixed_normal = true
    normal       = '0 -1 0'
    block        = '3 4'
  [../]
[]

# ==================================================
# Define Initial Orientations
# ==================================================

# Element orientations
[UserObjects]
  [./euler_angle_file]
    type           = ElementPropertyReadFile
    nprop          = 3
    prop_file_name = 'element_stats.csv'
    read_type      = element
    use_zero_based_block_indexing = false
  [../]
[]

# ==================================================
# Define Modules
# ==================================================

[Modules]
  [./TensorMechanics]
    [./Master]
      [./all]
        strain          = FINITE
        formulation     = TOTAL
        add_variables   = true
        new_system      = true
        volumetric_locking_correction = true # linear hex elements
        generate_output = 'elastic_strain_xx strain_xx cauchy_stress_xx mechanical_strain_xx'
      [../]
    [../]
  [../]
[]

# ==================================================
# Define Variables
# ==================================================

[AuxVariables]
  [./block_id]
    family = MONOMIAL
    order  = CONSTANT
  [../]
  [./volume]
    order  = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q1]
    order  = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q2]
    order  = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q3]
    order  = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q4]
    order  = CONSTANT
    family = MONOMIAL
  [../]
[]

# ==================================================
# Define Kernels
# ==================================================

[AuxKernels]
  [block_id]
    type          = ExtraElementIDAux
    variable      = block_id
    extra_id_name = block_id
  [../]
  [volume]
    type = VolumeAux
    variable = volume
  []
  [q1]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 0
    variable   = orientation_q1
    execute_on = 'initial timestep_end'
    block      = '1 2'
  [../]
  [q2]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 1
    variable   = orientation_q2
    execute_on = 'initial timestep_end'
    block      = '1 2'
  [../]
  [q3]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 2
    variable   = orientation_q3
    execute_on = 'initial timestep_end'
    block      = '1 2'
  [../]
  [q4]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 3
    variable   = orientation_q4
    execute_on = 'initial timestep_end'
    block      = '1 2'
  [../]
[]

# ==================================================
# Apply stress
# ==================================================

[Functions]
  [./applied_load]
    type = PiecewiseLinear
    x    = '0 4'
    y    = '0 4'
  [../]
[]

# ==================================================
# Boundary Conditions
# ==================================================

[BCs]
  [./z0hold]
    type     = DirichletBC
    boundary = 'z0'
    variable = disp_z
    value    = 0.0
  [../]
  [./y0hold]
    type     = DirichletBC
    boundary = 'y0'
    variable = disp_y
    value    = 0.0
  [../]
  [./x0hold]
    type     = DirichletBC
    boundary = 'x0'
    variable = disp_x
    value    = 0.0
  [../]
  [./x1load]
    type     = FunctionDirichletBC
    boundary = 'x1'
    variable = disp_x
    function = applied_load
    preset   = false
  [../]
[]

# ==================================================
# Dampers
# ==================================================

[Dampers]
  [./damper]
    type = ReferenceElementJacobianDamper
    max_increment = 0.005 # 0.002
    displacements = 'disp_x disp_y disp_z'
  [../]
[]

# ==================================================
# Define Material
# ==================================================

[Materials]
  [./stress1]
    type               = NEMLCrystalPlasticity
    database           = 'material.xml'
    model              = 'mat_1to1_cp'
    large_kinematics   = true
    euler_angle_reader = euler_angle_file
    angle_convention   = 'bunge'
    block              = '1 2'
  [../]
  [./stress2]
    type             = CauchyStressFromNEML
    database         = 'material.xml'
    model            = 'mat_1to1_vp'
    large_kinematics = true
    block            = '3 4'
  [../]
[]

# ==================================================
# Define Preconditioning
# ==================================================

[Preconditioning]
  [./SMP]
    type = SMP
    full = true
  [../]
[]

# ==================================================
# Define Postprocessing (History)
# ==================================================

[VectorPostprocessors]
  [./element]
    type     = ElementValueSampler
    variable = 'block_id volume
                orientation_q1 orientation_q2 orientation_q3 orientation_q4
                cauchy_stress_xx strain_xx elastic_strain_xx mechanical_strain_xx'
    contains_complete_history = false
    execute_on = 'INITIAL TIMESTEP_END'
    sort_by    = id
    block      = '1 2 3 4'
  [../]
[]

# ==================================================
# Define Postprocessing (Average Response)
# ==================================================

[Postprocessors]

  # Total Strain
  [./mTE_cpvp_xx]
    type     = ElementAverageValue
    variable = strain_xx
  [../]
  [./mTE_cp_xx]
    type     = ElementAverageValue
    variable = strain_xx
    block    = '1 2'
  [../]
  [./mTE_vp_xx]
    type     = ElementAverageValue
    variable = strain_xx
    block    = '3 4'
  [../]

  # Cuachy Stress
  [./mCS_cpvp_xx]
    type     = ElementAverageValue
    variable = cauchy_stress_xx
  [../]
  [./mCS_cp_xx]
    type     = ElementAverageValue
    variable = cauchy_stress_xx
    block    = '1 2'
  [../]
  [./mCS_vp_xx]
    type     = ElementAverageValue
    variable = cauchy_stress_xx
    block    = '3 4'
  [../]

  # Elastic Strain
  [./mEE_cpvp_xx]
    type     = ElementAverageValue
    variable = elastic_strain_xx
  [../]
  [./mEE_cp_xx]
    type     = ElementAverageValue
    variable = elastic_strain_xx
    block    = '1 2'
  [../]
  [./mEE_vp_xx]
    type     = ElementAverageValue
    variable = elastic_strain_xx
    block    = '3 4'
  [../]
[]

# ==================================================
# Define Simulation
# ==================================================

[Executioner]
  
  # Transient (time-dependent) and multi-physics problem
  type = Transient
  automatic_scaling = false

  # Solver
  solve_type = NEWTON # Use Newton-Raphson, not PJFNK
  residual_and_jacobian_together = true
  
  # Options for PETSc (to solve linear equations)
  petsc_options       = '-snes_converged_reason -ksp_converged_reason' 
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_package -ksp_gmres_restart 
                         -pc_hypre_boomeramg_strong_threshold -pc_hypre_boomeramg_interp_type -pc_hypre_boomeramg_coarsen_type 
                         -pc_hypre_boomeramg_agg_nl -pc_hypre_boomeramg_agg_num_paths -pc_hypre_boomeramg_truncfactor'
  petsc_options_value = 'hypre boomeramg 200 0.7 ext+i PMIS 4 2 0.4'
  
  # Solver tolerances
  l_max_its                = 500 
  l_tol                    = 1e-4 # 1e-6
  nl_max_its               = 16
  nl_rel_tol               = 1e-5 # 1e-6
  nl_abs_tol               = 1e-5 # 1e-6
  nl_forced_its            = 1
  # n_max_nonlinear_pingpong = 1
  line_search              = 'none'

  # Time variables
  start_time = 0.0
  end_time   = 4
  dtmin      = 0.01
  dtmax      = 4

  # Simulation speed up
  [./Predictor]
    type  = SimplePredictor
    scale = 1.0
  [../]

  # Timestep growth
  [./TimeStepper]
    type                   = IterationAdaptiveDT
    growth_factor          = 2
    cutback_factor         = 0.5
    linear_iteration_ratio = 100000000000
    optimal_iterations     = 8
    iteration_window       = 1
    dt                     = 1.0
  [../]
[]

# ==================================================
# Define Simulation Output
# ==================================================

[Outputs]
  print_linear_residuals = false
  [./console]
    type        = Console
    output_linear = false
    print_mesh_changed_info = false
  [../]
  [./outfile]
    type        = CSV
    file_base   = 'results'
    time_data   = true
    delimiter   = ','
    execute_on  = 'initial timestep_end'
    sync_only   = true
    sync_times  = '0.0 1 2 4'
  [../]
[]
