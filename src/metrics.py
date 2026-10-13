"""Metrics for comparing Processor A and Processor B."""

from.problem import cut_weight
from.routing import count_cx_gates, count_total_gates, circuit_depth

def evaluate_counts(graph, counts):
    """Calculate cut statistics from measurement counts."""
    total_shots = sum(counts.values())

    if total_shots == 0:
        raise ValueError("Measurement counts are empty.")

    weighted_sum = 0.0
    best_weight = float("-inf")
    best_bitstring = None
    cut_distribution = {}

    for key, count in counts.items():
        bits = key.replace(" ", "")[::-1]
        weight = cut_weight(graph, bits)

        weighted_sum += weight * count
        cut_distribution[weight] = (
            cut_distribution.get(weight, 0) + count
        )

        if weight > best_weight:
            best_weight = weight
            best_bitstring = bits

    return {
        "expected_cut_weight": weighted_sum / total_shots,
        "best_observed_cut_weight": best_weight,
        "best_observed_bitstring": best_bitstring,
        "approximation_ratio": None,
        "total_shots": total_shots,
        "cut_distribution": cut_distribution,
    }

def circuit_metrics(circuit):
    """Collect basic circuit resource metrics."""
    return {
        "circuit_depth": circuit_depth(circuit),
        "total_gates": count_total_gates(circuit),
        "cx_gates": count_cx_gates(circuit),
    }

def add_optimization_metrics(results, exact_optimum):
    """Add an approximation ratio against the exact classical optimum."""
    for result in results:
        if exact_optimum > 0:
            result["approximation_ratio"] = (
                result["expected_cut_weight"] / exact_optimum
            )
        else:
            result["approximation_ratio"] = None

    return results
