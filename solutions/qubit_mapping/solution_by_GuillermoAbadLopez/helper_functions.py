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


def get_circuit_gates(circuit):
    """Get the gates of the circuit.

    Args:
        circuit (qibo.models.Circuit): Circuit to get the gates from.

    Returns:
        list[dict]: List of gates in the circuit. Where each gate is a dictionary (keys: 'name', value: 'qubits').
    """
    return [{i.name: i.qubits} for i in circuit.queue]


def find_final_reordering(circuit, layout):
    """Get the final reordering of the qubits in the circuit, adding the layout and the SWAP gates.

    Args:
        circuit (qibo.models.Circuit): Circuit to extract the SWAPS from.
        layout (dict): Initial layout used for the circuit.

    Returns:
        dict: Final order of the qubits.
    """
    reordering_dict = deepcopy(layout)
    for operation in get_circuit_gates(circuit):
        for k, v in operation.items():
            gate, qubits = k, v  # This works, because each dict, only has one entry
        key_1 = None
        key_2 = None

        if gate == "swap":
            key_1 = qubits[0]
            key_2 = qubits[1]

            value1 = deepcopy(reordering_dict[f"q{key_1}"])
            value2 = deepcopy(reordering_dict[f"q{key_2}"])

            reordering_dict[f"q{key_1}"] = value2
            reordering_dict[f"q{key_2}"] = value1

    return reordering_dict


def circuits_equivalence_fidelity(og_circuit, transp_circuit, layout):
    """Check if two circuits are equivalent.

    Args:
        og_circuit (qibo.models.Circuit): Original circuit to compare.
        transp_circuit (qibo.models.Circuit): Transpiler circuit to compare.
        layout (dict): Layout used for the transpiled circuit.

    Returns:
        float: Fidelity between the two circuits.
    """
    reordering = find_final_reordering(transp_circuit, layout)

    circuit_2_copy = deepcopy(transp_circuit)

    # Block to mix the initial layout, with the SWAPS in the circuit
    while True:
        end = True
        for k, v in reordering.items():
            if int(k[1:]) != v:
                circuit_2_copy.add(gates.SWAP(int(k[1:]), v))
                swap_count_circuit = Circuit(circuit_2_copy.nqubits)
                swap_count_circuit.add(gates.SWAP(int(k[1:]), v))
                reordering = find_final_reordering(swap_count_circuit, reordering)
                end = False
                break
        if end:
            break

    U1 = og_circuit.unitary()
    U2 = circuit_2_copy.unitary()
    almost_identity = U1.transpose().conjugate() @ U2
    trace = np.trace(almost_identity)
    normalized = np.abs(trace) / (2**og_circuit.nqubits)
    return normalized**2


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
        custom_passes.append(StarConnectivityPlacer(connectivity=star_connectivity(), middle_qubit=2))

    if sabre:
        custom_passes.append(Sabre(connectivity=star_connectivity()))
    else:
        custom_passes.append(StarConnectivityRouter(connectivity=star_connectivity(), middle_qubit=2))

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
