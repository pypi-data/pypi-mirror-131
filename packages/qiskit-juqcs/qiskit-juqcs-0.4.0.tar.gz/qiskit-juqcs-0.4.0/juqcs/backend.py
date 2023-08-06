'''Collection of JUQCS backends.'''

from time import time
import datetime
from uuid import uuid4
import re
from math import ceil

import numpy as np

from qiskit.providers import BackendV1 as Backend, Options
from qiskit.providers.models import BackendStatus, QasmBackendConfiguration

from juqcs.client import submit, retrieve, save_log, PY_ALLOCATE, PY_DEALLOCATE
from juqcs.exceptions import AllocationError, JobFailureError, DeallocationError
from juqcs.job import JuqcsJob

class JuqcsBackend(Backend):
    '''
    Backend parent class for the JUCQS simulators
    '''    
    _default_qubits = None
    _max_qubits = None
    _max_minutes = 1440
    _alloc_qubits = None

    DEFAULT_CONFIGURATION = {
        'max_shots': 100000, 
        'backend_version': '0.1.0',
        'description': 'Exact massively parallel simulator of a universal quantum computer',
        'url': 'https://arxiv.org/abs/1805.04708',    
        'coupling_map': None,
        'basis_gates': ['u3', 'u2', 'u1', 'cx', 'id', 'x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg'],
        'gates': [
                {
                    'name': 'TODO',
                    'parameters': [],
                    'qasm_def': 'TODO'
                }
            ],
        'local': False,
        'simulator': True,
        'conditional': False,
        'memory': False,
        'open_pulse': False,
        }

    def __init__(self, 
                 configuration=None, 
                 provider=None, 
                 name=None,  
                 **fields):
        configuration = QasmBackendConfiguration.from_dict(
                            {**self.DEFAULT_CONFIGURATION, 
                            'backend_name': name,
                            'n_qubits': self._max_qubits})

        super().__init__(configuration, provider, **fields)
        self._expiration_time = None
        self._allocation_id   = None # TODO give option to instantiate backend passing the alloc id

    def _allocation_is_valid(self):
        '''Check if there is a running allocation attached to this backend instance.'''
        # never allocated or expired
        if (self._expiration_time is None) \
            or (self._expiration_time < datetime.datetime.now()):  
                self._expiration_time = None
                self._allocation_id   = None # delete expired ID
                self._alloc_qubits = None # delete alloc qubits
                return False
        else: 
            return True
        
    def status(self):
        '''Return backend status.'''
        if self._allocation_is_valid():
            status_msg = f'Resource allocation #{self._allocation_id} '+\
                         f'of {self._alloc_qubits} qubits '+\
                         f'available until {self._expiration_time}.'
        else:
            status_msg = 'No resource allocation running.'

        return BackendStatus(backend_name=self.name(),
                             backend_version=self.configuration().backend_version,
                             operational=True,
                             pending_jobs=0,
                             status_msg=status_msg)


    def _calc_expiration_dt(self, alloc_job, minutes):
        '''
        Parse the server's answer to the allocation request and calculate expiration datetime.
        Returns:
            alloc_expiration (datetime.datetime): stores the expiration time for the allocation.
        '''
        job_log = retrieve(alloc_job, 'job.log')
        line = job_log.split('\n')[-2] # check line before last (should be '<datetime>: Result: Success.')
        dt = re.search('(.+): Result: Success.', line)[1]        
        alloc_submission = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S %Z %Y') 
        alloc_duration = datetime.timedelta(minutes=minutes)
        alloc_expiration = alloc_submission + alloc_duration
        
        return alloc_expiration 


    def allocate(self, max_qubits=None, minutes=60, reservation=None):
        '''
        Request an allocation of HPC resources for a maximum of {max_qubits} qubits,
        a maximum runtime of {minutes}, optionally passing an HPC {reservation} ID.
        Raises:
            AllocationError: the allocation process failed.
        '''

        if max_qubits is None:
            max_qubits = self._default_qubits

        if max_qubits > self._max_qubits:
            raise AllocationError(
                f"Requested number of qubits 'max_qubits={max_qubits}' is larger than {self._max_qubits}, "
                'please reduce it and try again.')
        if minutes > self._max_minutes:
            raise AllocationError(
                f"Requested allocation time 'minutes={minutes}' is larger than {self._max_minutes}, "
                'please reduce it and try again.')

        self._reservation = reservation
        if self._allocation_is_valid() is False:
            #juniq-service: allocate.py
            alloc_description = {'Job type': 'interactive', 
                                 'Executable': PY_ALLOCATE,
                                 'Arguments': [str(max_qubits), 
                                               str(minutes),
                                               f'--reservation {self._reservation}' 
                                                    if self._reservation else '']
                                }
            print('Trying to allocate compute resources, this may take a few minutes... '
                  '(please do not abort, otherwise the allocation may be lost and the compute time wasted).')
            alloc_job = submit(alloc_description)
            save_log(alloc_job)

            stdout = retrieve(alloc_job, 'stdout')
            try:
                self._allocation_id = int(stdout)
            except ValueError:
                msg = 'JUNIQ-service returned the following error, please contact support: \n'
                stderr = retrieve(alloc_job, 'stderr')
                raise AllocationError(msg + stderr) from None # hides ValueError since it's irrelevant to the user
            else: # allocation was successful, so we calculate expiration time and set nr of qubits
                self._expiration_time = self._calc_expiration_dt(alloc_job, minutes)
                self._alloc_qubits = max_qubits
        else:
            print('A running allocation was found, please call backend.deallocate() before creating a new one.')
        print(self.status().status_msg)

    def run(self, run_input, **options):
        '''
        Run {run_input} (QuantumCircuit or list(QuantumCircuit)) on pre-existing allocation.
        Returns:
            JuqcsJob
        '''        
        job_id = str(uuid4())
        print('Submitting circuits for simulation, this may take a few minutes...')
        juqcs_job = JuqcsJob(self, job_id)\
                            .submit(run_input, **options)
        return juqcs_job
        

    def deallocate(self):
        '''
        If there is a running allocation attached to this instance, submit a request to 
        revoke it, else do nothing.
        Raises:
            DeallocationError: the deallocation process failed.
        '''
        if self._allocation_is_valid():
            #juniq_service: deallocate.py
            dealloc_description = {'Job type': 'interactive', 
                                   'Executable': PY_DEALLOCATE,
                                   'Arguments': [str(self._allocation_id)]
                                  }
            print('Trying to deallocate compute resources, this may take a few minutes...')
            dealloc_job = submit(dealloc_description)
            save_log(dealloc_job)
            exit_code = int(retrieve(dealloc_job, 'UNICORE_SCRIPT_EXIT_CODE'))

            if exit_code == 0:
                print(f'Allocation #{self._allocation_id} revoked.')
                self._expiration_time = None
                self._allocation_id   = None
            else: 
                msg = 'JUNIQ-service returned the following error, please contact support: \n'
                stderr = retrieve(dealloc_job, 'stderr')
                raise DeallocationError(msg + stderr)
        else:
            print('No running allocation found.')

        
    def _files_to_parse(self, unicore_job):
        '''
        Return the list of files within {unicore_job}'s work directory which should
        be parsed by this backend.
        Raises:
            RuntimeError: if no relevant files could be found (indicates something
            went wrong in the submission/execution process).
        '''
        files = [filename for filename in unicore_job.working_dir.listdir('/')
                            if self._result_regex.match(filename)]
        if files: 
            return files
        else:
            raise JobFailureError('No results were found for this experiment. '
                                  'Submit again or contact support if the problem persists.')

    def _parse_line(self, unicore_job, filename):
        '''
        Parse a relevant result file for this backend. Skip the file header,
        then yield one parsed line at a time until file footer is reached.
        Yields:
            idx: str(): bitstring representation of a register.
            vals: list(float()): value associated with the register {idx}.
        '''
        idx_col, *val_cols = self._result_columns
        with unicore_job.working_dir.stat(filename).raw() as f:
            while not self._result_header in next(f).decode('utf-8'): 
                pass # skip everything until header
            for line in f: # read every line after header
                try:
                    line = line.decode('utf-8').split()
                    idx = line[idx_col][1:-1]
                    vals = [float(line[column]) for column in val_cols]
                except IndexError:
                    break
                yield (idx, vals)
    

