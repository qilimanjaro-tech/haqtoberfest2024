"""Helper functions file.

This module contains helper functions for quantum information tasks.
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


from qiskit.visualization import plot_histogram
from qibo import Circuit, gates


def random_state():
    """Generates a random state vector.

    Returns:
        tuple: Randomly generated state angles theta, phi.
    """
    # Generate phi an theta for the state vector:
    theta = np.pi * (np.random.random()*2-1)
    phi = np.pi * (np.random.random()*2-1)

    return theta, phi


def print_random_state(theta, phi):
    """Prints the random state vector.

    Args:
        theta: theta angle of the state vector.
        phi: phi angle of the state vector.

    Returns:
        Prints of coefficeints and probabilities for the state vector.
    """
    alpha, beta = np.cos(theta/2), np.sin(theta/2)*np.exp(phi*1.j)*-1.j
    prob_a, prob_b = np.cos(theta/2)**2, np.sin(theta/2)**2
    print(f"Theta: {str(theta)}, Phi: {str(phi)}")
    print(f"State: alpha={alpha}  beta={beta}")
    print(f"Probabilities: prob_a={prob_a}  prob_b={prob_b}\n")


def print_theoretical_values(state, probabilities):
    """Prints the random state vector info.

    Args:
        state: theoretical state vector.
        probabilities: theoretical probabilities of the state vector.

    Returns:
        Prints the theoretical state and probabilities for the state vector.
    """
    print("THEORETICAL VALUES:")
    print(f"State: {state}")
    print(f"Probabilities: {probabilities}\n")


def print_sampled_values(samples, frequencies, sampled_probabilities):
    """Prints the random state vector info.

    Args:
        samples: samples gotten from the shots.
        frequencies: samples aggregated by 0 or 1's.
        sampled_probabilities: frequencies normalized to 1.

    Returns:
        Prints the samples and probabilities for the state vector.
    """
    print("SAMPLED VALUES:")
    print(f"Samples: {samples}")
    print(f"Frequencies: {frequencies}")
    print(f"Sampled probabilities: {sampled_probabilities}")
    return plot_histogram(sampled_probabilities)


def get_probabilities(counts: dict) -> dict:
    """Returns the counts as probabilities.

    Args:
        counts (dict): The counts of a results.

    Returns:
        dict: The probabilities associated to the given counts.
    """
    norm = sum(counts.values())
    return {i: count/norm for i, count in counts.items()}


def execute_get_samples_and_plot(circuit: Circuit, shots: int):
    """Executes circuit, gets probabilities and plots.

    Args:
       circuit (QuantumCircuit): Circuit to execute.
       shots (int): Number of shots.

    Returns:
       Plot figure and prints of samples.
    """
    # Run the circuit:
    result = circuit(nshots=shots)

    # Sampled values (with nshots):
    # (possible because we have a Measurement gate!)
    samples = np.stack(result.samples(), axis=1)
    frequencies = result.frequencies()
    sampled_probabilities = get_probabilities(frequencies)

    print("SAMPLED VALUES:")
    print(f"Samples: {samples}")
    print(f"Frequencies: {frequencies}")
    print(f"Sampled probabilities: {sampled_probabilities}")
    return plot_histogram(sampled_probabilities)


def create_networkx_graph(edges: dict) -> nx.Graph:
    """Create a networkx graph from a dicionary of edges.

    Args:
        edges (dict): The dicionary key is a tuple of the two nodes, and the value is the edge label.

    Returns:
        nx.Graph: Returns the constructed graph.
    """
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])

    return G


def print_networkx_graph(G: nx.Graph, labels: dict):
    """Prints a given graph, given the passed labels.

    Args:
        G (nx.Graph): graph to plot.
        labels (dict): labels to in the graph edges. The key is a tuple of the two nodes, and the value is the edge label.

    Returns:
        Displays the passed graph.
    """
    options = {"node_size": 1000, "node_color": "blue", "with_labels": True, "font_weight":'bold'}
    pos = nx.spring_layout(G)

    nx.draw(G, pos, **options)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

    plt.show()


def compute_network_path(graph: nx.Graph, sender: str, receiver: str) -> list[tuple]:
    """Computes the shortest path in the network and passes it to an edge list.

    Args:
        G (nx.Graph): graph of the network.
        sender (str): node of the graph to start the path from.
        receiver (str): node of the graph to end the path.

    Returns:
        list[tuple]: edge list, of the shortest path.
    """
    paths = list(nx.shortest_simple_paths(graph, sender, receiver))
    shortest_path = paths[0]

    return [
        (node, shortest_path[i + 1])
        for i, node in enumerate(shortest_path)
        if i != len(shortest_path) - 1
    ]


def create_secure_quantum_teleportation_path_circuit(init_gate: tuple, edges: list[tuple]):
    """Generates a qiskit circuit for the secure quantum teleportation network for a concrete path.

    Args:
        init_gate (tuple): theta, phi of the initial random gate.
        edges (list[tuple]): List of tuples containing the edges of the graph, starting by the emmiter, and ending in the receiver.

    Returns:
        QuantumCircuit: Returns the builded circuit.
    """
    # Define the circuit quantum channels:
    teleport_network_circuit = Circuit(1+2*len(edges))

    for i in range(len(edges)):
        teleport_network_circuit.add(gates.H(2*i+1))
        teleport_network_circuit.add(gates.CNOT(2*i+1, 2*i+2))

    # After some time, now Alice wants to teleport a state to Bob, given by:
    theta, phi = init_gate
    teleport_network_circuit.add(gates.U1q(q=0, theta=theta, phi=phi))

    for i in range(len(edges)):
        teleport_network_circuit.add(gates.CNOT(2*i, 2*i+1))
        teleport_network_circuit.add(gates.H(2*i))
        teleport_network_circuit.add(gates.M(2*i))
        teleport_network_circuit.add(gates.M(2*i+1))

    for i in range(len(edges)):
        teleport_network_circuit.add(gates.CZ(2*i, 2*len(edges)))
        teleport_network_circuit.add(gates.CNOT(2*i+1, 2*len(edges)))

    teleport_network_circuit.add(gates.M(len(edges)*2))

    return teleport_network_circuit
