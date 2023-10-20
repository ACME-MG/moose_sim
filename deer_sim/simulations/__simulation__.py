"""
 Title:         Simulation
 Description:   For creating simulation files
 Author:        Janzen Choi

"""

# Libraries
import importlib, os, pathlib, sys

# Simulation Class
class __Simulation__:

    def __init__(self, name:str, params:dict):
        """
        Template class for simulation objects
        
        Parameters:
        * `name`:   The name of the simulation
        * `params`: The parameter values
        """
        self.name   = name
        self.params = params

    def get_name(self) -> str:
        """
        Gets the name of the simulation
        """
        return self.name
    
    def get_param(self, param_name:str) -> float:
        """
        Gets a parameter value
        """
        if not param_name in self.params.keys():
            raise ValueError(f"The '{param_name}' parameter has not been initialised!")
        return self.params[param_name]
    
    def set_mesh_file(self, mesh_file) -> None:
        """
        Sets the name of the mesh file

        Parameters:
        * `mesh_file`: The path to the mesh file
        """
        self.mesh_file = mesh_file

    def get_mesh_file(self) -> str:
        """
        Gets the name of the mesh file
        """
        return self.mesh_file
    
    def set_num_grains(self, num_grains) -> None:
        """
        Sets the number of grains

        Parameters:
        * `num_grains`: The number of grains
        """
        self.num_grains = num_grains

    def get_num_grains(self) -> int:
        """
        Gets the path to the mesh file
        """
        return self.num_grains
    
    def set_orientation_file(self, orientation_file) -> None:
        """
        Sets the name of the orientation file

        Parameters:
        * `orientation_file`: The path to the orientation file
        """
        self.orientation_file = orientation_file

    def get_orientation_file(self) -> str:
        """
        Gets the name of the orientation file
        """
        return self.orientation_file

    def set_material_file(self, material_file) -> None:
        """
        Sets the material file

        Parameters:
        * `material_file`: The material file
        """
        self.material_file = material_file

    def get_material_file(self) -> str:
        """
        Gets the material file
        """
        return self.material_file

    def set_material_name(self, material_name) -> None:
        """
        Sets the material name

        Parameters:
        * `material_name`: The material name
        """
        self.material_name = material_name

    def get_material_name(self) -> str:
        """
        Gets the material name
        """
        return self.material_name

    def get_simulation(self, **kwargs) -> str:
        """
        Gets the content for the simulation file;
        must be overridden
        """
        raise NotImplementedError

def get_simulation(simulation_name:str, params:dict, mesh_file:str, num_grains:int,
                   orientation_file:str, material_file:str, material_name:str, **kwargs) -> str:
    """
    Gets the simulation file's content
    
    Parameters:
    * `simulation_name`:  The name of the simulation
    * `params`:           The parameter values
    * `mesh_file`:        The name of the mesh file
    * `num_grains`:       The nummber of grains in the mesh
    * `orientation_file`: The name of the orientation file
    * `material_file`:    The name of the material file
    * `material_name`:    The name of the material
    """

    # Get available simulations in current folder
    simulations_dir = pathlib.Path(__file__).parent.resolve()
    files = os.listdir(simulations_dir)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in ["__simulation__", "__pycache__"]]
    
    # Raise error if simulation name not in available simulations
    if not simulation_name in files:
        raise NotImplementedError(f"The simulation '{simulation_name}' has not been implemented")

    # Import and prepare simulation
    module_file = f"{simulations_dir}/{simulation_name}.py"
    spec = importlib.util.spec_from_file_location("simulation_file", module_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    
    # Initialise and return the simulation
    from simulation_file import Simulation
    simulation = Simulation(simulation_name, params)
    simulation.set_mesh_file(mesh_file)
    simulation.set_num_grains(num_grains)
    simulation.set_orientation_file(orientation_file)
    simulation.set_material_file(material_file)
    simulation.set_material_name(material_name)
    simulation_content = simulation.get_simulation(**kwargs)
    return simulation_content
