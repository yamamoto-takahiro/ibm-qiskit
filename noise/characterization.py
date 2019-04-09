import numpy as np
import matplotlib.pyplot as plt

import qiskit
from qiskit.providers.aer.noise.errors.standard_errors import thermal_relaxation_error, amplitude_damping_error
from qiskit.providers.aer.noise import NoiseModel

from qiskit.ignis.characterization.coherence import T1Fitter, T2StarFitter, T2Fitter
from qiskit.ignis.characterization.coherence import t1_circuits, t2_circuits, t2star_circuits

from qiskit import IBMQ, compile

# Measure the value of T1 (relaxation) time
# 12 numbers ranging from 10 to 1000, logarithmically spaced
# extra point at 1500
num_of_gates = np.append((np.logspace(1, 3, 12)).astype(int), np.array([1500]))
gate_time = 0.1 # time of running a single gate

# Select the qubits whose T1 are to be measured
qubits = [0]

# Generate experiments
circs, xdata = t1_circuits(num_of_gates, gate_time, qubits)

# Run the simulator
# IBMQ.backends()
#[
# <IBMQBackend('ibmqx4') from IBMQ()>, 
# <IBMQBackend('ibmqx2') from IBMQ()>, 
# <IBMQBackend('ibmq_16_melbourne') from IBMQ()>, 
# <IBMQBackend('ibmq_qasm_simulator') from IBMQ()>
# ]
# IBMQ device information:
# https://www.research.ibm.com/ibm-q/technology/devices/#ibmqx4

backend = qiskit.Aer.get_backend('qasm_simulator')
shots = 1024
backend_result = qiskit.execute(circs, backend, shots=shots).result()

for i in range(len(circs)):
    print(backend_result.get_counts(circs[i]))
# print(backend_result.get_counts(circs[0]))
print(xdata) # gate_time * num_of_gates

# Run on an IBMQ device
# Ref:
# https://qiskit.org/documentation/advanced_use_of_ibm_q_devices.html

IBMQ.load_accounts()
backend = IBMQ.get_backend('ibmqx2')
for i in range(len(circs)):
    qobj = compile(circs[i], backend=backend, shots=1024)
    job = backend.run(qobj)
    result = job.result()
    counts = result.get_counts()
    print(counts)

# Measure the value of T*2 (decoherence) time
# https://github.com/Qiskit/qiskit-tutorials/blob/master/community/ignis/coherence-overview.ipynb