class QasmSimulator(JuqcsBackend):
    '''Sampling simulator version of JUQCS.'''
   
    _default_qubits = 34
    _max_qubits = 40

    _result_type = 'counts'
    _result_regex = re.compile('events.out|events[0-9]{7}.out')
    _result_header = '#------------------------------------------------------------------\n'
    _result_columns = (0, -1) # (bitstring, count)

    def __init__(self, configuration=None, provider=None, **fields):
        super().__init__(provider=provider,
                         name='qasm_simulator',
                         **fields)

    @classmethod
    def _default_options(cls):
        return Options(shots=1024, seed=None)

    def _parse_line(self, unicore_job, filename):
        '''
        Format the output of super()._parse_line() line by line.
        Yields:
            idx: str() hex representation of a qubit register.
            val: int() nr. of times the register {idx} was sampled.

        '''
        for idx,val in super()._parse_line(unicore_job, filename):
            idx = hex(int(idx, 2)) # convert bitstring to int, then hex
            val = int(val[0]) # only one int (count) in this list
            yield (idx, val)

    def _parse_result(self, unicore_job):
        '''
        Parse result files and return them in the appropriate format for
        inserting into a qiskit.Result object.
        Returns:
            {'counts': {idx:val}}
        '''
        files_to_parse = self._files_to_parse(unicore_job)
        result = dict()
        for filename in files_to_parse:
            for idx,val in self._parse_line(unicore_job, filename):
                result[idx] = val
        return {self._result_type: result}


