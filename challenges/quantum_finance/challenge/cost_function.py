# Define the vector that contains the pauli opeations
import numpy as np
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

    v = 1 / np.power(2, range(1, K + 1))
    x = np.array(bit_string[i * K:(i + 1) * K])

    return np.dot(v, x)


# Return term

def return_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    """Corresponds to the first term of the expected value of the Hamiltonian in (7).

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """

    vA = np.array([A(i, bit_string) for i in range(0, NUM_ASSETS)])
    return np.dot(dataset, vA).mean()


# Volatility term

def tilde_sigma(i: int, j: int, dataset: pd.DataFrame) -> float:
    """Utility function for building the risk term of the hamiltonian. You can use pd.DataFrame.cov() to calculate the covariance matrix

    Args:
        i (int): rows
        j (int): columns
        dataset (pd.DataFrame): daily log returns

    Returns:
        float: 
    """
    cov = dataset.cov()

    if i == j:
        return cov.iloc[i, i]
    elif i < j:
        return 2 * cov.iloc[i, j]
    else:
        return 0


def risk_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    """Corresponds to the second term of the expected value of the Hamiltonian in (7).

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """

    vA = np.array([A(i, bit_string) for i in range(0, NUM_ASSETS)])

    t_sigma = np.array(
        [
            [
                tilde_sigma(i, j, dataset)
                for i in range(0, NUM_ASSETS)
            ]
            for j in range(0, NUM_ASSETS)
        ]
    )

    return np.dot(vA, np.dot(t_sigma, vA)) - SIGMA_TARGET ** 2


def normalization_cost_function(bit_string: list[int]) -> float:
    """Corresponds to the third term of the expected value of the Hamiltonian in (7).

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """

    return np.power(sum(A(i, bit_string) for i in range(0, NUM_ASSETS)) - 1, 2)


def compute_cost_function(dataset: pd.DataFrame, bit_string: list[int]) -> float:
    """Aggregates all the terms of the cost function.

    Args:
        dataset (pd.DataFrame): _description_
        bit_string (list[int]): _description_

    Returns:
        float: _description_
    """

    return - LAMBDA_1 * return_cost_function(dataset, bit_string) \
        + LAMBDA_2 * risk_cost_function(dataset, bit_string) \
        + LAMBDA_3 * normalization_cost_function(bit_string)


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

    freq = result.frequencies(binary=True)

    energy = np.sum([
        val * return_cost_function(dataset, [int(bit) for bit in k])
        for k, val in freq.items()
    ])

    return energy


def compute_risk_energy(result: qibo.result.CircuitResult, dataset: pd.DataFrame, nshots: int = NSHOTS) -> float:
    """Calls the risk cost functions and weights to contribution of every bistring to the energy of the second term of the hamiltonian in (7). 

    Args:
        result (qibo.result.CircuitResult): Result from measuring a qibo circuit. 
        dataset (pd.DataFrame): data
        nshots (int, optional): number of measurement of the ansatz. Defaults to NSHOTS.

    Returns:
        float: energy
    """


    freq = result.frequencies(binary=True)

    energy = np.sum([
        val * risk_cost_function(dataset, [int(bit) for bit in k])
        for k, val in freq.items()
    ])

    return energy

def compute_normalization_energy(result: qibo.result.CircuitResult, nshots: int = NSHOTS) -> float:
    """Calls the normalization cost functions and weights to contribution of every bistring to the energy of the third term of the hamiltonian in (7). 

    Args:
        result (qibo.result.CircuitResult): Result from measuring a qibo circuit. 
        dataset (pd.DataFrame): data
        nshots (int, optional): number of measurement of the ansatz. Defaults to NSHOTS.

    Returns:
        float: energy
    """

    freq = result.frequencies(binary=True)

    energy = np.sum([
        val * normalization_cost_function([int(bit) for bit in k])
        for k, val in freq.items()
    ])

    return energy

def compute_total_energy(parameters: list[float], circuit: qibo.Circuit, dataset: pd.DataFrame, nshots=NSHOTS, num_qubits=N) -> float:
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

    result = circuit.execute(nshots=nshots)

    return - LAMBDA_1 * compute_return_energy(result, dataset) \
        + LAMBDA_2 * compute_risk_energy(result, dataset) \
        + LAMBDA_3 * compute_normalization_energy(result)
