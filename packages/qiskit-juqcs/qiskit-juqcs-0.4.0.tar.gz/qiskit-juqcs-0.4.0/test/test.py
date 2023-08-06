from juqcs import Juqcs
import qiskit

circuit = qiskit.QuantumCircuit(5)
circuit.h(0)
circuit.cx(0,1)
circuit.cx(0,2)
circuit.measure_all()
print(circuit)

b = Juqcs.get_backend('statevector_simulator')
print('ALLOCATING...')
b.allocate(minutes=30, max_qubits=20, reservation='juniq-test')

print('SUBMITTING CIRCUITS...')
job = qiskit.execute([circuit,circuit], b, shots=1000, seed=10)
job.status()
res = job.result()
job.status()
'''

print('SUBMITTING CIRCUITS...')
job = qiskit.execute([circuit,0], b, shots=1000, seed=10)
job.status()
res = job.result()
job.status()
'''


from pprint import pprint
pprint(res.to_dict())

print('DEALLOCATING...')
b.deallocate()