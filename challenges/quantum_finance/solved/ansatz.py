
from model_params import LAMBDA_1, LAMBDA_2, LAMBDA_3, NLAYERS, NSHOTS, NUM_ASSETS, SIGMA_TARGET, TWO_QUBIT_GATES, K, N
from qibo import gates, models


def compute_number_of_params(num_qubits: int, num_layers: int) -> int:
    return num_qubits * (2 * num_layers + 2 + num_layers)

def build_hardware_efficient_ansatz(num_qubits: int = N, num_layers: int = NLAYERS, two_gate: str = "CNOT") -> models.Circuit:
    c = models.Circuit(num_qubits)
    c.add([gates.U2(qubit, 0, 0) for qubit in range(num_qubits)])
    for _ in range(num_layers):
        c.add([gates.U2(qubit, 0, 0) for qubit in range(num_qubits)])
        c.add([TWO_QUBIT_GATES[two_gate](qubit, qubit+1)] for qubit in range(0,num_qubits-1))
        c.add([gates.U1(qubit,0) for qubit in range(num_qubits)])
            
    c.add([gates.M(qubit) for qubit in range(num_qubits)])
    return c