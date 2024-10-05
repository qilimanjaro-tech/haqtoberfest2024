# Define the vector that contains the pauli opeations
import pandas as pd
import qibo
from ansatz import build_hardware_efficient_ansatz
from model_params import LAMBDA_1, LAMBDA_2, LAMBDA_3, NLAYERS, NSHOTS, NUM_ASSETS, SIGMA_TARGET, TWO_QUBIT_GATES, K, N
from utils import string_to_int_list

# All this functions should help you build the cost function of the problem, which is the expected value of the Hamiltonian defined in (7).

def A(i: int, bit_string: list[int]) -> float:
    """Building block of the hamiltonian. Note that we need to perform the change of variable x = (1-z)/2 where z are the eigenvalues of sigma_z. If we apply this change then this function depends on a bitstring, which is the outcome of quantum measurement. Make sure you undertand this point :)

    Args:
        i (int): index of the asset to which it applies              
        bit_string (list[int]): bit string that encodes a portfolio

    Returns:
        float: 
    """
    return 

# Return term

def return_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    """Corresponds to the first term of the expected value of the Hamiltonian in (7).

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """

    return 


# Volatility term

def tilde_sigma(i: int,j: int, dataset: pd.DataFrame) -> float:
    """Utility function for building the risk term of the hamiltonian. You can use pd.DataFrame.cov() to calculate the covariance matrix

    Args:
        i (int): rows
        j (int): columns
        dataset (pd.DataFrame): daily log returns

    Returns:
        float: 
    """
    return
        

def risk_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    """Corresponds to the second term of the expected value of the Hamiltonian in (7).

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """

    return 

def normalization_cost_function(bit_string: list[int]) -> float:
    """Corresponds to the third term of the expected value of the Hamiltonian in (7).

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """

    return 


def compute_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    """Aggregates all the terms of the cost function.

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """
    
    return 


### energy


def compute_return_energy(result: qibo.result.CircuitResult, dataset: pd.DataFrame, nshots: int = NSHOTS) -> float: 
    """Calls the return cost functions and weights to contribution of every bistring to the energy of the first term of the hamiltonian in (7). 

    Args:
        result (qibo.result.CircuitResult): Result from measuring a qibo circuit. 
        dataset (pd.DataFrame): data
        nshots (int, optional): number of measurement of the ansatz. Defaults to NSHOTS.

    Returns:
        float: energy
    """
    return 

def compute_risk_energy(result: qibo.result.CircuitResult, dataset: pd.DataFrame, nshots: int = NSHOTS) -> float: 
    """Calls the risk cost functions and weights to contribution of every bistring to the energy of the second term of the hamiltonian in (7). 

    Args:
        result (qibo.result.CircuitResult): Result from measuring a qibo circuit. 
        dataset (pd.DataFrame): data
        nshots (int, optional): number of measurement of the ansatz. Defaults to NSHOTS.

    Returns:
        float: energy
    """

    return
def compute_normalization_energy(result: qibo.result.CircuitResult, nshots: int = NSHOTS) -> float: 
    """Calls the normalization cost functions and weights to contribution of every bistring to the energy of the third term of the hamiltonian in (7). 

    Args:
        result (qibo.result.CircuitResult): Result from measuring a qibo circuit. 
        dataset (pd.DataFrame): data
        nshots (int, optional): number of measurement of the ansatz. Defaults to NSHOTS.

    Returns:
        float: energy
    """
    return 
    
def compute_total_energy(parameters: list[float], circuit, dataset: pd.DataFrame, nshots = NSHOTS, num_qubits = N) -> float:
    """Aggregates the the energies of all the terms. This is the loss function and the parametrs are the ones optimized. First, use Circuit.set_parameters(parameters) to load the new set of parameters to the ansatz at every iteration of the optimization process. Second, measure the circuit and forward to result to energy functions. 

    Args:
        parameters (list[float]): _description_
        circuit (_type_): _description_
        dataset (pd.DataFrame): _description_
        nshots (_type_, optional): _description_. Defaults to NSHOTS.
        num_qubits (_type_, optional): _description_. Defaults to N.

    Returns:
        float: _description_
    """
    
    return 