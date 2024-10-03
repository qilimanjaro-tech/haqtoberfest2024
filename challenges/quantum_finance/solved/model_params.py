K = 1 # number of qubits assigned per asset 

NUM_ASSETS = 5# number of assets
N = NUM_ASSETS*K # number of total qubits
NLAYERS = 2 # number of layers of the ansatz
NSHOTS = 10 # when measuring the ansatz

LAMBDA_1 = 1.0 # return penalty coefficient
LAMBDA_2 = 1.0 # risk penalty coefficient
LAMBDA_3 = 10.0 # normalization penalty coefficient
SIGMA_TARGET = 0.1 # target volatility

from qibo.gates import CNOT, CZ

TWO_QUBIT_GATES = {"CZ": CZ, "CNOT": CNOT} # tytpes of two-qubit gates
