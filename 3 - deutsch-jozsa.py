# %%
# Deutsch-Jozsa algorithm
# Diagram is shown on page 186 of the textbook:
# Quantum Computing for Computer Scientists

# %%
import numpy as np
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

# the number of bits the function f operates on
n_bits = 5

# %%
def unitary(f, n_bits):
    """The unitary matrix which applies to |x, y> to get |x, f(x) ^ y>.

    Parameters
    ----------
    f: callable
        It is the function which we're testing for. Should take an int, and
        return 0 or 1.

    n_bits: int
        The number of bits in the input x.

    Returns
    -------
    unitary_matrix: numpy.ndarray of shape (2 ** (n_bits + 1), 2 ** (n_bits + 1))
        The unitary matrix which applies to |x, y> to get |x, f(x) ^ y>.
    """
    # The unitary matrix is 2 ** (n_bits + 1) x 2 ** (n_bits + 1).
    unitary_matrix = np.zeros(shape=(2 ** (n_bits + 1), 2 ** (n_bits + 1)))
    for x in range(2**n_bits):
        for y in range(2):
            # note that the digits are in reverse order compared to the
            # textbook, since the book puts the x on the higher bit and the y
            # on the lower, but here we want x to be the lower bit (q0..q(n-1))
            # and y the higher bit (qn).
            unitary_matrix[x + 2**n_bits * (y ^ f(x)), x + 2**n_bits * y] = 1
    return unitary_matrix


# %%
# The function which we're testing for.
def f(x):
    return int(x % 2 == 1)
    # or return a constant 0 or 1


U_f = unitary(f, n_bits)

# %%
qc = QuantumCircuit(n_bits + 1, 1)
# initialize qubits to |0..01>
qc.initialize("0" * n_bits, list(range(n_bits)))  # set x to 0
qc.initialize("1", n_bits)  # set y to 1
qc.h(range(n_bits + 1))
qc.unitary(U_f, range(n_bits + 1))
qc.h(range(n_bits))
qc.measure(0, 0)
qc.draw()

# %%
# And finally run the circuit in a simulation.
sim = AerSimulator(shots=100)
job = sim.run(qc)
result = job.result()
print(result.get_counts())
# outputs 0 for a constant function, 1 for a balanced function

# %%
