"""Main runner for weighted Max-Cut QAOA benchmarking."""

import csv
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from src.problem import (
    build_weighted_graph,
    cut_weight,
    exact_max_cut,
    qaoa_circuit,
    bitstring_from_qiskit_key,
)
from src.processors import (
    load_processor_config,
    build_coupling_map,
    build_noise_model,
)
from src.routing import transpile_for_processor
from src.metrics import evaluate_counts, circuit_metrics
from src.visualization import (
    plot_weighted_graph,
    plot_processor_comparison,
    plot_resource_comparison,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"
FIGURES_DIR = RESULTS_DIR / "figures"


def optimize_qaoa_parameters(graph, layers=1, max_iterations=60):
    """Optimize QAOA parameters using an ideal statevector simulation."""
    n = graph.number_of_nodes()

    def objective(parameters):
        gammas = parameters[:layers]
        betas = parameters[layers:]

        circuit = qaoa_circuit(graph, gammas, betas)
        probabilities = Statevector.from_instruction(
            circuit
        ).probabilities_dict()

        expected_cut = 0.0

        for key, probability in probabilities.items():
            bits = bitstring_from_qiskit_key(key, n)
            expected_cut += probability * cut_weight(graph, bits)

        # Minimize negative expected cut to maximize the cut.
        return -expected_cut

    initial = np.concatenate([
        np.full(layers, 0.5),
        np.full(layers, 0.25),
    ])

    result = minimize(
        objective,
        initial,
        method="COBYLA",
        options={"maxiter": max_iterations, "rhobeg": 0.5},
    )

    parameters = result.x
    return parameters[:layers], parameters[layers:]


def run_processor(graph, processor_name, gammas, betas):
    """Transpile and execute QAOA on one configured noisy processor."""
    config = load_processor_config(processor_name)
    coupling_map = build_coupling_map(config)
    noise_model = build_noise_model(config)

    circuit = qaoa_circuit(graph, gammas, betas, measure=True)

    transpiled = transpile_for_processor(
        circuit, config, coupling_map
    )

    simulator = AerSimulator(noise_model=noise_model)

    job = simulator.run(
        transpiled,
        shots=config.get("shots", 4096),
        seed_simulator=42,
    )
    counts = job.result().get_counts()

    statistics = evaluate_counts(graph, counts)
    resources = circuit_metrics(transpiled)

    # A rough estimate only: excess CX gates divided by 3.
    # This is a proxy, not an exact SWAP count.
    logical_cx_estimate = (
        2 * graph.number_of_edges() * len(gammas)
    )
    estimated_swaps = max(
        0,
        resources["cx_gates"] - logical_cx_estimate,
    ) / 3

    return {
        "processor": processor_name,
        "physical_qubits": config["num_qubits"],
        **statistics,
        **resources,
        "estimated_swap_equivalents": estimated_swaps,
    }


def save_results(results):
    """Save benchmark results as a CSV table."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    output_file = TABLES_DIR / "benchmark_results.csv"

    with output_file.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=list(results[0].keys())
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output_file}")


def run():
    """Run the complete Processor A and B benchmark."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    graph = build_weighted_graph()
    exact_bits, exact_weight = exact_max_cut(graph)

    print("Weighted Graph Max-Cut using QAOA")
    print("----------------------------------")
    print(f"Exact classical optimum: {exact_weight}")
    print(f"One optimal bitstring:   {exact_bits}")

    gammas, betas = optimize_qaoa_parameters(graph)

    print(f"\nOptimized gamma values: {gammas}")
    print(f"Optimized beta values:  {betas}")

    results = []

    for processor_name in ["processor_A", "processor_B"]:
        print(f"\nRunning {processor_name}...")

        result = run_processor(
            graph, processor_name, gammas, betas
        )

        if exact_weight > 0:
            result["approximation_ratio"] = (
                result["expected_cut_weight"] / exact_weight
            )
        else:
            result["approximation_ratio"] = None

        results.append(result)

        print(
            f"Expected cut weight: "
            f"{result['expected_cut_weight']:.4f}"
        )
        print(f"Circuit depth: {result['circuit_depth']}")
        print(f"CX gates: {result['cx_gates']}")

    save_results(results)

    plot_weighted_graph(
        graph, FIGURES_DIR / "weighted_graph.png"
    )
    plot_processor_comparison(
        results, FIGURES_DIR / "cut_weight_comparison.png"
    )
    plot_resource_comparison(
        results, FIGURES_DIR / "resource_comparison.png"
    )

    print("\nBenchmark completed.")
    print(f"Figures saved in: {FIGURES_DIR}")


if __name__ == "__main__":
    run()
