# Weighted Graph Max-Cut Using QAOA

A quantum optimization project using the Quantum Approximate Optimization Algorithm (QAOA) and Qiskit to solve the Weighted Graph Max-Cut problem and benchmark circuit performance across two processor connectivity configurations.

## Project Overview

The Weighted Graph Max-Cut problem divides graph vertices into two groups to maximize the total weight of edges connecting different groups.

This project:
- Builds a weighted graph programmatically.
- Constructs a QAOA quantum circuit.
- Finds the exact classical optimum for comparison.
- Benchmarks Processor A and Processor B using their specified connectivity.
- Evaluates circuit depth, gate counts, expected cut weight, and approximation ratio.
- Uses a synthetic noise model to study noisy simulation results.

## Technologies Used

- Python
- Qiskit
- Qiskit Aer
- NumPy
- SciPy
- NetworkX
- Matplotlib
- Pandas

## Processor Configurations

### Processor A
- 5 physical qubits
- Linear-chain connectivity
- 4 coupling edges

### Processor B
- 9 physical qubits
- Sparse heavy-hex-inspired connectivity
- 12 coupling edges

Both configurations use the hackathon's specified basis gates, transpilation settings, and synthetic noise parameters.

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── main.ipynb
├── report.md
├── processors/
│   ├── processor_A.json
│   └── processor_B.json
└── src/
    ├── __init__.py
    ├── problem.py
    ├── processors.py
    ├── routing.py
    ├── metrics.py
    ├── visualization.py
    └── main.py
```

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Project

Run the benchmark from the repository root:

```bash
python -m src.main
```

Alternatively, open `main.ipynb` in a compatible Jupyter environment and execute its code cell.

## Outputs

The program is designed to generate:

- `results/tables/benchmark_results.csv`
- `results/figures/weighted_graph.png`
- `results/figures/cut_weight_comparison.png`
- `results/figures/resource_comparison.png`

These outputs should be checked after successfully running the program.

## Evaluation Metrics

- Expected cut weight
- Best observed cut weight
- Approximation ratio
- Transpiled circuit depth
- Total gate count
- CX gate count
- Estimated SWAP equivalents (a rough proxy)

## Limitations

This project uses a small, programmatically generated graph and synthetic noise simulation. It does not claim results from real quantum hardware. Benchmark conclusions will be added after successful execution and validation.

## Future Work

Potential extensions include testing additional graph structures, exploring deeper QAOA circuits, comparing routing strategies, and validating results against the official hackathon evaluation procedure.

## Event

Prepared for Qiskit Fall Fest 2026 at SRM University AP.