class StatevectorSimulator(JuqcsBackend):
    '''Statevector simulator version of JUQCS.'''

    _default_qubits = 20
    _max_qubits = 20

    _result_type = 'statevector'
    _result_regex = re.compile('states.[0-9]+.out')
    _result_header = '-----------------------------------------------------------------------------------------------------\n'
    _result_columns = (-1, 1, 2) # (bitstring, (Re(psi), Im(psi)))

    def __init__(self, configuration=None, provider=None):
        super().__init__(provider=provider,
                         name='statevector_simulator')

    @classmethod
    def _default_options(cls):
        return Options()

    def _parse_line(self, unicore_job, filename):
        '''
        Format the output of super()._parse_line() line by line.
        Yields:
            idx: int() integer representation of a qubit register.
            val: list() of length 2 containing the real and imaginary
                parts of the amplitude associated with register {idx}.
        '''
        for idx,val in super()._parse_line(unicore_job, filename):
            idx = int(idx, 2) # return an int so we can use it to place the state in the np array of states
            yield (idx,val)

    def _parse_result(self, unicore_job):
        '''
        Parse result files and return them in the appropriate format for
        inserting into a qiskit.Result object.
        Returns:
            {'statevector': list(val)}
        '''
        files_to_parse = self._files_to_parse(unicore_job)
        # how many bits long is the state? get any one to find out
        state0, _ = next(super()._parse_line(unicore_job, files_to_parse[0]))
        # preallocate array to store the states 
        result = np.zeros((2**len(state0), 2)) # 2^(nr. of qubits) X (Re(psi), Im(psi))
        for filename in files_to_parse:
            for idx,val in self._parse_line(unicore_job, filename):
                result[idx,:] = val
        return {self._result_type: result.tolist()} # we are done placing items, so convert to list in place
