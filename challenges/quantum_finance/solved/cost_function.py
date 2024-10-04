# Define the vector that contains the pauli opeations
import pandas as pd
import qibo
from ansatz import build_hardware_efficient_ansatz
from model_params import LAMBDA_1, LAMBDA_2, LAMBDA_3, NLAYERS, NSHOTS, NUM_ASSETS, SIGMA_TARGET, TWO_QUBIT_GATES, K, N
from utils import string_to_int_list


def A(i: int, bit_string: list[int]) -> float:
    return sum(2 ** (k - 2) * ((1 - bit_string[k + i*K]) / 2) for k in range(K))

# Return term

def return_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    h1 = 0
    for i, asset in enumerate(dataset.columns):
        h1 += A(i,bit_string) * dataset[asset].values
    return (-1)*sum(h1)


# Volatility term

def tilde_sigma(i: int,j: int, dataset: pd.DataFrame) -> float:
    if i==j: 
        return dataset.cov().values[i][j]
    elif i<j:
        return 2 * dataset.cov().values[i][j]
    else: 
        return 0

def risk_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    h2 = 0
    for i in range(NUM_ASSETS):
        for j in range(NUM_ASSETS):  
            h2 += tilde_sigma(i,j,dataset) * A(i, bit_string) * A(i, bit_string) - SIGMA_TARGET ** 2

    return h2 ** 2

def normalization_cost_function(bit_string: list[int]) -> float:
    h3 = 0
    for i in range(NUM_ASSETS): 
        h3 += A(i, bit_string)
    h3 -= -1
    return h3 ** 2

def compute_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    
    cost_function = LAMBDA_1 * return_cost_function(dataset, bit_string) + LAMBDA_2 * risk_cost_function(dataset, bit_string) + LAMBDA_3 * normalization_cost_function(bit_string)
    
    return cost_function
def compute_return_energy(result: qibo.result.CircuitResult, dataset: pd.DataFrame, nshots: int = NSHOTS) -> float: 
    return_energy = 0
    for bit_string, stat_freq in result.frequencies().items():
        return_energy += (stat_freq / nshots) * return_cost_function(dataset,string_to_int_list(bit_string))
    return return_energy

def compute_risk_energy(result: qibo.result.CircuitResult, dataset: pd.DataFrame, nshots: int = NSHOTS) -> float: 
    risk_energy = 0
    for bit_string, stat_freq in result.frequencies().items():
        risk_energy += (stat_freq / nshots) * risk_cost_function(dataset,string_to_int_list(bit_string))
    return risk_energy

def compute_normalization_energy(result: qibo.result.CircuitResult, nshots: int = NSHOTS) -> float: 
    norm_energy = 0
    for bit_string, stat_freq in result.frequencies().items():
        norm_energy += (stat_freq / nshots) * normalization_cost_function(string_to_int_list(bit_string))
    return norm_energy
    
def compute_total_energy(parameters: list[float], circuit, dataset: pd.DataFrame, nshots = NSHOTS, num_qubits = N) -> float:
    
    # circuit = build_hardware_efficient_ansatz(num_qubits,parameters)
    circuit.set_parameters(parameters)
    # Measure the qubits quantum state
    result = circuit(nshots=nshots) 
    total_energy = LAMBDA_1 * compute_return_energy(result,dataset) + LAMBDA_2 * compute_risk_energy(result,dataset) + LAMBDA_3 * compute_normalization_energy(result)
    print('Energy:', total_energy)
    return total_energy