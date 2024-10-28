from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from qibo import gates
from qibo.models import Circuit
from qibo.transpiler.pipeline import Passes
from qibo.transpiler.placer import Custom, StarConnectivityPlacer
from qibo.transpiler.router import Sabre, StarConnectivityRouter
from qibo.ui import plot_circuit


def gate_class(gate: gates.Gate) -> str:
    """Get the class name of the gate."""
    return type(gate).__name__


def get_circuit_gates(circuit: Circuit) -> list[dict]:
    """Get the gates of the circuit.

    Args:
        circuit (qibo.models.Circuit): Circuit to get the gates from.

    Returns:
        list[dict]: List of gates in the circuit. Where each gate is a dictionary (keys: 'name', value: 'qubits').
    """
    return [(gate_class(i), i.qubits) for i in circuit.queue]


def create_gate(gate_class: str, qubits: tuple[int]) -> gates.Gate:
    """Converts a tuple representation of qibo gate (name, qubits) into a Gate object.

    Args:
        gate_class (str): The class name of the gate. Can be "CNOT", "X", "H", or any Qibo supported class.
        qubits (tuple [int,] | tuple[int, int]): The qubits the gate acts on.

    Returns:
        gates.Gate: The qibo Gate object.
    """
    return getattr(gates, gate_class)(*qubits)


def find_final_reordering(circuit, layout):
    """Get the final reordering of the qubits in the circuit, adding the layout and the SWAP gates.

    Args:
        circuit (qibo.models.Circuit): Circuit to extract the SWAPS from.
        layout (dict): Initial layout used for the circuit.

    Returns:
        dict: Final order of the qubits.
    """
    reordering_dict = deepcopy(layout)
    for gate, qubits in get_circuit_gates(circuit):
        if gate == "SWAP":
            update_reordering(qubits, reordering_dict)
    return reordering_dict


def update_reordering(pair_to_change: tuple, layout):
    """Get a new reordering of the qubits, given a change in two qubits.

    Args:
        reordering (tuple[int, int]): Pair of qubits to swap in the given layout.
        layout (dict): Initial layout used for the circuit.

    Returns:
        dict: Final order of the qubits.
    """
    reordering_dict = deepcopy(layout)

    key_1 = pair_to_change[0]
    key_2 = pair_to_change[1]

    value1 = deepcopy(reordering_dict[f"q{key_1}"])
    value2 = deepcopy(reordering_dict[f"q{key_2}"])

    reordering_dict[f"q{key_1}"] = value2
    reordering_dict[f"q{key_2}"] = value1

    return reordering_dict


# Define connectivity as nx.Graph
def star_connectivity():
    """Generates star connectivity graph with networkx."""
    Q = list(range(5))
    chip = nx.Graph()
    chip.add_nodes_from(Q)
    graph_list = [(Q[i], Q[2]) for i in range(5) if i != 2]
    chip.add_edges_from(graph_list)
    return chip


def transpile_to_star_connectivity(
    circuit,
    initial_map=None,
    sabre=False,
):
    """Transpile the circuit with star connectivity.

    Args:
        circuit (qibo.models.Circuit): Circuit to transpile.
        initial_mapping (dict, optional): Initial layout to use.
        sabre (bool, optional): Use Sabre router, instead of star.

    Returns:
        qibo.models.Circuit: Transpiled circuit.
        dict: Final layout (initial_mapping) used.
    """
    # Layout and Routing passes
    custom_passes = []
    if initial_map:
        custom_passes.append(Custom(initial_map=initial_map, connectivity=star_connectivity()))
    else:
        custom_passes.append(StarConnectivityPlacer(middle_qubit=2))

    if sabre:
        custom_passes.append(Sabre(connectivity=star_connectivity()))
    else:
        custom_passes.append(StarConnectivityRouter(middle_qubit=2))

    # Define the general pipeline
    custom_pipeline = Passes(
        custom_passes,
        connectivity=star_connectivity(),
    )
    transpiled_circuit, final_layout = custom_pipeline(circuit)

    # Call the transpiler pipeline on the circuit
    return transpiled_circuit, final_layout


def plot_transpiled_circuit(circuit, final_layout):
    """Plot the transpiled circuit with the final layout.

    Args:
        circuit (qibo.models.Circuit): Transpiled circuit.
        final_layout (dict): Final layout used.
    """

    print("Final layout:", final_layout)
    ax, fig = plot_circuit(circuit)
    plt.show()


def find_best_routing(
    circuit,
    initial_map=None,
    sabre=False,
    transpiler_fun=transpile_to_star_connectivity,
    iterations=10,
):
    """Find the best initial mapping for the circuit.

    Args:
        circuit (qibo.models.Circuit): Circuit to transpile.
        sabre (bool, optional): Use Sabre router, instead of star.

    Returns:
        dict: Best initial mapping found.
    """
    best_score = None
    best_circuit = None
    best_layout = None

    for _ in range(iterations):
        transpiled_circ, final_layout = transpiler_fun(circuit, initial_map=initial_map, sabre=sabre)
        score = len(transpiled_circ.gates_of_type(gates.SWAP))

        if best_score is None or score < best_score:
            best_score = score
            best_circuit = transpiled_circ
            best_layout = final_layout

    return best_circuit, best_layout


def testing_circuit1():
    """Testing circuit 1."""
    c = Circuit(5)
    c.add(gates.CNOT(0, 2))
    c.add(gates.CNOT(2, 4))
    c.add(gates.CNOT(1, 3))
    c.add(gates.CNOT(2, 4))
    c.add(gates.X(0))
    c.add(gates.CNOT(1, 0))
    c.add(gates.CNOT(4, 3))
    c.add(gates.CNOT(1, 0))
    c.add(gates.X(0))
    c.add(gates.CNOT(1, 2))
    c.add(gates.CNOT(0, 1))
    c.add(gates.X(2))
    c.add(gates.H(0))
    c.add(gates.H(3))
    c.add(gates.CNOT(1, 0))
    c.add(gates.CNOT(3, 2))
    c.add(gates.CNOT(0, 3))
    c.add(gates.H(0))
    c.add(gates.H(0))
    c.add(gates.CNOT(0, 3))
    return c


def testing_circuit2():
    """Testing circuit 2."""
    circuit = Circuit(5)
    circuit.add(gates.CNOT(2, 0))
    circuit.add(gates.CNOT(3, 1))
    circuit.add(gates.X(0))
    circuit.add(gates.H(1))
    circuit.add(gates.CNOT(1, 4))
    circuit.add(gates.H(1))
    circuit.add(gates.X(0))
    circuit.add(gates.CNOT(0, 2))
    circuit.add(gates.H(3))
    circuit.add(gates.CNOT(4, 1))
    circuit.add(gates.CNOT(0, 4))
    circuit.add(gates.X(2))
    circuit.add(gates.H(3))
    circuit.add(gates.CNOT(1, 3))
    circuit.add(gates.H(0))
    circuit.add(gates.CNOT(0, 4))
    circuit.add(gates.CNOT(2, 3))
    circuit.add(gates.CNOT(0, 4))
    circuit.add(gates.X(4))
    circuit.add(gates.CNOT(0, 4))
    circuit.add(gates.CNOT(4, 0))
    circuit.add(gates.CNOT(1, 2))
    circuit.add(gates.H(2))
    circuit.add(gates.H(0))
    circuit.add(gates.CNOT(3, 4))
    circuit.add(gates.CNOT(3, 2))

    return circuit
