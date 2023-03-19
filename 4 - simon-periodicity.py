# %%
# Simon's periodicity algorithm
# Section 6.3, p187 of the textbook:
# Quantum Computing for Computer Scientists

# %%
import numpy as np
from pycryptosat import Solver
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

# the number of bits the function f operates on
# in this example this cannot be changed since the function is hardcoded.
n_bits = 3

# %%
def unitary(f, n_bits):
    """The unitary matrix which applies to |x, y> to get |x, f(x) ^ y>.

    Parameters
    ----------
    f: callable
        It is the function which we're testing for. Should take an int, and
        return an int. Input and output are supposed to have the same number of
        bits.

    n_bits: int
        The number of bits ``f`` operates on.

    Returns
    -------
    unitary_matrix: numpy.ndarray of shape (2 ** (n_bits * 2), 2 ** (n_bits * 2))
        The unitary matrix which applies to |x, y> to get |x, f(x) ^ y>.
    """
    # The unitary matrix is 2 ** (n_bits * 2) x 2 ** (n_bits * 2).
    unitary_matrix = np.zeros(shape=(2 ** (n_bits * 2), 2 ** (n_bits * 2)))
    for x in range(2**n_bits):
        for y in range(2**n_bits):
            # note that the digits are in reverse order compared to the
            # textbook, since the book puts the x on the higher bit and the y
            # on the lower, but here we want x to be the lower bit (q0..q(n-1))
            # and y the higher bit (qn).
            unitary_matrix[x + 2**n_bits * (y ^ f(x)), x + 2**n_bits * y] = 1
    return unitary_matrix

# %%
# The function which we're testing for.
def f(x):
    table = {
        0b000: 0,
        0b101: 0,
        0b001: 1,
        0b100: 1,
        0b010: 2,
        0b111: 2,
        0b011: 3,
        0b110: 3,
        0b100: 4,
        0b001: 4,
        0b101: 5,
        0b000: 5,
        0b110: 6,
        0b011: 6,
        0b111: 7,
        0b010: 7,
    }
    return table[x]
    # the function should be two to one, for ``c`` to be non-zero, otherwise
    # ``f`` needs to be one to one.

U_f = unitary(f, n_bits)

# %%
qc = QuantumCircuit(n_bits * 2, n_bits)
qc.initialize("0" * n_bits * 2, list(range(n_bits * 2)))  # set x and y to 0
qc.h(range(n_bits))
qc.unitary(U_f, range(n_bits * 2))
qc.h(range(n_bits))
qc.measure(range(n_bits), range(n_bits))
qc.draw()

# %%
# Simulate the circuit
simulator = AerSimulator()
result = simulator.run(qc).result()
counts = result.get_counts()
print(counts)

# %%
# Use pycryptosat to solve the system of equations
s = Solver(threads=1)

var_ids = {id: f"x{id}" for id in range(n_bits)}

for key in counts.keys():
    if key == '0' * n_bits:
        # ignore the all-zero key, since it's not a part of the solution
        continue
    # On an actual quantum computer, we need to filter only for the ones which
    # are not there due to noise, and have high frequencies. This example does
    # not include that step.
    clause = [bit + 1 for bit in range(n_bits) if key[bit] == '1']
    s.add_xor_clause(clause, False)

# not that we have the system of equations, we'd like to solve it, but since
# a set of 0s is always a solution, we iterate and assume one bit to be True
# at a time, and at the end we report all solutions.

solutions = set()
for positive in range(n_bits):
    sat, solution = s.solve(assumptions=[3])
    if sat:
        solutions.add(solution)

for solution in solutions:
    print(f"solution: {solution}")

    if (sat):
        for id, name in var_ids.items():
            print(f"{name} = {solution[id + 1]}")

if not solutions:
    print("No solution. Sorry!")

# %%
