"""Weighted Max-Cut problem and QAOA circuit construction."""

from itertools import product

import networkx as nx
from qiskit import QuantumCircuit

def build_weighted_graph():
    """Generate a reproducible five-vertex weighted graph."""
    graph = nx.Graph()
    graph.add_nodes_from(range(5))

    graph.add_weighted_edges_from([
        (0, 1, 3.0),
        (0, 2, 1.0),
        (1, 2, 2.0),
        (1, 3, 4.0),
        (2, 3, 2.0),
        (2, 4, 3.0),
        (3, 4, 1.0),
    ])

    return graph

def cut_weight(graph, bits):
    """Calculate the total weight of edges crossing the partition."""
    if isinstance(bits, str):
        bits = [int(bit) for bit in bits]

    total = 0.0

    for u, v, data in graph.edges(data=True):
        if bits[u]!= bits[v]:
            total += float(data["weight"])

    return total

def exact_max_cut(graph):
    """Find the exact classical optimum by exhaustive enumeration."""
    n = graph.number_of_nodes()
    best_bits = None
    best_weight = -1.0

    for bits in product([0, 1], repeat=n):
        weight = cut_weight(graph, bits)

        if weight > best_weight:
            best_bits = bits
            best_weight = weight

    return "".join(map(str, best_bits)), best_weight

def qaoa_circuit(graph, gammas, betas, measure=False):
    """Construct a QAOA circuit for the weighted Max-Cut objective."""
    n = graph.number_of_nodes()

    if len(gammas)!= len(betas):
        raise ValueError("The gamma and beta arrays must have equal length.")

    circuit = QuantumCircuit(n, n if measure else 0)

    # Initial uniform superposition.
    circuit.h(range(n))

    # QAOA cost and mixer layers.
    for gamma, beta in zip(gammas, betas):
        for u, v, data in graph.edges(data=True):
            weight = float(data["weight"])
            circuit.rzz(-gamma * weight, u, v)

        for qubit in range(n):
            circuit.rx(2 * beta, qubit)

    if measure:
        circuit.measure(range(n), range(n))

    return circuit

def bitstring_from_qiskit_key(key, n):
    """Convert Qiskit's displayed bit order to qubit-index order."""
    cleaned = key.replace(" ", "")
    return cleaned[::-1].zfill(n)
