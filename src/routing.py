"""Circuit transpilation and routing utilities."""

from qiskit import transpile

def transpile_for_processor(circuit, config, coupling_map):
    """Transpile a circuit for a processor's connectivity and basis gates."""
    settings = config["transpilation"]

    transpiled_circuit = transpile(
        circuit,
        basis_gates=config["basis_gates"],
        coupling_map=coupling_map,
        optimization_level=settings["optimization_level"],
        seed_transpiler=settings["seed_transpiler"],
    )

    return transpiled_circuit

def count_cx_gates(circuit):
    """Count CX gates in a transpiled circuit."""
    return circuit.count_ops().get("cx", 0)

def count_total_gates(circuit):
    """Count all operations, excluding barriers."""
    operations = circuit.count_ops()
    return sum(
        count for gate, count in operations.items()
        if gate != "barrier"
    )

def circuit_depth(circuit):
    """Return the transpiled circuit depth."""
    return circuit.depth()
