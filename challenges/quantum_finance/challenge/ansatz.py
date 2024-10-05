
from model_params import LAMBDA_1, LAMBDA_2, LAMBDA_3, NLAYERS, NSHOTS, NUM_ASSETS, SIGMA_TARGET, TWO_QUBIT_GATES, K, N
from qibo import gates, models


def build_hardware_efficient_ansatz(num_qubits: int = N, num_layers: int = NLAYERS, two_gate: str = "CNOT") -> models.Circuit:
    """Generates a HWEA with the same structure as in FIG 2. 

    Args:
        num_qubits (int, optional): _description_. Defaults to N.
        num_layers (int, optional): _description_. Defaults to NLAYERS.
        two_gate (str, optional): _description_. Defaults to "CNOT".

    Returns:
        models.Circuit: ansatz
    """
    c = models.Circuit(num_qubits)
   
    return c

def compute_number_of_params_hwea(num_qubits: int, num_layers: int) -> int:
    """Calculates the number of parameters (angles of rotation of the qubits) of the Hardware efficient ansatz (FIG 2) depending on the number of qubits and layers.
    """
    return 