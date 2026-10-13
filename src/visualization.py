"""Visualization utilities for Max-Cut benchmarking."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

def plot_weighted_graph(graph, output_path):
    """Save the weighted graph as an image."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    positions = nx.spring_layout(graph, seed=42)
    edge_labels = nx.get_edge_attributes(graph, "weight")

    plt.figure(figsize=(7, 5))
    nx.draw_networkx(
        graph,
        positions,
        node_color="lightblue",
        node_size=800,
        font_size=11,
    )
    nx.draw_networkx_edge_labels(
        graph, positions, edge_labels=edge_labels
    )

    plt.title("Weighted Graph for Max-Cut")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

def plot_processor_comparison(results, output_path):
    """Plot expected cut weights for Processor A and Processor B."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    labels = [result["processor"] for result in results]
    values = [result["expected_cut_weight"] for result in results]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values)
    plt.ylabel("Expected cut weight")
    plt.title("Processor A vs Processor B")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

def plot_resource_comparison(results, output_path):
    """Plot circuit depth and CX-gate counts for each processor."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    labels = [result["processor"] for result in results]
    depths = [result["circuit_depth"] for result in results]
    cx_counts = [result["cx_gates"] for result in results]

    figure, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].bar(labels, depths)
    axes[0].set_title("Transpiled circuit depth")
    axes[0].set_ylabel("Depth")

    axes[1].bar(labels, cx_counts)
    axes[1].set_title("CX gate count")
    axes[1].set_ylabel("Number of CX gates")

    figure.tight_layout()
    figure.savefig(output_path, dpi=200)
    plt.close(figure)
