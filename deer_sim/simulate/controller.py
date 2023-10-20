"""
 Title:         Controller
 Description:   Controller for the Deer Simulator
 Author:        Janzen Choi

"""

# Libraries
import csv, os, subprocess, shutil
from deer_sim.materials.__material__ import get_material
from deer_sim.simulations.__simulation__ import get_simulation

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
        self.get_input = get_input
        self.get_output = get_output

        # Define fixed paths
        self.material_file   = "material.xml"
        self.simulation_file = "simulation.i"
        self.material_path   = get_output(self.material_file)
        self.simulation_path = get_output(self.simulation_file)

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
        material_content = get_material(material_name, material_params, **kwargs)
        self.material_name = material_name
        with open(self.material_path, "w+") as fh:
            fh.write(material_content)

    def define_simulation(self, simulation_name:str, simulation_params:dict, **kwargs) -> None:
        """
        Defines the simulation

        Parameters:
        * `simulation_name`:   The name of the simulation
        * `simulation_params`: Dictionary of parameter values
        """
        simulation_content = get_simulation(simulation_name, simulation_params, self.mesh_file,
                                            self.num_grains, self.orientation_file, self.material_file,
                                            self.material_name, **kwargs)
        with open(self.simulation_path, "w+") as fh:
            fh.write(simulation_content)

    def run_simulation(self, deer_path:str, num_processors:int, output_path:str) -> None:
        """
        Runs the simulation

        Parameters:
        * `deer_path`:      Path to the deer executable
        * `num_processors`: The number of processors
        * `output_path`:    Path to the output directory
        """
        os.chdir("{}/{}".format(os.getcwd(), output_path))
        command = f"mpiexec -np {num_processors} {deer_path} -i {self.simulation_file}"
        subprocess.run([command], shell = True, check = True)
