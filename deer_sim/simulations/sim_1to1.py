"""
 Title:         Crystal Plasticity Model
 Description:   For creating the CP simulation file
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
from deer_sim.helper.general import transpose
from deer_sim.simulations.__simulation__ import __Simulation__

# Format for defining simulations
SIMULATION_FORMAT = """
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
    file         = '{mesh_file}'
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
    subdomains   = '{block_ids}'
    extra_element_id_names = 'block_id'
    extra_element_ids = '{block_ids}'
  [../]
  [./add_z_hold_side_set]
    input        = add_subdomain_ids
    type         = SideSetsAroundSubdomainGenerator
    new_boundary = 'z0'
    fixed_normal = true
    normal       = '0 0 -1'
    block        = '{grip_ids}'
  [../]
  [./add_y_hold_side_set]
    input        = add_z_hold_side_set
    type         = SideSetsAroundSubdomainGenerator
    new_boundary = 'y0'
    fixed_normal = true
    normal       = '0 -1 0'
    block        = '{grip_ids}'
  [../]
[]

# ==================================================
# Define Initial Orientations
# ==================================================

[UserObjects]
  [./euler_angle_file]
    type           = ElementPropertyReadFile
    nprop          = 3
    prop_file_name = '{orientation_file}'
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
        generate_output = 'elastic_strain_xx elastic_strain_yy elastic_strain_zz
                           strain_xx strain_yy strain_zz
                           cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz
                           mechanical_strain_xx mechanical_strain_yy mechanical_strain_zz'
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
  [./RGB_x]
    order  = CONSTANT
    family = MONOMIAL
  [../]
  [./RGB_y]
    order  = CONSTANT
    family = MONOMIAL
  [../]
  [./RGB_z]
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
  [q1]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 0
    variable   = orientation_q1
    execute_on = 'initial timestep_end'
    block      = '{grain_ids}'
  [../]
  [q2]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 1
    variable   = orientation_q2
    execute_on = 'initial timestep_end'
    block      = '{grain_ids}'
  [../]
  [q3]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 2
    variable   = orientation_q3
    execute_on = 'initial timestep_end'
    block      = '{grain_ids}'
  [../]
  [q4]
    type       = MaterialStdVectorAux
    property   = orientation
    index      = 3
    variable   = orientation_q4
    execute_on = 'initial timestep_end'
    block      = '{grain_ids}'
  [../]
  [RBG_x]
    type       = IPFColoring
    variable   = RGB_x
    q1         = orientation_q1
    q2         = orientation_q2
    q3         = orientation_q3
    q4         = orientation_q4
    sample_direction = '0.0 0.0 1.0'
    crystal_symmetry = '432'
    component  = 0
    execute_on = 'initial timestep_end'
    block      = '{grain_ids}'
  [../]
  [RBG_y]
    type       = IPFColoring
    variable   = RGB_y
    q1         = orientation_q1
    q2         = orientation_q2
    q3         = orientation_q3
    q4         = orientation_q4
    sample_direction = '0.0 0.0 1.0'
    crystal_symmetry = '432'
    component  = 1
    execute_on = 'initial timestep_end'
    block      = '{grain_ids}'
  [../]
  [RBG_z]
    type       = IPFColoring
    variable   = RGB_z
    q1         = orientation_q1
    q2         = orientation_q2
    q3         = orientation_q3
    q4         = orientation_q4
    sample_direction = '0.0 0.0 1.0'
    crystal_symmetry = '432'
    component  = 2
    execute_on = 'initial timestep_end'
    block      = '{grain_ids}'
  [../]
[]

# ==================================================
# Apply stress
# ==================================================

[Functions]
  [./applied_load]
    type = PiecewiseLinear
    x    = '0 {end_time}'
    y    = '0 {end_strain}'
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
    database           = '{material_file}'
    model              = '{material_name}_cp'
    large_kinematics   = true
    euler_angle_reader = euler_angle_file
    angle_convention   = 'bunge'
    block              = '{grain_ids}'
  [../]
  [./stress2]
    type             = CauchyStressFromNEML
    database         = '{material_file}'
    model            = '{material_name}_vp'
    large_kinematics = true
    block            = '{grip_ids}'
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
  [./VPEVS]
    type     = ElementValueSampler
    variable = 'block_id
                orientation_q1 orientation_q2 orientation_q3 orientation_q4
                cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz
                strain_xx strain_yy strain_zz
                elastic_strain_xx elastic_strain_yy elastic_strain_zz
                mechanical_strain_xx mechanical_strain_yy mechanical_strain_zz'
    contains_complete_history = false
    execute_on = 'INITIAL TIMESTEP_END'
    sort_by    = id
    block      = '{grain_ids}'
  [../]
