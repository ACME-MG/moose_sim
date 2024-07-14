"""
 Title:         Simulation Interface
 Description:   Interface for running deer simulations
 Author:        Janzen Choi

"""

# Libraries
import inspect, os, re, time
from deer_sim.controller import Controller

# Interface Class
class Interface:

    def __init__(self, title:str="", input_path:str="./data", output_path:str="./results",
                 verbose:bool=True, output_here:bool=False):
        """
        Class to interact with the optimisation code
        
        Parameters:
        * `title`:       Title of the output folder
        * `input_path`:  Path to the input folder
        * `output_path`: Path to the output folder
        * `verbose`:     If true, outputs messages for each function call
        * `output_here`: If true, just dumps the output in ths executing directory
        """
        
        # Initialise internal variables
        self.__print_index__ = 0
        self.__verbose__     = verbose
        
        # Starting code
        time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        self.__print__(f"\n  Starting on {time_str}\n", add_index=False)
        self.__start_time__ = time.time()
        time_stamp = time.strftime("%y%m%d%H%M%S", time.localtime(self.__start_time__))
        
        # Define input and output
        self.__input_path__ = input_path
        file_path = inspect.currentframe().f_back.f_code.co_filename
        file_name = file_path.split("/")[-1].replace(".py","")
        title = f"_{file_name}" if title == "" else f"_{title}"
        title = re.sub(r"[^a-zA-Z0-9_]", "", title.replace(" ", "_"))
        self.__output_dir__ = "." if output_here else time_stamp
        self.__output_path__ = "." if output_here else f"{output_path}/{self.__output_dir__}{title}"
        
        # Define input / output functions
        self.__get_input__  = lambda x : f"{self.__input_path__}/{x}"
        self.__get_output__ = lambda x : f"{self.__output_path__}/{x}"
        self.__controller__ = Controller(self.__get_input__, self.__get_output__)
        
        # Create directories
        if not output_here:
            safe_mkdir(output_path)
            safe_mkdir(self.__output_path__)
    
    def define_mesh(self, mesh_file:str, orientation_file:str, degrees:bool=True, active:bool=True) -> None:
        """
        Defining the mesh
        
        Parameters:
        * `mesh_file`:        The name of the mesh file
        * `orientation_file`: The name of the orientation file
        * `degrees`:          Whether the orientation data is in degrees (or radians)
        * `active`:           Whether the orientation data is active (or passive)
        """
        type_str = "deg" if degrees else "rad"
        self.__print__(f"Defining the mesh at '{mesh_file}' with orientations ({type_str}) at '{orientation_file}'")
        self.__controller__.define_mesh(mesh_file, orientation_file, degrees, active)
        
    def define_material(self, material_name:str, material_params:dict, **kwargs) -> None:
        """
        Defines the material

        Parameters:
        * `material_name`:   The name of the material
        * `material_params`: Dictionary of parameter values
        """
        self.__print__(f"Defining the material ({material_name})")
        self.__controller__.define_material(material_name, material_params, **kwargs)
    
    def define_simulation(self, simulation_name:str, simulation_params:dict={}, **kwargs) -> None:
        """
        Defines the simulation

        Parameters:
        * `simulation_name`:   The name of the simulation
        * `simulation_params`: Dictionary of parameter values
        * `stress`:            The stress to apply in the simulation
        """
        self.__print__(f"Defining the simulation ({simulation_name})")
        self.__controller__.define_simulation(simulation_name, simulation_params, **kwargs)

    def simulate(self, deer_path:str, num_processors:int, timeout:float=1e10) -> None:
        """
        Runs the simulation

        Parameters:
        * `deer_path`:      Path to the deer executable
        * `num_processors`: The number of processors
        * `timeout`:        The maximum amount of time (in seconds) to run the simulation
        """
        self.__print__("Running the simulation")
        self.__controller__.run_simulation(deer_path, num_processors, self.__output_path__, timeout)

    def export_params(self, params_file:str="params.txt") -> None:
        """
        Exports the parameters

        Parameters:
        * `params_file`: The name of the parameter file
        """
        self.__print__("Exporting the parameters")
        self.__controller__.export_params(params_file)

    def remove_artifacts(self) -> None:
        """
        Removes auxiliary files after the simulation ends
        """
        self.__print__("Removing auxiliary files")
        self.__controller__.remove_artifacts()

    def __print__(self, message:str, add_index:bool=True) -> None:
        """
        Displays a message before running the command (for internal use only)
        
        Parameters:
        * `message`:   the message to be displayed
        * `add_index`: if true, adds a number at the start of the message
        """
        if not add_index:
            print(message)
        if not self.__verbose__ or not add_index:
            return
        self.__print_index__ += 1
        print(f"   {self.__print_index__})\t{message} ...")
    
    def __del__(self):
        """
        Prints out the final message (for internal use only)
        """
        time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        duration = round(time.time() - self.__start_time__)
        duration_h = duration // 3600
        duration_m = (duration - duration_h * 3600) // 60
        duration_s = duration - duration_h * 3600 - duration_m * 60
        duration_str_list = [
            f"{duration_h} hours" if duration_h > 0 else "",
            f"{duration_m} mins" if duration_m > 0 else "",
            f"{duration_s} seconds" if duration_s > 0 else ""
        ]
        duration_str = ", ".join([d for d in duration_str_list if d != ""])
        duration_str = f"in {duration_str}" if duration_str != "" else ""
        self.__print__(f"\n  Finished on {time_str} {duration_str}\n", add_index=False)

def safe_mkdir(dir_path:str) -> None:
    """
    For safely making a directory

    Parameters:
    * `dir_path`: The path to the directory
    """
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
