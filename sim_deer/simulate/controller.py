"""
 Title:         Controller
 Description:   Controller for the Deer Simulator
 Author:        Janzen Choi

"""

# Libraries
import csv, os

# The Controller class
class Controller():

    def __init__(self):
        """
        Class to control all the components of the simulation
        """
        self.mesh_path        = None
        self.orientation_path = None
        self.num_grains       = None
    
    def define_mesh(self, mesh_path:str, orientation_path:str):
        """
        Defining the mesh
        
        Parameters:
        * `mesh_path`:        The path of the mesh file
        * `orientation_path`: The path of the orientation file
        """
        
        # Check if files exist
        if not os.path.exists(mesh_path):
            raise FileNotFoundError(f"No mesh file exists at '{mesh_path}'!")    
        if not os.path.exists(orientation_path):
            raise FileNotFoundError(f"No orientation file exists at '{mesh_path}'!")    
        
        # Initialise internal variables
        self.mesh_path = mesh_path
        self.orientation_path = orientation_path
        with open(orientation_path, "r", newline="") as file:
             self.num_grains = len([row for row in csv.reader(file, delimiter=" ")])

    def define_material(self, material_name:str, material_params:list):
        """
        Defining information about the material
        
        Parameters:
        * `material_name`:   The name of the material
        * `material_params`: The material parameter values
        """
        
    