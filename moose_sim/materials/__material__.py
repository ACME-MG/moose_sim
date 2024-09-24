"""
 Title:         Material
 Description:   For creating material files
 Author:        Janzen Choi

"""

# Libraries
import importlib, os, pathlib, sys

# Material Class
class __Material__:

    def __init__(self, name:str, params:dict):
        """
        Template class for material objects
        
        Parameters:
        * `name`:   The name of the material
        * `params`: The parameter values
        """
        self.name   = name
        self.params = params

    def get_name(self) -> str:
        """
        Gets the name of the material
        """
        return self.name
    
    def get_param(self, param_name:str) -> float:
        """
        Gets a parameter value
        """
        if not param_name in self.params.keys():
            raise ValueError(f"The '{param_name}' parameter has not been initialised!")
        return self.params[param_name]
    
    def get_material(self, **kwargs) -> str:
        """
        Gets the content for the material file;
        must be overridden
        """
        raise NotImplementedError

def get_material(material_name:str, params:dict, **kwargs) -> str:
    """
    Gets the material file's content
    
    Parameters:
    * `material_name`: The name of the material
    * `params`:        The parameter values
    """

    # Get available materials in current folder
    materials_dir = pathlib.Path(__file__).parent.resolve()
    files = os.listdir(materials_dir)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in ["__material__", "__pycache__"]]
    
    # Raise error if material name not in available materials
    if not material_name in files:
        raise NotImplementedError(f"The material '{material_name}' has not been implemented")

    # Import and prepare material
    module_path = f"{materials_dir}/{material_name}.py"
    spec = importlib.util.spec_from_file_location("material_file", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    
    # Initialise and return the material
    from material_file import Material
    material = Material(material_name, params)
    material_content = material.get_material(**kwargs)
    return material_content
