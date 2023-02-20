# %%
# An exercise to add two bits using qubits and gates of chapter 5 of the
# textbook: Quantum Computing for Computer Scientists.

# %%
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

# %%
# Add circuit: two input bits and two output bits
def add_circuit(x, y):
    qc = QuantumCircuit(4, 2)
    qc.initialize(f"{x}{y}", [0, 1])
    qc.cnot(control_qubit=0, target_qubit=2)
    qc.cnot(control_qubit=1, target_qubit=2)
    qc.ccx(control_qubit1=0, control_qubit2=1, target_qubit=3)
    qc.measure(qubit=[2, 3], cbit=[0, 1])
    return qc

# %%
for x in range(2):
    for y in range(2):
        qc = add_circuit(x, y)
        print(f"x={x}, y={y}")
        sim = AerSimulator(shots=100)
        job = sim.run(qc)
        result = job.result()
        print(result.get_counts())

# %%
