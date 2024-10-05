from unittest.mock import patch

import pytest
from qibo import Circuit
from qibo.gates import gates

from cost_function import compute_normalization_energy


@pytest.fixture
def circuit():
    c = Circuit(3)
    c.add(gates.RX(0, theta=0))
    c.add(gates.RY(1, theta=0))
    c.add(gates.CZ(1, 2))
    c.add(gates.fSim(0, 2, theta=0, phi=0))
    c.add(gates.H(2))
    c.add(gates.M(0))
    c.add(gates.M(1))
    c.add(gates.M(2))

    yield c


@pytest.fixture
def circuit_result(circuit):
    result = circuit.execute(nshots=2)

    yield result


@patch('model_params.K', 1)
@patch('model_params.NUM_ASSETS', 3)
def test_c_circuit(circuit_result):
    e = compute_normalization_energy(circuit_result)

    assert e >= 0

