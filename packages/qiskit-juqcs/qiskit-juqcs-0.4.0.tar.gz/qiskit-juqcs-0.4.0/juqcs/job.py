'''JUQCS Job class.'''

from time import time
from datetime import datetime

from qiskit.providers import JobV1 as Job
from qiskit.providers.jobstatus import JobStatus
from qiskit import QuantumCircuit
from qiskit.result import Result
from qiskit.result.models import ExperimentResult

from juqcs.client import submit, save_log, PY_RUN
from juqcs.exceptions import JobFailureError, JobSubmitError


class JuqcsJob(Job):
    '''JUQCS Job class.'''
    _async = False

    def __init__(self, backend, job_id):
        super().__init__(backend, job_id)
        self._unicore_jobs = []
        self._inputs = []
        self._status = JobStatus.INITIALIZING

    def _validate(self, run_input):
        '''
        Validate {run_input} before submitting.
        Returns:
            run_input
        Raises:
            JobSubmitError(msg)
        '''
        run_input = [run_input] if type(run_input) is QuantumCircuit else run_input 
        for circuit in run_input:
            if type(circuit) is not QuantumCircuit:
                raise JobSubmitError(
                        'Input should be QuantumCircuit or list(QuantumCircuit).')
            if circuit.num_qubits > self._backend._alloc_qubits:
                raise JobSubmitError(
                        f'Circuit {circuit.name} contains too many qubits for this allocation.')
        return run_input

    def _submit(self, circuit):
        '''
        Check if allocation is still running, then submit circuit for simulation.
        Returns:
            run_job (unicore.job): UNICORE job object for the simulated circuit.
        Raises:
            JobSubmitError: if no valid allocation was found.
        '''
        if not self._backend._allocation_is_valid():
            raise JobSubmitError(self._backend.status().status_msg)

        # build juqcs args
        if self._backend._result_type == 'statevector':
            args = ['--amplitudes']
        elif self._backend._result_type == 'counts':
            args = ['--repetitions', int(self._options['shots'])] +\
                   ['--seed', int(self._options['seed'])] if self._options['seed'] else [] 
        
        run_description = {
                           'Job type': 'interactive', 
                           'Executable': PY_RUN,
                           'Arguments': [str(self._backend._allocation_id),
                                         'circuit.qasm',
                                         *args]
                           }
        # save circuit to tmp file
        tmp_qasm = 'circuit.qasm'
        circuit.qasm(filename=tmp_qasm)
        run_job = submit(run_description, blocking=False, inputs=[tmp_qasm]) 
        save_log(run_job) 
        return run_job 
        
    def submit(self, run_input, **options):
        '''
        Submit all circuits for simulation.
        '''
        self._inputs = self._validate(run_input)
        self._options = options

        self._status = JobStatus.RUNNING
        start = time()
        for circuit in self._inputs:
            job = self._submit(circuit)
            self._unicore_jobs.append(job) # add to unicore_jobs
        self._time_taken = time() - start
        self._status = JobStatus.DONE

        return self        

    def result(self, partial=False):
        '''
        Return the qiskit.Result object for this job instance.
        Args:
            partial (bool): If True, return partial results if possible.
        Raises:
            JobFailureError: If partial=False and any results are missing due to a job failure.
        Returns:
            result (qiskit.Result)
        Note:
            When `partial=True`, this method will attempt to retrieve partial
            results of failed jobs. In this case, precaution should
            be taken when accessing individual experiments, as doing so might
            cause an exception. The ``success`` attribute of the returned
            :class:`~qiskit.result.Result` instance can be used to verify
            whether it contains partial results.

            For example, if one of the experiments in the job failed, trying to
            get the counts of the unsuccessful experiment would raise an exception
            since there are no counts to return::

                try:
                    counts = result.get_counts("failed_experiment")
                except QiskitError:
                    print("Experiment failed!")
        '''

        # TODO: pass on error from juwels/juniq-service in case of failure
        # iterate over all jobs in _unicore_jobs
        all_success = True
        experiment_results = []
        for (unicore_job, circuit) in zip(self._unicore_jobs, self._inputs):
            header = {'clbit_labels': [[cbit.register.name, cbit.index] 
                                        for creg in circuit.cregs 
                                            for cbit in creg],
                      'creg_sizes':   [[creg.name,creg.size] 
                                        for creg in circuit.cregs],
                      'qubit_labels': [[qbit.register.name, qbit.index] 
                                        for qreg in circuit.qregs 
                                            for qbit in qreg],
                      'qreg_sizes':   [[qreg.name,qreg.size] 
                                        for qreg in circuit.qregs],
                      'global_phase': circuit.global_phase,
                      'memory_slots': circuit.num_qubits,
                      'n_qubits': circuit.num_qubits,
                      'name': circuit.name}

            try:
                data = self._backend._parse_result(unicore_job)
            except JobFailureError as err:
                data = {}
                success = False
                status  = 'FAILED'
                all_success = False
                self._status = JobStatus.ERROR
                if not partial:
                    raise
            else:
                success = True
                status  = 'DONE'
            finally:
                experiment_result = {
                    "shots": self._options.get('shots', None),
                    "success": success,
                    "data": data,
                    "meas_level": 2, # only lv 2 is supported by JUQCS
                    "status": status,
                    "seed": self._options.get('seed', None),
                    "header": header
                    }
                experiment_results.append(experiment_result)

        result = Result.from_dict({
            "backend_name":    self._backend._configuration.backend_name,
            "backend_version": self._backend._configuration.backend_version,
            "qobj_id": None, # BackendV1 doesnt require QObj for submission so theres no ID
            "job_id": self._job_id,
            "success": all_success,
            "date": str(datetime.now()),
            "status": 'COMPLETED' if all_success else 'FAILED',
            "time_taken": self._time_taken,
            "results": experiment_results
            })

        return result
        
    def status(self):
        '''Return the status of the job.'''
        # since execution is blocking this will only be one of JOB_FINAL_STATES {DONE, ERROR}:
        return self._status