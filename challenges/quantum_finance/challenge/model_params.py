from qibo.gates import CNOT, CZ

K = 3 # number of qubits assigned per asset

NUM_ASSETS = 5 # number of assets
N = NUM_ASSETS*K # number of total qubits
NLAYERS = 2 # number of layers of the ansatz
NSHOTS = 100 # when measuring the ansatz

LAMBDA_1 = 1.0 # return penalty coefficient
LAMBDA_2 = 1.0 # risk penalty coefficient
LAMBDA_3 = 100.0 # normalization penalty coefficient
SIGMA_TARGET = 0.1 # target volatility

TWO_QUBIT_GATES = {"CZ": CZ, "CNOT": CNOT} # tytpes of two-qubit gates
RISK_FREE_RATE = 0.03 # return that can be acquired in the market without assuming any risk
TOLERANCE = 0.5 # probability threshold to consider a portfolio after the optimization process