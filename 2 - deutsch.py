# %%
# Deutsch algorithm
# Diagram is shown on page 176 of the textbook:
# Quantum Computing for Computer Scientists

# %%
import numpy as np
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

# %%
# First we need the function and the unitary matrix which applies to |x, y> to
# get |x, f(x) ^ y>.
def f(x):
    """The function which we're testing for.

    Should be constant 0 or 1 if *constant*, otherwise should be 1 - x or x - 1
    if *balanced*.
    """
    # 0 -> 0
    # 1 -> 1
    return 1 - x


# This is the matrix which applies to |x, y> to get |x, f(x) ^ y>
unitary_matrix = np.zeros(shape=(4, 4), dtype=int)
for x in range(2):
    for y in range(2):
        # note that the digits are in reverse order compared to the textbook,
        # since the book puts the x on the higher bit and the y on the lower,
        # but here we want x to be the lower bit (q0) and y the higher
        # bit (q1).
        unitary_matrix[x + 2 * (y ^ f(x)), x + 2 * y] = 1

# %%
qc = QuantumCircuit(2, 1)
# initialize qubits to |01> (the string is in reverse order), i.e. index 0 is
# the first qubit.
qc.initialize("10")
qc.h([0, 1])
qc.unitary(unitary_matrix, [0, 1])
qc.h(0)
qc.measure(0, 0)
qc.draw()

# %%
# And finally run the circuit in a simulation.
sim = AerSimulator(shots=100)
job = sim.run(qc)
result = job.result()
print(result.get_counts())

# %%
