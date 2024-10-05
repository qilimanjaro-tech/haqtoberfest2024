
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

    c.add((gates.U2(q, 0, 0) for q in range(num_qubits))) #First column of U2
    c.add((gates.U2(q, 0, 0) for q in range(num_qubits))) #Second column of U2
    c.add((gates.CNOT(q, q+1) for q in range(num_qubits-1))) #First CNOT Mesh

    c.add((gates.U1(q, 0) for q in range(num_qubits))) #First column of U1
    c.add((gates.U2(q, 0, 0) for q in range(num_qubits))) #Third column of U2
    c.add((gates.CNOT(q, q+1) for q in range(num_qubits-1))) #Second CNOT Mesh

    c.add((gates.U1(q, 0) for q in range(num_qubits))) #Second column of U1
    c.add((gates.U2(q, 0, 0) for q in range(num_qubits))) #Fourth column of U2
    c.add((gates.CNOT(q, q+1) for q in range(num_qubits-1))) #Third CNOT Mesh

    c.add((gates.U1(q, 0) for q in range(num_qubits))) #Third column of U1
    
    return c

def compute_number_of_params_hwea(num_qubits: int, num_layers: int) -> int:
    """Calculates the number of parameters (angles of rotation of the qubits) of the Hardware efficient ansatz (FIG 2) depending on the number of qubits and layers.
    """
    return 