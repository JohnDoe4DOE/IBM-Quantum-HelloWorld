# =============================================
# Full Bell-state example with EstimatorV2
# Works with current qiskit_ibm_runtime API
# =============================================

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
import matplotlib.pyplot as plt

# ---------------------------
# 1. Create the Bell-state circuit
# ---------------------------
qc = QuantumCircuit(2)
qc.h(0)       # Hadamard on qubit 0
qc.cx(0, 1)   # CNOT: control 0 -> target 1

# Draw the logical circuit
fig = qc.draw("mpl")
plt.show()

# ---------------------------
# 2. Define observables
# ---------------------------
observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
observables = [SparsePauliOp(label) for label in observables_labels]

# ---------------------------
# 3. Connect to IBM Quantum and select backend
# ---------------------------
service = QiskitRuntimeService()  # Uses saved credentials

backend = service.least_busy(simulator=False, operational=True)
print(f"Selected backend: {backend}")

# ---------------------------
# 4. Transpile circuit for hardware
# ---------------------------
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)

# Draw hardware-level circuit
fig = isa_circuit.draw("mpl", idle_wires=False)
plt.show()

# ---------------------------
# 5. Create EstimatorV2 with backend
#    (Pass the backend object as a positional argument)
# ---------------------------
estimator = Estimator(backend)

# Optional: configure error mitigation and shots
estimator.options.resilience_level = 1
estimator.options.default_shots = 5000

# Map observables to physical qubits layout
mapped_observables = [obs.apply_layout(isa_circuit.layout) for obs in observables]

# ---------------------------
# 6. Run the Estimator job
# ---------------------------
job = estimator.run([(isa_circuit, mapped_observables)])

# Print job ID
print(f">>> Job ID: {job.job_id()}")

# ---------------------------
# 7. Plot the result
# ---------------------------

from matplotlib import pyplot as plt

# Make sure pub_result is defined
job_result = job.result()
pub_result = job_result[0]  # First pub (your single submission)

# Get expectation values and (optional) standard deviations
values = pub_result.data.evs       # Array of expectation values
errors = getattr(pub_result.data, "stds", None)  # Some versions have stds

# Plotting graph
# Print the results in a readable way. You’ll see:
# Single-qubit observables ≈ 0 → random, independent
# Two-qubit observables (ZZ, XX) ≈ +1 → perfectly correlated → entangled
plt.figure(figsize=(8,5))
plt.errorbar(observables_labels, values, yerr=errors, fmt="-o", capsize=5)
plt.xlabel("Observables")
plt.ylabel("Expectation values")
plt.title("Bell-state Observable Results")
plt.grid(True)
plt.show()