Benchmark Results and Optimality Verification

The weighted graph contains five vertices and seven weighted edges. We exhaustively evaluated all (2^5 = 32) possible binary assignments to determine the exact maximum cut weight.

The optimal cut weight is 13, achieved by four bitstrings: "01001", "01100", "10011", and "10110".

Both Processor A and Processor B observed the optimal cut weight during 4,096-shot simulations.

Metric| Processor A| Processor B
Physical qubits| 5| 9
Expected cut weight| 10.6353| 10.6926
Optimal cut weight| 13| 13
Approximation ratio| 0.8181| 0.8225
Circuit depth| 49| 33
Total gates| 75| 69
CX gates| 23| 17
Estimated SWAP equivalents| 3| 1
Shots| 4,096| 4,096

Processor B achieved a slightly higher expected cut weight and a shallower transpiled circuit, with fewer total gates and CX gates. Both processors observed an optimal solution. These results suggest that Processor B's tested connectivity provides an advantage for this particular circuit and graph.

The estimated SWAP-equivalent metric is a routing-overhead proxy rather than an exact count of inserted SWAP gates. Results are based on the project's simulated noise model and should not be interpreted as measurements from physical quantum hardware.
