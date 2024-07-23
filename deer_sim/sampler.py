"""
 Title:         Sampler
 Description:   Auxiliary functions for running multiple simulations;
                Not attached to the Interface class
 Author:        Janzen Choi

"""

# Libraries
import itertools

def get_combinations(params_dict:dict) -> list:
    """
    Returns a list of possible combinations of a set of parameters
    
    Parameters:
    * `params_dict`: Dictionary of parameter lists

    Returns the list of parameter combinations
    """
    param_list = list(params_dict.values())
    combinations = list(itertools.product(*param_list))
    combinations = [list(c) for c in combinations]
    return combinations
