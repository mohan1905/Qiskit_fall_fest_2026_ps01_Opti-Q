"""Processor architecture and noise-model utilities."""

import json
from pathlib import Path

from qiskit.transpiler import CouplingMap
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

def load_processor_config(processor_name):
    """Load Processor A or B configuration from its JSON file."""
    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / "processors" / f"{processor_name}.json"

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)

def build_coupling_map(config):
    """Build the processor's connectivity map."""
    edges = config["coupling_edges"]

    # Treat the provided connectivity as bidirectional.
    bidirectional_edges = edges + [[v, u] for u, v in edges]

    return CouplingMap(couplinglist=bidirectional_edges)

def build_noise_model(config):
    """Create a synthetic noise model from processor settings."""
    noise = config["noise"]

    p1 = noise["single_qubit_depolarizing"]
    pcx = noise["cx_depolarizing"]
    readout_p = noise["readout_error"]

    noise_model = NoiseModel()

    # Apply single-qubit depolarizing noise to physical 1-qubit gates.
    one_qubit_error = depolarizing_error(p1, 1)
    noise_model.add_all_qubit_quantum_error(
        one_qubit_error, ["sx", "x"]
    )

    # Apply two-qubit depolarizing noise to CX gates.
    cx_error = depolarizing_error(pcx, 2)
    noise_model.add_all_qubit_quantum_error(cx_error, ["cx"])

    # Symmetric readout error: probability of flipping either outcome.
    readout_error = ReadoutError([
        [1 - readout_p, readout_p],
        [readout_p, 1 - readout_p],
    ])
    noise_model.add_all_qubit_readout_error(readout_error)

    return noise_model