[]

# ==================================================
# Define Postprocessing (Model Average)
# ==================================================

[Postprocessors]

  # General
  [./nelem]
    type = NumElems
  [../]
  [./ndof]
    type = NumDOFs
  [../]
  [./dt]
    type = TimestepSize
  [../]
  [./num_lin_it]
    type = NumLinearIterations
  [../]
  [./num_nonlin_it]
    type = NumNonlinearIterations
  [../]
 
  # Average stress of blocks
  [./mCS_cpvp_xx]
    type     = ElementAverageValue
    variable = cauchy_stress_xx
  [../]
  [./mCS_cpvp_yy]
    type     = ElementAverageValue
    variable = cauchy_stress_yy
  [../]
  [./mCS_cpvp_zz]
    type     = ElementAverageValue
    variable = cauchy_stress_zz
  [../]

  # Average stress of grains
  [./mCS_cp_xx]
    type     = ElementAverageValue
    variable = cauchy_stress_xx
    block    = '{grain_ids}'
  [../]
  [./mCS_cp_yy]
    type     = ElementAverageValue
    variable = cauchy_stress_yy
    block    = '{grain_ids}'
  [../]
  [./mCS_cp_zz]
    type     = ElementAverageValue
    variable = cauchy_stress_zz
    block    = '{grain_ids}'
  [../]

  # Average stress of grips
  [./mCS_vp_xx]
    type     = ElementAverageValue
    variable = cauchy_stress_xx
    block    = '{grip_ids}'
  [../]
  [./mCS_vp_yy]
    type     = ElementAverageValue
    variable = cauchy_stress_yy
    block    = '{grip_ids}'
  [../]
  [./mCS_vp_zz]
    type     = ElementAverageValue
    variable = cauchy_stress_zz
    block    = '{grip_ids}'
  [../]

  # Average strain of blocks
  [./mTE_cpvp_xx]
    type     = ElementAverageValue
    variable = strain_xx
  [../]
  [./mTE_cpvp_yy]
    type     = ElementAverageValue
    variable = strain_yy
  [../]
  [./mTE_cpvp_zz]
    type     = ElementAverageValue
    variable = strain_zz
  [../]

  # Average strain of grains
  [./mTE_cp_xx]
    type     = ElementAverageValue
    variable = strain_xx
    block = '{grain_ids}'
  [../]
  [./mTE_cp_yy]
    type     = ElementAverageValue
    variable = strain_yy
    block = '{grain_ids}'
  [../]
  [./mTE_cp_zz]
    type     = ElementAverageValue
    variable = strain_zz
    block = '{grain_ids}'
  [../]

  # Average strain of grips
  [./mTE_vp_xx]
    type     = ElementAverageValue
    variable = strain_xx
    block    = '{grip_ids}'
  [../]
  [./mTE_vp_yy]
    type     = ElementAverageValue
    variable = strain_yy
    block    = '{grip_ids}'
  [../]
  [./mTE_vp_zz]
    type     = ElementAverageValue
    variable = strain_zz
    block    = '{grip_ids}'
  [../]

  # Average mechanical strain of blocks
  [./mME_cpvp_xx]
    type     = ElementAverageValue
    variable = mechanical_strain_xx
  [../]
  [./mME_cpvp_yy]
    type     = ElementAverageValue
    variable = mechanical_strain_yy
  [../]
  [./mME_cpvp_zz]
    type     = ElementAverageValue
    variable = mechanical_strain_zz
  [../]

  # Average mechanical strain of grains
  [./mME_cp_xx]
    type     = ElementAverageValue
    variable = mechanical_strain_xx
    block    = '{grain_ids}'
  [../]
  [./mME_cp_yy]
    type     = ElementAverageValue
    variable = mechanical_strain_yy
    block    = '{grain_ids}'
  [../]
  [./mME_cp_zz]
    type     = ElementAverageValue
    variable = mechanical_strain_zz
    block    = '{grain_ids}'
  [../]

  # Average mechanical strain of grips
  [./mME_vp_xx]
    type     = ElementAverageValue
    variable = mechanical_strain_xx
    block    = '{grip_ids}'
  [../]
  [./mME_vp_yy]
    type     = ElementAverageValue
    variable = mechanical_strain_yy
    block    = '{grip_ids}'
  [../]
  [./mME_vp_zz]
    type     = ElementAverageValue
    variable = mechanical_strain_zz
    block    = '{grip_ids}'
  [../]

  # Average elastic strain of blocks
  [./mEE_cpvp_xx]
    type     = ElementAverageValue
    variable = elastic_strain_xx
  [../]
  [./mEE_cpvp_yy]
    type     = ElementAverageValue
    variable = elastic_strain_yy
  [../]
  [./mEE_cpvp_zz]
    type     = ElementAverageValue
    variable = elastic_strain_zz
  [../]

  # Average elastic strain of grains
  [./mEE_cp_xx]
    type     = ElementAverageValue
    variable = elastic_strain_xx
    block    = '{grain_ids}'
  [../]
  [./mEE_cp_yy]
    type     = ElementAverageValue
    variable = elastic_strain_yy
    block    = '{grain_ids}'
  [../]
  [./mEE_cp_zz]
    type     = ElementAverageValue
    variable = elastic_strain_zz
    block    = '{grain_ids}'
  [../]

  # Average elastic strain of grips
  [./mEE_vp_xx]
    type     = ElementAverageValue
    variable = elastic_strain_xx
    block    = '{grip_ids}'
  [../]
  [./mEE_vp_yy]
    type     = ElementAverageValue
    variable = elastic_strain_yy
    block    = '{grip_ids}'
  [../]
  [./mEE_vp_zz]
    type     = ElementAverageValue
    variable = elastic_strain_zz
    block    = '{grip_ids}'
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
  l_tol                    = 1e-4 #1e-6
  nl_max_its               = 16
  nl_rel_tol               = 1e-6
  nl_abs_tol               = 1e-6
  nl_forced_its            = 1
  n_max_nonlinear_pingpong = 1
  line_search              = 'none'

  # Time variables
  start_time = {start_time}
  end_time   = {end_time}
  dtmin      = {dt_min}
  dtmax      = {dt_max}

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
    linear_iteration_ratio = 1000
    optimal_iterations     = 8
    iteration_window       = 1
    dt                     = {dt_start}
  [../]
