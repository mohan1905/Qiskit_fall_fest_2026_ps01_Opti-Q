# Weighted Graph Max-Cut Using QAOA

## 1. Project Overview

This project implements the Weighted Graph Max-Cut problem using the Quantum Approximate Optimization Algorithm (QAOA) and Qiskit.

The objective is to divide the vertices of a weighted graph into two groups so that the total weight of edges connecting different groups is maximized.

## 2. Problem Definition

The graph contains five vertices and seven weighted edges. Each vertex is assigned to one of two partitions.

An edge contributes its weight to the cut when its two endpoints belong to different partitions.

The project calculates the exact classical optimum for reference and compares it with QAOA measurement results.

## 3. Quantum Algorithm

The implementation uses QAOA with a configurable number of layers.

The circuit:
1. Initializes the qubits in a uniform superposition.
2. Applies weighted cost operations for graph edges.
3. Applies mixer operations to explore candidate partitions.
4. Measures the qubits to obtain candidate solutions.

A classical optimizer adjusts the QAOA parameters using ideal statevector simulation.

## 4. Processor Architectures

### Processor A
- 5 physical qubits
- Linear-chain connectivity
- 4 reference coupling edges

### Processor B
- 9 physical qubits
- Sparse heavy-hex-inspired connectivity
- 12 reference coupling edges

Both configurations use the required basis gates and the synthetic noise settings specified by the hackathon instructions.

## 5. Benchmarking Methodology

The same weighted graph and optimized QAOA parameters are used for both processor configurations.

The circuits are transpiled using:
- Optimization level: 1
- Transpiler seed: 42
- Basis gates: `rz`, `sx`, `x`, `cx`
- Simulation shots: 4096

The synthetic noise model uses:
- Single-qubit depolarizing probability: 0.001
- CX depolarizing probability: 0.005
- Readout error probability: 0.01

## 6. Evaluation Metrics

The project records:
- Expected cut weight
- Best observed cut weight
- Approximation ratio
- Transpiled circuit depth
- Total gate count
- CX gate count
- Estimated SWAP equivalents as a rough proxy

The results are intended to illustrate how processor connectivity and circuit routing can affect quantum optimization experiments.

## 7. Results

Benchmark results will be added after the program has been executed and validated.

The generated CSV table and figures should be reviewed before drawing conclusions about which architecture performs better.

## 8. Limitations

This experiment uses a small, programmatically generated graph and a synthetic noise model. Its results do not represent measurements from real quantum hardware.

The estimated SWAP-equivalent metric is only a proxy and should not be interpreted as an exact count of inserted SWAP gates.

## 9. Future Work

Future improvements include testing additional graph structures, increasing the QAOA depth, comparing more routing strategies, and validating the implementation against the official hackathon evaluation procedure.

## 10. Conclusion

This project provides a framework for studying weighted Max-Cut with QAOA and comparing transpiled circuit resources and noisy simulation outcomes across two processor connectivity configurations.
