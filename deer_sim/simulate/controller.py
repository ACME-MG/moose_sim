"""
 Title:         Controller
 Description:   Controller for the Deer Simulator
 Author:        Janzen Choi

"""

# Libraries
import csv, os, subprocess, shutil
from deer_sim.materials.__material__ import get_material
from deer_sim.simulations.__simulation__ import get_simulation
from deer_sim.simulate.analyser import plot_creep

# The Controller class
class Controller():

    def __init__(self, get_input, get_output):
        """
        Class to control all the components of the simulation

        Parameters:
        * `get_input`:  Function to get the path to the input files
        * `get_output`: Function to get the path to the output files
        """

        # Initialise internal variables
        self.get_input         = get_input
        self.get_output        = get_output
        self.material_name     = ""
        self.simulation_name   = ""
        self.material_params   = {}
        self.simulation_params = {}

        # Initialise file names
        self.material_file   = "material.xml"
        self.simulation_file = "simulation.i"
        self.csv_file        = "results"
        self.analysis_file   = "analysis_plot"

        # Initialise file paths
        self.material_path   = get_output(self.material_file)
        self.simulation_path = get_output(self.simulation_file)
        self.csv_path        = get_output(f"{self.csv_file}.csv")
        self.analysis_path   = get_output(self.analysis_file)

    def define_mesh(self, mesh_file:str, orientation_file:str):
        """
        Defining the mesh
        
        Parameters:
        * `mesh_file`:        The name of the mesh file
        * `orientation_file`: The name of the orientation file
        """

        # Get paths to input files
        self.mesh_file = mesh_file
        self.orientation_file = orientation_file
        mesh_path = self.get_input(mesh_file)
        orientation_path = self.get_input(orientation_file)
        
        # Check if files exist
        if not os.path.exists(mesh_path):
            raise FileNotFoundError(f"No mesh file exists at '{mesh_path}'!")
        if not os.path.exists(orientation_path):
            raise FileNotFoundError(f"No orientation file exists at '{mesh_path}'!")
        
        # Calculate number of grains
        with open(orientation_path, "r", newline="") as file:
             self.num_grains = len([row for row in csv.reader(file, delimiter=" ")])
        
        # Copy the mesh and orientation files to the results folder
        shutil.copy(mesh_path, self.get_output(mesh_file))
        shutil.copy(orientation_path, self.get_output(orientation_file))

    def define_material(self, material_name:str, material_params:dict, **kwargs) -> None:
        """
        Defines the material
        
        Parameters:
        * `material_name`:   The name of the material
        * `material_params`: Dictionary of parameter values
        """

        # Save material information
        self.material_name = material_name
        self.material_params = material_params

        # Write the material file
        material_content = get_material(material_name, material_params, **kwargs)
        with open(self.material_path, "w+") as fh:
            fh.write(material_content)

    def define_simulation(self, simulation_name:str, simulation_params:dict, stress:float, **kwargs) -> None:
        """
        Defines the simulation

        Parameters:
        * `simulation_name`:   The name of the simulation
        * `simulation_params`: Dictionary of parameter values
        * `stress`:            The stress to apply in the simulation
        """

        # Save simulation information
        self.simulation_name = simulation_name
        self.simulation_params = simulation_params

        # Write the simulation file
        simulation_content = get_simulation(simulation_name, simulation_params, self.mesh_file,
                                            self.num_grains, self.orientation_file, self.material_file,
                                            self.material_name, self.csv_file, stress, **kwargs)
        with open(self.simulation_path, "w+") as fh:
            fh.write(simulation_content)

    def run_simulation(self, deer_path:str, num_processors:int, output_path:str, timeout:float) -> None:
        """
        Runs the simulation

        Parameters:
        * `deer_path`:      Path to the deer executable
        * `num_processors`: The number of processors
        * `output_path`:    Path to the output directory
        * `timeout`:        The maximum amount of time (in seconds) to run the simulation
        """

        # Check that the material and simulation are both defined
        if self.material_name == "":
            raise NotImplementedError("The material name has not been defined!")
        if self.simulation_name == "":
            raise NotImplementedError("The simulation name has not been defined!")

        # Run the simulation
        current_dir = os.getcwd()
        os.chdir("{}/{}".format(os.getcwd(), output_path))
        command = f"timeout {timeout}s mpiexec -np {num_processors} {deer_path} -i {self.simulation_file}"
        try:
            subprocess.run([command], shell=True, check=False)
        except:
            pass
        os.chdir(current_dir)

    def remove_artifacts(self) -> None:
        """
        Removes auxiliary files after the simulation ends
        """
        print(os.getcwd())
        os.remove(self.get_output(self.mesh_file))
        os.remove(self.get_output(self.orientation_file))

    def analyse_results(self, csv_file:str="", direction:str="x") -> None:
        """
        Analyses the results of the simulation

        Parameters:
        * `csv_file`:  The results file; if unspecified, gets the results from a
                       simulation that was just run
        * `direction`: The direction the plot uses to plot the results
        """
        
        # If filename specified, then check if it exists
        if csv_file != "" and not os.path.exists(self.get_input(csv_file)):
            raise FileNotFoundError(f"The '{csv_file}' file could not be found!")

        # If filename not specified, check if there was a simulation that just ran
        if csv_file == "" and not os.path.exists(self.csv_path):
            raise FileNotFoundError("The file has not been specified and no simulation has been run!")

        # Get path to CSV and conduct analysis
        csv_path = self.csv_path if csv_file == "" else self.get_input(csv_file)
        plot_creep(csv_path, self.analysis_path, direction)

    def export_params(self, params_file:str) -> None:
        """
        Exports the parameters

        Parameters:
        * `params_file`: The name of the parameter file
        """
        
        # Prepare path and content
        params_path = self.get_output(params_file)
        params_dict = {**self.material_params, **self.simulation_params}

        # Write parameters to file
        with open(params_path, "w+") as fh:
            for param_name in params_dict.keys():
                fh.write(f"{param_name}: {params_dict[param_name]}\n")