[]

# ==================================================
# Define Simulation Output
# ==================================================

[Outputs]
  # perf_graph = true
  # checkpoint = true
  print_linear_residuals = false
  [./exodus]
    type        = Exodus
    file_base   = '{csv_file}'
    interval    = 1
    execute_on  = 'initial timestep_end'
    sync_only   = true
    sync_times  = '{times}'
    elemental_as_nodal = true
  [../]
  [./console]
    type        = Console
    show        = 'dt mME_cp_xx mME_vp_xx mME_cpvp_xx mCS_cp_xx mCS_vp_xx mCS_cpvp_xx'
    max_rows    = 5
    # output_linear = true
    output_linear = false
    print_mesh_changed_info = true
  [../]
  [./outfile]
    type        = CSV
    file_base   = '{csv_file}'
    time_data   = true
    delimiter   = ','
    execute_on  = 'initial timestep_end'
    sync_only   = true
    sync_times  = '{times}'
  [../]
[]
"""

# CP Model Class
class Simulation(__Simulation__):
    
    def get_simulation(self, time_intervals:list, end_strain:float) -> str:
        """
        Gets the content for the simulation file;
        must be overridden

        Parameters:
        * `time_intervals`: The time intervals to save the results
        * `end_strain`:     The final strain
        """

        # Get orientation data
        orientation_file = self.get_orientation_file()
        orientation_info = np.loadtxt(self.get_input(orientation_file), delimiter=",")
        orientation_info = transpose(orientation_info)
        block_ids = list(set([int(block_id) for block_id in orientation_info[4]]))
        grain_ids = block_ids[:-2]
        grip_ids = block_ids[-2:]
        
        # Define simulation file
        simulation_content = SIMULATION_FORMAT.format(

            # File names
            mesh_file        = self.get_mesh_file(),
            orientation_file = orientation_file,
            material_file    = self.get_material_file(),
            material_name    = self.get_material_name(),
            csv_file         = self.get_csv_file(),
            
            # Block IDs
            block_ids = " ".join([str(id) for id in block_ids]),
            grain_ids = " ".join([str(id) for id in grain_ids]),
            grip_ids  = " ".join([str(id) for id in grip_ids]),

            # Temporal parameters
            start_time = time_intervals[0],
            end_time   = time_intervals[-1],
            dt_start   = 1e-4,
            dt_min     = 1e-8,
            dt_max     = time_intervals[-1]//10,
            times      = " ".join([str(ti) for ti in time_intervals]),

            # Other parameters
            end_strain = end_strain,
        )
        return simulation_content
