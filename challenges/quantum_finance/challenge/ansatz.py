
from model_params import LAMBDA_1, LAMBDA_2, LAMBDA_3, NLAYERS, NSHOTS, NUM_ASSETS, SIGMA_TARGET, TWO_QUBIT_GATES, K, N
from qibo import gates, models


def build_hardware_efficient_ansatz(num_qubits: int = N, num_layers: int = NLAYERS, two_gate: str = "CNOT") -> models.Circuit:
    """Generates a HWEA with the same structure as in FIG 2. 

    Args:
        num_qubits (int, optional): Is the number of used qubits. Defaults to N.
        num_layers (int, optional): Is the number of layers applied in the circuit. Defaults to NLAYERS.
        two_gate (str, optional): It is the two gate used in the mesh of controled gates at the layers, it can be "CNOT" or "CZ" gates. Defaults to "CNOT".

    Returns:
        models.Circuit: ansatz. Returns the constructed circuit with the desired number of qubits, layers and two-qubit gates.
    """
    def add_layer(): #layer definition
        c.add((gates.U2(q, 0, 0) for q in range(num_qubits))) #Column of U2
        if two_gate == "CNOT": c.add((gates.CNOT(q, q+1) for q in range(num_qubits-1))) #CNOT Mesh
        if two_gate == "CZ": c.add((gates.CZ(q, q+1) for q in range(num_qubits-1))) #CZ Mesh
        c.add((gates.U1(q, 0) for q in range(num_qubits))) #Column of U1

    c = models.Circuit(num_qubits) #Initialize an empty circuit
    c.add((gates.U2(q, 0, 0) for q in range(num_qubits))) #First column of U2
    for _ in range(num_layers): add_layer() #Recursive line to create NLAYERS at the circuit
    c.add((gates.M(q) for q in range(num_qubits))) #Column of qubit Measurement

    return c

def compute_number_of_params_hwea(num_qubits: int, num_layers: int) -> int:
    """Calculates the number of parameters (angles of rotation of the qubits) of the Hardware efficient ansatz (FIG 2) depending on the number of qubits and layers.
    """
    return num_qubits * (2 + 3 * num_layers) 